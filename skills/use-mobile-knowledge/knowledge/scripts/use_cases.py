#!/usr/bin/env python3
"""Render, audit and retrieve Mobile editorial use cases with their complete evidence."""
import argparse
import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATEGORIES = {
    'travel': '旅行与独自出镜', 'relationships': '同行与关系记录',
    'parenting': '亲子共同参与', 'pets': '猫狗与低角度',
    'everyday': '日常拍摄与镜头练习', 'practice': '舞蹈健身与技能回看',
    'solo_content': '独自口播与内容制作', 'live_teaching': '直播与远程教学',
    'craft_product': '手作与商品展示', 'space_business': '空间与经营记录',
    'workflow_legacy': '拍摄流程与旧款再利用',
}


def context(groups=None):
    from maintain import all_records, MODELS
    groups = all_records() if groups is None else groups
    records = {r['id']: r for kind in ('facts', 'compatibility') for _, _, r in groups[kind]}
    selling = {r['id']: r for _, _, r in groups['selling_points']}
    cases = [r for _, _, r in groups['use_cases']]
    return groups, MODELS, records, selling, cases


def audit(groups=None, case_ids=None):
    groups, models, records, selling, cases = context(groups)
    if case_ids is not None:
        cases = [c for c in cases if c.get('id') in case_ids]
    errors = []
    def check(ok, message):
        if not ok:
            errors.append(message)
    mappings = {kind: {r['id']: r for _, _, r in groups[kind]}
                for kind in ('facts', 'compatibility', 'audiences', 'scenarios')}
    required = {'id', 'title', 'category', 'models', 'audience_ids', 'selling_point_ids',
                'scenario_ids', 'kind', 'status', 'edited_at', 'moment', 'task', 'friction',
                'use_plan', 'value_hypothesis', 'psychology', 'writing_material',
                'when_not_needed', 'conditions', 'avoid_claims', 'fact_ids',
                'compatibility_ids', 'retrieval_tags'}
    seen = set()
    if case_ids is None:
        check(bool(cases), 'use_cases: 没有场景选材记录')
    for c in cases:
        key = c.get('id')
        check(required <= c.keys(), f'{key}: 场景选材字段缺失 {required - c.keys()}')
        check(isinstance(key, str) and bool(re.fullmatch(r'MOBILE-USE-\d{3}', key)), f'{key}: 场景编号格式无效')
        check(key not in seen, f'{key}: 场景编号重复'); seen.add(key)
        check(c.get('category') in CATEGORIES, f'{key}: 分类无效')
        model_list = c.get('models', [])
        valid_models = isinstance(model_list, list) and len(model_list) == 1 and model_list[0] in models
        check(valid_models, f'{key}: 须对应一个准确型号')
        check(c.get('kind') == 'editorial_synthesis' and c.get('status') == 'hypothesis_only', f'{key}: 场景不得标为研究或实测')
        try:
            check(date.fromisoformat(c.get('edited_at', '')) <= date.today(), f'{key}: 编辑日期在未来')
        except (TypeError, ValueError):
            check(False, f'{key}: 编辑日期无效')
        for field in ('title', 'moment', 'task', 'friction', 'value_hypothesis', 'when_not_needed'):
            check(isinstance(c.get(field), str) and bool(c[field].strip()), f'{key}: {field}须有具体内容')
        for field in ('use_plan', 'conditions', 'avoid_claims', 'retrieval_tags', 'audience_ids', 'selling_point_ids', 'fact_ids'):
            val = c.get(field)
            check(isinstance(val, list) and bool(val) and all(isinstance(x, str) and x.strip() for x in val), f'{key}: {field}须为非空字符串数组')
        for field, mapping in [('audience_ids', mappings['audiences']), ('scenario_ids', mappings['scenarios']),
                               ('selling_point_ids', selling), ('fact_ids', mappings['facts']),
                               ('compatibility_ids', mappings['compatibility'])]:
            val = c.get(field, [])
            if not isinstance(val, list):
                check(False, f'{key}: {field}须为数组'); continue
            check(len(val) == len(set(val)), f'{key}: {field}引用重复')
            for rid in val:
                check(rid in mapping, f'{key}: 引用不存在 {rid}')
                if rid not in mapping: continue
                target = mapping[rid]
                if field in ('selling_point_ids', 'fact_ids', 'compatibility_ids') and valid_models:
                    check(set(model_list) <= set(target['models']), f'{key}: 跨型号引用 {rid}')
                if field in ('fact_ids', 'compatibility_ids'):
                    check(target['status'] == 'verified', f'{key}: 待核或冲突不能支撑能力 {rid}')
                if field == 'selling_point_ids':
                    for evidence_id in target['fact_ids'] + target['compatibility_ids']:
                        check(evidence_id in records, f'{key}: 卖点依据不存在 {evidence_id}')
                        if evidence_id in records:
                            item = records[evidence_id]
                            check(item['status'] == 'verified', f'{key}: 卖点依据待核或冲突 {evidence_id}')
                            if valid_models:
                                check(set(model_list) <= set(item['models']), f'{key}: 卖点依据跨型号 {evidence_id}')
        psyche = c.get('psychology', {})
        check(isinstance(psyche, dict) and all(isinstance(psyche.get(f), str) and psyche[f].strip()
              for f in ('want', 'hesitation', 'tradeoff')), f'{key}: 心理取舍字段不全')
        material = c.get('writing_material', {})
        if not isinstance(material, dict):
            check(False, f'{key}: 选材须为对象'); continue
        check(material.get('content_mode') == 'training_fiction' and material.get('calibration_status') == 'pending_calibration'
              and material.get('user_endorsed') is False and material.get('source_kind') == 'synthetic_planning',
              f'{key}: 选材不能冒充真实来源或认可范文')
        for field in ('entry_angles', 'concrete_details', 'suitable_post_contexts', 'do_not_invent_as_post'):
            val = material.get(field)
            check(isinstance(val, list) and bool(val) and all(isinstance(x, str) and x.strip() for x in val), f'{key}: 缺少选材维度 {field}')
    return errors


