import sys
import os

# Ensure the parent directory (Auto_YAML) is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from scripts.tagging import extract_reference_tags, identify_new_tags, generate_tags_and_categories
import yaml
from scripts.file_utils import extract_yaml_header

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

def test_generate_tags_and_categories(mocker):
        content = "This is a test content."
        reference_content = """---
        tags:
        - AI
        - Machine Learning
        - Deep Learning
        ---
        Reference file example."""
        prompt_template = "Reference: {reference}\nContent: {target_content}\nGenerate tags and categories."

        mock_response = {
            "choices": [
                {
                    "message": {
                        "content": yaml.dump({
                            "tags": ["AI", "Deep Learning", "NLP"],
                            "categories": ["Technology", "Science"]
                        })
                    }
                }
            ]
        }

        mocker.patch('openai.ChatCompletion.create', return_value=mock_response)

        result = generate_tags_and_categories(content, reference_content, prompt_template)

        assert isinstance(result, dict)
        assert "tags" in result
        assert "categories" in result
        assert set(result["tags"]) == {"AI", "Deep Learning", "NLP"}
        assert set(result["categories"]) == {"Technology", "Science"}