# tests/test_process_notes.py

import pytest
from unittest.mock import patch
from scripts.process_notes import process_file, process_folder

# Mocks for the functions used in process_file
@pytest.fixture
def mock_dependencies():
    with patch("scripts.process_notes.load_file_content") as mock_load_file_content, \
         patch("scripts.process_notes.extract_yaml_header") as mock_extract_yaml_header, \
         patch("scripts.process_notes.generate_tags_and_categories") as mock_generate_tags_and_categories, \
         patch("scripts.process_notes.identify_new_tags") as mock_identify_new_tags, \
         patch("scripts.process_notes.write_updated_file") as mock_write_updated_file, \
         patch("scripts.process_notes.log_action") as mock_log_action, \
         patch("scripts.process_notes.log_new_tags") as mock_log_new_tags:

        # Mock return values
        mock_load_file_content.return_value = "file content"
        mock_extract_yaml_header.return_value = ("yaml_header", "body")
        
        # Ensure generate_tags_and_categories returns a dict, not a string
        mock_generate_tags_and_categories.return_value = {"tags": ["AI", "ML"], "categories": ["Technology"]}  # Dictionary return value
        
        mock_identify_new_tags.return_value = {"AI", "ML"}
        mock_write_updated_file.return_value = None
        mock_log_action.return_value = None
        mock_log_new_tags.return_value = None

        yield {
            "mock_load_file_content": mock_load_file_content,
            "mock_extract_yaml_header": mock_extract_yaml_header,
            "mock_generate_tags_and_categories": mock_generate_tags_and_categories,
            "mock_identify_new_tags": mock_identify_new_tags,
            "mock_write_updated_file": mock_write_updated_file,
            "mock_log_action": mock_log_action,
            "mock_log_new_tags": mock_log_new_tags
        }

# Test for processing a single file (process_file)
def test_process_file(mock_dependencies):
    # Call process_file
    process_file("test.md", "reference content", "prompt template", {"AI", "ML"}, False)

    # Check that the required functions were called with correct arguments
    mock_dependencies["mock_load_file_content"].assert_called_once_with("test.md")
    mock_dependencies["mock_extract_yaml_header"].assert_called_once_with("file content")
    mock_dependencies["mock_generate_tags_and_categories"].assert_called_once_with("body", "reference content", "prompt template")
    mock_dependencies["mock_identify_new_tags"].assert_called_once_with(["AI", "ML"], {"AI", "ML"})
    mock_dependencies["mock_write_updated_file"].assert_called_once()
    mock_dependencies["mock_log_action"].assert_called_once_with("process_log.txt", "Updated", "test.md")
    mock_dependencies["mock_log_new_tags"].assert_called_once_with("test.md", {"AI", "ML"}, "new_tags_log.txt")
