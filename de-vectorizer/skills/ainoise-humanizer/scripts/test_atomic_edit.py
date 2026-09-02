#!/usr/bin/env python3

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("atomic_edit.py")
TRACE = {
    "example_source": "02_AI惯用语黑名单与识别标注表.md#测试章节",
    "whitelist_check": "未命中白名单例外",
}


class AtomicEditTests(unittest.TestCase):
    def run_editor(self, source_text: str, payload: dict) -> tuple[subprocess.CompletedProcess[str], Path, Path, tempfile.TemporaryDirectory[str]]:
        temp_dir = tempfile.TemporaryDirectory()
        root = Path(temp_dir.name)
        source = root / "source.md"
        edits = root / "edits.json"
        output = root / "source_润色版.md"
        source.write_text(source_text, encoding="utf-8")
        edits.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        result = subprocess.run(
            [sys.executable, str(SCRIPT), str(source), str(edits), str(output)],
            check=False,
            capture_output=True,
            text=True,
        )
        return result, output, Path(str(output) + ".editlog.json"), temp_dir

    def test_replace_delete_and_log(self) -> None:
        payload = {
            "operations": [
                {"op": "replace", "line": 1, "column": 2, "old": "乙", "new": "丁", "rule_id": "B07", "reason": "测试替换", **TRACE},
                {"op": "delete", "line": 1, "column": 3, "old": "丙", "new": "", "rule_id": "B04", "reason": "测试删除", **TRACE},
            ]
        }
        result, output, log_path, temp_dir = self.run_editor("甲乙丙。\n", payload)
        self.addCleanup(temp_dir.cleanup)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(output.read_text(encoding="utf-8"), "甲丁。\n")
        self.assertEqual(json.loads(log_path.read_text(encoding="utf-8"))["operation_count"], 2)

    def test_multiple_inserts_keep_declared_order(self) -> None:
        payload = {
            "operations": [
                {"op": "insert", "line": 1, "column": 2, "old": "", "new": "中", "order": 1, "rule_id": "B07", "reason": "测试插入", **TRACE},
                {"op": "insert", "line": 1, "column": 2, "old": "", "new": "文", "order": 2, "rule_id": "B07", "reason": "测试插入", **TRACE},
            ]
        }
        result, output, _, temp_dir = self.run_editor("甲乙", payload)
        self.addCleanup(temp_dir.cleanup)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(output.read_text(encoding="utf-8"), "甲中文乙")

    def test_rejects_multi_character_replacement(self) -> None:
        payload = {
            "operations": [
                {"op": "replace", "line": 1, "column": 1, "old": "甲乙", "new": "丁", "rule_id": "B07", "reason": "非法多字替换", **TRACE}
            ]
        }
        result, output, _, temp_dir = self.run_editor("甲乙", payload)
        self.addCleanup(temp_dir.cleanup)
        self.assertEqual(result.returncode, 2)
        self.assertFalse(output.exists())
        self.assertIn("one Unicode character", result.stderr)

    def test_requires_original_example_source(self) -> None:
        payload = {
            "operations": [
                {
                    "op": "replace",
                    "line": 1,
                    "column": 1,
                    "old": "甲",
                    "new": "丁",
                    "rule_id": "B07",
                    "reason": "缺少原始出处",
                    "whitelist_check": "未命中白名单例外",
                }
            ]
        }
        result, output, _, temp_dir = self.run_editor("甲乙", payload)
        self.addCleanup(temp_dir.cleanup)
        self.assertEqual(result.returncode, 2)
        self.assertFalse(output.exists())
        self.assertIn("example_source is required", result.stderr)

    def test_rejects_output_as_log_before_writing(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source.md"
            edits = root / "edits.json"
            output = root / "source_润色版.md"
            source.write_text("甲乙", encoding="utf-8")
            edits.write_text(
                json.dumps(
                    {
                        "operations": [
                            {
                                "op": "replace",
                                "line": 1,
                                "column": 1,
                                "old": "甲",
                                "new": "丁",
                                "rule_id": "B07",
                                "reason": "测试日志路径",
                                **TRACE,
                            }
                        ]
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(source), str(edits), str(output), "--log", str(output)],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 2)
            self.assertFalse(output.exists())
            self.assertIn("log path must differ", result.stderr)


if __name__ == "__main__":
    unittest.main()
