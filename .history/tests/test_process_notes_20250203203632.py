# tests/test_process_notes.py

import os
import pytest
from unittest.mock import patch, MagicMock
from scripts.process_notes import process_file, process_folder

# Mock paths for testing
MOCK_FILE_PATH = "test.md"
MOCK_REFERENCE_CONTENT = "reference content"
MOCK_PROMPT_TEMPLATE = "prompt template"
MOCK_REFERENCE_TAGS = {"AI", "ML"}
MOCK_FORCE_UPDATE = False

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

        # Setup mock return values
        mock_load_file_content.return_value = "file content"
        mock_extract_yaml_header.return_value = ("yaml_header", "body")
        mock_generate_tags_and_categories.return_value = {"tags": ["AI", "ML"]}
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
    mock_load_file_content = mock_dependencies["mock_load_file_content"]
    mock_extract_yaml_header = mock_dependencies["mock_extract_yaml_header"]
    mock_generate_tags_and_categories = mock_dependencies["mock_generate_tags_and_categories"]
    mock_identify_new_tags = mock_dependencies["mock_identify_new_tags"]
    mock_write_updated_file = mock_dependencies["mock_write_updated_file"]
    mock_log_action = mock_dependencies["mock_log_action"]
    mock_log_new_tags = mock_dependencies["mock_log_new_tags"]

    # Call process_file
    process_file(MOCK_FILE_PATH, MOCK_REFERENCE_CONTENT, MOCK_PROMPT_TEMPLATE, MOCK_REFERENCE_TAGS, MOCK_FORCE_UPDATE)

    # Check that the required functions were called with correct arguments
    mock_load_file_content.assert_called_once_with(MOCK_FILE_PATH)
    mock_extract_yaml_header.assert_called_once_with("file content")
    mock_generate_tags_and_categories.assert_called_once_with("body", MOCK_REFERENCE_CONTENT, MOCK_PROMPT_TEMPLATE)
    mock_identify_new_tags.assert_called_once_with(["AI", "ML"], MOCK_REFERENCE_TAGS)
    mock_write_updated_file.assert_called_once()
    mock_log_action.assert_called_once_with("process_log.txt", "Updated", MOCK_FILE_PATH)
    mock_log_new_tags.assert_called_once_with(MOCK_FILE_PATH, {"AI", "ML"}, "new_tags_log.txt")

# Test for processing all files in a folder (process_folder)
def test_process_folder(mock_dependencies):
    with patch("os.walk") as mock_os_walk:
        mock_os_walk.return_value = [("root", [], ["file1.md", "file2.md"])]
        
        process_folder("mock_folder", MOCK_REFERENCE_CONTENT, MOCK_PROMPT_TEMPLATE, MOCK_REFERENCE_TAGS, MOCK_FORCE_UPDATE)
        
        # Ensure process_file was called twice (once for each file)
        mock_dependencies["mock_log_action"].assert_any_call("process_log.txt", "Updated", "mock_folder/file1.md")
        mock_dependencies["mock_log_action"].assert_any_call("process_log.txt", "Updated", "mock_folder/file2.md")
