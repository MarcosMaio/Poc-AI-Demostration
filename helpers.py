import json
import re
import pymupdf4llm
import os
import glob

def clean_agent_output(value):
    pattern = r'```json\s*([\s\S]+?)```'
    match = re.search(pattern, value)
    
    if match:
        json_str = match.group(1).strip()
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            pass
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return value

def extract_text_from_pdf(file_path):
    return pymupdf4llm.to_markdown(file_path)

def process_file():
    source_dir = "file_to_read"
    target_dir = os.path.join("knowledge", "data", "file")
    
    source_files = glob.glob(os.path.join(source_dir, "*"))
    if not source_files:
        raise FileNotFoundError(f"No files found in {source_dir}")
    
    pdf_file = source_files[0]
    
    markdown_text = extract_text_from_pdf(pdf_file)
    
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    
    target_files = glob.glob(os.path.join(target_dir, "*"))
    for existing_file in target_files:
        os.remove(existing_file)

    target_file = os.path.join(target_dir, "search_source.md")

    with open(target_file, "w", encoding="utf-8") as f:
        f.write(markdown_text)
    
    print(f"Processed '{pdf_file}' and saved markdown to '{target_file}'.")
    
    
def get_detailed_instructions_from_file():
    file_path = os.path.join("detailed_instructions", "detailed_instructions.md")
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()
    
def get_doc_content_from_file():
    file_path = os.path.join("knowledge", "data", "file", "search_source.md")
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()