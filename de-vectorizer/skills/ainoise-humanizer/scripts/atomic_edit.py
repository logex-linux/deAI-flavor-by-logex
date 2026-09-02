#!/usr/bin/env python3
"""Apply auditable single-code-point edits to a UTF-8 text file."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


RULE_ID = re.compile(r"^B(?:0[1-9]|1[0-9]|2[0-6])$")


class EditError(ValueError):
    pass


def read_utf8(path: Path) -> str:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return handle.read()


def write_utf8(path: Path, text: str) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        handle.write(text)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def line_records(text: str) -> list[tuple[int, str]]:
    records: list[tuple[int, str]] = []
    offset = 0
    for raw_line in text.splitlines(keepends=True):
        body = raw_line.rstrip("\r\n")
        records.append((offset, body))
        offset += len(raw_line)
    if not records or text.endswith(("\n", "\r")):
        records.append((offset, ""))
    return records


def require_single_char(value: Any, field: str, allow_empty: bool) -> str:
    if not isinstance(value, str):
        raise EditError(f"{field} must be a string")
    allowed_lengths = {0, 1} if allow_empty else {1}
    if len(value) not in allowed_lengths:
        size = "zero or one" if allow_empty else "one"
        raise EditError(f"{field} must contain {size} Unicode character")
    if "\n" in value or "\r" in value:
        raise EditError(f"{field} cannot contain a newline")
    return value


def normalize_operations(text: str, payload: dict[str, Any]) -> list[dict[str, Any]]:
    operations = payload.get("operations")
    if not isinstance(operations, list) or not operations:
        raise EditError("operations must be a non-empty list")

    records = line_records(text)
    normalized: list[dict[str, Any]] = []
    occupied_chars: set[int] = set()
    insertion_keys: set[tuple[int, int]] = set()

    for index, raw in enumerate(operations, start=1):
        if not isinstance(raw, dict):
            raise EditError(f"operation {index} must be an object")

        op = raw.get("op")
        if op not in {"insert", "delete", "replace"}:
            raise EditError(f"operation {index}: unsupported op {op!r}")

        line = raw.get("line")
        column = raw.get("column")
        if not isinstance(line, int) or line < 1 or line > len(records):
            raise EditError(f"operation {index}: line is out of range")
        if not isinstance(column, int):
            raise EditError(f"operation {index}: column must be an integer")

        line_start, body = records[line - 1]
        max_column = len(body) + (1 if op == "insert" else 0)
        if column < 1 or column > max_column:
            raise EditError(f"operation {index}: column is out of range for line {line}")

        old = require_single_char(raw.get("old", ""), f"operation {index}.old", allow_empty=True)
        new = require_single_char(raw.get("new", ""), f"operation {index}.new", allow_empty=True)

        if op == "insert" and (old != "" or len(new) != 1):
            raise EditError(f"operation {index}: insert requires empty old and one-character new")
        if op == "delete" and (len(old) != 1 or new != ""):
            raise EditError(f"operation {index}: delete requires one-character old and empty new")
        if op == "replace" and (len(old) != 1 or len(new) != 1 or old == new):
            raise EditError(f"operation {index}: replace requires different one-character old/new values")

        rule_id = raw.get("rule_id")
        if not isinstance(rule_id, str) or not RULE_ID.fullmatch(rule_id):
            raise EditError(f"operation {index}: rule_id must be B01 through B26")
        reason = raw.get("reason")
        if not isinstance(reason, str) or not reason.strip():
            raise EditError(f"operation {index}: reason is required")
        example_source = raw.get("example_source")
        if not isinstance(example_source, str) or not example_source.strip():
            raise EditError(f"operation {index}: example_source is required")
        if not any(name in example_source for name in ("02_AI惯用语黑名单", "03_反车轱辘话")):
            raise EditError(
                f"operation {index}: example_source must point to the original 02/03 rule files"
            )
        whitelist_check = raw.get("whitelist_check")
        if not isinstance(whitelist_check, str) or not whitelist_check.strip():
            raise EditError(f"operation {index}: whitelist_check is required")

        offset = line_start + column - 1
        order = raw.get("order", 1)
        if not isinstance(order, int) or order < 1:
            raise EditError(f"operation {index}: order must be a positive integer")

        if op == "insert":
            key = (offset, order)
            if key in insertion_keys:
                raise EditError(f"operation {index}: duplicate insert order at line {line}, column {column}")
            if offset in occupied_chars:
                raise EditError(f"operation {index}: insert conflicts with a character edit")
            insertion_keys.add(key)
        else:
            if offset in occupied_chars or any(key[0] == offset for key in insertion_keys):
                raise EditError(f"operation {index}: overlapping edit at line {line}, column {column}")
            if text[offset] != old:
                raise EditError(
                    f"operation {index}: expected {old!r} at line {line}, column {column}, found {text[offset]!r}"
                )
            occupied_chars.add(offset)

        normalized.append(
            {
                "op": op,
                "line": line,
                "column": column,
                "old": old,
                "new": new,
                "rule_id": rule_id,
                "reason": reason.strip(),
                "example_source": example_source.strip(),
                "whitelist_check": whitelist_check.strip(),
                "order": order,
                "offset": offset,
            }
        )

    return normalized


def apply_operations(text: str, operations: list[dict[str, Any]]) -> str:
    revised = text
    for item in sorted(operations, key=lambda value: (value["offset"], value["order"]), reverse=True):
        offset = item["offset"]
        if item["op"] == "insert":
            revised = revised[:offset] + item["new"] + revised[offset:]
        elif item["op"] == "delete":
            revised = revised[:offset] + revised[offset + 1 :]
        else:
            revised = revised[:offset] + item["new"] + revised[offset + 1 :]
    return revised


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("edits", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--log", type=Path, dest="log_path")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source = args.source.resolve()
    output = args.output.resolve()
    edits_path = args.edits.resolve()

    if source == output:
        raise EditError("output must not overwrite the source file")
    if not source.is_file():
        raise EditError(f"source file does not exist: {source}")
    if not edits_path.is_file():
        raise EditError(f"edits file does not exist: {edits_path}")
    if not output.parent.is_dir():
        raise EditError(f"output directory does not exist: {output.parent}")

    original = read_utf8(source)
    with edits_path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise EditError("edit plan must be a JSON object")

    expected_hash = payload.get("source_sha256")
    original_hash = sha256_text(original)
    if expected_hash is not None and expected_hash != original_hash:
        raise EditError("source_sha256 does not match the source file")

    operations = normalize_operations(original, payload)
    revised = apply_operations(original, operations)

    log_path = args.log_path.resolve() if args.log_path else Path(str(output) + ".editlog.json")
    if log_path == source or log_path == output:
        raise EditError("log path must differ from source and output")
    if not log_path.parent.is_dir():
        raise EditError(f"log directory does not exist: {log_path.parent}")

    write_utf8(output, revised)

    public_operations = [{key: value for key, value in item.items() if key != "offset"} for item in operations]
    log_payload = {
        "source": str(source),
        "output": str(output),
        "source_sha256": original_hash,
        "output_sha256": sha256_text(revised),
        "operation_count": len(public_operations),
        "operations": public_operations,
    }
    with log_path.open("w", encoding="utf-8") as handle:
        json.dump(log_payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")

    print(json.dumps({"output": str(output), "log": str(log_path), "operations": len(operations)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (EditError, json.JSONDecodeError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(2)
