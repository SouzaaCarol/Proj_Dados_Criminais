from sqlalchemy import create_engine
import pandas as pd

def carregar_dados():
    DB_USER = 'root'
    DB_PASSWORD = 'ana0104'
    DB_HOST = '127.0.0.1'
    DB_PORT = '3306'
    DB_NAME = 'dados_criminais2'

    engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

    query = """
        SELECT 
            ano_estatistica, 
            mes_estatistica, 
            bairro, 
            natureza_apurada, 
            latitude, 
            longitude,
            subtipo_local,
            data_ocorrencia          
        FROM ocorrencias_criminais
    """

    df = pd.read_sql(query, con=engine)
    return df
