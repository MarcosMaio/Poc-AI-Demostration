import json
import re
import pymupdf4llm
import os
import glob
from crewai import LLM
import os
import pandas as pd
import json

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
    source_dir = "files_to_read"
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
    
def initialize_llm(model_name, api_key, config):
    if not model_name or not api_key:
        raise ValueError("Both model_name and api_key must be provided.")
    if not config:
        raise ValueError("config must be provided.")
    return LLM(model=model_name, api_key=api_key, temperature=config["temperature"], top_p=config["top_p"] if model_name < "o3-2025-04-16" else None)

def extract_text_from_file(data_folder, file_name):
    """
    This function extracts text from a file (either Excel, JSON or Markdown) located in a specified folder.

    Args:
        data_folder (str): The name of the folder inside 'files_to_read' where the file is located.
        file_name (str): The name of the file (including extension) to extract text from.

    Returns:
        str: The extracted text from the file.
    """
    base_path = 'files_to_read'
    file_path = os.path.join(base_path, data_folder, file_name)

    if not os.path.exists(file_path):
        return "Error: File not found at the specified path."

    _, file_extension = os.path.splitext(file_name)

    if file_extension == '.xlsx':
        try:
            df = pd.read_excel(file_path)
            return df.to_string()
        except Exception as e:
            return f"Error reading Excel file: {e}"
    elif file_extension == '.json':
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                return json.dumps(data, indent=4)
        except Exception as e:
            return f"Error reading JSON file: {e}"
    elif file_extension == '.md':
        try:
            with open(file_path, 'r') as f:
                return f.read()
        except Exception as e:
            return f"Error reading Markdown file: {e}"
    else:
        return "Error: Unsupported file type. Please use an Excel (.xlsx), JSON (.json) or Markdown (.md) file."

