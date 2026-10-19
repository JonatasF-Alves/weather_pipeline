from datetime import datetime, timedelta
from airflow.decorators import dag, task
from pathlib import Path
import sys, os

sys.path.insert(0, '/opt/airflow/src/pipeline_weather')

from src.pipeline_weather.extract_data import extract_weather_data
from src.pipeline_weather.load_data import load_weather_data
from src.pipeline_weather.transform_data import data_transformation
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent / 'config' / '.env'
load_dotenv(env_path)

API_KEY = os.getenv('API_KEY')
url = f'https://api.openweathermap.org/data/2.5/weather?q=Rio de Janeiro,BR&units=metric&appid={API_KEY}'

@dag(
    dag_id='weather_pipeline',
    default_args={
        'owner': 'airflow',
        'depends_on_past': False,
        'retries': 2,
        'retry_delay': timedelta(minutes=5),
    },
    description='Pipeline de ETL para dados meteorológicos',
    schedule='0 */1 * * *',  # Executa a cada hora
    start_date=datetime(2026, 10, 19),
    catchup=False,
)
def weather_pipeline():
    @task
    def extract():
        extract_weather_data(url)

    @task
    def transform():
        df = data_transformation()
        df.to_parquet('data/weather_data.parquet', index=False)

    @task
    def load():
        import pandas as pd
        df = pd.read_parquet('data/weather_data.parquet')
        load_weather_data('rj_weather', df)

    extract() >> transform() >> load()

weather_pipeline()