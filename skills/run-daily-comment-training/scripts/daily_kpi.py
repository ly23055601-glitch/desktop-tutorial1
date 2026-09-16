#!/usr/bin/env python3
"""Read daily training ledgers and report counts; never write any files."""

import argparse
from datetime import date, datetime
import json
from pathlib import Path
import re
import sys
from zoneinfo import ZoneInfo


REVIEW_KEYS = ("facts", "naturalness", "product_interest", "difference")
PRODUCT_CODES = {"op", "om", "dm", "oq", "ow"}
SHANGHAI = ZoneInfo("Asia/Shanghai")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def timestamp(value):
    require(isinstance(value, str), "时间必须是带时区的 ISO 字符串")
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    require(parsed.tzinfo is not None, f"时间缺少时区：{value}")
    return parsed


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def artifact(base, value):
    require(nonempty(value), "产物或证据引用不能为空")
    resolved = (base / value).resolve()
    require(resolved.is_file(), f"引用文件不存在：{resolved}")
    return str(resolved)


def validate_delivery(delivery, base, started):
    require(timestamp(delivery["delivered_at"]) >= started, "交付时间早于批次开始")
    version_paths = {artifact(base, delivery[key]) for key in ("draft_ref", "training_state_ref")}
    require(len(version_paths) == 2, "稿件与训练状态必须使用不同文件")
    for key in ("main_comments", "replies"):
        require(type(delivery[key]) is int and delivery[key] >= 0, f"{key} 必须是非负整数")
    require(delivery["main_comments"] > 0, "交付必须有主评")
    review = delivery.get("review", {})
    for key in REVIEW_KEYS:
        require(type(review.get(key, False)) is bool, f"复核字段 {key} 必须是布尔值")
    if any(review.get(key) for key in REVIEW_KEYS):
        artifact(base, review.get("self_check_ref"))
    if delivery.get("independent_review_ref"):
        artifact(base, delivery["independent_review_ref"])
    return version_paths


