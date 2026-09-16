#!/usr/bin/env python3
"""Regenerate Mic coverage, gap, source and scenario reading reports from JSONL."""
from datetime import datetime
import json
from pathlib import Path

from mic_knowledge import ROOT, MODELS, PRIMARY, TOPICS, TOPIC_NAMES, audit, load


def write(path, lines):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main():
    data, issues = load(ROOT)
    result = audit(data, issues, ROOT)
    if not result["ok"]:
        raise SystemExit(json.dumps(result["issues"], ensure_ascii=False, indent=2))
    stamp = datetime.now().astimezone().isoformat(timespec="seconds")
    note = f"生成时间：{stamp}。由 `scripts/build_reports.py` 按当前记录生成；生成时间不改变事实核验日期。"
    names = {r["id"]: r["official_name"] for r in data["models"]}
    coverage = ["# Mic 知识库覆盖清单", "", note, "", "## 实际记录数", "",
                "| 类别 | 数量 |", "|---|---:|"]
    for key, label in (("models", "型号"), ("sources", "官方来源"), ("facts", "产品事实（含待核）"), ("compatibility", "兼容记录（含待核）"), ("scenarios", "编辑场景")):
        coverage.append(f"| {label} | {result['counts'][key]} |")
    unique_urls = len({s['url'] for s in data['sources']})
    coverage += ["", f"官方来源为分组登记数，对应 {unique_urls} 个不同 URL；共用文档可在两款产品组各保留其读取范围。"]
    coverage += ["", "## 按型号覆盖", "", "| 型号 | 深度 | 已核验事实 | 待核／冲突事实 | 兼容记录 | 场景 |", "|---|---|---:|---:|---:|---:|"]
    for row in result["coverage"]:
        states = row["statuses"]
        coverage.append(f"| {names[row['model']]} | {'重点' if row['model'] in PRIMARY else '基础'} | {states.get('verified', 0)} | {states.get('pending', 0) + states.get('conflict', 0)} | {row['compatibility']} | {row['scenarios']} |")
    coverage += ["", "跨型号记录可能计入多款的覆盖数；总记录数以第一张表为准。", "", "## 两个重点型号的主题", "", "| 主题 | Mic 3 | Mic Mini 2S |", "|---|---|---|"]
    for topic in TOPICS:
        cells = []
        for model in ("mic_3", "mic_mini_2s"):
            rows = [r for r in data["facts"] if model in r["models"] and r["topic"] == topic]
            cells.append("、".join(f"{r['id']}（{'已核' if r['status'] == 'verified' else '待核' if r['status'] == 'pending' else '冲突'}）" for r in rows) or "未覆盖")
        coverage.append(f"| {TOPIC_NAMES[topic]} | {cells[0]} | {cells[1]} |")
    coverage += ["", "结构审计与事实正确性、网页今日可达性分开验收。具体未确认内容见 [GAPS.md](GAPS.md)，实际测试见 [验收记录](evaluation/acceptance.md)。"]
    write(ROOT / "COVERAGE.md", coverage)
    (ROOT / "coverage.json").write_text(json.dumps({"generated_at": stamp, **result}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    gaps = ["# Mic 知识库缺口与冲突", "", note, "", "下面的条目不能作为肯定产品能力。明确不支持的已核验兼容记录不算缺口。"]
    for row in result["gaps"]:
        gaps += ["", f"## {row['id']} · {'／'.join(names[m] for m in row['models'])}", "", f"状态：{row['status']}", "", row["statement"], "", "待核原因：" + row["reason"]]
        for ref in row["source_refs"]:
            src = next(r for r in data["sources"] if r["id"] == ref["source_id"])
            gaps.append(f"- [{src['title']}]({src['url']})：{ref['locator']}（{src['region']}；核验 {src['checked_at']}）")
    for row in result["coverage"]:
        if row["missing_topics"]:
            gaps += ["", f"## {names[row['model']]} 主题缺口", "", "、".join(TOPIC_NAMES[t] for t in row["missing_topics"])]
    gaps += ["", "## 首版有意保留的边界", "", "- 手机、App、相机及固件更新可能改变兼容；表外设备保留未确认，不由相近型号推断。", "- 型号基础覆盖不等于所有旧款功能的完整手册复刻。", "- 不含真实消费者语料、主观听感排行、竞品研究、实时促销或库存。", "- 未做本机音频实测；官方可用能力不证明某个原帖启用了该功能。"]
    write(ROOT / "GAPS.md", gaps)

    sources = ["# Mic 官方来源目录", "", note, "", "实际核验范围由 read_scope 记录。兼容表同名不代表版本相同；PDF 页面以记录中的页码／表格定位核对。"]
    for src in sorted(data["sources"], key=lambda r: r["id"]):
        sources += ["", f"## {src['id']} · {src['title']}", "", f"[官方来源]({src['url']})", "",
                    f"地区：{src['region']}；语言：{src['language']}；核验：{src['checked_at']}；类型：{src['source_type']}",
                    f"版本：{src.get('document_version') or '未标注'}；文档／页面日期：{src.get('published_at') or '未标注'}", "",
                    "实际读取：" + src["read_scope"], "", "摘要：" + src["summary"]]
        if src.get("local_path"):
            sources += ["", f"[本地读取证据](../{src['local_path']})"]
    write(ROOT / "sources/README.md", sources)

    scenarios = ["# Mic 场景问答", "", note, "", "这些场景是基于官方事实的编辑归纳，不是访谈、真实消费者体验或可直接粘贴的评论。"]
    for row in data["scenarios"]:
        scenarios += ["", f"## {row['id']} · {'／'.join(names[m] for m in row['models'])} · {row['scenario']}", "", "**" + row["question"] + "**", "", row["answer"], "", "操作路径："]
        scenarios += [f"{n}. {step}" for n, step in enumerate(row["steps"], 1)]
        scenarios += ["", "限制：" + "；".join(row["limitations"]), "", "依据：" + "、".join(row["fact_ids"] + row["compatibility_ids"])]
    write(ROOT / "scenarios/guide.md", scenarios)
    print(json.dumps({"ok": True, "counts": result["counts"], "gaps": len(result["gaps"])}, ensure_ascii=False))


if __name__ == "__main__":
    main()
