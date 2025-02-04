import os
from scripts.file_utils import load_file_content, extract_yaml_header, write_updated_file
from scripts.tagging import generate_yaml_header, identify_new_tags
from scripts.logging_utils import log_action, log_new_tags

def merge_yaml_headers(existing_yaml, new_yaml):
    """
    Merge two YAML dictionaries:
    - Lists (like tags) are combined (old + new, removing duplicates).
    - Scalar values (like category, phase) are overwritten by new YAML values.
    """
    merged_yaml = existing_yaml.copy()  # Copy the existing YAML

    for key, value in new_yaml.items():
        if isinstance(value, list):  # Merge lists (tags, aliases, etc.)
            merged_yaml[key] = list(set(existing_yaml.get(key, []) + value))  # Remove duplicates
        else:  # Overwrite scalars (category, phase, etc.)
            merged_yaml[key] = value

    return merged_yaml

def process_file(file_path, reference_content, prompt_template, reference_tags, opt1, opt2, log_file, new_tags_log):
    """Process an individual Markdown file with different processing modes."""
    content = load_file_content(file_path)
    yaml_header, body = extract_yaml_header(content)

    # If no YAML header exists and neither option is used, skip the file
    if not yaml_header and not (opt1 or opt2):
        log_action(log_file, "Skipped (No YAML Header)", file_path)
        return

    # Generate new YAML metadata using AI
    ai_metadata = generate_yaml_header(body, reference_content, prompt_template)

    # Option 1: Merge existing YAML with new YAML (preserving old tags)
    if yaml_header and opt1:
        merged_metadata = merge_yaml_headers(yaml_header, ai_metadata)
    # Option 2: Replace existing YAML with new YAML
    elif yaml_header and opt2:
        merged_metadata = ai_metadata  # Discard existing YAML, use only new AI-generated metadata
    # Default: Use AI-generated YAML as the only metadata (when no existing YAML)
    else:
        merged_metadata = ai_metadata

    # Identify new tags
    new_tags = identify_new_tags(merged_metadata.get("tags", []), reference_tags)
    if new_tags:
        log_new_tags(file_path, new_tags, new_tags_log)

    # Write updated file
    write_updated_file(file_path, merged_metadata, body)

    log_action(log_file, "Updated", file_path)

def process_folder(folder_path, reference_content, prompt_template, reference_tags, opt1, opt2, log_file, new_tags_log):
    """Iterate through Markdown files in the folder and process them."""
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".md"):
                process_file(os.path.join(root, file), reference_content, prompt_template, reference_tags, opt1, opt2, log_file, new_tags_log)
