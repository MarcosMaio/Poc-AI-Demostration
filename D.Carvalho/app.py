import logging
import os
import json
from agents import Agents
from helpers import (
    create_database,
    create_table_from_excel,
    clean_agent_output
)


logger = logging.getLogger("poc_presentations")


def main() -> None:
    """
    Função principal do script.
    """
    db_name = "database.db"
    
    create_database(db_name)
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    tablets_path = os.path.join(BASE_DIR, "tables_data_files")
    for file in os.listdir(tablets_path):
        if file.endswith(".xlsx"):
            create_table_from_excel(db_name, os.path.join(tablets_path, file))

if __name__ == "__main__":
    main()

