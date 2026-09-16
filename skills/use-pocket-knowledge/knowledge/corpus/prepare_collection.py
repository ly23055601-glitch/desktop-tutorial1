"""Freeze the complete candidate ledger before social-helper capture; no network."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent
FILES = ['xiaohongshu-candidates.jsonl', 'bilibili-selected.jsonl', 'douyin-candidates.jsonl']
DOMAINS = {'xiaohongshu': ('xiaohongshu.com', 'xhslink.com'), 'bilibili': ('bilibili.com', 'b23.tv'), 'douyin': ('douyin.com',)}

def read(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]

def main():
    if (ROOT / 'input-ledger.jsonl').exists():
        raise SystemExit('Ledger already frozen; resume existing run instead of rebuilding it')
    rows, seen = [], {}
    for filename in FILES:
        for item in read(ROOT / 'discovery' / filename):
            p = urlsplit(item['url'])
            platform = item['platform']
            if p.scheme != 'https' or p.username or p.password or p.port not in (None,443) or not any(p.hostname == d or p.hostname.endswith('.'+d) for d in DOMAINS[platform]):
                raise ValueError('Unsafe or unsupported candidate URL')
            url = p._replace(query='',fragment='').geturl().rstrip('/')
            work_id = item.get('id') or url.rsplit('/',1)[-1]
            key = (platform, work_id)
            if key in seen:
                continue
            row = {'workId': work_id, 'platform': platform, 'canonicalUrl': url,
                   'inputOrder': len(rows)+1, 'sourceInputOrders': [len(rows)+1],
                   'aliasRefs': [url], 'state': 'pending', 'autoSkipped': False,
                   'attempts': {'posts': 0, 'comments': 0}, 'model_hint': item.get('model_hint','unknown'),
                   'title_hint': item.get('title_hint'), 'discovery_source': 'discovery/'+filename,
                   'content_verified': False, 'split': 'train', 'batch_id': None,
                   'submission_url_ref': item.get('submission_url_ref', url)}
            seen[key] = row; rows.append(row)
    for platform in DOMAINS:
        candidates = [r for r in rows if r['platform']==platform]
        chosen = []
        for model in ('pocket_4','pocket_4p'):
            matching = sorted([r for r in candidates if r['model_hint']==model], key=lambda r: hashlib.sha256(r['workId'].encode()).hexdigest())
            chosen.extend(matching[:5])
        for row in chosen: row['split'] = 'holdout'
        if len(chosen)!=10: raise ValueError(f'{platform}: cannot reserve 10 holdout candidates')
        for n,row in enumerate(candidates):
            row['batch_id'] = f'{platform}-posts-{n//20+1:02}' if platform=='xiaohongshu' else f'{platform}-posts-01'
    now = datetime.now(timezone.utc).isoformat()
    for name, values in [('input-ledger.jsonl',rows), ('works.jsonl',[
        {'work_id':r['workId'],'platform':r['platform'],'canonical_url':r['canonicalUrl'],
         'author_id':None,'model_id':'unknown','model_basis':None,'model_hint':r['model_hint'],
         'status':'pending','split':r['split'],'source_path':None,'read_scope':[], 'collected_at':None,
         'limitations':['候选发现，尚未读取原帖和评论；型号提示不是已核验的型号'],'input_order':r['inputOrder']}
        for r in rows])]:
        (ROOT/name).write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in values))
    batches=[]
    for batch_id in dict.fromkeys(r['batch_id'] for r in rows):
        group=[r for r in rows if r['batch_id']==batch_id]
        batches.append({'batch_id':batch_id,'platform':group[0]['platform'],'work_ids':[r['workId'] for r in group], 'status':'pending'})
    state={'runStatus':'ready','startedAt':now,'completeInputCount':len(rows),
           'canonicalSkill':'/Users/luocaihua/.codex/skills/read-social-links-with-social-helper/MODULE.md',
           'fullInputHandedAt':now,'inputLedger':'input-ledger.jsonl','batches':batches,
           'commentsRequired':True,'mediaPolicy':'only where title/body/comments cannot support selected analysis',
           'blockedBy':None,'completedWorkIds':[],'failedWorkIds':[],'pendingWorkIds':[r['workId'] for r in rows]}
    (ROOT/'run-state.json').write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'complete_input_count':len(rows),'batches':[(b['batch_id'],len(b['work_ids'])) for b in batches],'holdout':sum(r['split']=='holdout' for r in rows)},ensure_ascii=False))

if __name__ == '__main__': main()
