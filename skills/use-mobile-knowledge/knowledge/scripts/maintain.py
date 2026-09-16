#!/usr/bin/env python3
"""Render the Mobile knowledge records, or audit their structure and saved evidence."""
import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from datetime import date
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
MODELS = {
    'osmo_mobile_8p': 'Osmo Mobile 8P', 'osmo_mobile_8': 'Osmo Mobile 8',
    'osmo_mobile_7p': 'Osmo Mobile 7P', 'osmo_mobile_7': 'Osmo Mobile 7',
    'osmo_mobile_6': 'Osmo Mobile 6', 'osmo_mobile_se': 'Osmo Mobile SE',
    'dji_om_5': 'DJI OM 5',
}
TOPICS = {
    'identity': '身份与组件', 'stabilization': '增稳与运镜', 'controls': '安装与操作',
    'tracking': '跟随与遥控', 'compatibility': '手机与配件兼容', 'audio': '收音连接',
    'power': '续航与供电', 'kits': '套装', 'maintenance': '维护与限制', 'software': '软件与固件',
}


def read_records(pattern):
    rows = []
    for path in sorted(ROOT.glob(pattern)):
        for number, line in enumerate(path.read_text(encoding='utf-8').splitlines(), 1):
            if line.strip():
                try:
                    record = json.loads(line)
                except json.JSONDecodeError as exc:
                    raise ValueError(f'{path.relative_to(ROOT)}:{number}: {exc}') from exc
                rows.append((path, number, record))
    return rows


def all_records():
    return {
        'sources': read_records('sources/*.jsonl'),
        'facts': read_records('products/*.facts.jsonl'),
        'compatibility': read_records('compatibility/*.jsonl'),
        'models': read_records('products/models.jsonl'),
        'scenarios': read_records('scenarios/cards.jsonl'),
        'audiences': read_records('audiences/profiles.jsonl'),
        'selling_points': read_records('selling_points/cards.jsonl'),
        'use_cases': read_records('use_cases/cards.jsonl'),
    }


def text_list(values):
    return '；'.join(str(v) for v in values) if values else '来源未另列；不作额外推断'


def source_ref(ref, sources, prefix='../'):
    src = sources.get(ref['source_id'])
    if not src:
        return f"{ref['source_id']}（来源缺失）"
    return f"[{ref['source_id']}]({prefix}sources/README.md#{ref['source_id'].lower()})｜{ref['locator']}"


def fact_block(record, sources):
    lines = [f"<a id=\"{record['id'].lower()}\"></a>", f"### {record['id']}｜{record['statement']}", '',
             f"- 型号：{', '.join(MODELS[x] for x in record['models'])}；组件：{record['component']}",
             f"- 状态：`{record['status']}`；实际核验：{record['checked_at']}",
             f"- 条件：{text_list(record['conditions'])}", f"- 限制与不可推论：{text_list(record['limitations'])}"]
    if 'method' in record:
        lines += [f"- 设备：{text_list(record['devices'])}；路径：{record['method']}",
                  f"- 支持结论：`{record['support']}`；功能：{text_list(record['features'])}"]
    if record.get('gap_reason'):
        lines.append(f"- 待核／冲突原因：{record['gap_reason']}")
    lines.append('- 依据：' + '；'.join(source_ref(r, sources) for r in record['source_refs']))
    return '\n'.join(lines) + '\n'


