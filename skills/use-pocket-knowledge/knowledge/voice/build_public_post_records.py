#!/usr/bin/env python3
"""Promote selected already-read train posts; never collect links or read holdout text."""
import json
import hashlib
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / 'knowledge/pocket'
EXCLUDED = {5, 16, 20, 21, 23, 28, 30, 40, 41, 42, 43, 44, 46}
BLOCKED_AUTHOR_INPUTS = {7, 17, 18, 52}

def read_rows(path):
    return [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines() if line.strip()]

def dump(path, rows):
    path.write_text(''.join(json.dumps(row, ensure_ascii=False) + '\n' for row in rows), encoding='utf-8')

def main():
    # Apply the split filter before joining notes or examining post content.
    works = {row['work_id']: row for row in read_rows(BASE / 'corpus/works.jsonl') if row.get('split') == 'train'}
    works_sha = hashlib.sha256((BASE / 'corpus/works.jsonl').read_bytes()).hexdigest()
    notes = {}
    for batch in ['01', '02', '03']:
        path = BASE / f'corpus/analysis/xiaohongshu-posts-{batch}.train-notes.jsonl'
        for row in read_rows(path):
            if row.get('split') != 'train':
                continue
            notes[row['work_id']] = (row, str(path.relative_to(ROOT)))
    promoted, skipped = [], []
    for batch in ['01', '02', '03']:
        path = BASE / f'corpus/normalized/xiaohongshu-posts-{batch}.jsonl'
        sha = hashlib.sha256(path.read_bytes()).hexdigest()
        for line_number, row in enumerate(read_rows(path), 1):
            if row.get('split') != 'train':
                continue
            order = row['inputOrder']
            if order in EXCLUDED:
                skipped.append({'input_order': order, 'work_id': row['work_id'], 'reason': '正文只有标签、泛教程口号或未展开的导语；保留train-notes，不进入可调用原话记录'})
                continue
            work = works[row['work_id']]
            note, note_path = notes[row['work_id']]
            assert work['split'] == 'train' and row.get('text')
            blocked = order in BLOCKED_AUTHOR_INPUTS
            limits = [
                '公开帖子作者原话，不是评论；没有评论父句，不计主评或父句回复。',
                '只读取导出文字，未读取图片、连续视频或音轨；标题和正文不证明媒体实际效果。',
                'model_id沿用corpus/works的当前讨论主型号；不认证作者实际持有、拍摄设备或功能使用。',
                '作者的第一人称、身份、关系和技术说法未经认证，不转为他人的经历或产品事实。',
                '公共作者不等同独立消费者；商业关系、内容原创性和真人身份均未认证。',
            ]
            for limitation in note.get('limitations', []):
                if any(marker in limitation for marker in ['unknown', '规范化', '未修改voice', '未改voice', '不修改voice']):
                    continue
                if limitation not in limits:
                    limits.append(limitation)
            if blocked:
                limits.append('本账号存在跨split多篇作品；本条仅保留原话，不参与新pattern的独立作品或作者支持计数。')
            column = row['source_columns']['post_text']['column']
            original_locator = row['source_locator']
            record = {
                'id': 'post:xiaohongshu:' + row['work_id'], 'work_id': row['work_id'],
                'platform': 'xiaohongshu', 'material_kind': 'public_post', 'source_kind': 'public_post',
                'speaker_scope': 'work_author', 'thread_role': 'post', 'parent_id': None, 'root_id': None,
                'parent_basis': 'not_a_comment_no_parent', 'split': 'train', 'input_order': order,
                'author_id': row.get('author_id'), 'author_identity_status': 'exported_account_id_unverified_person',
                'model_id': work.get('model_id', 'unknown'), 'model_basis': work.get('model_basis'),
                'model_scope': 'discussion_subject_only', 'actual_capture_model': work.get('actual_capture_model', 'unknown'),
                'model_source_path': 'knowledge/pocket/corpus/works.jsonl', 'model_source_sha256': works_sha,
                'original_parser_model_id': row.get('model_id'), 'mentioned_model_ids': row.get('model_candidates', []),
                'title': row.get('title'), 'text': row['text'], 'text_status': 'available',
                'canonical_url': row.get('canonical_url'),
                'source_path': str(path.relative_to(ROOT)), 'source_sha256': sha,
                'source_locator': {'line': line_number, 'json_pointer': '/text', 'original_file': row['source_path'],
                                   **original_locator, 'column': column, 'cell': column + str(original_locator['row'])},
                'raw_source_path': row['source_path'], 'raw_source_sha256': row['source_sha256'],
                'collected_at': row.get('collected_at'), 'created_at': row.get('created_at'),
                'timestamp_timezone': row.get('timestamp_timezone'),
                'read_scope': 'train_exported_post_title_and_text_only; no_comments_or_media',
                'content_role': note['content_role'], 'analysis_note_id': note['id'], 'analysis_note_path': note_path,
                'pattern_support_eligible': not blocked,
                'pattern_support_basis': 'excluded_shared_author_cluster_by_research_rule' if blocked else 'eligible_for_case_by_case_selection_not_automatic_pattern_support',
                'limitations': limits,
            }
            promoted.append(record)
    assert len(promoted) == 37 and len(skipped) == 13
    output = BASE / 'voice/records.jsonl'
    prior = read_rows(output)
    new_ids = {row['id'] for row in promoted}
    preserved = [row for row in prior if row['id'] not in new_ids]
    assert not any(row.get('split') == 'holdout' for row in promoted)
    dump(output, preserved + promoted)
    report = {
        'checked_at': '2026-09-06', 'source_scope': '50 previously read train public_post notes',
        'promoted_public_post_records': len(promoted), 'preserved_other_records': len(preserved),
        'by_canonical_model': dict(Counter(row['model_id'] for row in promoted)),
        'pattern_blocked_input_orders': sorted(BLOCKED_AUTHOR_INPUTS), 'excluded_train_posts': skipped,
        'new_main_comments': 0, 'new_parent_reply_pairs': 0, 'holdout_records_read_or_promoted': 0,
        'limitations': ['原始导出均按split过滤后才检查正文；未打开平台、媒体或holdout正文。',
                        '37条是可检索的作者文字材料，不是37篇研究验收通过的作品，也不是评论。'],
    }
    (BASE / 'voice/public-post-ingest-report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({key: value for key, value in report.items() if key != 'excluded_train_posts'}, ensure_ascii=False))

if __name__ == '__main__':
    main()
