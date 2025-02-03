import yaml

def load_file_content(file_path):
    """Load the content of a file."""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read().strip()

def extract_yaml_header(content):
    """Extract YAML frontmatter if it exists."""
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) > 2:
            return yaml.safe_load(parts[1]), parts[2].strip()
    return None, content.strip()

def write_updated_file(file_path, metadata, body):
    """Write the updated YAML frontmatter and content to the file."""
    new_yaml_header = yaml.dump(metadata, default_flow_style=False, sort_keys=False).strip()
    new_content = f"---\n{new_yaml_header}\n---\n\n{body}"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)

