import pandas as pd
from pathlib import Path
import json

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

path = Path(__file__).parent.parent / 'data' / 'weather_data.json'
columns_names_to_drop = ['weather', 'weather_icon', 'sys.type']
dict_columns_names_to_rename = {
            "base": "base",
            "visibility": "visibility",
            "dt": "datetime",
            "timezone": "timezone",
            "id": "city_id",
            "name": "city_name",
            "cod": "code",
            "coord.lon": "longitude",
            "coord.lat": "latitude",
            "main.temp": "temperature",
            "main.feels_like": "feels_like",
            "main.temp_min": "temp_min",
            "main.temp_max": "temp_max",
            "main.pressure": "pressure",
            "main.humidity": "humidity",
            "main.sea_level": "sea_level",
            "main.grnd_level": "grnd_level",
            "mind.speed": "wind_speed",
            "wind.deg": "wind_deg",
            "wind.gust": "wind_gust",
            "clouds.all": "clouds",
            "sys.type": "sys_type",
            "sys.id": "sys_id",
            "sys.country": "country",
            "sys.sunrise": "sunrise",
            "sys.sunset": "sunset",
            #weather_id, weather_main, weather_description
}
columns_names_to_normalize = ['datetime', 'sunrise', 'sunset']

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

def drop_columns(df: pd.DataFrame, columns_names:list[str]) -> pd.DataFrame:
    logging.info(f'\n/ Removendo colunas: {columns_names}')
    df = df.drop(columns=columns_names)
    logging.info(f'\n/ Colunas removidas: {columns_names} - {len(df.columns)} colunas restantes.')
    return df

def rename_columns(df: pd.DataFrame, columns_names:dict[str, str]) -> pd.DataFrame:
    logging.info(f'\n/ Renomeando colunas: {columns_names}')
    df = df.rename(columns=columns_names)
    logging.info(f'\n/ Colunas renomeadas: {columns_names} - {len(df.columns)} colunas restantes.')
    return df

def normalize_datetime_columns(df: pd.DataFrame, columns_names: list[str]) -> pd.DataFrame:
    logging.info(f'\n/ Normalizando colunas datetime: {columns_names}')
    for name in columns_names:
        df[name] = pd.to_datetime(df[name], unit='s', utc=True).dt.tz_convert('America/Rio_de_Janeiro')
        logging.info(f'\n/ Coluna {name} normalizada para datetime.')
        return df

def data_transformation():
    print('\n/ Iniciando a transformação')
    df = create_dataframe(path)
    df = normalize_dataframe(df)
    df = drop_columns(df, columns_names_to_drop)
    df = rename_columns(df, dict_columns_names_to_rename)
    df = normalize_datetime_columns(df, columns_names_to_normalize)
    logging.info(f'\n/ DataFrame final com {len(df)} linhas e {len(df.columns)} colunas.')
    return df