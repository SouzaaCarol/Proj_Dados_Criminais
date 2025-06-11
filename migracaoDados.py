
# codigo 4 - versão robusta
import pandas as pd
from sqlalchemy import create_engine
import os

# CONFIGURAÇÕES DO BANCO DE DADOS
DB_USER = 'root'
DB_PASSWORD = 'ana0104'
DB_HOST = '127.0.0.1'
DB_PORT = '3306'
DB_NAME = 'dados_criminais2'

# Caminhos dos arquivos Excel
arquivos = [
    'SPDadosCriminais_2024.xlsx',
    'SPDadosCriminais_2025.xlsx'
]

# Conectar ao MySQL
engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# Colunas necessárias (Excel → Banco)
colunas_necessarias = {
    'NUM_BO': 'num_bo',
    'ANO_BO': 'ano_bo',
    'DATA_REGISTRO': 'data_registro',
    'DATA_OCORRENCIA_BO': 'data_ocorrencia',
    'HORA_OCORRENCIA_BO': 'hora_ocorrencia',
    'DESC_PERIODO': 'desc_periodo',
    'NOME_MUNICIPIO': 'nome_municipio',
    'NOME_DEPARTAMENTO': 'nome_departamento',
    'NOME_SECCIONAL': 'nome_seccional',
    'NOME_DELEGACIA': 'nome_delegacia',
    'RUBRICA': 'rubrica',
    'NATUREZA_APURADA': 'natureza_apurada',
    'DESCR_CONDUTA': 'descr_conduta',
    'LATITUDE': 'latitude',
    'LONGITUDE': 'longitude',
     'BAIRRO': 'bairro',
    'DESCR_SUBTIPOLOCAL': 'subtipo_local',
    'LOGRADOURO': 'logradouro',
    'MES_ESTATISTICA': 'mes_estatistica',
    'ANO_ESTATISTICA': 'ano_estatistica',
   
}

# Função para registrar erros em log
def registrar_log(mensagem):
    with open("erros_importacao.log", "a", encoding='utf-8') as f:
        f.write(mensagem + "\n")

# Função para importar todas as abas de uma planilha
def importar_planilha(caminho_arquivo):
    print(f'\n🟨 Importando: {caminho_arquivo}')
    try:
        xls = pd.ExcelFile(caminho_arquivo)
        abas = xls.sheet_names

        for aba in abas:
            print(f'➡️  Lendo aba: {aba}')
            try:
                df = pd.read_excel(xls, sheet_name=aba)

                # Remover espaços dos nomes das colunas
                df.columns = df.columns.str.strip()

                # Preencher colunas ausentes com None
                for coluna in colunas_necessarias.keys():
                    if coluna not in df.columns:
                        print(f"⚠️ Coluna ausente: {coluna} — será preenchida com None.")
                        df[coluna] = None

                # Filtrar e renomear colunas
                df = df[list(colunas_necessarias.keys())].rename(columns=colunas_necessarias)

                # Validar latitude e longitude
                df = df[pd.to_numeric(df['latitude'], errors='coerce').abs() <= 90]
                df = df[pd.to_numeric(df['longitude'], errors='coerce').abs() <= 180]

                # Eliminar registros com campos essenciais faltando
                df = df.dropna(subset=['num_bo', 'data_ocorrencia', 'ano_bo', 'mes_estatistica'])

                # Corrigir tipos 
                df['num_bo'] = df['num_bo'].astype(str)
                df['ano_bo'] = pd.to_numeric(df['ano_bo'], errors='coerce').astype('Int64')
                df['mes_estatistica'] = pd.to_numeric(df['mes_estatistica'], errors='coerce').astype('Int64')

                # Filtrar MES entre 1 e 12
                df = df[df['mes_estatistica'].between(1, 12)]

                # Enviar para o banco em lotes
                df.to_sql('ocorrencias_criminais', con=engine, if_exists='append', index=False, chunksize=10000)
                print(f'✅ Dados importados da aba "{aba}" ({len(df)} registros).\n')

            except Exception as e_aba:
                msg = f'❗ Erro ao importar aba {aba} do arquivo {caminho_arquivo}: {e_aba}'
                print(msg)
                registrar_log(msg)

    except Exception as e:
        msg = f'❗ Erro ao abrir {caminho_arquivo}: {e}'
        print(msg)
        registrar_log(msg)

# Executar importação para todos os arquivos
for arquivo in arquivos:
    if os.path.exists(arquivo):
        importar_planilha(arquivo)
    else:
        print(f'❌ Arquivo não encontrado: {arquivo}')
        registrar_log(f'❌ Arquivo não encontrado: {arquivo}')