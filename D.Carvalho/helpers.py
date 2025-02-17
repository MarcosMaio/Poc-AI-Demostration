import os
import sqlite3
import pandas as pd
import json
import re
from crewai.knowledge.source.base_knowledge_source import BaseKnowledgeSource
import sqlalchemy
from typing import Any

def create_database(db_path):
    """
    Cria o banco de dados SQLite se ele ainda não existir.
    
    Parâmetros:
      db_path (str): Caminho/nome do arquivo do banco de dados.
    """
    if not os.path.exists(db_path):
        try:
            conn = sqlite3.connect(db_path)
            conn.close()
            print(f"Banco de dados '{db_path}' criado.")
        except Exception as e:
            print(f"Erro ao criar o banco de dados: {e}")
            return

def create_table_from_excel(db_path, excel_file):
    """
    Lê o arquivo Excel e cria uma tabela no banco de dados SQLite.
    O nome da tabela é derivado do nome do arquivo Excel: 
    convertido para minúsculas e com espaços substituídos por "_".
    
    Parâmetros:
      db_path (str): Caminho/nome do arquivo do banco de dados.
      excel_file (str): Caminho/nome do arquivo Excel a ser importado.
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
        conn = sqlite3.connect(db_path)
        df.to_sql(table_name, conn, if_exists="replace", index=False)
        conn.close()
        print(f"Tabela '{table_name}' criada no banco de dados '{db_path}'.")
    except Exception as e:
        print(f"Erro ao criar a tabela: {e}")
        return
    
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

