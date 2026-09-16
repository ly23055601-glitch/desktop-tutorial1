#!/usr/bin/env python3
"""Run Mic tests and twelve retrieval cases; save the actual validation results."""
from datetime import datetime
import json
import re
import subprocess
import sys

from mic_knowledge import ROOT, audit, load, search


def main():
    data, issues = load(ROOT)
    report = audit(data, issues, ROOT)
    command = [sys.executable, "-m", "unittest", "discover", "-s", str(ROOT / "tests"), "-v"]
    run = subprocess.run(command, capture_output=True, text=True)
    cases = [json.loads(line) for line in (ROOT / "evaluation/cases.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    results = []
    if report["ok"]:
        for case in cases:
            result = search(data, case["query"], case["model"], 3)
            found = {r["id"] for rows in result["results"].values() for r in rows}
            found.update(e["id"] for r in result["results"]["scenarios"] for e in r.get("evidence", []))
            results.append({"id": case["id"], "model": case["model"], "query": case["query"],
                            "pass": bool(set(case["expected_any"]) & found), "expected_any": case["expected_any"],
                            "returned_ids": {table: [r["id"] for r in rows] for table, rows in result["results"].items()},
                            "unresolved_ids": [r["id"] for r in result["unresolved"]]})
    test_output = run.stdout + run.stderr
    count = re.search(r"Ran (\d+) tests?", test_output)
    valid = report["ok"] and run.returncode == 0 and len(results) == 12 and all(r["pass"] for r in results)
    record = {"checked_at": datetime.now().astimezone().isoformat(timespec="seconds"), "ok": valid,
              "library_counts": report["counts"], "distinct_official_urls": len({r["url"] for r in data["sources"]}),
              "verified_facts": sum(r["status"] == "verified" for r in data["facts"]),
              "verified_compatibility": sum(r["status"] == "verified" for r in data["compatibility"]),
              "unresolved_records": len(report["gaps"]),
              "audit": {k: report[k] for k in ("ok", "errors", "warnings", "issues")},
              "tests": {"command": command, "exit_code": run.returncode, "count": int(count.group(1)) if count else None, "output": test_output},
              "retrieval_cases": results,
              "review_reports": ["mic3-independent-review.json", "mini2s-independent-review.json", "tool-independent-review.json"],
              "scope": "Local structural checks, behavior tests, and retrieval cases; no live HTTP or audio tests."}
    path = ROOT / "evaluation/validation.json"
    path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"ok": valid, "tests": record["tests"]["count"], "retrieval_passed": sum(r["pass"] for r in results),
                      "verified_facts": record["verified_facts"], "verified_compatibility": record["verified_compatibility"],
                      "unresolved": record["unresolved_records"]}, ensure_ascii=False))
    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
