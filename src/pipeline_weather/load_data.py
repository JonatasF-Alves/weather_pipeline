import os
import logging
from pathlib import Path
from urllib.parse import quote_plus

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

env_path = Path(__file__).parents[2] / 'config' / '.env'
load_dotenv(env_path)


def get_engine():
    logging.info("Criando engine de conexão com o banco de dados PostgreSQL")
    user = os.environ['DB_USER']
    password = os.environ['DB_PASSWORD']
    database = os.environ['DB_NAME']
    host = os.getenv('DB_HOST', 'localhost')
    return create_engine(
        f"postgresql+psycopg2://{user}:{quote_plus(password)}@{host}/{database}"
    )


def load_weather_data(table_name: str, df):
    engine = get_engine()

    df.to_sql(name=table_name, con=engine, if_exists='append', index=False)
    logging.info(f"Dados carregados com sucesso na tabela {table_name}")

    df_check = pd.read_sql_query(f"SELECT * FROM {table_name} LIMIT 5", con=engine)
    logging.info(f"Verificação dos dados carregados na tabela {table_name}:\n{df_check}")
