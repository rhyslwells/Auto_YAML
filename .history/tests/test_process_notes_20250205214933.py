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
    """Test merging YAML headers with different cases."""

    # Case 1: Merge non-empty existing YAML with non-empty new YAML
    existing_yaml = {
        "tags": ["AI", "Machine Learning"],
        "category": "Technology",
        "topic": "Neural Networks"
    }
    new_yaml = {
        "tags": ["Deep Learning", "AI"],
        "category": "Advanced Technology",
        "phase": "Training"
    }

    merged = merge_yaml_headers(existing_yaml, new_yaml)
    
    assert merged == {
        "tags": ["AI", "Machine Learning", "Deep Learning"],  # Merged tags with no duplicates
        "category": "Advanced Technology",  # Replaced category
        "topic": "Neural Networks",  # Kept from existing YAML
        "phase": "Training"  # Added from new YAML
    }

    # Case 2: Handle empty new YAML fields
    new_yaml_with_empty_field = {
        "tags": [],
        "category": "New Category",
        "phase": ""
    }

    merged = merge_yaml_headers(existing_yaml, new_yaml_with_empty_field)
    
    assert merged == {
        "tags": ["AI", "Machine Learning"],  # Existing tags remain unchanged as new tags is empty
        "category": "New Category",  # Replaced with new category
        "topic": "Neural Networks",  # Kept from existing YAML
        "phase": "Training"  # Kept from existing YAML as phase was empty in new YAML
    }

    # Case 3: Handle when existing_yaml is a string (YAML string)
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

    # Parse the existing YAML string
    existing_yaml_parsed = yaml.safe_load(existing_yaml_str)

    merged = merge_yaml_headers(existing_yaml_parsed, new_yaml)

    assert merged == {
        "tags": ["AI", "Machine Learning", "Deep Learning"],  # Merged tags with no duplicates
        "category": "Advanced Technology",  # Replaced category
        "topic": "Neural Networks",  # Kept from existing YAML
        "phase": "Training"  # Added from new YAML
    }

    # Case 4: Handle when existing_yaml is an empty dictionary
    empty_existing_yaml = {}
    merged = merge_yaml_headers(empty_existing_yaml, new_yaml)

    assert merged == new_yaml  # Since existing YAML is empty, return new YAML as is


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