def load_ledgers(root):
    ledgers, tasks, task_keys = [], {}, set()
    for path in sorted(root.glob("*/B*/ledger.json")):
        day, batch = path.parent.parent.name, path.parent.name
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", day):
            continue
        require(date.fromisoformat(day).isoformat() == day, f"日期目录无效：{day}")
        require(re.fullmatch(r"B\d{3,}", batch), f"批次目录无效：{batch}")
        try:
            ledger = json.loads(path.read_text(encoding="utf-8"))
            require(ledger["schema_version"] == 1, "不支持的 schema_version")
            require(ledger["date"] == day and ledger["batch_id"] == batch, "日期或批次与目录不一致")
            started = timestamp(ledger["started_at"])
            require(started.astimezone(SHANGHAI).date().isoformat() == day, "开始时间不属于上海日期目录")
            ledger["_path"] = path
            for source in ledger["sources"]:
                require(nonempty(source["material_id"]), "material_id 不能为空")
                require(type(source["read_required"]) is bool, "read_required 必须是布尔值")
                allowed = {"pending", "blocked", "qualified", "reused"} if source["read_required"] else {"provided"}
                require(source["status"] in allowed, "来源状态与 read_required 不一致")
                if source["read_required"]:
                    require(nonempty(source.get("url")), "待读链接需要保留 url")
                if source["status"] in {"qualified", "reused", "provided"}:
                    artifact(path.parent, source.get("evidence_ref"))
                if source["status"] in {"qualified", "reused"}:
                    timestamp(source.get("verified_at"))
                if source["status"] == "blocked":
                    require(nonempty(source.get("reason")), "受阻来源需要明确原因")
            for task in ledger["tasks"]:
                require(re.fullmatch(r"T\d{3,}", task["id"]), "任务 ID 应为 T001 等")
                require(task["product_code"] in PRODUCT_CODES, "产品代码不在当前五项映射内")
                require(nonempty(task["material_id"]), "任务 material_id 不能为空")
                ref = f"{day}/{batch}/{task['id']}"
                key = (day, task["product_code"], task["material_id"])
                require(ref not in tasks and key not in task_keys, "重复任务定义；重复输入应映射到原 task_ref")
                task_keys.add(key)
                tasks[ref] = (task, ledger)
                require(task["status"] in {"pending", "delivered", "blocked", "concluded"}, "任务状态无效")
                first = task.get("first_delivery")
                require((first is not None) == (task["status"] == "delivered"), "实交快照与 delivered 状态必须一致")
                if task["status"] in {"blocked", "concluded"}:
                    require(nonempty(task.get("conclusion")), "闭环需有明确结论或阻塞说明")
                version_paths = validate_delivery(first, path.parent, started) if first else set()
                feedback_by_id = {}
                for feedback in task.get("user_feedback", []):
                    require(nonempty(feedback["id"]) and feedback["id"] not in feedback_by_id, "反馈 ID 为空或重复")
                    require(first is not None, "未交付任务不能有首稿或改稿验收")
                    require(timestamp(feedback["at"]) >= timestamp(first["delivered_at"]), "用户反馈早于首交")
                    require(feedback["target"] in {"first_draft", "revision"}, "反馈 target 无效")
                    require(feedback["outcome"] in {"accepted", "changes_requested", "reviewed"}, "反馈 outcome 无效")
                    require(nonempty(feedback.get("source_ref")), "用户反馈必须保留消息定位或用户原话文件")
                    if feedback["target"] == "revision":
                        number = feedback.get("revision_number")
                        require(type(number) is int and 1 <= number <= len(task.get("revisions", [])), "改稿反馈须定位 revision_number")
                    feedback_by_id[feedback["id"]] = feedback
                previous = timestamp(first["delivered_at"]) if first else started
                for revision in task.get("revisions", []):
                    require(first is not None, "改稿必须保留首稿")
                    revision_paths = validate_delivery(revision, path.parent, previous)
                    require(version_paths.isdisjoint(revision_paths), "不同交付版本不能复用稿件或训练状态文件，须保留首稿及各版")
                    version_paths.update(revision_paths)
                    previous = timestamp(revision["delivered_at"])
                    for feedback_id in revision.get("feedback_ids", []):
                        require(feedback_id in feedback_by_id, "改稿引用了不存在的用户反馈")
                        require(timestamp(feedback_by_id[feedback_id]["at"]) <= previous, "改稿早于引用的用户反馈")
                for feedback in feedback_by_id.values():
                    if feedback["target"] == "revision":
                        reviewed = task["revisions"][feedback["revision_number"] - 1]
                        require(timestamp(feedback["at"]) >= timestamp(reviewed["delivered_at"]), "改稿验收早于该版交付")
                error_ids = set()
                for error in task.get("hard_errors", []):
                    require(nonempty(error["id"]) and error["id"] not in error_ids, "硬错 ID 为空或重复")
                    error_ids.add(error["id"])
                    require(error["kind"] in {"product_fact", "post_fabrication", "source_attribution"}, "硬错误类型无效")
                    require(error["stage"] in {"internal", "delivered"}, "硬错误阶段无效")
                    require(nonempty(error.get("detail")), "硬错误须有具体说明")
                    detected = timestamp(error["detected_at"])
                    if error.get("resolved_at"):
                        require(timestamp(error["resolved_at"]) >= detected, "修复时间早于发现时间")
            for block in ledger.get("external_blocks", []):
                require(timestamp(block["started_at"]) >= started, "外部阻塞早于批次开始")
                require(nonempty(block.get("reason")), "外部阻塞须注明原因")
                if block.get("ended_at"):
                    require(timestamp(block["ended_at"]) >= timestamp(block["started_at"]), "外部阻塞区间倒置")
            ledgers.append(ledger)
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError(f"{path}: {exc}") from exc
    mapped = set()
    source_keys = {(ledger["date"], source["material_id"]) for ledger in ledgers for source in ledger["sources"]}
    available_source_keys = {(ledger["date"], source["material_id"]) for ledger in ledgers for source in ledger["sources"] if source["status"] in {"qualified", "reused", "provided"}}
    for ledger in ledgers:
        for entry in ledger["inputs"]:
            ref = entry["task_ref"]
            require(ref in tasks, f"输入引用不存在的任务：{ref}")
            task, owner = tasks[ref]
            require(nonempty(entry["original_index"]), "输入必须保留原序号或收到时分配的序号")
            require(entry["product_code"] == task["product_code"] and entry["material_id"] == task["material_id"], "输入与所映射任务的产品或材料不一致")
            require(owner["date"] <= ledger["date"], "输入不能引用未来日期任务")
            mapped.add(ref)
        for task in ledger["tasks"]:
            source_key = (ledger["date"], task["material_id"])
            require(source_key in source_keys, "任务缺少当日来源记录；复用证据也需登记 reused")
            if task.get("first_delivery"):
                ref = f"{ledger['date']}/{ledger['batch_id']}/{task['id']}"
                require(source_key in available_source_keys, f"{ledger['_path']}：任务 {ref}（{task['material_id']}）已登记实交但无当日可用来源；须有 qualified/reused/provided 及存在的证据文件，只有 blocked/pending 不能计交付")
    require(mapped == set(tasks), "任务缺少原始输入映射")
    return ledgers, tasks