def render():
    groups = all_records()
    for directory in ('products', 'compatibility', 'sources', 'scenarios'):
        (ROOT / directory).mkdir(exist_ok=True)
    srcs = {r['id']: r for _, _, r in groups['sources']}
    facts = [r for _, _, r in groups['facts']]
    compatibility = [r for _, _, r in groups['compatibility']]
    records = facts + compatibility
    for model, name in MODELS.items():
        rows = [r for r in facts if model in r['models']]
        lines = [f'# {name} 产品事实', '', '本页由结构化记录生成；引用前读取完整条件和官方依据。`verified` 只表示按记录日期核验，不表示实机测试。', '']
        for topic, title in TOPICS.items():
            matches = [r for r in rows if r['topic'] == topic]
            if matches:
                lines += [f'## {title}', ''] + [fact_block(r, srcs) for r in matches]
        (ROOT / 'products' / f'{model}.md').write_text('\n'.join(lines), encoding='utf-8')
    lines = ['# 兼容与连接路径', '', '按具体云台型号阅读。安装、蓝牙连接、快门控制、取景和跟随分别核对；未列出的组合不代表不支持。', '']
    for model, name in MODELS.items():
        matches = [r for r in compatibility if model in r['models']]
        if matches:
            lines += [f'## {name}', ''] + [fact_block(r, srcs) for r in matches]
    (ROOT / 'compatibility' / 'guide.md').write_text('\n'.join(lines), encoding='utf-8')
    lines = ['# 官方来源台账', '', '只登记实际读取资料。快照哈希对应保存文件；核验日不是发布日期，海外页面不直接证明中国区套装。', '']
    for src in srcs.values():
        lines += [f"<a id=\"{src['id'].lower()}\"></a>", f"## {src['id']}｜{src['title']}", '',
                  f"- [官方原链接]({src['url']})；[保存证据]({src['local_path'].removeprefix('sources/')})",
                  f"- 类型：{src['type']}；语言：{src['language']}；地区：{src['region']}",
                  f"- 实际读取：{src['checked_at']}；发布日期：{src.get('published_at') or '未明示'}；版本：{src.get('document_version') or '未明示'}",
                  f"- 阅读范围：{src['read_scope']}", f"- SHA256：`{src['sha256']}`", '']
        if src.get('snapshot_path'):
            lines += [f"- [提取快照]({src['snapshot_path'].removeprefix('sources/')})；提取方式：{src.get('extraction', '见快照文件说明')}",
                      f"- 快照 SHA256：`{src.get('snapshot_sha256', '未登记')}`", '']
        if src.get('download_page_date'):
            lines += [f"- 下载中心标注日期：{src['download_page_date']}；{src.get('date_note', '不自动视为PDF正文声明的发布日期')}", '']
    (ROOT / 'sources' / 'README.md').write_text('\n'.join(lines), encoding='utf-8')
    lines = ['# 主题覆盖表', '', '数字为事实和兼容记录数量；数量不等于资料完整。主型号每个主题应有已核依据或明确缺口。辅助型号仅承担识别及关键差异。', '', '| 型号 | 主题 | 已核 | 待核／冲突 |', '|---|---|---:|---:|']
    for model, name in MODELS.items():
        for topic, title in TOPICS.items():
            rows = [r for r in records if model in r['models'] and r['topic'] == topic]
            lines.append(f"| {name} | {title} | {sum(r['status'] == 'verified' for r in rows)} | {sum(r['status'] != 'verified' for r in rows)} |")
    (ROOT / 'products' / 'topic-coverage.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    lines = ['# 缺口与资料冲突', '', '这些条目只提示需要核实的问题，不作为肯定能力依据。无命中不等于明确不支持。', '']
    for record in records:
        if record['status'] != 'verified':
            lines += [f"## {record['id']}", '', f"- 型号：{', '.join(MODELS[m] for m in record['models'])}",
                      f"- 问题：{record['statement']}", f"- 状态：`{record['status']}`", f"- 原因：{record.get('gap_reason', '未填写')}",
                      '- 现有依据：' + '；'.join(source_ref(r, srcs, '') for r in record['source_refs']), '']
    lines += ['## 首版资料边界', '', '本库没有设备实测、真实消费者语料或竞品横评。手机兼容表的全部机型未逐项转写；具体手机仍须读取对应原表的型号列、系统条件及脚注。当前保存版本之外的后续固件、App、价格和套装变化需要重新核验。', '']
    (ROOT / 'GAPS.md').write_text('\n'.join(lines), encoding='utf-8')
    scenarios = [r for _, _, r in groups['scenarios']]
    if scenarios:
        record_paths = {r['id']: ('../compatibility/guide.md' if 'method' in r else f"../products/{r['models'][0]}.md") for r in records}
        lines = ['# 场景解释', '', '以下均为编辑推演，用于理解拍摄任务和消费者可能关注的问题，不代表真实用户反馈或原帖内容。', '',
                 '需要更具体的拍摄时刻、卖点用途和培训表达方向时，读取[详细场景选材](../use_cases/guide.md)；本页保留七类概览。', '']
        for row in scenarios:
            lines += [f"<a id=\"{row['id'].lower()}\"></a>", f"## {row['id']}｜{row['title']}", '',
                      f"- 型号：{', '.join(MODELS[x] for x in row['models'])}", f"- 任务：{row['task']}",
                      f"- 可能关注：{text_list(row['possible_concerns'])}", f"- 解释：{row['guidance']}",
                      f"- 条件：{text_list(row['conditions'])}", f"- 限制：{text_list(row['limitations'])}",
                      '- 依据：' + '、'.join(f"[{key}]({record_paths[key]}#{key.lower()})" for key in row['fact_ids'] + row['compatibility_ids']), '']
        (ROOT / 'scenarios' / 'guide.md').write_text('\n'.join(lines), encoding='utf-8')
    from render_audiences import render as render_audiences
    render_audiences()
    from selling_points import render as render_selling_points
    render_selling_points(groups)
    from use_cases import render as render_use_cases
    render_use_cases(groups)
    print(json.dumps({'rendered': True, 'facts': len(facts), 'compatibility': len(compatibility), 'sources': len(srcs), 'scenarios': len(scenarios), 'audiences': len(groups['audiences']), 'selling_points': len(groups['selling_points']), 'use_cases': len(groups['use_cases'])}, ensure_ascii=False))


def audit():
    groups = all_records()
    errors = []
    all_ids = {}
    def check(ok, message):
        if not ok:
            errors.append(message)
    for kind, rows in groups.items():
        check(bool(rows), f'{kind}: 没有记录')
        for path, number, row in rows:
            label = f'{path.relative_to(ROOT)}:{number}'
            key = row.get('id')
            check(isinstance(key, str) and bool(key), f'{label}: 缺少ID')
            check(key not in all_ids, f'{label}: 重复ID {key}')
            all_ids[key] = row
    sources = {r['id']: r for _, _, r in groups['sources']}
    fact_rows = {r['id']: r for _, _, r in groups['facts']}
    compat_rows = {r['id']: r for _, _, r in groups['compatibility']}
    source_required = {'id', 'title', 'url', 'type', 'language', 'region', 'document_version', 'published_at', 'checked_at', 'read_scope', 'local_path', 'sha256'}
    for src in sources.values():
        key = src['id']
        check(source_required <= src.keys(), f'{key}: 来源字段缺失 {source_required - src.keys()}')
        host = urlsplit(src.get('url', '')).hostname or ''
        check(any(host == base or host.endswith('.' + base) for base in ('dji.com', 'djicdn.com', 'dji.net', 'djiits.com')), f'{key}: 非已知官方域名 {host}')
        local = (ROOT / src.get('local_path', '')).resolve()
        check(local.is_relative_to(ROOT), f'{key}: 证据越出本库')
        check(local.is_file(), f'{key}: 保存证据不存在')
        if local.is_file():
            check(hashlib.sha256(local.read_bytes()).hexdigest() == src.get('sha256'), f'{key}: SHA256不一致')
        if src.get('snapshot_path'):
            snapshot = (ROOT / src['snapshot_path']).resolve()
            check(snapshot.is_relative_to(ROOT) and snapshot.is_file(), f'{key}: 快照路径无效')
            if snapshot.is_file():
                check(hashlib.sha256(snapshot.read_bytes()).hexdigest() == src.get('snapshot_sha256'), f'{key}: 快照SHA256不一致')
    required = {'id', 'models', 'component', 'topic', 'statement', 'conditions', 'limitations', 'source_refs', 'checked_at', 'status', 'keywords'}
    for key, row in {**fact_rows, **compat_rows}.items():
        check(required <= row.keys(), f'{key}: 事实字段缺失 {required - row.keys()}')
        check(bool(row.get('models')) and set(row.get('models', [])) <= MODELS.keys(), f'{key}: 无效型号')
        check(row.get('topic') in TOPICS, f'{key}: 无效主题')
        check(row.get('status') in {'verified', 'pending', 'conflict'}, f'{key}: 无效状态')
        for field in ('models', 'conditions', 'limitations', 'source_refs', 'keywords'):
            check(isinstance(row.get(field), list), f'{key}: {field}不是数组')
        try:
            when = date.fromisoformat(row.get('checked_at', ''))
            check(when <= date.today(), f'{key}: 核验日期在未来')
        except ValueError:
            check(False, f'{key}: 日期格式无效')
        if row.get('status') == 'verified':
            check(bool(row.get('source_refs')), f'{key}: 已核事实无来源')
        else:
            check(bool(row.get('gap_reason')), f'{key}: 未核事实无原因')
        for ref in row.get('source_refs', []):
            check(ref.get('source_id') in sources and bool(ref.get('locator')), f'{key}: 来源引用无效 {ref}')
        if key in compat_rows:
            extra = {'gimbal_model', 'devices', 'method', 'support', 'features'}
            check(extra <= row.keys(), f'{key}: 兼容字段缺失 {extra - row.keys()}')
            check(row.get('models') == [row.get('gimbal_model')], f'{key}: 兼容型号端点不一致')
            check(row.get('support') in {'supported', 'not_supported', 'conditional', 'unconfirmed'}, f'{key}: 无效兼容状态')
            check(not (row.get('status') == 'verified' and row.get('support') == 'unconfirmed'), f'{key}: 已核兼容却未确认')
    model_ids = {r['id'] for _, _, r in groups['models']}
    check(model_ids == MODELS.keys(), '型号目录未准确覆盖约定七款')
    for _, _, row in groups['models']:
        for key in row.get('fact_ids', []):
            check(key in fact_rows and row['id'] in fact_rows[key]['models'], f"{row['id']}: 型号事实引用错误 {key}")
    for _, _, row in groups['scenarios']:
        key = row['id']
        check(row.get('kind') == 'editorial_synthesis', f'{key}: 场景性质错误')
        check(bool(row.get('fact_ids')), f'{key}: 场景无事实依据')
        check(set(row.get('models', [])) <= MODELS.keys(), f'{key}: 场景型号无效')
        for field, mapping in [('fact_ids', fact_rows), ('compatibility_ids', compat_rows)]:
            for ref in row.get(field, []):
                check(ref in mapping, f'{key}: 场景引用不存在 {ref}')
                if ref in mapping:
                    check(mapping[ref]['status'] == 'verified', f'{key}: 场景肯定依据未核 {ref}')
                    check(bool(set(row['models']) & set(mapping[ref]['models'])), f'{key}: 场景依据型号不相交 {ref}')
    for model in ('osmo_mobile_8p', 'osmo_mobile_8'):
        covered = {r['topic'] for r in [*fact_rows.values(), *compat_rows.values()] if model in r['models']}
        check(covered >= TOPICS.keys(), f'{model}: 主型号主题缺失 {TOPICS.keys() - covered}')
    scenario_ids = {r['id'] for _, _, r in groups['scenarios']}
    audience_required = {'id', 'role', 'kind', 'status', 'created_at', 'basis', 'task',
                         'possible_motives', 'psychological_tension', 'acceptable_operation_load',
                         'abandon_or_switch_triggers', 'alternative_explanations', 'selection_cues',
                         'natural_expression', 'fact_ids', 'compatibility_ids', 'scenario_ids',
                         'claim_guardrails', 'model_scope_note'}
    for _, _, row in groups['audiences']:
        key = row['id']
        check(audience_required <= row.keys(), f'{key}: 人群字段缺失 {audience_required - row.keys()}')
        check(row.get('kind') == 'editorial_hypothesis' and row.get('status') == 'hypothesis_only', f'{key}: 心理假设性质错误')
        basis = row.get('basis', {})
        check(basis.get('type') == 'editorial_reasoning' and basis.get('empirical_evidence_refs') == [], f'{key}: 编辑假设不得冒充实证研究')
        for field in ('possible_motives', 'abandon_or_switch_triggers', 'alternative_explanations', 'selection_cues', 'claim_guardrails'):
            check(isinstance(row.get(field), list) and bool(row[field]), f'{key}: {field}须为非空数组')
        for field, mapping in [('fact_ids', fact_rows), ('compatibility_ids', compat_rows)]:
            for ref in row.get(field, []):
                check(ref in mapping, f'{key}: 人群引用不存在 {ref}')
                if ref in mapping:
                    check(mapping[ref]['status'] == 'verified', f'{key}: 人群肯定依据未核 {ref}')
        check(set(row.get('scenario_ids', [])) <= scenario_ids, f'{key}: 人群场景引用不存在')
        examples = row.get('natural_expression', {}).get('illustrative_fragments', [])
        check(bool(examples), f'{key}: 缺少表达示意')
        for example in examples:
            check(example.get('content_mode') == 'training_fiction', f'{key}: 示意未标训练虚构')
            check(example.get('calibration_status') == 'pending_calibration' and example.get('user_endorsed') is False, f'{key}: 待校准示意不得成为认可范文')
            check(example.get('source_kind') == 'synthetic_illustration' and example.get('product_claims') == [], f'{key}: 心理表达不能冒充原话或产品事实')
    from selling_points import audit as audit_selling_points
    errors.extend(audit_selling_points(groups))
    from use_cases import audit as audit_use_cases
    errors.extend(audit_use_cases(groups))
    link_count = 0
    for path in ROOT.rglob('*.md'):
        for match in re.finditer(r'(?<!!)\[[^\]]+\]\(([^)]+)\)', path.read_text(encoding='utf-8')):
            target = match.group(1).strip('<>')
            parsed = urlsplit(target)
            if parsed.scheme:
                continue
            file = unquote(parsed.path)
            dest = (path.parent / file).resolve() if file else path
            link_count += 1
            check(dest.is_file(), f'{path.relative_to(ROOT)}: 链接不存在 {target}')
            if dest.is_file() and parsed.fragment and dest.suffix == '.md':
                body = dest.read_text(encoding='utf-8')
                anchors = set(re.findall(r'<a\s+id="([^"]+)"', body))
                anchors.update(re.sub(r'[^\w\- ]', '', line.strip().lower()).replace(' ', '-') for line in re.findall(r'^#+\s+(.+)$', body, re.M))
                check(unquote(parsed.fragment) in anchors, f'{path.relative_to(ROOT)}: 锚点不存在 {target}')
    result = {'ok': not errors, 'counts': {k: len(v) for k, v in groups.items()},
              'statuses': dict(Counter(r['status'] for r in [*fact_rows.values(), *compat_rows.values()])),
              'local_links_checked': link_count, 'errors': errors}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['render', 'audit'])
    args = parser.parse_args()
    if args.command == 'render':
        render()
        return 0
    return audit()


if __name__ == '__main__':
    sys.exit(main())
