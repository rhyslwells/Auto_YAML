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

        functions = []
        classes = []
        imports = []
        variables = []

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


# ✅ Process a file and update JSON structure
def process_file(path, json_structure):
    """Processes a Python file and extracts metadata, updating json_structure."""
    if path.endswith(".py"):
        relative_path = os.path.relpath(path, directory).replace("\\", "/")
        json_structure[relative_path] = extract_python_metadata(path)


# ✅ Process directories in the focus list
def process_directory(root_dir, focus_list, json_structure, indent=""):
    """Processes only directories/files listed in Focus.md."""
    tree_str = ""

    for item in sorted(os.listdir(root_dir)):
        path = os.path.join(root_dir, item)
        relative_path = os.path.relpath(path, directory).replace("\\", "/")

        if relative_path in focus_list:
            logging.info(f"📂 Processing folder: {relative_path}" if os.path.isdir(path) else f"📄 Processing file: {relative_path}")
            tree_str += f"{indent}📂 {item}/\n" if os.path.isdir(path) else f"{indent}📄 {item}\n"

            if os.path.isdir(path):
                process_directory(path, focus_list, json_structure, indent + "  ")
            else:
                process_file(path, json_structure)

    return tree_str, json_structure


# ✅ Multi-threaded metadata extraction for faster processing
def process_files_parallel(files):
    """Processes multiple files in parallel to speed up metadata extraction."""
    with ThreadPoolExecutor() as executor:
        executor.map(lambda file: process_file(file, json_structure), files)


# ✅ Set the **root** directory (move one level up from `utils/`)
directory = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
focus_list = load_focus_list(os.path.join(os.path.dirname(__file__), "Focus.md"))

# ✅ Initialize JSON structure using defaultdict for robustness
json_structure = defaultdict(dict)

# ✅ Generate the folder structure and metadata (limited to the focus list)
tree_output, json_output = process_directory(directory, focus_list, json_structure)

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