def ratio(numerator, denominator):
    return {"numerator": numerator, "denominator": denominator, "value": numerator / denominator if denominator else None}


def closed_block_seconds(blocks):
    intervals = sorted((timestamp(item["started_at"]), timestamp(item["ended_at"])) for item in blocks if item.get("ended_at"))
    merged = []
    for start, end in intervals:
        if merged and start <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(end, merged[-1][1]))
        else:
            merged.append((start, end))
    return sum((end - start).total_seconds() for start, end in merged)


def metrics(ledgers, days):
    selected = [ledger for ledger in ledgers if ledger["date"] in days]
    tasks = [(task, ledger) for ledger in selected for task in ledger["tasks"]]
    delivered = [(task, ledger) for task, ledger in tasks if task.get("first_delivery")]
    reviewed, accepted, semantic, independent, feedback_rounds = 0, 0, 0, 0, 0
    current_acceptance = {key: 0 for key in ("accepted", "changes_requested", "reviewed", "pending")}
    for task, _ in delivered:
        first_reviews = sorted((event for event in task.get("user_feedback", []) if event["target"] == "first_draft"), key=lambda event: timestamp(event["at"]))
        reviewed += bool(first_reviews)
        decision = next((event for event in first_reviews if event["outcome"] != "reviewed"), None)
        changed_before_acceptance = bool(decision and any(timestamp(revision["delivered_at"]) <= timestamp(decision["at"]) for revision in task.get("revisions", [])))
        accepted += bool(decision and decision["outcome"] == "accepted" and not changed_before_acceptance)
        current = (task.get("revisions") or [task["first_delivery"]])[-1]
        semantic += all(current.get("review", {}).get(key, False) for key in REVIEW_KEYS)
        independent += bool(current.get("independent_review_ref"))
        feedback_rounds += sum(bool(revision.get("feedback_ids")) for revision in task.get("revisions", []))
        revision_count = len(task.get("revisions", []))
        if revision_count:
            current_events = sorted((event for event in task.get("user_feedback", []) if event["target"] == "revision" and event["revision_number"] == revision_count), key=lambda event: timestamp(event["at"]))
        else:
            current_events = first_reviews
        current_decision = next((event for event in reversed(current_events) if event["outcome"] != "reviewed"), current_events[-1] if current_events else None)
        current_acceptance[current_decision["outcome"] if current_decision else "pending"] += 1
    required, qualified = set(), set()
    task_sources = {(ledger["date"], task["material_id"]) for task, ledger in tasks}
    for ledger in selected:
        for source in ledger["sources"]:
            key = (ledger["date"], source["material_id"])
            if source["read_required"] and key in task_sources:
                required.add(key)
                if source["status"] in {"qualified", "reused"}:
                    qualified.add(key)
    errors = [error for task, _ in tasks for error in task.get("hard_errors", [])]
    timings = []
    for ledger in selected:
        if not ledger["tasks"]:
            continue
        deliveries = [timestamp(task["first_delivery"]["delivered_at"]) for task in ledger["tasks"] if task.get("first_delivery")]
        first = min(deliveries) if deliveries else None
        blocks = ledger.get("external_blocks", [])
        timings.append({"batch_ref": f"{ledger['date']}/{ledger['batch_id']}", "started_at": ledger["started_at"], "first_delivery_at": first.isoformat() if first else None, "wall_seconds_to_first_delivery": (first - timestamp(ledger["started_at"])).total_seconds() if first else None, "closed_external_block_seconds": closed_block_seconds(blocks) if any(block.get("ended_at") for block in blocks) else None, "open_external_blocks": sum(not block.get("ended_at") for block in blocks), "external_blocks": blocks})
    return {
        "input_tasks": len(tasks),
        "delivered_tasks": len(delivered),
        "input_closure": ratio(sum(task["status"] != "pending" for task, _ in tasks), len(tasks)),
        "reading_success": ratio(len(qualified), len(required)),
        "draft_completion": ratio(len(delivered), len(tasks)),
        "semantic_review_coverage": ratio(semantic, len(delivered)),
        "independent_review_coverage": ratio(independent, len(delivered)),
        "first_draft_acceptance": ratio(accepted, reviewed),
        "first_draft_review_coverage": ratio(reviewed, len(delivered)),
        "pending_first_draft_review": len(delivered) - reviewed,
        "current_user_acceptance": current_acceptance,
        "production": {"main_comments": sum(task["first_delivery"]["main_comments"] for task, _ in delivered), "replies": sum(task["first_delivery"]["replies"] for task, _ in delivered)},
        "current_production": {key: sum((task.get("revisions") or [task["first_delivery"]])[-1][key] for task, _ in delivered) for key in ("main_comments", "replies")},
        "hard_errors": {"total": len(errors), "internal": sum(error["stage"] == "internal" for error in errors), "delivered": sum(error["stage"] == "delivered" for error in errors), "unresolved": sum(not error.get("resolved_at") for error in errors)},
        "user_feedback_revision_rounds": feedback_rounds,
        "blockers": [{"task_ref": f"{ledger['date']}/{ledger['batch_id']}/{task['id']}", "reason": task["conclusion"]} for task, ledger in tasks if task["status"] == "blocked"],
        "timings": timings,
    }


