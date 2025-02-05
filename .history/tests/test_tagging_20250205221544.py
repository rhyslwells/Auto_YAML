import pytest
from unittest.mock import patch
import yaml
from scripts.tagging import extract_reference_tags, identify_new_tags, generate_yaml_header

def test_extract_reference_tags():
    """Test extracting tags from a reference YAML header."""
    reference_content = """---
    tags:
    - AI
    - Machine Learning
    - Deep Learning
    ---
    Reference file example."""

    ref_tags = extract_reference_tags(reference_content)

    assert isinstance(ref_tags, set)
    assert ref_tags == {"AI", "Machine Learning", "Deep Learning"}

def test_extract_reference_tags_empty():
    """Test extracting tags when reference content is empty."""
    reference_content = ""
    ref_tags = extract_reference_tags(reference_content)

    assert isinstance(ref_tags, set)
    assert ref_tags == set()  # Should return an empty set

def test_identify_new_tags():
    """Test identifying new tags that are not in the reference file."""
    reference_tags = {"AI", "Machine Learning"}
    generated_tags = ["AI", "Deep Learning", "NLP"]

    new_tags = identify_new_tags(generated_tags, reference_tags)
    
    assert isinstance(new_tags, set)
    assert new_tags == {"Deep Learning", "NLP"}

def test_identify_new_tags_no_difference():
    """Test when there are no new tags."""
    reference_tags = {"AI", "Machine Learning", "Deep Learning"}
    generated_tags = ["AI", "Machine Learning", "Deep Learning"]

    new_tags = identify_new_tags(generated_tags, reference_tags)

    assert isinstance(new_tags, set)
    assert new_tags == set()  # No new tags expected


import pytest
from unittest.mock import patch
import yaml
from your_module import generate_yaml_header  # Update the import path for your module

def test_generate_yaml_header_trial():
    """Test generating a trial YAML header without OpenAI API call."""

    # Call the function in test mode
    result = generate_yaml_header("Some content", "Some reference", "Some prompt", test_mode=True)

    # Check that the result is a dictionary
    assert isinstance(result, dict)

    # Verify required keys exist
    assert "tags" in result
    assert "aliases" in result
    assert "category" in result
    assert "phase" in result
    assert "topic" in result
    assert "filename" in result

    # Check the values returned are as expected for trial mode
    assert result["tags"] == ["AI", "Machine Learning", "Deep Learning"]
    assert result["aliases"] == ["ML Model", "AI Model"]
    assert result["category"] == "Technology"
    assert result["phase"] == "Model Training"
    assert result["topic"] == "Neural Networks"
    assert result["filename"] == "neural_network_model.py"


@pytest.fixture
def mock_openai(mocker):
    """Mock OpenAI API response."""
    mock_response = {
        "choices": [
            {
                "message": {
                    "content": yaml.dump({
                        "tags": ["AI", "Deep Learning", "NLP"],
                        "aliases": ["ML Model", "AI Model"],
                        "category": "Technology",
                        "phase": "Training",
                        "topic": "Neural Networks",
                        "filename": "nn_model.py"
                    })
                }
            }
        ]
    }
    # Mocking the OpenAI API call
    return mocker.patch("openai.ChatCompletion.create", return_value=mock_response)


def test_generate_yaml_header_openai(mock_openai):
    """Test generating YAML header using OpenAI mock."""

    content = "This is a test content."
    reference_content = """---
    tags:
      - AI
      - Machine Learning
      - Deep Learning
    ---
    Reference file example."""
    prompt_template = "Reference: {reference}\nContent: {target_content}\nGenerate tags and categories."

    # Call the function, now in real mode (using the mocked OpenAI response)
    result = generate_yaml_header(content, reference_content, prompt_template, test_mode=False)

    # Ensure the result is a dictionary
    assert isinstance(result, dict)

    # Verify that all expected keys exist in the result
    assert "tags" in result
    assert "aliases" in result
    assert "category" in result
    assert "phase" in result
    assert "topic" in result
    assert "filename" in result

    # Check if the tags are correctly returned, comparing sets to ignore order
    assert set(result["tags"]) == {"AI", "Deep Learning", "NLP"}
    
    # Verify that the aliases, category, phase, topic, and filename are correctly set
    assert result["aliases"] == ["ML Model", "AI Model"]
    assert result["category"] == "Technology"
    assert result["phase"] == "Training"
    assert result["topic"] == "Neural Networks"
    assert result["filename"] == "nn_model.py"
