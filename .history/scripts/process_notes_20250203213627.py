import os
from scripts.file_utils import load_file_content, extract_yaml_header, write_updated_file
from scripts.tagging import generate_yaml_header, identify_new_tags
from scripts.logging_utils import log_action, log_new_tags

def process_file(file_path, reference_content, prompt_template, reference_tags, force_update, log_file, new_tags_log):
    """Process an individual Markdown file."""
    content = load_file_content(file_path)
    yaml_header, body = extract_yaml_header(content)
    
    if yaml_header and not force_update and "tags" in yaml_header and "category" in yaml_header:
        # Print just the file name, not the full path
        print(f"Skipping (already tagged): {os.path.basename(file_path)}")
        log_action(log_file, "Skipped", file_path)  # Using the full path of log file here
        return
    
    metadata = yaml_header if yaml_header else {}
    ai_metadata = generate_yaml_header(body, reference_content, prompt_template)
    
    new_tags = identify_new_tags(ai_metadata.get("tags", []), reference_tags)
    if new_tags:
        log_new_tags(file_path, new_tags, new_tags_log)  # Using the full path of new tags log here

    metadata.update(ai_metadata)
    write_updated_file(file_path, metadata, body)
    
    # Print just the file name, not the full path
    print(f"Updated: {os.path.basename(file_path)}")
    log_action(log_file, "Updated", file_path)  # Using the full path of log file here

def process_folder(folder_path, reference_content, prompt_template, reference_tags, force_update, log_file, new_tags_log):
    """Iterate through Markdown files in the folder and process them."""
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".md"):
                process_file(os.path.join(root, file), reference_content, prompt_template, reference_tags, force_update, log_file, new_tags_log)
