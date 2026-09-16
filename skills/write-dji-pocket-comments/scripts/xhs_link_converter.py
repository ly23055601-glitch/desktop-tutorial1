#!/usr/bin/env python3
"""Normalize supported Xiaohongshu links to the standard PC-share form."""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import parse_qsl, quote, unquote, urlparse


XHS_HOST = "www.xiaohongshu.com"
NOTE_PATH = re.compile(
    r"^/(?:explore|discovery/item|search_result)/([0-9a-fA-F]{24})$"
)
TOKEN = re.compile(r"^[A-Za-z0-9_-]{8,512}={0,2}$")
URL = re.compile(r"https?://[^\s<>\"'，。；;]+")


class ConvertError(ValueError):
    pass


@dataclass(frozen=True)
class DirectLink:
    note_id: str
    token: str


def _query_values(parsed, key: str) -> list[str]:
    return [value for name, value in parse_qsl(parsed.query, keep_blank_values=True) if name == key]


def _parse_direct(raw_url: str, expected_id: str | None = None) -> DirectLink:
    parsed = urlparse(html.unescape(raw_url.strip()))
    if parsed.scheme != "https" or parsed.hostname != XHS_HOST:
        raise ConvertError("仅支持 https://www.xiaohongshu.com 的作品直链")
    if parsed.username or parsed.password or parsed.fragment:
        raise ConvertError("链接不得包含 userinfo 或 fragment")
    try:
        port = parsed.port
    except ValueError as exc:
        raise ConvertError("端口格式异常") from exc
    if port not in (None, 443):
        raise ConvertError("小红书直链只能使用默认 443 端口")
    match = NOTE_PATH.fullmatch(unquote(parsed.path))
    if not match:
        raise ConvertError("作品路径或 24 位作品 ID 格式不受支持")
    note_id = match.group(1).lower()
    if expected_id and note_id != expected_id.lower():
        raise ConvertError("返回链接的作品 ID 与输入作品不匹配")
    values = _query_values(parsed, "xsec_token")
    unique = set(values)
    if len(values) != 1 or len(unique) != 1 or not values[0]:
        raise ConvertError("缺少、重复或存在冲突的 xsec_token")
    token = values[0]
    if not TOKEN.fullmatch(token):
        raise ConvertError("xsec_token 格式异常")
    return DirectLink(note_id=note_id, token=token)


def _pc_share(link: DirectLink) -> str:
    token = quote(link.token, safe="-_.~=")
    return (
        f"https://{XHS_HOST}/explore/{link.note_id}"
        f"?source=webshare&xhsshare=pc_web&xsec_token={token}&xsec_source=pc_share"
    )


def _extract_urls(text: str) -> list[str]:
    text = html.unescape(text)
    return [match.rstrip(").]】）") for match in URL.findall(text)]


def convert(raw_url: str) -> dict[str, str]:
    direct = _parse_direct(raw_url)
    return {"status": "success", "note_id": direct.note_id, "pc_share_url": _pc_share(direct)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("links", nargs="*", help="链接；含敏感参数时建议改用标准输入")
    parser.add_argument("--input-file", type=Path, help="从本地文件读取链接，避免把完整链接写进命令")
    parser.add_argument("--output-file", type=Path, required=True, help="把结果写入权限为 0600 的文件，不输出到终端")
    parser.add_argument("--format", choices=("jsonl", "text"), default="jsonl")
    args = parser.parse_args()
    if args.links and args.input_file:
        parser.error("位置参数与 --input-file 不能同时使用")
    if args.input_file:
        source = args.input_file.read_text(encoding="utf-8")
    else:
        source = "\n".join(args.links) if args.links else sys.stdin.read()
    urls = _extract_urls(source)
    if not urls:
        print("未找到受支持的 URL", file=sys.stderr)
        return 2
    failed = False
    output_lines: list[str] = []
    for index, raw_url in enumerate(urls, 1):
        try:
            result = convert(raw_url)
            if args.format == "text":
                output_lines.append(result["pc_share_url"])
            else:
                output_lines.append(json.dumps({"index": index, **result}, ensure_ascii=False))
        except (ConvertError, ValueError) as exc:
            failed = True
            error = {"index": index, "status": "error", "message": str(exc)}
            if args.format == "text":
                print(f"ERROR[{index}]: {exc}", file=sys.stderr)
            else:
                output_lines.append(json.dumps(error, ensure_ascii=False))
    output = "\n".join(output_lines)
    if output:
        output += "\n"
    args.output_file.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(args.output_file, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    os.fchmod(fd, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        handle.write(output)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
