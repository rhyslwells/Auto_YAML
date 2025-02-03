import os
import argparse
from file_utils import load_file_content, extract_yaml_header, write_updated_file
from tagging import extract_reference_tags, generate_tags_and_categories, identify_new_tags
from logging_utils import log_action, log_new_tags

# Paths
FOLDER_PATH = "/path/to/your/obsidian/notes"
REFERENCE_FILE_PATH = "/path/to/config/reference.md"
PROMPT_FILE_PATH = "/path/to/config/prompt.txt"
LOG_FILE = "process_log.txt"
NEW_TAGS_LOG = "new_tags_log.txt"

def process_file(file_path, reference_content, prompt_template, reference_tags, force_update):
    """Process an individual Markdown file."""
    content = load_file_content(file_path)
    yaml_header, body = extract_yaml_header(content)
    
    if yaml_header and not force_update and "tags" in yaml_header and "category" in yaml_header:
        print(f"Skipping (already tagged): {file_path}")
        log_action(LOG_FILE, "Skipped", file_path)
        return
    
    metadata = yaml_header if yaml_header else {}
    ai_metadata = generate_tags_and_categories(body, reference_content, prompt_template)
    
    new_tags = identify_new_tags(ai_metadata.get("tags", []), reference_tags)
    if new_tags:
        log_new_tags(file_path, new_tags)

    metadata.update(ai_metadata)
    write_updated_file(file_path, metadata, body)
    
    print(f"Updated: {file_path}")
    log_action(LOG_FILE, "Updated", file_path)

def process_folder(folder_path, reference_content, prompt_template, reference_tags, force_update):
    """Iterate through Markdown files in the folder and process them."""
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".md"):
                process_file(os.path.join(root, file), reference_content, prompt_template, reference_tags, force_update)

# **Parse command-line arguments**
parser = argparse.ArgumentParser(description="Process Obsidian notes with AI-generated YAML metadata.")
parser.add_argument("--force", action="store_true", help="Force update all files, even if already tagged.")
args = parser.parse_args()

# **Load reference and prompt once**
reference_content = load_file_content(REFERENCE_FILE_PATH)
prompt_template = load_file_content(PROMPT_FILE_PATH)
reference_tags = extract_reference_tags(reference_content)

# **Clear log files before processing**
open(LOG_FILE, "w").close()
open(NEW_TAGS_LOG, "w").close()

# **Process folder with optional force update**
process_folder(FOLDER_PATH, reference_content, prompt_template, reference_tags, args.force)

