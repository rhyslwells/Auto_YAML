import pytest
from unittest.mock import patch, MagicMock
import os
from main import main

@pytest.fixture
def mock_dependencies():
    with patch("main.process_folder") as mock_process_folder, \
         patch("main.load_file_content") as mock_load_file_content, \
         patch("main.extract_reference_tags") as mock_extract_reference_tags, \
         patch("scripts.process_notes.generate_yaml_header") as mock_generate_yaml_header, \
         patch("scripts.process_notes.identify_new_tags") as mock_identify_new_tags, \
         patch("os.path.exists") as mock_exists, \
         patch("scripts.logging_utils.log_action") as mock_log_action, \
         patch("scripts.logging_utils.log_new_tags") as mock_log_new_tags:

        # Mock return values for loading content
        mock_load_file_content.return_value = "mock content"
        mock_extract_reference_tags.return_value = {"AI", "ML"}
        mock_generate_yaml_header.return_value = {"tags": ["AI", "ML"]}
        mock_identify_new_tags.return_value = {"AI", "ML"}
        mock_exists.return_value = True  # Simulate that paths exist (reference file, prompt file, etc.)
        
        yield {
            "mock_process_folder": mock_process_folder,
            "mock_load_file_content": mock_load_file_content,
            "mock_extract_reference_tags": mock_extract_reference_tags,
            "mock_generate_yaml_header": mock_generate_yaml_header,
            "mock_identify_new_tags": mock_identify_new_tags,
            "mock_exists": mock_exists,
            "mock_log_action": mock_log_action,
            "mock_log_new_tags": mock_log_new_tags
        }

def test_main(mock_dependencies):
    """Test processing the main function with different modes."""

    # Test with --opt1 (merge mode)
    with patch("sys.argv", ["main.py", "--opt1"]):  
        # Call the main function
        main()

        # Ensure process_folder was called
        mock_dependencies["mock_process_folder"].assert_called_once()

        # Ensure that generate_yaml_header was called during file processing
        mock_dependencies["mock_generate_yaml_header"].assert_called_once()  # This ensures it was called

        # Validate logging actions
        mock_dependencies["mock_log_action"].assert_any_call(
            "logs/process_log.txt", "Merged YAML", 'test.md'
        )
        mock_dependencies["mock_log_new_tags"].assert_called_once_with(
            "test.md", {"AI", "ML"}, "logs/new_tags_log.txt"
        )

    # Test with --opt2 (replace mode)
    with patch("sys.argv", ["main.py", "--opt2"]):  
        # Call the main function
        main()

        # Ensure process_folder was called
        mock_dependencies["mock_process_folder"].assert_called_once()

        # Ensure that generate_yaml_header was called during file processing
        mock_dependencies["mock_generate_yaml_header"].assert_called_once()  # This ensures it was called

    # Test with --test (test mode)
    with patch("sys.argv", ["main.py", "--test"]):  
        # Call the main function
        main()

        # Ensure process_folder was called
        mock_dependencies["mock_process_folder"].assert_called_once()

        # Ensure the AI generation header is mocked (test mode)
        mock_dependencies["mock_generate_yaml_header"].assert_called_with(
            "mock body", "reference content", "prompt template", True
        )

    # Test logging error if config files don't exist
    mock_dependencies["mock_exists"].return_value = False  # Simulate non-existent files
    with patch("sys.stdout", new_callable=MagicMock()) as mock_stdout:
        with pytest.raises(SystemExit):  # Expecting a system exit due to missing files
            main()

        # Check if error messages were printed
        mock_stdout.write.assert_called_with(
            "Error: Notes directory not found: notes/notes_test\n"
        )
