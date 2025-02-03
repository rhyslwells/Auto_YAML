import openai
import yaml
import os
from scripts.file_utils import extract_yaml_header

openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_reference_tags(reference_content):
    """Extract tags from the reference file."""
    ref_metadata, _ = extract_yaml_header(reference_content)
    return set(ref_metadata.get("tags", [])) if ref_metadata else set()

def generate_yaml_header(content, reference_content, prompt_template, use_trial=False):
    """Generate YAML header using OpenAI based on reference context, or return a trial header."""
    
    if use_trial:
        # Return a trial example header without calling OpenAI
        return {
            "tags": ["AI", "Machine Learning", "Deep Learning"],
            "aliases": ["ML Model", "AI Model"],
            "category": "Technology",
            "phase": "Model Training",
            "topic": "Neural Networks",
            "filename": "neural_network_model.py"
        }

    # If not using the trial header, generate using OpenAI
    prompt = prompt_template.format(reference=reference_content, target_content=content)
    
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[{"role": "system", "content": "You categorize notes using a provided reference."},
                  {"role": "user", "content": prompt}]
    )
    
    # Parse and return the generated YAML
    return yaml.safe_load(response["choices"][0]["message"]["content"].strip())

def identify_new_tags(generated_tags, reference_tags):
    """Identify new tags that are not present in the reference file."""
    return set(generated_tags) - reference_tags
