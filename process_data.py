
import json

def extract_text_from_file(data_folder, file_name):
    base_path = 'Create_Use_Cases/files_to_read'
    file_path = f"{base_path}/{data_folder}/{file_name}"
    if data_folder == "extraction_comparison_use_cases" and file_name == "template.json":
        file_path = f"{base_path}/template.json"
    with open(file_path, 'r') as f:
        if file_name.endswith('.json'):
            return json.load(f)
        else:
            return f.read()

ExtractionAccuracyAnalyzeInputs = {
    "template": extract_text_from_file("extraction_comparison_use_cases", "template.json"),
    "agents_response_to_analyze": extract_text_from_file("extraction_comparison_use_cases", "agents_response.json"),
    "rules_to_follow": extract_text_from_file("extraction_comparison_use_cases", "general_rules.md"),
    "llm": "gemini-1.5-pro"
}

with open("output.txt", "w") as outfile:
    for key, value in ExtractionAccuracyAnalyzeInputs.items():
        outfile.write(f"--- {key} ---\n")
        if isinstance(value, dict):
            for doc_id, content in value.items():
                outfile.write(f"--- Document ID: {doc_id} ---\n")
                outfile.write(json.dumps(content, indent=4))
                outfile.write("\n")
        else:
            outfile.write(value)
        outfile.write("\n" * 2)