def output_groups(ledgers, tasks, selected_date):
    """Group input positions for delivery without changing task/read accounting."""
    groups, first_seen = [], {}
    selected = sorted((ledger for ledger in ledgers if ledger["date"] == selected_date), key=lambda ledger: int(ledger["batch_id"][1:]))
    for ledger in selected:
        inputs = ledger["inputs"]
        for start in range(0, len(inputs), 10):
            group_ref = f"{ledger['date']}/{ledger['batch_id']}/G{start // 10 + 1:03d}"
            items = []
            for position, entry in enumerate(inputs[start:start + 10], start + 1):
                task, owner = tasks[entry["task_ref"]]
                item = {key: entry[key] for key in ("original_index", "product_code", "material_id", "task_ref")}
                item.update(position=position, task_status=task["status"])
                current = (task.get("revisions") or [task.get("first_delivery")])[-1]
                if current:
                    item["draft_ref"] = artifact(owner["_path"].parent, current["draft_ref"])
                if entry["task_ref"] in first_seen:
                    item["first_occurrence"] = first_seen[entry["task_ref"]]
                else:
                    first_seen[entry["task_ref"]] = {"group_ref": group_ref, "position": position}
                items.append(item)
            groups.append({"group_ref": group_ref, "input_start": start + 1, "input_end": start + len(items), "input_count": len(items), "items": items})
    return groups


def report(root, selected_date=None):
    ledgers, tasks = load_ledgers(root)
    execution_days = sorted({ledger["date"] for ledger in ledgers if ledger["tasks"]})
    selected_date = selected_date or (execution_days[-1] if execution_days else None)
    visible_days = [day for day in execution_days if selected_date is None or day <= selected_date]
    baseline_days = visible_days[:7]
    recent = []
    for day in visible_days[-7:]:
        selected = [ledger for ledger in ledgers if ledger["date"] == day]
        recent.append({"date": day, "directories": [str(ledger["_path"].parent.resolve()) for ledger in selected], "drafts": [artifact(ledger["_path"].parent, delivery["draft_ref"]) for ledger in selected for task in ledger["tasks"] for delivery in ([task["first_delivery"]] if task.get("first_delivery") else []) + task.get("revisions", [])], "confirmed_feedback": [{"task_ref": f"{day}/{ledger['batch_id']}/{task['id']}", **event} for ledger in selected for task in ledger["tasks"] for event in task.get("user_feedback", [])]})
    return {"selected_date": selected_date, "execution_days": visible_days, "daily": metrics(ledgers, [selected_date] if selected_date else []), "first_seven_baseline": {"days": baseline_days, "ready": len(baseline_days) == 7, "next_step": "请根据首 7 个执行日实际结果提出下一阶段目标，脚本不设置阈值" if len(baseline_days) == 7 else "继续记录，尚未满 7 个实际执行日", "metrics": metrics(ledgers, baseline_days)}, "recent_execution_days": recent, "output_groups": output_groups(ledgers, tasks, selected_date)}


