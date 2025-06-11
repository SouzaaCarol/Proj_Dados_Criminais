import streamlit as st
import pandas as pd
from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import plotly.express as px
from database.conexao import carregar_dados

# Configuração da Página
st.set_page_config(page_title="Segurança em Foco: Painel Cidadão", layout="wide")
st.title("🔍 Painel de Ocorrências para Cidadãos e Jornalistas")
st.markdown("""
Este painel foi criado para **informar a população** e **apoiar jornalistas** com dados atualizados de ocorrências policiais.
Você pode **explorar os dados por ano, bairro, tipo de crime e período do ano**.

ℹ️ *Fonte: Base oficial de registros policiais.*
""")

# 1. Carregando os dados
df = carregar_dados()

# 2. Filtro de ano
anos_disponiveis = sorted(df['ano_estatistica'].dropna().unique())
anos_selecionados = st.multiselect("📅 Selecione o(s) ano(s) para visualizar os dados:", anos_disponiveis, default=anos_disponiveis)

df = df[df['ano_estatistica'].isin(anos_selecionados)]
if df.empty:
    st.warning("⚠️ Nenhum dado encontrado para os anos selecionados.")
    st.stop()

# 3. Indicadores gerais
total = len(df)
bairro_top = df['bairro'].value_counts().idxmax()
tipo_top = df['natureza_apurada'].value_counts().idxmax()

st.markdown("## 📊 Indicadores Gerais de Ocorrências")
col1, col2, col3 = st.columns(3)
col1.metric("Número Total de Ocorrências", total)
col2.metric("Bairro com Mais Ocorrências", bairro_top)
col3.metric("Crime Mais Comum", tipo_top)

# 4. Gráfico de Ocorrências por Dia da Semana
st.markdown("## 📅 Ocorrências por Dia da Semana")

# Garante que a coluna de data esteja no formato datetime
df['data_ocorrencia'] = pd.to_datetime(df['data_ocorrencia'], errors='coerce')

# Extrai o dia da semana
df['dia_semana'] = df['data_ocorrencia'].dt.day_name()

# Traduz os dias da semana para português (opcional)
traducao_dias = {
    'Monday': 'Segunda-feira',
    'Tuesday': 'Terça-feira',
    'Wednesday': 'Quarta-feira',
    'Thursday': 'Quinta-feira',
    'Friday': 'Sexta-feira',
    'Saturday': 'Sábado',
    'Sunday': 'Domingo'
}
df['dia_semana'] = df['dia_semana'].map(traducao_dias)

# Ordena os dias corretamente
ordem_dias = ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira',
              'Sexta-feira', 'Sábado', 'Domingo']

ocorrencias_dia = df['dia_semana'].value_counts().reindex(ordem_dias)

fig_dia_semana = px.bar(
    x=ocorrencias_dia.index,
    y=ocorrencias_dia.values,
    labels={'x': 'Dia da Semana', 'y': 'Quantidade de Ocorrências'},
    color=ocorrencias_dia.values,
    color_continuous_scale='Reds',
    title='Distribuição de Ocorrências por Dia da Semana'
)
st.plotly_chart(fig_dia_semana, use_container_width=True)

# 7. Análise de Bairros
st.subheader("📍 Análise de Bairros com Mais Ocorrências")
top_bairros = df['bairro'].value_counts().head(10)
bairro_escolhido = st.selectbox("Selecione um Bairro para análise:", top_bairros.index)

# 8. Tipos de Crimes no Bairro
st.write(f"Analisando o bairro **{bairro_escolhido}**:")
df_bairro = df[df['bairro'] == bairro_escolhido]
tipos_bairro = df_bairro['natureza_apurada'].value_counts().head(10)

fig_bairro = px.bar(x=tipos_bairro.index, y=tipos_bairro.values, labels={'x': 'Tipo de Crime', 'y': 'Total de Crimes'}, title=f"Tipos de Crimes em {bairro_escolhido}")
fig_bairro.update_layout(title_x=0.5)
st.plotly_chart(fig_bairro)

# 10. Tendências: Épocas do Ano com Maior Criminalidade
st.subheader("Tendências: Épocas do Ano com Maior Incidência de Criminalidade")

# Caixa para escolher crime
crime_escolhido = st.selectbox("Selecione o tipo de crime para a análise sazonal:", df['natureza_apurada'].unique())

df_crime = df[df['natureza_apurada'] == crime_escolhido]
sazonalidade = df_crime.groupby('mes_estatistica').size().reset_index(name='total_crimes')
meses_nomes = {1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril', 5: 'Maio', 6: 'Junho',
               7: 'Julho', 8: 'Agosto', 9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'}
sazonalidade['mes_nome'] = sazonalidade['mes_estatistica'].map(meses_nomes)

fig_sazonalidade = px.bar(sazonalidade, x='mes_nome', y='total_crimes', title="Incidência de Criminalidade nas Épocas do Ano", labels={'mes_nome': 'Mês', 'total_crimes': 'Total de Crimes'})
fig_sazonalidade.update_layout(title_x=0.5)
st.plotly_chart(fig_sazonalidade)

mes_top = sazonalidade.sort_values(by='total_crimes', ascending=False).iloc[0]
st.info(f"No mês de {mes_top['mes_nome']} observou-se o maior número de crimes ({mes_top['total_crimes']} casos) para o tipo de crime: {crime_escolhido}.")
