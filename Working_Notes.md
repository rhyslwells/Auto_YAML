# running tests:
pytest tests/

python -m pytest

# Creating .gitignore and editing 
```bash
touch .gitignore
nano .gitignore  # or use any text editor
```

# Test cases
Look at test_notes and compare the predicited YAML headers against ones that i have generated in the past.

# updating requirements.txt
pip freeze > requirements.txt
pip install -r requirements.txt

# docs
pdoc -o docs ./scripts



# Useage
Run normally (uses OpenAI)
python main.py

Run in test mode (bypasses OpenAI)
python main.py --test

Run with merging (--opt1) in test mode
python main.py --opt1 --test

Run with replacement (--opt2) in test mode
python main.py --opt2 --test

# running scripts

2. Run the Script from the Project Root
Navigate to Auto_YAML/ before running your script:

cd C:\Users\RhysL\Desktop\Auto_YAML
venv\Scripts\activate  # Activate the virtual environment (if using venv)
python -m scripts.tagging  # Run with the module path

This ensures Python treats scripts/ as a package.

I dont know why new_tags are not being recorded in logs\new_tags_log.txt

How to use vscode debug.

For merge yamls do we need to have it specific to what format i have given? doubt it.




