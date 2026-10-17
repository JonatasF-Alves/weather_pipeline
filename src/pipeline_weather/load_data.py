from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
import os
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

env_path = Path(__file__).parent.parent / 'config' / '.env'
load_dotenv(env_path)

user = os.getenv('user')
password = os.getenv('password')
database = os.getenv('database')
host = 'host.docker.internal'

def create_engine():
    logging.info("Criando engine de conexão com o banco de dados PostgreSQL")
    return create_engine(
        f"postgresql+psycopg2://{user}:{quote_plus(password)}@{host}/{database}"    
    )

engine = get_engine()

def load_data(table_name: str, df):
    df.to_sql(
        name=table_name,
        con=engine,
        if_exists='append',
        index=False
    )

    logging.info(f"Dados carregados com sucesso na tabela {table_name} do banco de dados PostgreSQL")

    df_check = pd.read_sql_query(f"SELECT * FROM {table_name} LIMIT 5", con=engine)
    logging.info(f"Verificação dos dados carregados na tabela {table_name}:\n){df_check}")

    