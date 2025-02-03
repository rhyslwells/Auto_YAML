def log_action(log_file, action, file_path):
    """Log processed or skipped files."""
    with open(log_file, "a", encoding="utf-8") as log:
        log.write(f"{action}: {file_path}\n")

def log_new_tags(file_path, new_tags, log_file="new_tags_log.txt"):
    """Log newly introduced tags that were not in the reference file."""
    with open(log_file, "a", encoding="utf-8") as log:
        log.write(f"New Tags in {file_path}: {', '.join(new_tags)}\n")

