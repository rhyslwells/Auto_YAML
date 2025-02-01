# **AUTO_YAML – Obsidian Notes YAML Tagging Automation**  

**AUTO_YAML** automates the process of adding **YAML frontmatter** to your Obsidian notes. It scans notes in a specified folder, checks if they already have `tags` and `category`, and generates missing metadata using **OpenAI's GPT**.  

New tags that are **not in the reference file** are automatically logged for review.  

## **Features**  

✔ **AI-Powered Tagging** – Generates relevant tags based on note content.  
✔ **Selective Processing** – Skips notes that already have `tags` and `category`.  
✔ **New Tag Tracking** – Logs newly introduced tags that aren’t in the reference file.  
✔ **Force Update Mode** – Allows reprocessing all files if needed.  
✔ **Unit Testing** – Includes test coverage for core components.  

## **Contributions**  

Contributions are welcome! Feel free to submit a **pull request** with improvements.  

### **Recent Improvements**
✔ **More logical flow** – From **installation** → **setup** → **usage** → **troubleshooting**.  
✔ **Redundant sections removed** – Avoids repeating API key setup and virtual environment steps.  
✔ **More concise customization instructions**
✔ **Troubleshooting improved** – Covers common issues with clear solutions.  

## **1. Installation & Setup**  

### **1.1. Clone the Repository**  
```bash
git clone https://github.com/rhyslwells/AUTO_YAML.git
cd AUTO_YAML
```

### **1.2. Set Up a Virtual Environment**  
Ensure you’re running commands inside the virtual environment:  
```bash
python -m venv venv
venv\Scripts\activate # macOS/Linux
source venv/Scripts/activate #windows git bash
venv\Scripts\activate  # Windows
```

### **1.3. Install Dependencies**  
```bash
pip install -r requirements.txt
```

## **2. Setting Up OpenAI API Key**  

Your OpenAI API key must be set as an **environment variable** for security.  

```bash
export OPENAI_API_KEY="your-api-key" #Linux/macOS
```

**Windows (Command Prompt)**  
```cmd
setx OPENAI_API_KEY "your-api-key"
```

**"API Key Not Found" Error**:
- Ensure your OpenAI API key is correctly set as an environment variable.  
- Verify with:
  ```bash
  echo $OPENAI_API_KEY  # Linux/macOS
  echo %OPENAI_API_KEY%  # Windows
  ```

You can verify that the API key is set by running:  

- **Linux/macOS:** `echo $OPENAI_API_KEY`  
- **Windows:** `echo %OPENAI_API_KEY%`  

If the key is missing, add it to your **shell profile** (`~/.bashrc`, `~/.zshrc`) for persistence.

## **3. Project Structure**  
```
/AUTO_YAML/
│── /scripts/              # Core Python scripts
│   ├── process_notes.py   # Main script to process notes
│   ├── file_utils.py      # File handling functions
│   ├── tagging.py         # AI-based tag generation
│   ├── logging_utils.py   # Logging utilities
│
│── /tests/                # Unit tests
│   ├── test_file_utils.py
│   ├── test_tagging.py
│   ├── test_logging_utils.py
│
│── /config/               # Configuration files
│   ├── reference.md       # Known tags/categories
│   ├── prompt.md         # AI instruction template
│
│── /notes/                # Markdown notes to process
│── process_log.md        # Log file for processed/skipped notes
│── new_tags_log.md       # Log for newly discovered tags
│── requirements.txt       # Dependencies
│── README.md              # Documentation
```

## **4. Usage**  

To process all notes in your Obsidian folder:  
```bash
python scripts/process_notes.py
```

To force update all notes (even those already tagged):  
```bash
python scripts/process_notes.py --force
```

## **5. Logging & Tracking**  

- `process_log.md` → Logs processed and skipped files.  
- `new_tags_log.md` → Logs any new tags added to files that were not in the reference file.  

## **6. Running Tests**  

This project includes **unit tests** for core modules.  

To run all tests:  
```bash
pytest tests/
```

**Example Output:**  
```
==================== test session starts ====================
collected 7 items

tests/test_file_utils.py ....                             [100%]
tests/test_tagging.py ..                                  [100%]
tests/test_logging_utils.py ..                            [100%]

===================== 7 passed in 0.23s =====================
```

## **7. Customization**  

- **Modify `config/reference.md`** to change predefined tags and categories.  
- **Edit `config/prompt.md`** to fine-tune how AI generates tags.  
- **Update `scripts/tagging.py`** if you want a different tagging strategy.  


## **8. Troubleshooting**  



### **Skipping All Files**  
- If all notes are skipped, they likely already contain `tags` and `category`.  
  Use **force mode** to update all files:  
  ```bash
  python scripts/process_notes.py --force
  ```

## **9. License**  

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

