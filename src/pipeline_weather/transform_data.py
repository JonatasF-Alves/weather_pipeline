import pandas as pd
from pathlib import Path
import json

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

path = Path(__file__).parent.parent / 'data' / 'weather_data.json'

def create_dataframe(path_name:str) -> pd.DataFrame:
    logging.info(f"Iniciando a criação do DataFrame a partir do arquivo {path_name}")
    path = path_name
    
    if not path.exists():
        raise FileNotFoundError(f"Arquivo {path} não encontrado.")

    with open(path) as f:
        data = json.load(f)

    df = pd.json_normalize(data)
    logging.info(f"DataFrame criado com {len(df)} linhas.")
    return df

def normalize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df_weather = pd.json_normalize(df['weather'].apply(lambda x: x[0]))

    df_weather = df_weather.rename(columns={
        'id': 'weather_id',
        'main': 'weather_main',
        'description': 'weather_description',
        'icon': 'weather_icon'
    })

    df = pd.concat([df, df_weather], axis=1)
    logging.info(f'\n/ Coluna weather normalizada - {len(df.columns)} colunas.')
    return df

