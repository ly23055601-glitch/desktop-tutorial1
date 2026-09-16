#!/usr/bin/env python3
"""Write a dated coverage snapshot from the actual library; never change records."""
from datetime import datetime
from collections import Counter, defaultdict
import json
from pathlib import Path
from pocket_knowledge import DEFAULT_ROOT, audit, load, source_path


def acquisition_scope(root, data):
    """Count library records by origin; inspect batch metadata, never old attachments.

    Research counts use actual corpus identities. A manifest supplies only the
    authorized target/window, never the reported number of successful records.
    The same comment can belong to several research batches; batch totals must
    therefore not be added to produce a unique library total.
    """
    works, comments = data['works'], data['comments']
    work_index = {(w.get('platform'), w.get('work_id')): w for w in works}
    batches = defaultdict(lambda: {'works': set(), 'comments': {}, 'manifest_candidates': set()})

    def comment_key(row):
        return (row.get('platform'), row.get('work_id'), row.get('comment_id') or row.get('id'))

    def add_manifest_candidate(bucket, value, evidence=False):
        path = source_path(root, value)
        if path:
            bucket['manifest_candidates'].add((path.parent.parent if evidence else path.parent) / 'manifest.json')

    for work in works:
        batch_id = work.get('research_batch_id')
        if batch_id:
            bucket = batches[batch_id]
            bucket['works'].add((work.get('platform'), work.get('work_id')))
            add_manifest_candidate(bucket, work.get('source_path'), evidence=True)
    for row in comments:
        for occurrence in row.get('source_occurrences', []):
            batch_id = occurrence.get('batch_id')
            if not batch_id or not (occurrence.get('research_path') or batch_id in batches):
                continue
            bucket = batches[batch_id]
            bucket['works'].add((row.get('platform'), row.get('work_id')))
            bucket['comments'][comment_key(row)] = row
            add_manifest_candidate(bucket, occurrence.get('research_path'))
    research_comment_keys = {identity for batch in batches.values() for identity in batch['comments']}
    by_batch = {}
    for batch_id, bucket in sorted(batches.items()):
        manifest, manifest_path = {}, None
        for path in sorted(bucket['manifest_candidates']):
            if not path.is_file():
                continue
            candidate = json.loads(path.read_text(encoding='utf-8'))
            if candidate.get('batch_id') == batch_id:
                manifest, manifest_path = candidate, path
                break
        rows = list(bucket['comments'].values())
        present_works = bucket['works'].intersection(work_index)
        sourced_works = {identity for identity in present_works if work_index[identity].get('read_scope') and
                         (path := source_path(root, work_index[identity].get('source_path'))) and path.is_file()}
        with_comments = {(r.get('platform'), r.get('work_id')) for r in rows}
        platform_works = Counter(platform for platform, _ in sourced_works)
        platform_comments = Counter(r.get('platform') for r in rows)
        target = manifest.get('target', {})
        work_target = target.get('works')
        comment_target = target.get('comments', target.get('comments_approx'))
        if comment_target is None and isinstance(work_target, int) and isinstance(target.get('comments_per_work_approx'), int):
            comment_target = work_target * target['comments_per_work_approx']
        per_platform = target.get('per_platform')
        if isinstance(per_platform, int):
            per_platform = {platform: per_platform for platform in manifest.get('platforms', manifest.get('inputs', {}).keys())}
        per_platform = per_platform if isinstance(per_platform, dict) else {}
        shortfall = {'works': max(0, work_target - len(sourced_works)) if isinstance(work_target, int) else None,
                     'comments_approx': max(0, comment_target - len(rows)) if isinstance(comment_target, int) else None,
                     'per_platform': {platform: max(0, count - platform_works[platform]) for platform, count in per_platform.items() if isinstance(count, int)}}
        known = isinstance(work_target, int) and isinstance(comment_target, int)
        met = known and shortfall['works'] == 0 and shortfall['comments_approx'] == 0 and not any(shortfall['per_platform'].values())
        records_by_id = {r.get('id'): r for r in comments}
        replies = [r for r in rows if r.get('thread_role') == 'reply']
        confirmed = [r for r in replies if (p := records_by_id.get(r.get('parent_id'))) and p.get('work_id') == r.get('work_id') and p.get('platform') == r.get('platform') and p.get('text')]
        by_batch[batch_id] = {
            'works_in_corpus': len(present_works), 'works_with_post_source': len(sourced_works), 'unread_work_records': len(present_works - sourced_works),
            'works_with_comments': len(sourced_works & with_comments), 'post_only_works': len(sourced_works - with_comments), 'comment_records': len(rows),
            'root_comment_records': sum(r.get('thread_role') == 'root' for r in rows), 'reply_records': len(replies),
            'replies_with_resolvable_parent': len(confirmed),
            'new_comment_records': sum(bool(r.get('source_occurrences')) and r['source_occurrences'][0].get('batch_id') == batch_id for r in rows),
            'by_platform': {platform: {'works': platform_works[platform], 'comments': platform_comments[platform]} for platform in sorted(set(platform_works) | set(platform_comments) | set(per_platform))},
            'targets': {'works': work_target, 'comments_approx': comment_target, 'per_platform': per_platform},
            'shortfall': shortfall, 'sampling_target_status': 'met_numbers_only' if met else 'not_met' if known else 'target_not_available',
            'manifest_path': str(manifest_path) if manifest_path else None, 'recorded_batch_status': manifest.get('status'),
            'work_publication_window': manifest.get('window'),
            'count_basis': 'Unique actual corpus identities associated through research_batch_id or source_occurrences; manifest actual counts are not used.',
            'boundary': 'Sampling targets are separate from historical cancelled quotas, collection completeness, semantic review and user acceptance; comments are a sample, not platform totals.',
        }
    historical_batches = defaultdict(set)
    for row in comments:
        for occurrence in row.get('source_occurrences', []):
            if occurrence.get('batch_id') and occurrence['batch_id'] not in batches:
                historical_batches[occurrence['batch_id']].add(comment_key(row))
    state_path = root / 'corpus/run-state.json'
    state = json.loads(state_path.read_text(encoding='utf-8')) if state_path.is_file() else {}
    old_status = {b.get('batch_id'): b for b in state.get('batches', [])}
    history = []
    for batch_id in sorted(set(historical_batches) | {name for name, b in old_status.items() if b.get('retained_rows')}):
        item = old_status.get(batch_id, {})
        history.append({'batch_id': batch_id, 'platform': item.get('platform'), 'status': item.get('status'),
                        'ingested_comment_records': len(historical_batches[batch_id]),
                        'retained_unreviewed_rows': item.get('retained_rows', 0) if item.get('included_in_learning') is False else 0,
                        'old_queue_resumed': False})
    platforms = sorted({w.get('platform') for w in works if w.get('platform')} | {r.get('platform') for r in comments if r.get('platform')})
    return {'historical_candidate_works': sum(not w.get('research_batch_id') for w in works),
            'research_added_work_records': sum(bool(w.get('research_batch_id')) for w in works),
            'research_associated_comment_records': len(research_comment_keys),
            'historical_only_comment_records': sum(comment_key(r) not in research_comment_keys for r in comments),
            'by_platform': {platform: {'work_records': sum(w.get('platform') == platform for w in works),
                                       'ingested_comments': sum(r.get('platform') == platform for r in comments),
                                       'research_added_works': sum(w.get('platform') == platform and bool(w.get('research_batch_id')) for w in works),
                                       'research_associated_comments': sum(identity[0] == platform for identity in research_comment_keys)} for platform in platforms},
            'research_batches': by_batch, 'historical_comment_batches': history,
            'batch_totals_are_additive': False}


