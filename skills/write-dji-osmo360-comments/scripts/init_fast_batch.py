#!/usr/bin/env python3
"""Initialize a minimal Osmo 360 comment batch from pasted links."""

from __future__ import annotations

import argparse
import csv
import html
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse


RULE_VERSION = "2026-09-03-SEED1"
URL_RE = re.compile(r"https?://[^\s<>\]\)]+", re.IGNORECASE)
TRAILING_PUNCTUATION = "'\".,;:!?，。；：！？|"


def normalize_url(raw: str) -> str:
    value = html.unescape(raw).replace(r"\&", "&").replace(r"\_", "_")
    return value.rstrip(TRAILING_PUNCTUATION)


def extract_urls(text: str) -> list[str]:
    seen: set[str] = set()
    urls: list[str] = []
    for match in URL_RE.finditer(text):
        url = normalize_url(match.group(0))
        if url and url not in seen:
            seen.add(url)
            urls.append(url)
    return urls


def classify(url: str, index: int) -> tuple[str, str]:
    parsed = urlparse(url)
    host = parsed.netloc.lower()
    path = parsed.path

    patterns = (
        ("xiaohongshu", r"/(?:discovery/item|explore)/([^/?#]+)"),
        ("douyin", r"/(?:video|note)/(\d+)"),
        ("bilibili", r"/video/(BV[A-Za-z0-9]+)"),
        ("weibo", r"/\d+/([A-Za-z0-9]+)"),
    )
    for platform, pattern in patterns:
        if platform in host or (platform == "xiaohongshu" and "xhslink" in host):
            match = re.search(pattern, path)
            return platform, match.group(1) if match else f"{platform}-{index:02d}"
    return host or "unknown", f"link-{index:02d}"


def ensure_new(paths: list[Path]) -> None:
    existing = [str(path) for path in paths if path.exists()]
    if existing:
        raise FileExistsError("refusing to overwrite: " + ", ".join(existing))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="包含链接的 txt/Markdown 文件")
    parser.add_argument("output_dir", help="新批次工作目录")
    args = parser.parse_args()

    input_path = Path(args.input).expanduser().resolve()
    output_dir = Path(args.output_dir).expanduser().resolve()
    if not input_path.is_file():
        print(f"input not found: {input_path}", file=sys.stderr)
        return 2

    urls = extract_urls(input_path.read_text(encoding="utf-8", errors="replace"))
    if not urls:
        print("no links found", file=sys.stderr)
        return 2

    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = output_dir / "links.tsv"
    evidence_path = output_dir / "evidence.md"
    draft_path = output_dir / "draft.md"
    state_path = output_dir / "osmo360_comment_state.json"
    final_path = output_dir / "final.md"
    try:
        ensure_new([manifest_path, evidence_path, draft_path, state_path, final_path])
    except FileExistsError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    rows = []
    for index, url in enumerate(urls, start=1):
        platform, item_id = classify(url, index)
        rows.append((index, platform, item_id, f"{index:02d}_{item_id}", url))

    with manifest_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(("index", "platform", "id", "media_item", "url"))
        writer.writerows(rows)

    evidence_lines = ["# Osmo 360 批次证据", ""]
    draft_lines = []
    for index, _platform, _item_id, _media_item, url in rows:
        evidence_lines.extend(
            [
                f"## {index:02d}｜{url}",
                "",
                "状态：pending｜评论：unknown｜型号：unknown",
                "时间/地点/场景：",
                "画面锚点：",
                "可用产品点：",
                "不可推断：",
                "",
            ]
        )
        draft_lines.extend([f"## {index:02d}｜{url}", ""])

    evidence_path.write_text("\n".join(evidence_lines), encoding="utf-8")
    draft_path.write_text("\n".join(draft_lines), encoding="utf-8")

    template_path = Path(__file__).resolve().parents[1] / "assets" / "osmo360_comment_state.template.json"
    state = json.loads(template_path.read_text(encoding="utf-8"))
    state.update(
        {
            "rule_version": RULE_VERSION,
            "input_path": str(input_path),
            "link_manifest_path": str(manifest_path),
            "media_manifest_path": str(output_dir / "media_sample" / "manifest.json"),
            "evidence_path": str(evidence_path),
            "pending_ids": [row[2] for row in rows],
            "draft_path": str(draft_path),
            "output_path": str(final_path),
        }
    )
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(
        json.dumps(
            {
                "links": len(rows),
                "manifest": str(manifest_path),
                "media_output": str(output_dir / "media_sample"),
                "evidence": str(evidence_path),
                "draft": str(draft_path),
                "state": str(state_path),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