def case_link(c):
    return f"[{c['id']}｜{c['title']}]({c['category']}.md#{c['id'].lower()})"


def record_link(r):
    path = '../compatibility/guide.md' if 'method' in r else f"../products/{r['models'][0]}.md"
    return f"[{r['id']}]({path}#{r['id'].lower()})"


def render(groups=None):
    groups, models, records, selling, cases = context(groups)
    errors = audit(groups)
    if errors: raise ValueError('\n'.join(errors))
    out = ROOT / 'use_cases'; out.mkdir(exist_ok=True)
    audiences = {r['id']: r for _, _, r in groups['audiences']}
    guide = ['# Mobile 详细使用场景与培训选材', '',
             f'本版 {len(cases)} 张微场景卡，把具体时刻、拍摄任务、卖点用途、心理取舍与表达切入点连接起来。', '',
             '场景与价值为编辑推演，心理为待验证假设；选材为 `training_fiction / pending_calibration`，不是用户研究、真实原帖、已发生经历或认可范文。卡片字段供分析取用，不是每条评论的必写步骤或固定句式。', '',
             '## 按当前任务找场景', '', '| 场景组 | 数量 | 可选情境 |', '|---|---:|---|']
    for category, name in CATEGORIES.items():
        selected = [c for c in cases if c['category'] == category]
        if not selected: continue
        guide.append(f"| [{name}]({category}.md) | {len(selected)} | {'；'.join(c['title'] for c in selected)} |")
        body = [f'# {name}', '',
                '由 cards.jsonl 生成。以下情境均为编辑推演；表达材料是待校准的培训选项。具体手机、系统、App、固件、组件与连接方式以各卡关联的完整产品记录为准。', '',
                '[返回场景目录](guide.md)｜[按卖点反查场景](selling-point-map.md)｜[交给写手时怎样取材](WRITER_HANDOFF.md)', '', '## 场景目录', '']
        body += [f"- [{c['id']}｜{c['title']}](#{c['id'].lower()})" for c in selected]
        for c in selected:
            w = c['writing_material']; p = c['psychology']
            body += ['', f'<a id="{c["id"].lower()}"></a>', f"## {c['id']}｜{c['title']}", '',
                     f"**型号**：{models[c['models'][0]]}；场景编辑：{c['edited_at']}（不替代事实核验日期）", '',
                     '**可关联角色**：' + '、'.join(f"[{audiences[a]['role']}](../audiences/guide.md#{a.lower()})" for a in c['audience_ids']), '',
                     f"**发生时刻**：{c['moment']}", '', f"**想完成的拍摄**：{c['task']}", '',
                     f"**具体难点**：{c['friction']}", '', '**卖点如何参与**：', '']
            body += [f'- {s}' for s in c['use_plan']]
            body += ['', '**对应卖点**：' + '、'.join(f"[{selling[s]['title']}](../selling_points/{c['models'][0]}.md#{s.lower()})" for s in c['selling_point_ids']), '',
                     f"**可能价值**：{c['value_hypothesis']}", '',
                     f"**心理取舍（假设）**：想要——{p['want']}；犹豫——{p['hesitation']}；取舍——{p['tradeoff']}", '',
                     '**可供训练选择的表达方向**（分析线索，非待复制评论）：', '']
            body += [f'- {s}' for s in w['entry_angles']]
            body += ['', '**可选细节**（只有在当批训练人物中设定，或由真实材料证实后才能使用）：' + '；'.join(w['concrete_details']), '',
                     '**可能适用的话题语境**（假想条件，实际选材先读原帖）：' + '；'.join(w['suitable_post_contexts']), '',
                     '**不能据此替真实原帖补写**：' + '；'.join(w['do_not_invent_as_post']), '',
                     f"**何时不需要这项能力**：{c['when_not_needed']}", '',
                     '**关键条件摘要**：' + '；'.join(c['conditions']), '',
                     '**不可推论**：' + '；'.join(c['avoid_claims']), '',
                     '**事实、完整条件与实际核验日期**：', '']
            for rid in c['fact_ids'] + c['compatibility_ids']:
                r = records[rid]
                body.append(f"- {record_link(r)}｜{r['component']}｜`{r['status']}`｜核验 {r['checked_at']}")
            body += ['', f"相关限制同时查阅[本库缺口](../GAPS.md)；用 `scripts/use_cases.py query --id {c['id']}` 可取全卡、卖点、完整事实及其来源和该型号的待核／冲突。", '',
                     '**检索词**：' + '、'.join(c['retrieval_tags'])]
        (out / f'{category}.md').write_text('\n'.join(body) + '\n', encoding='utf-8')
    guide += ['', '## 从卖点反查用途', '',
              '[卖点—场景对应表](selling-point-map.md)覆盖现有卖点及其可关联场景；同一卖点可以有不同关注点，也可能对当前任务没有必要。', '',
              '## 交给后续培训文案', '',
              '[选材接入说明](WRITER_HANDOFF.md)说明如何把相关场景交给同一共享写手；不要求一条评论塞进全部维度。', '',
              '## 检索', '', '以下命令在本知识库目录运行；跨项目可用脚本绝对路径，参数与工作目录无关。', '',
              '```sh', "rg -n '同行|全身|白板|装夹|旧款' use_cases/cards.jsonl", 
              "rg -n 'MOBILE-SELL-001' use_cases/cards.jsonl", 
              'python3 scripts/use_cases.py query --model osmo_mobile_8p --keyword 合影',
              'python3 scripts/use_cases.py query --selling-point MOBILE-SELL-002',
              'python3 scripts/use_cases.py query --id MOBILE-USE-001', '```', '',
              '查询返回整张卡、所引卖点、直接和卖点关联的完整事实、官方来源登记及该型号的全部待核／冲突。多个筛选条件取交集；无命中表示未找到选材，不代表产品不支持。产品事实单独查询仍用原 `scripts/query.py`。', '',
              '格式见[SCHEMA](SCHEMA.md)，维护见[总维护说明](../MAINTENANCE.md)。']
    (out / 'guide.md').write_text('\n'.join(guide) + '\n', encoding='utf-8')
    matrix = ['# 按卖点反查详细场景', '',
              '用途为编辑推演，具体条件随所引事实维护。点击场景读发生时刻、操作用途、心理取舍及培训切入点。', '',
              '| 型号与卖点 | 可关联的详细场景 |', '|---|---|']
    for s in selling.values():
        selected = [c for c in cases if s['id'] in c['selling_point_ids']]
        label = f"{models[s['models'][0]]}：[{s['title']}](../selling_points/{s['models'][0]}.md#{s['id'].lower()})"
        matrix.append(f"| {label} | {'；'.join(case_link(c) for c in selected) or '尚无细化卡；仍可查原卖点用途'} |")
    (out / 'selling-point-map.md').write_text('\n'.join(matrix) + '\n', encoding='utf-8')


