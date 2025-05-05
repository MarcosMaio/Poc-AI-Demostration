import json
import re


def clean_agent_output(value):
    """
    Limpa a saída do agente, que pode conter trechos de código JSON.
    """
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

