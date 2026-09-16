#!/usr/bin/env python3
"""Check Nano package structure and provenance; does not verify product truth or style."""
import argparse
from collections import Counter
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import unquote


def validate():
    skill = Path(__file__).resolve().parents[1]
    root = skill.parents[2]
    kb = root / 'knowledge/nano'
    failures = []

    def check(ok, message):
        if not ok:
            failures.append(message)

    def rows(path, required):
        result = []
        for line_no, line in enumerate(path.read_text().splitlines(), 1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
                check(isinstance(row, dict), f'{path}:{line_no}: expected object')
                if not isinstance(row, dict):
                    continue
                check(set(required) <= row.keys(), f'{path}:{line_no}: missing required fields')
                result.append(row)
            except ValueError as exc:
                failures.append(f'{path}:{line_no}: {exc}')
        ids = [r.get('id') for r in result]
        check(len(ids) == len(set(ids)), f'{path}: duplicate IDs')
        return result

    facts = rows(kb/'products/facts.jsonl', ['id','models','components','topic','fact','conditions','not_infer','source_refs','checked_at','status'])
    sources = rows(kb/'sources/official.jsonl', ['id','url','local_path','sha256','checked_at'])
    scenes = rows(kb/'scenarios/cards.jsonl', ['id','basis','product_connections','conditions','not_infer'])
    hypotheses = rows(skill/'references/audience-hypotheses.jsonl', ['id','basis','review_status','role_or_need','possible_motives','possible_frictions','expression_focus','avoid_inference','related_fact_ids','origin'])
    selling = rows(kb/'selling-points/cards.jsonl', ['id','title','basis','review_status','fact_ids','capability_summary','user_value','strong_fit_signals','weak_fit_signals','possible_motives','tradeoffs','conditions','not_infer','expression_angles','keywords','prepared_at'])
    training_fields = ['id','title','group','basis','review_status','moment','shooting_goal','audience_or_recipient','possible_motives','frictions','capture_approach','fact_ids','selling_point_ids','why_these_points','strong_fit_signals','weak_fit_signals','expression_angles','variation_axes','conditions','not_infer','keywords','prepared_at']
    training = [row for path in sorted((kb/'scenarios').glob('training-*.jsonl')) for row in rows(path,training_fields)]
    check(len({r['id'] for r in training}) == len(training), 'training scenes: duplicate IDs across files')
    fact_map = {r['id']:r for r in facts}
    source_ids = {r['id'] for r in sources}
    hash_checks = 0
    for source in sources:
        path = kb/source['local_path']
        check(path.is_file(), f'{source["id"]}: source file missing')
        if path.is_file():
            check(hashlib.sha256(path.read_bytes()).hexdigest() == source['sha256'], f'{source["id"]}: source hash mismatch')
            hash_checks += 1
    for fact in facts:
        check(fact['models'] == ['osmo_nano'], f'{fact["id"]}: unexpected model')
        check(fact['status'] in {'verified','pending'}, f'{fact["id"]}: unsupported status')
        check(bool(fact['source_refs']), f'{fact["id"]}: no source reference')
        for ref in fact['source_refs']:
            check(ref.get('source_id') in source_ids and bool(ref.get('locator')), f'{fact["id"]}: invalid source or locator')
    for scene in scenes:
        check(scene['basis'] == 'editorial_hypothesis', f'{scene["id"]}: scenario basis changed')
        for ref in scene['product_connections']:
            check(fact_map.get(ref.get('fact_id'),{}).get('status') == 'verified', f'{scene["id"]}: missing or pending fact')
    for hypothesis in hypotheses:
        hid = hypothesis['id']
        check(hypothesis['basis'] == 'editorial_hypothesis', f'{hid}: unsupported research basis')
        check(hypothesis['review_status'] in {'pending_user_calibration','user_calibrated'}, f'{hid}: invalid review status')
        for fid in hypothesis['related_fact_ids']:
            check(fact_map.get(fid,{}).get('status') == 'verified', f'{hid}: missing or pending fact {fid}')
        origin = hypothesis['origin']
        origin_path = (skill/'references'/origin['path']).resolve()
        check(origin_path.is_file(), f'{hid}: origin missing')
        if origin_path.is_file():
            original = json.loads(origin_path.read_text())
            check(original.get('content_mode') == 'training_fiction', f'{hid}: origin is not training fiction')
            check(any(p.get('id') == origin.get('persona_id') for p in original.get('personas',[])), f'{hid}: origin persona missing')
    selling_ids = {row['id'] for row in selling}
    for row in selling + training:
        rid = row['id']
        expected_basis = 'editorial_interpretation' if rid in selling_ids else 'editorial_hypothesis'
        check(row['basis'] == expected_basis, f'{rid}: incorrect material basis')
        check(row['review_status'] in {'pending_user_calibration','user_calibrated'}, f'{rid}: invalid review status')
        check(bool(row['fact_ids']), f'{rid}: no fact references')
        for fid in row['fact_ids']:
            check(fact_map.get(fid,{}).get('status') == 'verified', f'{rid}: missing or pending fact {fid}')
        for key in ['strong_fit_signals','weak_fit_signals','conditions','not_infer','expression_angles','keywords']:
            check(isinstance(row[key],list) and bool(row[key]) and all(isinstance(item,str) and item.strip() for item in row[key]), f'{rid}: empty or invalid {key}')
    for row in training:
        rid = row['id']
        check(bool(row['selling_point_ids']), f'{rid}: no selling point references')
        for sid in row['selling_point_ids']:
            check(sid in selling_ids, f'{rid}: missing selling point {sid}')
        reasons = row['why_these_points']
        valid_reasons = all(isinstance(item,dict) and item.get('selling_point_id') in row['selling_point_ids'] and isinstance(item.get('value_reason'),str) and item['value_reason'].strip() for item in reasons)
        check(valid_reasons, f'{rid}: invalid selling point rationale')
        if valid_reasons:
            check({item['selling_point_id'] for item in reasons} == set(row['selling_point_ids']), f'{rid}: missing selling point rationale')
        if 'viewer_payoff' in row:
            check(isinstance(row['viewer_payoff'],str) and bool(row['viewer_payoff'].strip()),f'{rid}: invalid viewer payoff')
        if 'usage_stage_angles' in row:
            angles=row['usage_stage_angles']
            check(isinstance(angles,list) and bool(angles) and all(isinstance(a,str) and a.strip() for a in angles),f'{rid}: invalid usage-stage angles')
        for key in ['observable_details','interest_branches']:
            if key in row:
                check(isinstance(row[key],list) and bool(row[key]) and all(isinstance(v,str) and v.strip() for v in row[key]), f'{rid}: invalid {key}')
        if 'differentiation_note' in row:
            check(isinstance(row['differentiation_note'],str) and bool(row['differentiation_note'].strip()), f'{rid}: invalid differentiation note')
    for row in selling:
        if 'decision_lenses' in row:
            lenses=row['decision_lenses']
            check(isinstance(lenses,list) and bool(lenses) and all(isinstance(v,dict) and all(isinstance(v.get(k),str) and v[k].strip() for k in ['situation','why_it_matters','when_value_falls','what_to_observe']) for v in lenses),f'{row["id"]}: invalid decision lenses')
        if 'value_facets' in row:
            facets=row['value_facets']
            check(isinstance(facets,list) and bool(facets) and all(isinstance(f,dict) and all(isinstance(f.get(k),str) and f[k].strip() for k in ['focus','viewer_or_user_value','material_cue']) for f in facets),f'{row["id"]}: invalid value facets')
    shared_route_files = {root/'AGENTS.md', root/'.agents/skills/write-consumer-training-comments/SKILL.md'}
    documents = [*kb.rglob('*.md'), *skill.rglob('*.md'), *sorted(shared_route_files)]
    link_checks = 0
    out_of_scope_links = []
    for document in documents:
        for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', document.read_text()):
            if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', target):
                continue
            target = unquote(target.split('#',1)[0].strip('<>'))
            if not target:
                continue
            line_match = re.fullmatch(r'(.+):(\d+)', target)
            line_number = int(line_match[2]) if line_match else None
            if line_match:
                target = line_match[1]
            path = Path(target) if target.startswith('/') else document.parent/target
            if document in shared_route_files and 'nano' not in str(path).casefold():
                if not path.exists():
                    out_of_scope_links.append(f'{document.relative_to(root)}: unrelated route target missing: {target}')
                continue
            check(path.exists(), f'{document.relative_to(root)}: broken link {target}')
            if line_number is not None and path.is_file():
                check(1 <= line_number <= len(path.read_text().splitlines()),
                      f'{document.relative_to(root)}: source line out of range {target}:{line_number}')
            link_checks += 1
    return {
        'checked_at':datetime.now().astimezone().isoformat(timespec='seconds'),
        'result':'pass' if not failures else 'fail',
        'facts':len(facts), 'fact_status':dict(Counter(f['status'] for f in facts)),
        'sources':len(sources), 'source_hashes_checked':hash_checks,
        'scenarios':len(scenes), 'audience_hypotheses':len(hypotheses),
        'selling_points':len(selling), 'training_scenarios':len(training),
        'selling_value_facets':sum(len(row.get('value_facets',[])) for row in selling),
        'selling_decision_lenses':sum(len(row.get('decision_lenses',[])) for row in selling),
        'scenes_with_detail_branches':sum(bool(row.get('observable_details')) and bool(row.get('interest_branches')) for row in training),
        'scenes_with_usage_stages':sum(bool(row.get('usage_stage_angles')) for row in training),
        'training_expression_angles':sum(len(row['expression_angles']) for row in training),
        'hypothesis_review_status':dict(Counter(h['review_status'] for h in hypotheses)),
        'local_link_targets_checked':link_checks,
        'shared_route_scope':'Nano edges only; all links inside Nano knowledge and skill files are checked, including shared dependencies.',
        'out_of_scope_route_notes':out_of_scope_links,
        'pending_fact_ids':[f['id'] for f in facts if f['status'] == 'pending'],
        'limitations':['Does not re-fetch official sources, check Markdown anchors, verify product truth, evaluate expression quality, or grant user endorsement.'],
        'failures':failures,
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    report = validate()
    text = json.dumps(report, ensure_ascii=False, indent=2) + '\n'
    if args.output:
        args.output.write_text(text)
    print(text, end='')
    raise SystemExit(0 if report['result'] == 'pass' else 1)
