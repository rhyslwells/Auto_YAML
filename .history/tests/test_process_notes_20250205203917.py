import pytest
import os
from unittest.mock import patch
from scripts.process_notes import process_file

# Fixture for dependency mocking
@pytest.fixture
def mock_dependencies(mocker):
    """Mock dependencies used in `process_file`."""
    mocks = {
        "mock_load_file_content": mocker.patch("scripts.file_utils.load_file_content", return_value="mock file content"),
        "mock_extract_yaml_header": mocker.patch("scripts.file_utils.extract_yaml_header", return_value=({}, "mock body")),
        "mock_generate_yaml_header": mocker.patch("scripts.tagging.generate_yaml_header", return_value={"tags": ["AI", "ML"]}),
        "mock_identify_new_tags": mocker.patch("scripts.tagging.identify_new_tags", return_value={"ML"}),
        "mock_write_updated_file": mocker.patch("scripts.file_utils.write_updated_file"),
        "mock_log_action": mocker.patch("scripts.logging_utils.log_action"),
        "mock_log_new_tags": mocker.patch("scripts.logging_utils.log_new_tags"),
    }
    return mocks

def test_process_file(mock_dependencies):
    """Test processing a file while ensuring all dependencies are called correctly."""
    
    # Call process_file with proper parameters
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
