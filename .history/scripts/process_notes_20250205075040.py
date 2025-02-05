import os
from scripts.file_utils import load_file_content, extract_yaml_header, write_updated_file
from scripts.tagging import generate_yaml_header, identify_new_tags
from scripts.logging_utils import log_action, log_new_tags

def merge_yaml_headers(existing_yaml, new_yaml):
    """
    Merge YAML metadata, keeping existing values when AI returns empty ones.

    - Merges lists (e.g., tags) without duplicates.
    - Overwrites scalar values only if AI-generated ones are not empty.
    
    Parameters:
        - existing_yaml (dict): The original YAML header.
        - new_yaml (dict): The AI-generated YAML header.

    Returns:
        - dict: The merged YAML metadata.
    """
    merged_yaml = existing_yaml.copy()

    for key, value in new_yaml.items():
        if not value:  # Ignore empty AI-generated fields
            continue

        if isinstance(value, list):  # Merge lists, ensuring no duplicates
            merged_yaml[key] = list(set(existing_yaml.get(key, []) + value))
        else:
            merged_yaml[key] = value  # Overwrite scalar values

    return merged_yaml


def process_file(file_path, reference_content, prompt_template, reference_tags, opt1, opt2, test_mode, log_file, new_tags_log):
    """
    Process an individual Markdown file with different processing modes.

    - If no YAML header exists, the file is skipped unless `opt1` or `opt2` is used.
    - If `opt1` is set, existing YAML metadata is **merged** with AI-generated metadata.
    - If `opt2` is set, existing YAML metadata is **replaced** with AI-generated metadata.
    - Otherwise, the AI-generated YAML is used as the only metadata.

    Parameters:
        - file_path (str): Path to the Markdown file.
        - reference_content (str): Reference content for generating tags.
        - prompt_template (str): Template for the AI prompt.
        - reference_tags (set): Existing tags from the reference content.
        - opt1 (bool): Merge AI-generated YAML with existing metadata.
        - opt2 (bool): Replace existing metadata with AI-generated YAML.
        - test_mode (bool): Use predefined trial metadata instead of OpenAI.
        - log_file (str): Path to log file.
        - new_tags_log (str): Path to new tags log file.
    """
    content = load_file_content(file_path)
    yaml_header, body = extract_yaml_header(content)
    file_name = os.path.basename(file_path)  # Extract just the file name

    # If no YAML header exists and neither option is used, skip the file
    if not yaml_header and not (opt1 or opt2):
        log_action(log_file, "Skipped (No YAML Header)", file_name)
        return

    # Generate new YAML metadata using AI or trial mode
    ai_metadata = generate_yaml_header(body, reference_content, prompt_template, test_mode)

    # Processing modes
    if yaml_header and opt1:
        merged_metadata = merge_yaml_headers(yaml_header, ai_metadata)
        log_action(log_file, "Merged YAML", file_name)
    elif yaml_header and opt2:
        merged_metadata = ai_metadata  # Completely replace existing YAML
        log_action(log_file, "Replaced YAML", file_name)
    else:
        merged_metadata = ai_metadata  # Default case: use AI-generated YAML only
        log_action(log_file, "Added YAML", file_name)

    # Identify and log new tags
    new_tags = identify_new_tags(merged_metadata.get("tags", []), reference_tags)
    if new_tags:
        log_new_tags(file_name, new_tags, new_tags_log)

    # Write updated file
    write_updated_file(file_path, merged_metadata, body)


def process_folder(folder_path, reference_content, prompt_template, reference_tags, opt1, opt2, test_mode, log_file, new_tags_log):
    """
    Iterate through Markdown files in the folder and process them.

    - Applies processing logic to each `.md` file found.
    
    Parameters:
        - folder_path (str): Path to the folder containing Markdown files.
        - reference_content (str): Reference content for generating tags.
        - prompt_template (str): Template for the AI prompt.
        - reference_tags (set): Existing tags from the reference content.
        - opt1 (bool): Merge AI-generated YAML with existing metadata.
        - opt2 (bool): Replace existing metadata with AI-generated YAML.
        - test_mode (bool): Use predefined trial metadata instead of OpenAI.
        - log_file (str): Path to log file.
        - new_tags_log (str): Path to new tags log file.
    """
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".md"):
                process_file(
                    os.path.join(root, file), reference_content, prompt_template, 
                    reference_tags, opt1, opt2, test_mode, log_file, new_tags_log
                )
