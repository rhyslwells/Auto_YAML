import pytest
from unittest.mock import patch
from scripts.process_notes import process_file
import yaml
from scripts.process_notes import merge_yaml_headers


@pytest.fixture
def mock_dependencies():
    """Mock dependencies used in `process_file`."""
    with patch("scripts.process_notes.load_file_content", return_value="mock file content") as mock_load_file_content, \
         patch("scripts.process_notes.extract_yaml_header", return_value=({"tags": ["OldTag"]}, "mock body")) as mock_extract_yaml_header, \
         patch("scripts.process_notes.generate_yaml_header", return_value={"tags": ["AI", "ML"]}) as mock_generate_yaml_header, \
         patch("scripts.process_notes.identify_new_tags", return_value={"ML"}) as mock_identify_new_tags, \
         patch("scripts.process_notes.write_updated_file") as mock_write_updated_file, \
         patch("scripts.process_notes.log_action") as mock_log_action, \
         patch("scripts.process_notes.log_new_tags") as mock_log_new_tags:

        yield {
            "mock_load_file_content": mock_load_file_content,
            "mock_extract_yaml_header": mock_extract_yaml_header,
            "mock_generate_yaml_header": mock_generate_yaml_header,  # ✅ Correct reference
            "mock_identify_new_tags": mock_identify_new_tags,
            "mock_write_updated_file": mock_write_updated_file,
            "mock_log_action": mock_log_action,
            "mock_log_new_tags": mock_log_new_tags
        }


def test_process_file(mock_dependencies):
    """Test processing a file while ensuring all dependencies are called correctly."""
    
    # Call process_file with mock data
    process_file(
        file_path="test.md",
        reference_content="reference content",
        prompt_template="prompt template",
        reference_tags={"AI", "ML"},
        opt1=False,
        opt2=False,
        test_mode=True,  # Bypass OpenAI
        log_file="logs/process_log.txt",
        new_tags_log="logs/new_tags_log.txt"
    )

    # Assertions: Ensure required functions were called correctly
    mock_dependencies["mock_load_file_content"].assert_called_once_with("test.md")
    mock_dependencies["mock_extract_yaml_header"].assert_called_once_with("mock file content")
    mock_dependencies["mock_generate_yaml_header"].assert_called_once_with("mock body", "reference content", "prompt template", True)
    mock_dependencies["mock_identify_new_tags"].assert_called_once_with(["AI", "ML"], {"AI", "ML"})
    mock_dependencies["mock_write_updated_file"].assert_called_once_with("test.md", {"tags": ["AI", "ML"]}, "mock body")
    mock_dependencies["mock_log_action"].assert_called_once_with("logs/process_log.txt", "Added YAML", "test.md")
    mock_dependencies["mock_log_new_tags"].assert_called_once_with("test.md", {"ML"}, "logs/new_tags_log.txt")


def test_merge_yaml_headers():
    """Test merging YAML headers flexibly."""

    # Case 1: Merge non-empty existing YAML with non-empty new YAML
    existing_yaml = {
        "tags": ["AI", "Machine Learning"],
        "category": "Technology",
        "custom_field": "Value1",
        "topic": "Neural Networks"
    }
    new_yaml = {
        "tags": ["Deep Learning", "AI"],
        "category": "Advanced Technology",
        "custom_field": "UpdatedValue",
        "phase": "Training"
    }

    merged = merge_yaml_headers(existing_yaml, new_yaml)

    # Ensure lists are merged without duplicates
    assert set(merged["tags"]) == {"AI", "Machine Learning", "Deep Learning"}
    assert merged["category"] == "Advanced Technology"  # Overwritten
    assert merged["custom_field"] == "UpdatedValue"  # Overwritten
    assert merged["topic"] == "Neural Networks"  # Kept from existing
    assert merged["phase"] == "Training"  # Added from new_yaml

    # Case 2: Handle empty new YAML fields (should not overwrite existing ones)
    new_yaml_with_empty = {
        "tags": [],
        "category": "",
        "custom_field": None,
        "phase": ""  # Should not override existing "phase"
    }

    merged = merge_yaml_headers(existing_yaml, new_yaml_with_empty)

    assert set(merged["tags"]) == {"AI", "Machine Learning"}  # Unchanged
    assert merged["category"] == "Technology"  # Kept from existing
    assert merged["custom_field"] == "Value1"  # Kept from existing
    assert "phase" not in merged  # Not added

    # Case 3: Handle when `existing_yaml` is a string (parsed YAML)
    existing_yaml_str = """
    tags:
      - AI
      - Machine Learning
    category: Technology
    topic: Neural Networks
    """
    new_yaml = {
        "tags": ["Deep Learning", "AI"],
        "category": "Advanced Technology",
        "phase": "Training"
    }

    existing_yaml_parsed = yaml.safe_load(existing_yaml_str)
    merged = merge_yaml_headers(existing_yaml_parsed, new_yaml)

    assert set(merged["tags"]) == {"AI", "Machine Learning", "Deep Learning"}
    assert merged["category"] == "Advanced Technology"
    assert merged["topic"] == "Neural Networks"
    assert merged["phase"] == "Training"

    # Case 4: Handle when `existing_yaml` is an empty dictionary
    empty_existing_yaml = {}
    merged = merge_yaml_headers(empty_existing_yaml, new_yaml)

    assert set(merged["tags"]) == set(new_yaml["tags"])
    assert merged["category"] == new_yaml["category"]
    assert merged["phase"] == new_yaml["phase"]
    assert "topic" not in merged  # Should not assume default values

    # Ensure it supports any arbitrary keys
    arbitrary_existing_yaml = {
        "authors": ["Alice", "Bob"],
        "version": "1.0",
        "related_work": []
    }
    arbitrary_new_yaml = {
        "authors": ["Charlie"],
        "version": "2.0",
        "related_work": ["Paper A"]
    }

    merged = merge_yaml_headers(arbitrary_existing_yaml, arbitrary_new_yaml)

    assert set(merged["authors"]) == {"Alice", "Bob", "Charlie"}
    assert merged["version"] == "2.0"  # Overwritten
    assert merged["related_work"] == ["Paper A"]  # Added


@pytest.mark.parametrize("existing_yaml, new_yaml, expected_result", [
    # Case: Both YAMLs are empty
    ({}, {}, {}),

    # Case: Existing YAML is empty, new YAML has content
    ({}, {"tags": ["AI"], "category": "Technology"}, {"tags": ["AI"], "category": "Technology"}),

    # Case: Both YAMLs have the same content (should be unchanged)
    ({"tags": ["AI"], "category": "Technology"}, {"tags": ["AI"], "category": "Technology"}, {"tags": ["AI"], "category": "Technology"})
])


def test_merge_yaml_headers_parametrized(existing_yaml, new_yaml, expected_result):
    """Test merging YAML headers with parameterized cases."""
    merged = merge_yaml_headers(existing_yaml, new_yaml)
    assert merged == expected_result
