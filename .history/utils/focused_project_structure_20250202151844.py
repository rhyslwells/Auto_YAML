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

def build_directory_structure(root_dir, focus_list, indent="", depth=5):
    """Generates a tree-like structure and extracts file metadata, considering only files/folders in focus_list."""
    print(f"🔍 Entering: {root_dir}")  # Log entry into each directory
    start_time = time.time()

    tree_str = ""
    json_structure = {}

    try:
        for item in sorted(os.listdir(root_dir)):
            path = os.path.join(root_dir, item)
            relative_path = os.path.relpath(path, directory).replace("\\", "/")  # Normalize paths

            # ✅ Only process files and folders listed in the focus_list
            if relative_path not in focus_list:
                print(f"🚫 Skipping: {relative_path}")  # Debugging
                continue

            if os.path.isdir(path):
                # Special handling for __pycache__ in any subfolder
                if "__pycache__" in relative_path:
                    print(f"🚫 Skipping __pycache__ in {relative_path}")
                    continue

                if depth == 0:
                    tree_str += f"{indent}📂 {item}/...\n"
                    json_structure[item] = "(Skipped deeper folders)"
                    continue

                print(f"📂 Processing folder: {item}")
                sub_tree_str, sub_json = build_directory_structure(path, focus_list, indent + "  ", depth - 1)
                if sub_tree_str.strip():  # Only add if the folder contains valid content
                    tree_str += f"{indent}📂 {item}/\n" + sub_tree_str
                    json_structure[item] = sub_json
            else:
                print(f"📄 Processing file: {item}")
                tree_str += f"{indent}📄 {item}\n"

                file_start_time = time.time()
                if item.endswith(".py"):
                    json_structure[item] = extract_python_metadata(path)
                elif item.endswith(".json"):
                    json_structure[item] = extract_json_keys(path)
                else:
                    json_structure[item] = None  # Other file types
                
                elapsed = time.time() - file_start_time
                if elapsed > 5:  # Flag files taking too long
                    print(f"⚠️ Warning: {item} took {elapsed:.2f}s to process")

    except Exception as e:
        print(f"❌ Error processing {root_dir}: {e}")

    elapsed_time = time.time() - start_time
    print(f"🔙 Exiting: {root_dir} (Took {elapsed_time:.2f}s)")

    return tree_str if tree_str else "", json_structure  # Ensure empty directories are not added

# ✅ Set the **root** directory (move one level up from `utils/`)
directory = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
focus_list = load_focus_list(os.path.join(os.path.dirname(__file__), "focus.md"))

# Generate the folder structure and metadata
tree_output, json_output = build_directory_structure(directory, focus_list)

# ✅ Fix: Write files using UTF-8 to prevent Unicode errors
output_dir = os.path.join(directory, "utils", "outputs")  # Saving to utils/outputs
os.makedirs(output_dir, exist_ok=True)  # Create the output directory if it doesn't exist

# Save text output
with open(os.path.join(output_dir, "directory_structure.txt"), "w", encoding="utf-8") as f:
    f.write(tree_output if tree_output.strip() else "(No content)\n")

# Save JSON output
with open(os.path.join(output_dir, "directory_structure.json"), "w", encoding="utf-8") as f:
    json.dump(json_output if json_output else {"message": "No relevant files found"}, f, indent=4)

# Print outputs
print("📁 Folder Structure:\n")
print(tree_output)
print("\n📄 JSON Metadata:\n")
print(json.dumps(json_output, indent=4))
