import pytest
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

def test_generate_yaml_header_trial():
    """Test generating a trial YAML header without OpenAI API call."""
    result = generate_yaml_header("Some content", "Some reference", "Some prompt", test_mode=True)

    assert isinstance(result, dict)
    assert "tags" in result
    assert "aliases" in result
    assert "category" in result
    assert "phase" in result
    assert "topic" in result
    assert "filename" in result
    assert result["tags"] == ["AI", "Machine Learning", "Deep Learning"]
    assert result["aliases"] == ["ML Model", "AI Model"]


@pytest.fixture
def mock_openai(mocker):
    """Mock OpenAI API response."""
    mock_response = {
        "choices": [
            {
                "message": {
                    "content": yaml.dump({
                        "tags": ["AI", "Deep Learning", "NLP"],
                        "category": "Technology",
                        "phase": "Training",
                        "topic": "Neural Networks",
                        "filename": "nn_model.py"
                    })
                }
            }
        ]
    }
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

    result = generate_yaml_header(content, reference_content, prompt_template, use_trial=False)

    assert isinstance(result, dict)
    assert "tags" in result
    assert "category" in result
    assert "phase" in result
    assert "topic" in result
    assert "filename" in result
    assert set(result["tags"]) == {"AI", "Deep Learning", "NLP"}
    assert result["category"] == "Technology"
    assert result["phase"] == "Training"
    assert result["topic"] == "Neural Networks"
    assert result["filename"] == "nn_model.py"
