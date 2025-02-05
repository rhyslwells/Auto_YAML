"""
This script scans a project directory, extracts metadata from files, and outputs a structured view of the project’s directory and metadata. 
It reads the `focus.md` file to determine which files and directories to include in the process. The script processes files listed within the folders specified in 
`focus.md` and generates both a visual directory structure and metadata for Python and JSON files.### Key Features:
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

Need to also get files in main dir
"""

import os
import json
import ast
import logging
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

# ✅ Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# ✅ Load focus list from Focus.md
def load_focus_list(focus_file):
    """Reads Focus.md and returns a set of focused files/folders."""
    focus_list = set()
    if os.path.exists(focus_file):
        with open(focus_file, "r", encoding="utf-8") as f:
            focus_list = {line.strip().replace("\\", "/") for line in f if line.strip() and not line.startswith("#")}
    return focus_list

# ✅ Extract Python metadata (functions, classes, imports, variables)
def extract_python_metadata(file_path):
    """Extracts functions, classes, imports, and variables from a Python file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()
        tree = ast.parse(code)

        functions, classes, imports, variables = [], [], [], []

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions.append({
                    "name": node.name,
                    "args": [arg.arg for arg in node.args.args],
                    "docstring": ast.get_docstring(node),
                    "decorators": [d.id for d in node.decorator_list if isinstance(d, ast.Name)]
                })
            elif isinstance(node, ast.ClassDef):
                classes.append({
                    "name": node.name,
                    "docstring": ast.get_docstring(node)
                })
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.append(node.module)
            elif isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name):
                variables.append(node.targets[0].id)

        return {"functions": functions, "classes": classes, "imports": imports, "variables": variables}
    except Exception as e:
        return {"error": str(e)}

# ✅ Process a Python file and store metadata
def process_file(file_path, json_structure, tree_list, indent):
    """Processes a Python file, extracts metadata, and updates the JSON structure."""
    relative_path = os.path.relpath(file_path, directory).replace("\\", "/")
    directory_key = os.path.dirname(relative_path)

    # ✅ Ensure directory key exists
    if directory_key not in json_structure:
        json_structure[directory_key] = {}

    # ✅ Extract Python metadata and store it
    json_structure[directory_key][os.path.basename(file_path)] = extract_python_metadata(file_path)

    # ✅ Add to directory structure output **(Only if not duplicate)**
    if f"{indent}📄 {os.path.basename(file_path)}" not in tree_list:
        tree_list.append(f"{indent}📄 {os.path.basename(file_path)}")

# ✅ Process directories from the focus list
def process_directory(root_dir, focus_list, json_structure, tree_list, indent=""):
    """Processes only directories and files explicitly listed in Focus.md."""
    for item in sorted(os.listdir(root_dir)):
        path = os.path.join(root_dir, item)
        relative_path = os.path.relpath(path, directory).replace("\\", "/")

        # 🚫 **Skip `__pycache__` directories**
        if "__pycache__" in relative_path:
            logging.info(f"🚫 Skipping: {relative_path} (Cache folder)")
            continue

        # ✅ Process only if inside a focused directory
        if any(relative_path.startswith(focus) for focus in focus_list):
            logging.info(f"📂 Processing folder: {relative_path}" if os.path.isdir(path) else f"📄 Processing file: {relative_path}")

            # ✅ Add folder to directory structure output **(Only if not duplicate)**
            if os.path.isdir(path):
                if f"{indent}📂 {item}/" not in tree_list:
                    tree_list.append(f"{indent}📂 {item}/")
                process_directory(path, focus_list, json_structure, tree_list, indent + "  ")
            elif path.endswith(".py"):
                process_file(path, json_structure, tree_list, indent)

    return "\n".join(tree_list), json_structure

# ✅ Multi-threaded metadata extraction for faster processing
def process_files_parallel(files):
    """Processes multiple files in parallel to speed up metadata extraction."""
    with ThreadPoolExecutor() as executor:
        executor.map(lambda file: process_file(file, json_structure, tree_list, ""), files)

# ✅ Set the **root** directory (move one level up from `utils/`)
directory = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
focus_list = load_focus_list(os.path.join(os.path.dirname(__file__), "Focus.md"))

# ✅ Initialize JSON structure using defaultdict for robustness
json_structure = defaultdict(dict)
tree_list = []

# ✅ Generate the folder structure and metadata (limited to the focus list)
tree_output, json_output = process_directory(directory, focus_list, json_structure, tree_list)

# ✅ Ensure output files are saved in the `utils/outputs/` folder
output_folder = os.path.join(directory, "utils", "outputs")
os.makedirs(output_folder, exist_ok=True)

# ✅ Write the results using buffered writing for efficiency
with open(os.path.join(output_folder, "directory_structure.txt"), "w", encoding="utf-8") as f:
    f.write(tree_output if tree_output.strip() else "(No content)\n")

with open(os.path.join(output_folder, "directory_structure.json"), "w", encoding="utf-8") as f:
    json.dump(json_output if json_output else {"message": "No relevant files found"}, f, indent=4)

# ✅ Logging final results
logging.info("📁 Folder Structure:\n" + tree_output)
logging.info("📄 JSON Metadata:\n" + json.dumps(json_output, indent=4))
