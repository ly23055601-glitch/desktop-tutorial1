#!/usr/bin/env python3
"""Select Pocket4/4P selling points and detailed use cases with bounded evidence."""
from __future__ import annotations
import argparse
from collections import Counter
from datetime import date
import json
from pathlib import Path
import re
import sys

ROOT=Path(__file__).resolve().parents[1]
MODELS={'pocket_4','pocket_4p'}
TABLES={'selling':'selling_points/cards.jsonl','scene':'use_cases/cards.jsonl',
        'facts':'products/facts.jsonl','sources':'sources/official.jsonl','voice':'voice/cards.jsonl'}


def read(root):
    data={}
    for key,path in TABLES.items():
        data[key]=[json.loads(line) for line in (root/path).read_text().splitlines() if line.strip()]
    return data


def as_index(rows,key='id'):return {r[key]:r for r in rows}


def audit(data):
    issues=[]
    facts=as_index(data['facts']); sources=as_index(data['sources'],'source_id'); voices=as_index(data['voice'])
    for kind in ['selling','scene']:
        for identifier,n in Counter(c.get('id') for c in data[kind]).items():
            if not identifier or n!=1:issues.append({'id':identifier,'code':'duplicate_or_missing_id'})
        for c in data[kind]:
            def fail(code,**kwargs):issues.append({'id':c.get('id'),'code':code,**kwargs})
            models=set(c.get('models',[]))
            if not models or not models<=MODELS:fail('model_scope')
            refs=c.get('fact_ids',[])
            if not refs:fail('no_supporting_fact')
            for identifier in refs:
                f=facts.get(identifier)
                if not f or f.get('status')!='verified':fail('fact_not_verified',fact_id=identifier);continue
                if not models.intersection(f.get('models',[])):fail('unrelated_model_fact',fact_id=identifier)
                if not f.get('source_refs'):fail('fact_without_source',fact_id=identifier)
                for r in f.get('source_refs',[]):
                    s=sources.get(r.get('source_id'))
                    if not s or not r.get('quote') or r['quote'] not in s.get('excerpt',''):fail('source_reference_invalid',fact_id=identifier)
            for model in models:
                if not any(model in facts.get(i,{}).get('models',[]) for i in refs):fail('model_has_no_support',model=model)
            for key in ['title','conditions','tradeoffs','tags','checked_at']:
                if not c.get(key):fail('required_field_missing',field=key)
            try:
                if date.fromisoformat(c['checked_at'])>date.today():fail('future_edit_date')
            except (KeyError,ValueError,TypeError):fail('invalid_edit_date')
            if kind=='selling':
                for key in ['official_capability','user_value','not_infer','relevant_needs','scenario_directions']:
                    if not c.get(key):fail('required_field_missing',field=key)
                if c.get('value_basis')!='editorial_interpretation':fail('value_not_labeled_interpretation')
            else:
                for key in ['situation','trigger','user_task','friction','desired_result','workflow','model_notes','not_suitable','opening_reasons','reply_opportunities','voice_evidence_note']:
                    if not c.get(key):fail('required_field_missing',field=key)
                if c.get('evidence_kind')!='editorial_hypothesis':fail('scenario_not_labeled_hypothesis')
                if set(c.get('model_notes',{}))!=models:fail('model_notes_incomplete')
                for identifier in c.get('voice_card_ids',[]):
                    v=voices.get(identifier)
                    if not v or v.get('split')=='holdout':fail('voice_missing_or_holdout',voice_id=identifier)
                for identifier in c.get('selling_point_ids',[]):
                    point=next((s for s in data['selling'] if s.get('id')==identifier),None)
                    if not point or not models.intersection(point['models']):fail('selling_point_missing_or_model_mismatch',selling_id=identifier)
    return {'integrity_ok':not issues,'counts':{k:len(data[k]) for k in ['selling','scene']},'issues':issues,
            'boundary':'Reference/schema audit only; value and scenes require semantic review and do not constitute user research.'}


SYNONYMS=({'独自','一个人','自拍','独拍'}, {'传输','导出','传素材','拷贝'}, {'慢放','慢动作','升格'},
          {'收音','无线麦','讲话','录音'}, {'宠物','猫咪','小猫','小狗'}, {'人像','人物','半身'},
          {'夜间','夜景','晚上','低光'},{'收纳','装袋','携带'})
LOW={'pocket','pocket4','pocket4p','4','4p','使用','产品','场景','卖点','拍摄','功能'}


def terms(query):
    out=set(re.findall(r'[a-z0-9]+',query.lower()))
    for part in re.findall(r'[\u4e00-\u9fff]+',query):
        out.add(part);out.update(part[i:i+2] for i in range(len(part)-1))
    out-=LOW
    for group in SYNONYMS:
        if any(word in query for word in group):out.update(group)
    return out


def score(card,query):
    if query==card['id'] or query in card.get('fact_ids',[]):return 10000
    if query in card.get('selling_point_ids',[]):return 9000
    fields={'title':5,'tags':5,'situation':3,'user_task':3,'friction':2,'trigger':2,
            'relevant_needs':3,'scenario_directions':2,'user_value':2,'official_capability':1}
    ts=terms(query)
    # Do not match negative examples, provenance metadata, or other model names.
    return sum(weight*sum((2 if len(t)>2 else 1) for t in ts if t in json.dumps(card.get(k,''),ensure_ascii=False).lower()) for k,weight in fields.items())


