#!/usr/bin/env python3
"""Render and audit editorial selling-point cards linked to canonical Mobile facts."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def context(groups=None):
    from maintain import all_records, MODELS
    groups = groups if groups is not None else all_records()
    records = {r['id']: r for kind in ('facts', 'compatibility') for _, _, r in groups[kind]}
    cards = [r for _, _, r in groups['selling_points']]
    return groups, MODELS, records, cards


def audit(groups=None):
    groups, models, records, cards = context(groups)
    errors = []
    def check(ok, message):
        if not ok: errors.append(message)
    audience_ids = {r['id'] for _, _, r in groups['audiences']}
    fact_ids = {r['id'] for _, _, r in groups['facts']}
    compatibility_ids = {r['id'] for _, _, r in groups['compatibility']}
    required = {'id', 'models', 'title', 'kind', 'value_status', 'edited_at', 'capability_summary',
                'task', 'possible_value', 'audience_ids', 'scope_note', 'fact_ids', 'compatibility_ids', 'avoid_claims'}
    seen = set()
    for card in cards:
        key = card.get('id')
        check(required <= card.keys(), f'{key}: 卖点字段不全')
        check(isinstance(key, str) and key not in seen, f'{key}: 卖点编号无效或重复');seen.add(key)
        check(card.get('kind') == 'editorial_synthesis', f'{key}: 卖点不是编辑解释')
        check(card.get('value_status') == 'hypothesis_not_measured', f'{key}: 价值不能标成实测或用户研究')
        check(len(card.get('models', [])) == 1 and set(card['models']) <= models.keys(), f'{key}: 卖点须精确对应一个型号')
        check(bool(card.get('audience_ids')) and set(card['audience_ids']) <= audience_ids, f'{key}: 角色引用无效')
        check(bool(card.get('avoid_claims')), f'{key}: 缺少不可推论')
        refs = card.get('fact_ids', []) + card.get('compatibility_ids', [])
        check(bool(refs), f'{key}: 卖点无事实依据')
        check(set(card.get('fact_ids', [])) <= fact_ids, f'{key}: 产品事实编号不存在')
        check(set(card.get('compatibility_ids', [])) <= compatibility_ids, f'{key}: 兼容编号不存在')
        for rid in refs:
            if rid not in records: continue
            r = records[rid]
            check(r['status'] == 'verified', f'{key}: 不能用待核或冲突支撑肯定能力 {rid}')
            check(set(card['models']) <= set(r['models']), f'{key}: 跨型号借用 {rid}')
    check({m for c in cards for m in c['models']} == models.keys(), '卖点尚未覆盖约定七款')
    return errors


def record_link(record):
    path = '../compatibility/guide.md' if 'method' in record else f"../products/{record['models'][0]}.md"
    return f"[{record['id']}]({path}#{record['id'].lower()})"


def render(groups=None):
    groups, models, records, cards = context(groups)
    errors = audit(groups)
    if errors: raise ValueError('\n'.join(errors))
    audience = {r['id']:r for _,_,r in groups['audiences']}
    out = ROOT/'selling_points';out.mkdir(exist_ok=True)
    lines = ['# Mobile 产品卖点与用户价值', '',
             '卖点是把已核能力与拍摄任务连接起来的编辑说明；用户价值是有条件的推演，不是实测结果、购买排名或用户研究。先确认型号，再选与当前人物和任务有关的1—3项。', '',
             '每张卡区分能力、具体用途、可能价值、适用角色和不可推论。参数条件直接读取产品事实和兼容记录，卖点卡不另存一套参数。', '',
             '## 按型号选取', '', '| 型号 | 本版卖点 | 阅读入口 |','|---|---:|---|']
    for model, name in models.items():
        selected = [c for c in cards if model in c['models']]
        lines.append(f'| {name} | {len(selected)} | [{name} 卖点]({model}.md) |')
        body = [f'# {name} 卖点', '', '由 cards.jsonl 生成。角色匹配与价值均为编辑推演；来源核验日期见各事实，卡片编辑日期不等于官网核验日期。', '', '## 选取目录', '']
        for card in selected:
            body.append(f"- [{card['id']}｜{card['title']}](#{card['id'].lower()})")
        gaps = [r for r in records.values() if model in r['models'] and r['status'] != 'verified']
        if gaps:
            body += ['', '## 相关待核与冲突', '', '下列项目不能被卖点中的通用说法覆盖；按实际手机、配件与软件检查是否相关。', '']
            body += [f"- {record_link(r)}｜`{r['status']}`｜{r.get('gap_reason', r['statement'])}" for r in gaps]
        for c in selected:
            body += ['', f'<a id="{c["id"].lower()}"></a>', f'## {c["id"]}｜{c["title"]}', '',
                     f"**能力概括**：{c['capability_summary']}", '', f"**具体用途**：{c['task']}", '',
                     f"**可能价值（编辑推演）**：{c['possible_value']}", '',
                     '**可匹配角色**：' + '、'.join(f"[{audience[a]['role']}](../audiences/guide.md#{a.lower()})" for a in c['audience_ids']), '',
                     f"**型号与路径**：{c['scope_note']}", '', '**不应扩写为**：' + '；'.join(c['avoid_claims']), '',
                     '**事实及完整条件入口**（命中后须一并读取条件、限制、官方定位与日期）：', '']
            for rid in c['fact_ids']+c['compatibility_ids']:
                r=records[rid]
                body.append(f"- {record_link(r)}｜{r['component']}｜`{r['status']}`｜核验 {r['checked_at']}")
        (out/f'{model}.md').write_text('\n'.join(body)+'\n')
    lines += ['', '## 具体场景与培训选材', '',
              '从[详细场景库](../use_cases/guide.md)查看具体时刻、拍摄难点和人物取舍，或用[卖点反查场景](../use_cases/selling-point-map.md)选择用途。表达方向是待校准的培训选项，使用时接入同一共享写手，不逐字段拼成评论。', '',
              '## 先看这些区别', '',
              '- 8P 可优先按任务选 FrameTap 远程取景、模块2触屏选物、A/B创意运镜；新增手机夹和三脚架结构也有独立事实。手机投屏与模块图传分别说明。',
              '- 8 可按低机位、摇杆/拨轮操作、不同跟随路径和一代模块收音选材。经适配固件支持模块2，不能因此借用8P触屏和任意物体手动框选。',
              '- 旧款按现有内置杆、内置或外接脚架、滑杆/拨轮及软件路径说明可用价值；不依据型号年份判断当前软件，不编价格或购买排名。', '',
              '## 检索和写作接入', '',
              '在本知识库目录用 `rg -n \'MOBILE-SELL-001|取景|低机位|续航\' selling_points/cards.jsonl`，或按 `"models": ["osmo_mobile_8p"]` 精确筛选。JSONL保留整卡，但参数条件与来源在所引用的事实记录；可继续用 `scripts/query.py --id 事实编号` 取完整依据及型号缺口。', '',
              '评论任务仍进入[个人能力入口](../../SKILL.md)指向的同一共享写手。先回应原帖，按当前任务取必要卖点；不强制每条评论展示功能，也不把“能力→用途→价值”变成成稿句式。产品断言绑定产品来源，假想经历留在训练状态。', '',
              '记录字段见[格式说明](SCHEMA.md)，官方重取与本轮验收见[验收记录](../evaluation/selling-points/acceptance.md)。']
    (out/'guide.md').write_text('\n'.join(lines)+'\n')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=['render','audit']);args=parser.parse_args()
    if args.command=='render':render();return 0
    errors=audit();print(json.dumps({'ok':not errors,'errors':errors},ensure_ascii=False,indent=2));return bool(errors)

if __name__=='__main__':raise SystemExit(main())
