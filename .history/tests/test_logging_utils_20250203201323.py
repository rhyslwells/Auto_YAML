import pytest
import os
from scripts.logging_utils import log_action, log_new_tags


def test_log_action(tmp_path):
    log_file = tmp_path / "log.txt"
    log_action(log_file, "Updated", "test.md")

    with open(log_file, "r", encoding="utf-8") as f:
        content = f.read().strip()

    assert "Updated: test.md" in content

def test_log_new_tags(tmp_path):
    log_file = tmp_path / "new_tags_log.txt"
    log_new_tags("test.md", ["Deep Learning", "NLP"], log_file)

    with open(log_file, "r", encoding="utf-8") as f:
        content = f.read().strip()

    assert "New Tags in test.md: Deep Learning, NLP" in content
