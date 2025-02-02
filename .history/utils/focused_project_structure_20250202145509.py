import os
import json
import ast
import time

# Load focus list from Focus.md
def load_focus_list(focus_file):
    """Reads Focus.md and returns a list of files/folders to include."""
    focus_list = set()
    if os.path.exists(focus_file):
        with open(focus_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):  # Ignore comments
                    focus_list.add(line.replace("\\", "/"))  # Normalize paths
    return focus_list

def extract_python_metadata(file_path):
    """Extracts functions, classes, imports, and variables from a Python file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()
        tree = ast.parse(code)
        functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
        imports = [node.module for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)]
        variables = [node.targets[0].id for node in ast.walk(tree) if isinstance(node, ast.Assign)]
        return {"functions": functions, "classes": classes, "imports": imports, "variables": variables}
    except Exception as e:
        return {"error": str(e)}

def extract_json_keys(file_path):
    """Extracts top-level keys from a JSON file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return {"keys": list(data.keys())}
    except Exception as e:
        return {"error": str(e)}

def process_file(path, item, json_structure):
    """Process a file based on its type and update json_structure."""
    if item.endswith(".py"):
        json_structure[item] = extract_python_metadata(path)
    elif item.endswith(".json"):
        json_structure[item] = extract_json_keys(path)
    else:
        json_structure[item] = None  # Non-Python, non-JSON files (e.g., LICENSE, README)

def process_directory(root_dir, focus_list, json_structure, indent="", depth=5):
    """Processes files and directories in the focus list."""
    tree_str = ""
    for item in sorted(os.listdir(root_dir)):
        path = os.path.join(root_dir, item)
        relative_path = os.path.relpath(path, directory).replace("\\", "/")  # Normalize paths

        # ✅ Only include files/folders listed in Focus.md
        if relative_path in focus_list:
            print(f"📂 Processing folder: {item}" if os.path.isdir(path) else f"📄 Processing file: {item}")
            tree_str += f"{indent}📂 {item}/\n" if os.path.isdir(path) else f"{indent}📄 {item}\n"

            if os.path.isdir(path):
                process_directory(path, focus_list, json_structure, indent + "  ")  # Recursively process subdirectory
            else:
                process_file(path, item, json_structure)  # Process the file

    return tree_str, json_structure

# ✅ Set the **root** directory (move one level up from `utils/`)
directory = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
focus_list = load_focus_list(os.path.join(os.path.dirname(__file__), "Focus.md"))

# Initialize json_structure to store the file metadata
json_structure = {}

# Generate the folder structure and metadata (limited to the focus list)
tree_output, json_output = process_directory(directory, focus_list, json_structure)

# ✅ Ensure output files are saved in the `utils` folder
output_folder = os.path.join(os.path.dirname(__file__), "outputs")

# Create utils directory if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# ✅ Write the results to the utils folder
with open(os.path.join(output_folder, "directory_structure.txt"), "w", encoding="utf-8") as f:
    f.write(tree_output if tree_output.strip() else "(No content)\n")

with open(os.path.join(output_folder, "directory_structure.json"), "w", encoding="utf-8") as f:
    json.dump(json_output if json_output else {"message": "No relevant files found"}, f, indent=4)

# Print outputs
print("📁 Folder Structure:\n")
print(tree_output)
print("\n📄 JSON Metadata:\n")
print(json.dumps(json_output, indent=4))
