import pytest
from ..scripts.file_utils import extract_yaml_header, load_file_content, write_updated_file
import yaml
import os

def test_extract_yaml_header():
    content = """---
tags:
  - AI
  - NLP
category: "Machine Learning"
---
This is a test note."""
    
    yaml_data, body = extract_yaml_header(content)
    
    assert isinstance(yaml_data, dict)
    assert yaml_data["category"] == "Machine Learning"
    assert "AI" in yaml_data["tags"]
    assert "NLP" in yaml_data["tags"]
    assert body == "This is a test note."

def test_load_file_content(tmp_path):
    file_path = tmp_path / "test.md"
    file_path.write_text("Test content")

    content = load_file_content(file_path)
    assert content == "Test content"

def test_write_updated_file(tmp_path):
    file_path = tmp_path / "test.md"
    
    metadata = {"tags": ["ML"], "category": "Data Science"}
    body = "Test note content."
    
    write_updated_file(file_path, metadata, body)
    
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    expected_content = """---
tags:
- ML
category: Data Science
---

Test note content."""
    
    assert content.strip() == expected_content.strip()  # Strip to avoid whitespace issues
