import os
import sqlite3
import json
import re
from pathlib import Path
import pandas as pd

def create_database(db_path: str) -> None:
    """
    Cria um banco de dados SQLite no caminho especificado, caso não exista.
    """
    if not os.path.exists(db_path):
        try:
            conn = sqlite3.connect(db_path)
            conn.close()
            print(f"Banco de dados '{db_path}' criado.")
        except Exception as e:
            print(f"Erro ao criar o banco de dados: {e}")
    else:
        print(f"Banco de dados '{db_path}' já existe.")

def create_table_from_excel(db_path: str, excel_file: str) -> None:
    """
    Lê um arquivo Excel e cria/atualiza uma tabela no banco de dados SQLite.
    """
    if not os.path.exists(db_path):
        print(f"O banco de dados '{db_path}' não existe.")
        return
    try:
        base_name = os.path.basename(excel_file)
        table_name, _ = os.path.splitext(base_name)
        table_name = table_name.lower().replace(" ", "_")
    except Exception as e:
        print(f"Erro ao criar o nome da tabela: {e}")
        return

    try:
        df = pd.read_excel(excel_file)
        df.columns = df.columns.str.replace(r"[+/\s]+", "_", regex=True)
        df.columns = df.columns.str.lower()

        for col in df.columns:
            if col.startswith("data"):
                try:
                    df[col] = pd.to_datetime(df[col], dayfirst=True, errors='coerce')
                except Exception as e:
                    print(f"Não foi possível converter a coluna {col} para datetime: {e}")

        dtype_mapping = {}
        for col in df.columns:
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                dtype_mapping[col] = "DATETIME"
            elif pd.api.types.is_integer_dtype(df[col]):
                dtype_mapping[col] = "INTEGER"
            elif pd.api.types.is_float_dtype(df[col]):
                dtype_mapping[col] = "REAL"
            else:
                dtype_mapping[col] = "TEXT"

        conn = sqlite3.connect(db_path)
        df.to_sql(table_name, conn, if_exists="replace", index=False, dtype=dtype_mapping)
        conn.close()
        print(f"Tabela '{table_name}' criada no banco de dados '{db_path}'.")
    except Exception as e:
        print(f"Erro ao criar a tabela: {e}")

def process_excel_tables(db_path: str, tables_dir: Path) -> None:
    """
    Encontra todos os arquivos .xlsx em tables_dir e cria/atualiza as tabelas
    no banco de dados apontado por db_path.
    """
    for excel_file in tables_dir.glob("*.xlsx"):
        create_table_from_excel(db_path, str(excel_file))
    
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