def build_report(root=DEFAULT_ROOT):
    root = Path(root)
    data, issues = load(root)
    report = audit(root, data, issues)
    materials = None
    if (root / 'selling_points/cards.jsonl').is_file() and (root / 'use_cases/cards.jsonl').is_file():
        from pocket_materials import read as read_materials, audit as audit_materials
        materials = audit_materials(read_materials(root))
        report['selling_and_use_cases'] = materials
    report['snapshot_at'] = datetime.now().astimezone().isoformat()
    ready = report['integrity_ok'] and report['current_library']['status'] == 'usable_with_documented_gaps' and (materials is None or materials['integrity_ok'])
    report['delivery_summary'] = {
        'profile': report['project_scope'].get('profile'),
        'status': 'organized_and_callable' if ready else 'review_required',
        'scale_targets': 'cancelled_by_user' if report['historical_target']['status'] == 'cancelled_by_user' else 'see_historical_target',
        'counts_scope': 'Actual corpus, research batches and historical stopped attachments are separate. Cancelling the old 150-work quota does not complete or cancel a new research target.',
        'acceptance_boundary': 'Reference integrity is not semantic proof or user approval of the two example drafts. No comparative evaluation pass is inferred.',
    }
    report['acquisition_progress'] = {
        'candidate_works': len(data['works']),
        'works_with_post_source': sum(bool(w.get('read_scope') and (path := source_path(root, w.get('source_path'))) and path.is_file()) for w in data['works']),
        'ingested_comment_records': report['counts']['ingested_comment_records'],
        'retained_unreviewed_comment_rows': report['counts']['retained_unreviewed_comment_rows'],
        'voice_cards_total': len(data['voice']),
        'new_voice_cards': sum(c.get('source_kind') in {'public_post', 'public_comment'} for c in data['voice']),
        'legacy_voice_cards': sum(c.get('split') == 'legacy' for c in data['voice']),
        'legacy_voice_patterns': sum(c.get('split') == 'legacy' and c.get('status') == 'pattern' for c in data['voice']),
        'legacy_voice_cases': sum(c.get('split') == 'legacy' and c.get('status') == 'case' for c in data['voice']),
        'public_post_records': sum(r.get('material_kind') == 'public_post' for r in data['records']),
        'public_post_patterns': sum(c.get('source_kind') == 'public_post' and c.get('status') == 'pattern' for c in data['voice']),
        'public_post_cases': sum(c.get('source_kind') == 'public_post' and c.get('status') == 'case' for c in data['voice']),
        'public_comment_records': len({r['id'] for r in data['records'] + data['comments'] if r.get('split') in {'train', 'holdout'} and r.get('material_kind', 'comment') == 'comment'}),
        'public_comment_patterns': sum(c.get('source_kind') == 'public_comment' and c.get('status') == 'pattern' for c in data['voice']),
        'public_comment_cases': sum(c.get('source_kind') == 'public_comment' and c.get('status') == 'case' for c in data['voice']),
    }
    report['acquisition_progress'].update(acquisition_scope(root, data))
    report['delivery_summary']['research_sampling_targets'] = {batch_id: batch['sampling_target_status'] for batch_id, batch in report['acquisition_progress']['research_batches'].items()}
    return report


