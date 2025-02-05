import os
import sys
import argparse
import logging
from scripts.process_notes import process_folder
from scripts.file_utils import load_file_content
from scripts.tagging import extract_reference_tags

# Ensure the script runs from the project root
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.path.join(BASE_DIR, "config")
NOTES_DIR = os.path.join(BASE_DIR, "notes", "notes_test")
LOGS_DIR = os.path.join(BASE_DIR, "logs")

# Ensure logs directory exists
os.makedirs(LOGS_DIR, exist_ok=True)

# Paths for configuration and logs
REFERENCE_FILE_PATH = os.path.join(CONFIG_DIR, "reference.md")
PROMPT_FILE_PATH = os.path.join(CONFIG_DIR, "prompt.md")
LOG_FILE = os.path.join(LOGS_DIR, "process_log.txt")
NEW_TAGS_LOG = os.path.join(LOGS_DIR, "new_tags_log.txt")

# Configure logging to write to log files
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def main():
    """Main entry point to process Obsidian notes."""
    
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Process Obsidian notes with AI-generated YAML metadata.")
    parser.add_argument("--opt1", action="store_true", help="Merge existing YAML with AI-generated YAML.")
    parser.add_argument("--opt2", action="store_true", help="Replace existing YAML with AI-generated YAML.")
    parser.add_argument("--test", action="store_true", help="Run in test mode (bypass OpenAI API).")
    c = parser.parse_args()

    if args.opt1 and args.opt2:
        print("Error: --opt1 and --opt2 cannot be used together.")
        sys.exit(1)

    # Verify configuration files exist
    missing_files = []
    if not os.path.exists(REFERENCE_FILE_PATH):
        missing_files.append(f"Reference file not found: {REFERENCE_FILE_PATH}")
    if not os.path.exists(PROMPT_FILE_PATH):
        missing_files.append(f"Prompt file not found: {PROMPT_FILE_PATH}")
    
    if missing_files:
        for msg in missing_files:
            print(msg)
        sys.exit(1)

    # Load reference content and prompt template
    try:
        reference_content = load_file_content(REFERENCE_FILE_PATH)
        prompt_template = load_file_content(PROMPT_FILE_PATH)
        reference_tags = extract_reference_tags(reference_content)
    except Exception as e:
        print(f"Error loading configuration files: {e}")
        logging.error(f"Error loading configuration files: {e}")
        sys.exit(1)

    # Verify the notes directory exists
    if not os.path.exists(NOTES_DIR):
        print(f"Error: Notes directory not found: {NOTES_DIR}")
        sys.exit(1)

    try:
        # Process folder with test mode flag
        process_folder(NOTES_DIR, reference_content, prompt_template, reference_tags, args.opt1, args.opt2, args.test, LOG_FILE, NEW_TAGS_LOG)
        logging.info("Processing completed successfully.")
        print("Processing completed successfully.")
    except Exception as e:
        logging.error(f"An error occurred during processing: {e}")
        print(f"An error occurred during processing: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
