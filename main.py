from src.pipeline_weather.extract_data import extract_weather_data
from src.pipeline_weather.load_data import load_weather_data
from src.pipeline_weather.transform_data import data_transformation

import os
import logging
from pathlib import Path
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

env_path = Path(__file__).resolve().parent / 'config' / '.env'
load_dotenv(env_path)

API_KEY = os.getenv('API_KEY')

url = f'https://api.openweathermap.org/data/2.5/weather?q=Rio de Janeiro,BR&units=metric&appid={API_KEY}'
table_name = 'rj_weather'


def pipeline():
    try:
        logging.info("ETAPA 1: EXTRACT")
        extract_weather_data(url)

        logging.info("ETAPA 2: TRANSFORM")
        df = data_transformation()

        logging.info("ETAPA 3: LOAD")
        load_weather_data(table_name, df)

        print("\n" + "=" * 60)
        print("✅ Pipeline concluído com sucesso!")
        print("=" * 60)

    except Exception:
        logging.exception("❌ ERRO no Pipeline")


if __name__ == "__main__":
    pipeline()
