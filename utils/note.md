"""
This script scans a project directory, extracts metadata from files, and outputs a structured view of the project’s directory and metadata. 
It reads the `focus.md` file to determine which files and directories to include in the process. The script processes files listed within the folders specified in 
`focus.md` and generates both a visual directory structure and metadata for Python and JSON files.

### Key Features:
1. **Focus List**: Reads the `focus.md` file to identify which folders and files to include. Only the contents of the directories listed in the `focus.md` file will be processed.
   
2. **Metadata Extraction**:
   - For Python files (`.py`): Extracts functions, classes, variables, and imports.
   - For JSON files (`.json`): Extracts the top-level keys of the JSON file.

3. **Recursive Directory Traversal**: The script traverses the directory tree recursively, including all subdirectories inside those listed in the `focus.md` file.

4. **Output**:
   - A text file (`directory_structure.txt`) that visually represents the project directory structure.
   - A JSON file (`directory_structure.json`) containing metadata about the files and folders that were processed.

6. **Performance**: The script logs the time taken to process files and raises warnings for files that take longer than expected.

### Usage:
- Place the script in a project directory.
- Make sure to include a `focus.md` file in the same directory or adjust the file path to match your project structure.
- Run the script, and the results will be saved in the `utils/outputs` directory.

### `focus.md` Example:
"""