def render_report(report):
    ready = report['delivery_summary']['status'] == 'organized_and_callable'
    c, p = report['counts'], report['acquisition_progress']
    lines = [
        '# Pocket4 / Pocket4P 覆盖清单',
        '', f"当前资料库：{'已整理，可按需调用' if ready else '需要处理结构或材料问题'}。旧版规模计划与后续研究批次分别统计；资料库可调用不表示本批采样目标已完成。",
        '', f"更新时间：{report['snapshot_at']}。以下只列实际记录；采集状态、未整理附件与验收结论分别保留。", '',
        '| 项目 | 实际记录 | 说明 |', '|---|---:|---|',
        f"| 主款已核事实 | {c['primary_verified_facts']} | 两款共享事实去重；使用前仍复核官网 |",
        f"| 主款待核事实 | {c['primary_pending_facts']} | 不作为确定断言 |",
        f"| 官方来源 | {c['official_sources']} | 含旧代对照来源 |",
        f"| 作品记录总数 | {p['candidate_works']} | 历史候选 {p['historical_candidate_works']}；研究新增作品记录 {p['research_added_work_records']}；不等于均已完成读取 |",
        f"| 已保存作品字段来源 | {p['works_with_post_source']} | 不等于已读图片、视频或完整评论 |",
        f"| 已入库评论 | {p['ingested_comment_records']} | 含学习/留出、未知层级、空文字或媒体占位；不是独立讨论数 |",
        f"| 另存未整理评论附件 | {p['retained_unreviewed_comment_rows']} | C3停止时留存；不入库、不计有效作品、不用于表达学习 |",
        f"| 表达卡总数 | {p['voice_cards_total']} | 公开材料卡累计 {p['new_voice_cards']}；历史种子 {p['legacy_voice_cards']} |",
        f"| 历史表达规律 / 个案 | {p['legacy_voice_patterns']} / {p['legacy_voice_cases']} | 保留历史来源，不算本轮新采 |",
        f"| 公开帖子原话记录累计 | {p['public_post_records']} | 不计主评论或回复 |",
        f"| 正文表达规律 / 个案累计 | {p['public_post_patterns']} / {p['public_post_cases']} | 规律需独立作品支持 |",
        f"| 评论表达规律 / 个案累计 | {p['public_comment_patterns']} / {p['public_comment_cases']} | 只从学习材料归纳，出处与审读见表达库 |",
        f"| 合格公共作品累计 | {c['eligible_new_works']} | 型号、作者、来源、评论与采样限制均成立；不是单次研究实得数 |",
        f"| 独立文字主评讨论 | {c['main_discussions']} | 仅实际有来源且层级明确的文字主评；未知层级不推断 |",
        f"| 有明确文字父句回复的讨论 | {c['discussions_with_verified_parent_reply']} | 同楼更多回复不增加讨论数；纯表情不充文字讨论 |", '',
        f"学习 / 留出有效分布：`{json.dumps(c['by_split'], ensure_ascii=False)}`。平台分布：`{json.dumps(c['by_platform'], ensure_ascii=False)}`。", '',
        f"引用结构：{'通过' if report['integrity_ok'] else '存在错误'}。这不等于语义结论已经证明，也不等于两帖例稿已获用户认可；对照验收独立记录。", '',
        '历史说明：原150篇作品、450组主评与30篇对照验收属于已取消的规模计划，未宣称目标达成。仅需回看原配额时，可运行 `python3 scripts/pocket_knowledge.py audit --require-target --historical-target`。', '',
        '逐帖计入与排除原因见 [coverage.json](coverage.json)，原始来源见 [corpus/README.md](corpus/README.md)，主题缺口见 [products/topic-coverage.md](products/topic-coverage.md)，对照验收见 [evaluation/README.md](evaluation/README.md)。',
    ]
    lines += ['', '## 后续研究批次', '', '以下数量从库内作品、评论与批次引用计算；目标取自相应研究 manifest。不同批次可能复读同一条评论，不能相加当作库内唯一总量。']
    if not p['research_batches']:
        lines.append('\n暂无已关联入库材料的研究批次。')
    for batch_id, batch in p['research_batches'].items():
        targets = batch['targets']
        label = {'not_met': '采样目标未满', 'met_numbers_only': '数量达到，语义审读和用户验收另计', 'target_not_available': '目标元数据未找到，不推断完成'}[batch['sampling_target_status']]
        lines += ['', f"### {batch_id}", '',
                  f"有原帖来源作品 {batch['works_with_post_source']} / 目标 {targets['works'] if targets['works'] is not None else '未知'}；评论 {batch['comment_records']} / 约 {targets['comments_approx'] if targets['comments_approx'] is not None else '未知'}。{label}。",
                  f"库内关联作品记录 {batch['works_in_corpus']}；其中缺读取范围或原帖文件 {batch['unread_work_records']}。",
                  f"有评论作品 {batch['works_with_comments']}；仅原帖、无入库评论作品 {batch['post_only_works']}；主评 {batch['root_comment_records']}、回复 {batch['reply_records']}，其中父句可解析 {batch['replies_with_resolvable_parent']}。",
                  f"平台实得：`{json.dumps(batch['by_platform'], ensure_ascii=False)}`。缺口：`{json.dumps(batch['shortfall'], ensure_ascii=False)}`。",
                  '原150篇计划已取消不改变本批目标；读取量不等于全部评论、媒体已读或研究代表性。']
    lines += ['', '## 历史评论批次与停止附件', '', '| 批次 | 已入库评论 | 另存未学习行 | 历史状态 |', '|---|---:|---:|---|']
    for batch in p['historical_comment_batches']:
        lines.append(f"| {batch['batch_id']} | {batch['ingested_comment_records']} | {batch['retained_unreviewed_rows']} | {batch['status'] or '未记录'} |")
    lines.append('\n以上为旧台账状态，不表示后续研究再次停止或旧队列已恢复。')
    materials = report.get('selling_and_use_cases')
    if materials is not None:
        lines.append(f"\n卖点与详细场景：{materials['counts']['selling']}张卖点卡、{materials['counts']['scene']}张详细场景卡，引用结构{'通过' if materials['integrity_ok'] else '存在问题'}。使用价值是编辑解释，场景是待验证假设，不增加公开用户语料数量。见[卖点指南](selling_points/guide.md)、[详细场景](use_cases/guide.md)与[选材入口](TRAINING.md)。")
    return '\n'.join(lines) + '\n'


def main():
    root = DEFAULT_ROOT
    report = build_report(root)
    (root / 'coverage.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    (root / 'COVERAGE.md').write_text(render_report(report))
    print(json.dumps({'snapshot_at': report['snapshot_at'], 'integrity_ok': report['integrity_ok'], 'delivery_summary': report['delivery_summary'], 'historical_target_met': report['corpus_target_complete'], 'progress': report['acquisition_progress']}, ensure_ascii=False))


if __name__ == '__main__':
    main()
