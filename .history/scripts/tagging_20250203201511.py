import openai
import yaml
import os
from file_utils import extract_yaml_header
from file_utils import extract_yaml_header


openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_reference_tags(reference_content):
    """Extract tags from the reference file."""
    ref_metadata, _ = extract_yaml_header(reference_content)
    return set(ref_metadata.get("tags", [])) if ref_metadata else set()

def generate_tags_and_categories(content, reference_content, prompt_template):
    """Generate tags and categories using OpenAI based on reference context."""
    prompt = prompt_template.format(reference=reference_content, target_content=content)
    
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[{"role": "system", "content": "You categorize notes using a provided reference."},
                  {"role": "user", "content": prompt}]
    )
    
    return yaml.safe_load(response["choices"][0]["message"]["content"].strip())

def identify_new_tags(generated_tags, reference_tags):
    """Identify new tags that are not present in the reference file."""
    return set(generated_tags) - reference_tags
