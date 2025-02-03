# tests/test_main.py

import pytest
from unittest.mock import patch
from main import main

@pytest.fixture
def mock_dependencies():
    with patch("main.process_folder") as mock_process_folder, \
         patch("scripts.file_utils.load_file_content") as mock_load_file_content, \
         patch("scripts.process_notes.extract_yaml_header") as mock_extract_yaml_header, \
         patch("scripts.process_notes.generate_tags_and_categories") as mock_generate_tags_and_categories, \
         patch("scripts.process_notes.identify_new_tags") as mock_identify_new_tags:

        # Mock return values for loading content
        mock_load_file_content.return_value = "mock content"
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

def test_main(mock_dependencies):
    with patch("sys.argv", ["main.py", "--force"]):
        # Call the main function
        main()

        # Ensure process_folder was called
        mock_dependencies["mock_process_folder"].assert_called_once()
