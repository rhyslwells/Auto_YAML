import os

def log_action(log_file, action, file_path):
    """Log processed or skipped files with the basename of the file."""
    # Get the basename of the file (i.e., the file name without the path)
    file_name = os.path.basename(file_path)
    with open(log_file, "a", encoding="utf-8") as log:
        log.write(f"{action}: {file_name}\n")

def log_new_tags(file_path, new_tags, log_file="new_tags_log.txt"):
    """Log newly introduced tags that were not in the reference file, using the basename of the file."""
    # Get the basename of the file (i.e., the file name without the path)
    file_name = os.path.basename(file_path)
    with open(log_file, "a", encoding="utf-8") as log:
        log.write(f"New Tags in {file_name}: {', '.join(new_tags)}\n")
