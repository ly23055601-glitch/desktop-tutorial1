#!/usr/bin/env python3
"""Find complete Nano material cards and include referenced facts and sources."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
KB = ROOT / 'knowledge/nano'


def read_rows(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def lookup(terms, kind, limit):
    selling = read_rows(KB/'selling-points/cards.jsonl')
    scenes = [row for path in sorted((KB/'scenarios').glob('training-*.jsonl')) for row in read_rows(path)]
    candidates = scenes if kind == 'scene' else selling
    terms = list(dict.fromkeys(t.casefold() for t in terms if t.strip()))

    def score(row):
        total = 0
        for term in terms:
            if term == row['id'].casefold():
                total += 100
            for field, weight in [('title',8),('keywords',6),('moment',4),('value_facets',4),('decision_lenses',4),('shooting_goal',3),('viewer_payoff',3),('usage_stage_angles',3),('observable_details',3),('interest_branches',3),('strong_fit_signals',2)]:
                value = json.dumps(row.get(field,''),ensure_ascii=False).casefold()
                if term in value:
                    total += weight
            if term in json.dumps(row,ensure_ascii=False).casefold():
                total += 1
        return total

    ranked = sorted(((score(row),row) for row in candidates),key=lambda item:(-item[0],item[1]['id']))
    selected = [row for score_value,row in ranked if score_value > 0][:limit]
    sp_ids = {sid for row in selected for sid in row.get('selling_point_ids',[])}
    linked_selling = [row for row in selling if row['id'] in sp_ids] if kind == 'scene' else []
    fids = {fid for row in selected+linked_selling for fid in row.get('fact_ids',[])}
    facts = [f for f in read_rows(KB/'products/facts.jsonl') if f['id'] in fids]
    source_ids = {ref['source_id'] for fact in facts for ref in fact['source_refs']}
    sources = [s for s in read_rows(KB/'sources/official.jsonl') if s['id'] in source_ids]
    return {'query_terms':terms,'kind':kind,'matches':selected,'related_selling_points':linked_selling,
            'facts':facts,'sources':sources,
            'use_note':'关键词命中只表示相关，不证明适用；完整条件、不可推论和原核验日期均保留。价值/场景仍是编辑推演，正文产品断言须复核当前官方来源。'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('terms',nargs='+',help='关键词或完整卡片ID；多个关键词按相关度合并')
    parser.add_argument('--kind',choices=['scene','selling'],default='scene')
    parser.add_argument('--limit',type=int,default=2)
    args = parser.parse_args()
    if not 1 <= args.limit <= 8:
        parser.error('--limit must be between 1 and 8')
    print(json.dumps(lookup(args.terms,args.kind,args.limit),ensure_ascii=False,indent=2))
