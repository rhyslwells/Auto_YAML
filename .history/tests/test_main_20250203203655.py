# tests/test_main.py

import os
import pytest
import sys
from unittest.mock import patch, MagicMock
from main import main

# Mock paths for testing
MOCK_FILE_PATH = "test.md"
MOCK_REFERENCE_CONTENT = "reference content"
MOCK_PROMPT_TEMPLATE = "prompt template"
MOCK_REFERENCE_TAGS = {"AI", "ML"}
MOCK_FORCE_UPDATE = False

# Mocks for the functions used in main.py
@pytest.fixture
def mock_dependencies():
    with patch("main.process_folder") as mock_process_folder, \
         patch("scripts.file_utils.load_file_content") as mock_load_file_content, \
         patch("scripts.process_notes.extract_yaml_header") as mock_extract_yaml_header, \
         patch("scripts.process_notes.generate_tags_and_categories") as mock_generate_tags_and_categories, \
         patch("scripts.process_notes.identify_new_tags") as mock_identify_new_tags:

        # Setup mock return values
        mock_load_file_content.return_value = "file content"
        mock_extract_yaml_header.return_value = ("yaml_header", "body")
        mock_generate_tags_and_categories.return_value = {"tags": ["AI", "ML"]}
        mock_identify_new_tags.return_value = {"AI", "ML"}

        yield {
            "mock_process_folder": mock_process_folder,
            "mock_load_file_content": mock_load_file_content,
            "mock_extract_yaml_header": mock_extract_yaml_header,
            "mock_generate_tags_and_categories": mock_generate_tags_and_categories,
            "mock_identify_new_tags": mock_identify_new_tags
        }

# Test for running main.py
def test_main(mock_dependencies):
    with patch("sys.argv", ["main.py", "--force"]):
        # Call the main function
        main()

        # Check that process_folder was called
        mock_dependencies["mock_process_folder"].assert_called_once_with(
            "notes/notes_test", MOCK_REFERENCE_CONTENT, MOCK_PROMPT_TEMPLATE, MOCK_REFERENCE_TAGS, True
        )