def format_ratio(item):
    return f"{item['numerator']}/{item['denominator']}（{item['value']:.1%}）" if item["value"] is not None else "暂无数据"


def print_text(result):
    if not result["execution_days"]:
        print("暂无数据：没有实际执行日。")
        return
    data = result["daily"]
    print(f"日期：{result['selected_date']}；输入 {data['input_tasks']} 个任务，实交 {data['delivered_tasks']} 个任务；首交产量：主评 {data['production']['main_comments']} 条，回复 {data['production']['replies']} 条")
    print(f"当前稿库存：主评 {data['current_production']['main_comments']} 条，回复 {data['current_production']['replies']} 条（不累加为新增产量）")
    for title, key in (("输入闭环率", "input_closure"), ("读取成功率", "reading_success"), ("稿件实交率", "draft_completion"), ("内容复核覆盖率", "semantic_review_coverage"), ("独立审稿覆盖率", "independent_review_coverage"), ("首稿验收率", "first_draft_acceptance"), ("首稿审阅覆盖率", "first_draft_review_coverage")):
        print(f"{title}：{format_ratio(data[key])}")
    print("教学完整交付：依据适用写手规则、正文与实际审稿另行汇总；实交和复核覆盖不代表质量通过")
    errors = data["hard_errors"]
    print(f"硬错误：{errors['total']}（内部发现 {errors['internal']}，已交付问题 {errors['delivered']}，未修复 {errors['unresolved']}）；首稿待验收 {data['pending_first_draft_review']} 个任务；用户反馈后改稿 {data['user_feedback_revision_rounds']} 轮")
    current = data["current_user_acceptance"]
    print(f"当前版本用户验收：已认可 {current['accepted']}，要求修改 {current['changes_requested']}，已审阅待结论 {current['reviewed']}，待验收 {current['pending']}")
    for item in data["blockers"]:
        print(f"阻塞 {item['task_ref']}：{item['reason']}")
    for item in data["timings"]:
        wall = "暂无数据" if item["wall_seconds_to_first_delivery"] is None else f"{item['wall_seconds_to_first_delivery'] / 60:.1f} 分钟"
        blocked = "暂无记录" if item["closed_external_block_seconds"] is None else f"{item['closed_external_block_seconds'] / 60:.1f} 分钟"
        print(f"{item['batch_ref']} 首交墙钟：{wall}；已结束外部阻塞 {blocked}，未结束 {item['open_external_blocks']} 项（不从墙钟扣除）")
    for group in result["output_groups"]:
        print(f"输出组 {group['group_ref']}：输入位置 {group['input_start']}–{group['input_end']}，共 {group['input_count']} 条（失败及重复位置保留）")
    baseline = result["first_seven_baseline"]
    print(f"基线：{len(baseline['days'])}/7 个执行日；{baseline['next_step']}")
    if baseline["ready"]:
        summary = baseline["metrics"]
        print(f"首 7 日合计：输入 {summary['input_tasks']}，实交 {summary['delivered_tasks']}；首稿验收 {format_ratio(summary['first_draft_acceptance'])}，审阅覆盖 {format_ratio(summary['first_draft_review_coverage'])}；完整基线用 --json 查看")
    print("最近执行日目录：")
    for day in result["recent_execution_days"]:
        for directory in day["directories"]:
            print(directory)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path, help="outputs/daily-comment-training 根目录")
    parser.add_argument("--date", dest="selected_date", help="上海日期 YYYY-MM-DD；默认最新实际执行日")
    parser.add_argument("--json", action="store_true", help="输出含基线、近期稿件/反馈定位与每 10 输入位置分组的 JSON")
    args = parser.parse_args()
    try:
        if args.selected_date:
            require(date.fromisoformat(args.selected_date).isoformat() == args.selected_date, "--date 应为 YYYY-MM-DD")
        result = report(args.root, args.selected_date)
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print_text(result)
    except (OSError, KeyError, TypeError, ValueError) as exc:
        print(f"台账错误：{exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
