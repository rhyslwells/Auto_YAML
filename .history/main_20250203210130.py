import os
import sys
from scripts.process_notes import process_folder
from scripts.file_utils import load_file_content
from scripts.tagging import extract_reference_tags
import argparse
import logging

# Ensure the script runs from the project root
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.path.join(BASE_DIR, "config")
NOTES_DIR = os.path.join(BASE_DIR, "notes", "notes_test")
LOGS_DIR = os.path.join(BASE_DIR, "logs")

# Ensure logs directory exists
os.makedirs(LOGS_DIR, exist_ok=True)

# Configure logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Paths
REFERENCE_FILE_PATH = os.path.join(CONFIG_DIR, "reference.md")
PROMPT_FILE_PATH = os.path.join(CONFIG_DIR, "prompt.md")
LOG_FILE = os.path.join(LOGS_DIR, "process_log.txt")
NEW_TAGS_LOG = os.path.join(LOGS_DIR, "new_tags_log.txt")

def main():
    """Main entry point to process Obsidian notes."""
    
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Process Obsidian notes with AI-generated YAML metadata.")
    parser.add_argument("--force", action="store_true", help="Force update all files, even if already tagged.")
    args = parser.parse_args()

    # Verify config files exist
    if not os.path.exists(REFERENCE_FILE_PATH):
        raise FileNotFoundError(f"Reference file not found: {REFERENCE_FILE_PATH}")
    if not os.path.exists(PROMPT_FILE_PATH):
        raise FileNotFoundError(f"Prompt file not found: {PROMPT_FILE_PATH}")

    # Load reference and prompt
    reference_content = load_file_content(REFERENCE_FILE_PATH)
    prompt_template = load_file_content(PROMPT_FILE_PATH)
    reference_tags = extract_reference_tags(reference_content)

    # Clear log files before processing
    open(LOG_FILE, "w").close()
    open(NEW_TAGS_LOG, "w").close()

    # Verify the notes directory exists
    if not os.path.exists(NOTES_DIR):
        raise FileNotFoundError(f"Notes directory not found: {NOTES_DIR}")

    try:
        # Process folder with optional force update
        process_folder(NOTES_DIR, reference_content, prompt_template, reference_tags, args.force)
        logging.info("Processing completed successfully.")
    except Exception as e:
        logging.error(f"An error occurred during processing: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
