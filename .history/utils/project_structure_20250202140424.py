import os
import json
import ast
print("running..")

# Load skip list from Skip.md
def load_skip_list(skip_file):
    """Reads skip.md and returns a list of files/folders to ignore."""
    skip_list = set()
    if os.path.exists(skip_file):
        with open(skip_file, "r", encoding="utf-8") as f:
            skip_list = {line.strip() for line in f if line.strip()}
    return skip_list

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

def build_directory_structure(root_dir, skip_list, indent=""):
    """Generates a tree-like structure and extracts file metadata, skipping specified files/folders."""
    tree_str = ""
    json_structure = {}

    for item in sorted(os.listdir(root_dir)):  # Sort for consistency
        if item in skip_list:
            continue  # skip files/folders listed in skip.md

        path = os.path.join(root_dir, item)

        if os.path.isdir(path):
            sub_tree_str, sub_json = build_directory_structure(path, skip_list, indent + "  ")
            tree_str += f"{indent}📂 {item}/\n" + sub_tree_str
            json_structure[item] = sub_json
        else:
            tree_str += f"{indent}📄 {item}\n"

            if item.endswith(".py"):
                json_structure[item] = extract_python_metadata(path)
            else:
                json_structure[item] = None  # Other file types (Markdown, text)

    return tree_str if tree_str else "(Empty Directory)\n", json_structure

# ✅ Set the **root** directory (move one level up from `utils/`)
directory = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
skip_file = os.path.join(directory, "utils/skip.md")
skip_list = load_skip_list(skip_file)

# Generate the folder structure and metadata
tree_output, json_output = build_directory_structure(directory, skip_list)

# Ensure output files are always created
with open("directory_structure.txt", "w") as f:
    f.write(tree_output if tree_output.strip() else "(Empty Directory)\n")

with open("directory_structure.json", "w") as f:
    json.dump(json_output if json_output else {"message": "No relevant files found"}, f, indent=4)

# Print outputs
print("📁 Folder Structure:\n")
print(tree_output)
print("\n📄 JSON Metadata:\n")
print(json.dumps(json_output, indent=4))