def search(data,query,model=None,kind='all',limit=3):
    facts=as_index(data['facts']);sources=as_index(data['sources'],'source_id')
    all_cards={c['id']:c for k in ['selling','scene'] for c in data[k]}
    exact=bool(re.fullmatch(r'(?:PSP|PUC|PKF)-[A-Z0-9-]+',query))
    result={'query':query,'model':model,'kind':kind,'selling':[],'scene':[],
            'boundaries':['用户价值是编辑解释，详细场景是待验证假设；不计真实用户样本',
             '只在当前帖有相应触发线索时选材，不把字段拼成固定句式或强加回复',
             '产品事实须按当前官网核验；保留模式、地区、固件、配件及不适合情况',
             '事实ID只返回适用型号的已核项，缺资料不等于不支持；pending不作肯定卖点',
             '真实表达原话和训练人物经历分开；本查询不加载留出正文或停止附件']}
    for k in ['selling','scene']:
        if kind not in {k,'all'}:continue
        ranked=[]
        for c in data[k]:
            if model and model not in c['models']:continue
            if exact:
                # IDs are lookup intent, never a fuzzy keyword that can return unrelated models.
                matched=query==c['id'] or query in c.get('fact_ids',[]) or query in c.get('selling_point_ids',[])
                if not matched:continue
            n=score(c,query)
            if n>0:ranked.append((n,c))
        for _,c in sorted(ranked,key=lambda p:(-p[0],p[1]['id']))[:limit]:
            item=dict(c)
            item['card_models']=c['models'];item['selected_model']=model
            if model and 'model_notes' in item:item['model_notes']={model:item['model_notes'][model]}
            selected=[facts[i] for i in c['fact_ids'] if i in facts and facts[i]['status']=='verified' and (not model or model in facts[i]['models'])]
            item['fact_ids']=[f['id'] for f in selected]
            item['facts']=[{'id':f['id'],'models':f['models'],'fact':f['fact'],'conditions':f.get('conditions',[]),'not_infer':f.get('not_infer',[]),
                'checked_at':f['checked_at'],'sources':[{'url':sources[r['source_id']]['url'],'locator':r['locator'],'source_id':r['source_id']} for r in f['source_refs']]} for f in selected]
            if k=='selling':
                item['related_scenes']=[{'id':s['id'],'title':s['title']} for s in data['scene'] if c['id'] in s.get('selling_point_ids',[]) and (not model or model in s['models'])]
            result[k].append(item)
    return result


def render(r):
    lines=[f"# Pocket卖点与场景选材：{r['query']}"]
    for key,title in [('selling','卖点与使用价值'),('scene','详细使用场景')]:
        if r['kind'] not in {key,'all'}:continue
        lines.append('\n## '+title)
        if not r[key]:lines.append('没有匹配资料；可换具体任务、单个卡片ID或明确型号继续查询')
        for c in r[key]:
            lines.append(f"\n### {c['id']}｜{c['title']}（{' / '.join(c['models'])}）")
            for field,label in [('official_capability','官方能力摘要'),('user_value','使用价值（编辑解释）'),('situation','具体处境（假设）'),('trigger','开口触发'),('user_task','想完成的事'),('friction','卡住的动作'),('desired_result','期望'),('workflow','过程'),('model_notes','分型号说明'),('conditions','条件'),('tradeoffs','取舍'),('not_suitable','不适合'),('not_infer','不可推断'),('opening_reasons','可关注方向'),('reply_opportunities','可承接方向')]:
                value=c.get(field)
                if value:
                    text='；'.join(f"{k}：{v.get('capability',v) if isinstance(v,dict) else v}" for k,v in value.items()) if isinstance(value,dict) else '；'.join(value) if isinstance(value,list) else value
                    lines.append(f'- {label}：{text}')
            for f in c['facts']:
                refs='；'.join(f"[官网]({s['url']}) · {s['locator']}" for s in f['sources'])
                lines.append(f"- 依据 {f['id']}：{f['fact']}（核验 {f['checked_at']}）；{refs}")
                lines.append('- 事实条件：'+'；'.join(f['conditions'])+'；不可推断：'+'；'.join(f['not_infer']))
            if c.get('related_scenes'):lines.append('- 对应场景：'+'；'.join(f"{s['id']} {s['title']}" for s in c['related_scenes']))
            if c.get('voice_card_ids'):lines.append('- 表达机制参考：'+'、'.join(c['voice_card_ids'])+'；'+c['voice_evidence_note'])
    lines+=['\n## 选材边界']+['- '+b for b in r['boundaries']]
    return '\n'.join(lines)


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,default=ROOT)
    sub=p.add_subparsers(dest='command',required=True)
    a=sub.add_parser('audit');a.add_argument('--format',choices=['json','markdown'],default='json')
    s=sub.add_parser('search');s.add_argument('query');s.add_argument('--model',choices=sorted(MODELS));s.add_argument('--kind',choices=['all','selling','scene'],default='all');s.add_argument('--limit',type=int,default=2);s.add_argument('--format',choices=['json','markdown'],default='markdown')
    args=p.parse_args(argv)
    try:data=read(args.root);check=audit(data)
    except (OSError,ValueError,KeyError,TypeError) as exc:
        print(json.dumps({'error':'materials_unavailable','detail':str(exc)},ensure_ascii=False));return 1
    if args.command=='audit' or not check['integrity_ok']:
        print(json.dumps(check,ensure_ascii=False,indent=2));return 0 if check['integrity_ok'] else 1
    if not 1<=args.limit<=10:p.error('--limit requires 1–10')
    r=search(data,args.query,args.model,args.kind,args.limit)
    print(json.dumps(r,ensure_ascii=False,indent=2) if args.format=='json' else render(r));return 0

if __name__=='__main__':raise SystemExit(main())