def query(args, groups=None):
    groups, models, records, selling, cases = context(groups)
    sources = {r['id']: r for _, _, r in groups['sources']}
    def evidence(r):
        return {'record': r, 'sources': [sources[ref['source_id']] for ref in r['source_refs']]}
    matched = [c for c in cases
               if (not args.id or c['id'] == args.id)
               and (not args.model or args.model in c['models'])
               and (not args.selling_point or args.selling_point in c['selling_point_ids'])
               and (not args.keyword or args.keyword.casefold() in json.dumps(c, ensure_ascii=False).casefold())]
    result, blocked = [], []
    for c in matched:
        gaps = [evidence(r) for r in records.values()
                if set(c.get('models', [])) & set(r['models']) and r['status'] != 'verified']
        errors = audit(groups, case_ids={c['id']})
        if errors:
            blocked.append({'id': c['id'], 'models': c.get('models'), 'errors': errors, 'model_gaps': gaps})
            continue
        selected_selling = [selling[sid] for sid in c['selling_point_ids']]
        ids = list(dict.fromkeys(c['fact_ids'] + c['compatibility_ids'] +
                   [rid for s in selected_selling for rid in s['fact_ids'] + s['compatibility_ids']]))
        result.append({'card': c, 'selling_points': selected_selling,
                       'evidence': [evidence(records[rid]) for rid in ids],
                       'model_gaps': gaps})
    return {'count': len(result), 'matched_count': len(matched), 'blocked_count': len(blocked),
            'blocked': blocked, 'material_kind': 'editorial_synthesis',
            'knowledge_root': str(ROOT),
            'notice': '场景与心理不是实证，选材不是原帖；事实保留核验日期，使用前核对当前来源和具体组合。无命中不等于不支持。',
            'results': result}


def main():
    from maintain import MODELS
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('render'); sub.add_parser('audit')
    qp = sub.add_parser('query')
    qp.add_argument('--id'); qp.add_argument('--model', choices=list(MODELS))
    qp.add_argument('--keyword'); qp.add_argument('--selling-point')
    args = parser.parse_args()
    if args.command == 'render': render(); return 0
    if args.command == 'audit':
        errors = audit()
        print(json.dumps({'ok': not errors, 'errors': errors}, ensure_ascii=False, indent=2)); return bool(errors)
    if not any((args.id, args.model, args.keyword, args.selling_point)):
        qp.error('请提供场景编号、准确型号、关键词或卖点编号')
    result = query(args)
    print(json.dumps(result, ensure_ascii=False, indent=2)); return bool(result['blocked_count'])


if __name__ == '__main__':
    raise SystemExit(main())
