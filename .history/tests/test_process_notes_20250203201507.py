import os
import pytest
from unittest.mock import patch, mock_open
from scripts.process_notes import process_file, process_folder
from scripts.file_utils import load_file_content
from scripts.tagging import extract_reference_tags

@pytest.fixture
def mock_files():
    return {
        "test.md": "---\ntags: []\ncategory: \n---\nThis is a test note.",
        "reference.md": "---\ntags:\n- AI\n- Machine Learning\n- Deep Learning\n---",
        "prompt.txt": "Reference: {reference}\nContent: {target_content}\nGenerate tags and categories."
    }

@patch("builtins.open", new_callable=mock_open)
@patch("scripts.file_utils.write_updated_file")
@patch("scripts.logging_utils.log_action")
@patch("scripts.logging_utils.log_new_tags")
def test_process_file(mock_log_new_tags, mock_log_action, mock_write, mock_open, mock_files):
    mock_open.side_effect = lambda file, mode='r', *args, **kwargs: mock_open(read_data=mock_files.get(os.path.basename(file), "")).return_value
    
    reference_content = load_file_content("reference.md")
    prompt_template = load_file_content("prompt.txt")
    reference_tags = extract_reference_tags(reference_content)
    
    with patch("scripts.tagging.generate_tags_and_categories", return_value={"tags": ["AI", "NLP"], "category": "Technology"}):
        process_file("test.md", reference_content, prompt_template, reference_tags, force_update=False)
    
    mock_write.assert_called()
    mock_log_action.assert_called_with("process_log.txt", "Updated", "test.md")
    mock_log_new_tags.assert_called_with("test.md", {"NLP"})

@patch("os.walk")
@patch("scripts.main.process_file")
def test_process_folder(mock_process_file, mock_os_walk, mock_files):
    mock_os_walk.return_value = [("/path/to/notes", [], ["test.md"])]
    
    reference_content = load_file_content("reference.md")
    prompt_template = load_file_content("prompt.txt")
    reference_tags = extract_reference_tags(reference_content)
    
    process_folder("/path/to/notes", reference_content, prompt_template, reference_tags, force_update=False)
    
    mock_process_file.assert_called_with("/path/to/notes/test.md", reference_content, prompt_template, reference_tags, False)
