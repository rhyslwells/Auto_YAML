import pytest
from scripts.tagging import extract_reference_tags, identify_new_tags
import yaml

def test_extract_reference_tags():
    reference_content = """---
tags:
  - AI
  - Machine Learning
  - Deep Learning
---
Reference file example."""
    
    ref_tags = extract_reference_tags(reference_content)
    
    assert isinstance(ref_tags, set)
    assert "AI" in ref_tags
    assert "Machine Learning" in ref_tags
    assert "Deep Learning" in ref_tags

def test_identify_new_tags():
    reference_tags = {"AI", "Machine Learning"}
    generated_tags = ["AI", "Deep Learning", "NLP"]

    new_tags = identify_new_tags(generated_tags, reference_tags)
    
    assert new_tags == {"Deep Learning", "NLP"}
