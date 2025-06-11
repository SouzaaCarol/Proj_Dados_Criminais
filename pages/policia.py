
import streamlit as st
import pandas as pd
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import base64
import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO
from datetime import datetime 
import plotly.express as px
from database.conexao import carregar_dados

st.set_page_config(page_title="Análise Criminal Interativa", layout="wide")
st.title("👮‍♀️ Dashboard de Segurança Pública")

# 1. Carregar dados
df = carregar_dados()

# 2. Filtro de ano
anos_disponiveis = sorted(df['ano_estatistica'].dropna().unique())
anos_selecionados = st.multiselect("Selecione o(s) ano(s) para análise:", anos_disponiveis, default=anos_disponiveis)

df = df[df['ano_estatistica'].isin(anos_selecionados)]
if df.empty:
    st.warning("⚠️ Nenhum dado encontrado para os anos selecionados.")
    st.stop()

# 3. Indicadores rápidos
total = len(df)
bairro_top = df['bairro'].value_counts().idxmax()
tipo_top = df['natureza_apurada'].value_counts().idxmax()

st.markdown("### 📌 Indicadores Gerais")
col1, col2, col3 = st.columns(3)
col1.metric("Total de Ocorrências", total)
col2.metric("Bairro com Mais Casos", bairro_top)
col3.metric("Natureza Mais Comum", tipo_top)

# 4. Tendência Mensal de Crimes
st.subheader("📈 Tendência Mensal de Crimes")
tendencia = df.groupby(['ano_estatistica', 'mes_estatistica']).size().reset_index(name='total_crimes')
tendencia['data'] = pd.to_datetime(tendencia['ano_estatistica'].astype(str) + '-' + tendencia['mes_estatistica'].astype(str) + '-01')

fig_tendencia = px.line(tendencia, x='data', y='total_crimes', color='ano_estatistica', title="Tendência de Crimes por Mês")
fig_tendencia.update_layout(title_x=0.5)
st.plotly_chart(fig_tendencia)

# 5. Ocorrências por Dia da Semana
st.subheader("🗕️ Ocorrências por Dia da Semana")
# Após criar a coluna 'dia_semana'
df['dia_semana'] = pd.to_datetime(df['data_ocorrencia'], errors='coerce').dt.day_name()

# Dicionário de tradução
traducao_dias = {
    'Monday': 'Segunda',
    'Tuesday': 'Terça',
    'Wednesday': 'Quarta',
    'Thursday': 'Quinta',
    'Friday': 'Sexta',
    'Saturday': 'Sábado',
    'Sunday': 'Domingo'
}

# Traduzir
df['dia_semana_pt'] = df['dia_semana'].map(traducao_dias)

# Ordenar dias da semana em português
dias_ordenados_pt = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
crimes_por_dia = df['dia_semana_pt'].value_counts().reindex(dias_ordenados_pt).fillna(0)

# Gráfico
fig_dia = px.bar(x=crimes_por_dia.index, y=crimes_por_dia.values,
                 labels={'x': 'Dia da Semana', 'y': 'Número de Crimes'},
                 title="Ocorrências por Dia da Semana")
fig_dia.update_layout(title_x=0.5)
st.plotly_chart(fig_dia)



st.subheader("📅 Crimes Mais Comuns por Dia da Semana")

# Traduzir dias da semana
df['dia_semana'] = pd.to_datetime(df['data_ocorrencia'], errors='coerce').dt.day_name()
dias_traduzidos = {
    'Monday': 'Segunda',
    'Tuesday': 'Terça',
    'Wednesday': 'Quarta',
    'Thursday': 'Quinta',
    'Friday': 'Sexta',
    'Saturday': 'Sábado',
    'Sunday': 'Domingo'
}
df['dia_semana_pt'] = df['dia_semana'].map(dias_traduzidos)

# Top 5 crimes mais comuns
top_crimes = df['natureza_apurada'].value_counts().head(5).index
df_top_crimes = df[df['natureza_apurada'].isin(top_crimes)]

# Agrupar por crime e dia da semana
agrupado = df_top_crimes.groupby(['natureza_apurada', 'dia_semana_pt']).size().reset_index(name='total')

# Garantir a ordem dos dias
dias_ordenados = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
agrupado['dia_semana_pt'] = pd.Categorical(agrupado['dia_semana_pt'], categories=dias_ordenados, ordered=True)
agrupado = agrupado.sort_values(by='dia_semana_pt')

# Gráfico de barras agrupadas
fig_crimes_dia = px.bar(
    agrupado,
    x='dia_semana_pt',
    y='total',
    color='natureza_apurada',
    labels={'dia_semana_pt': 'Dia da Semana', 'total': 'Número de Crimes', 'natureza_apurada': 'Tipo de Crime'},
    title="Crimes Mais Comuns por Dia da Semana",
    barmode='group'
)
fig_crimes_dia.update_layout(title_x=0.5)
st.plotly_chart(fig_crimes_dia)

# 9. Crimes por Tipo e Local
# 9. Crimes por Tipo e Local
st.subheader("🧐 Crimes por Tipo e Local")

# Caixa para selecionar tipo de local
local_selecionado = st.selectbox("Escolha o tipo de local para análise:", df['subtipo_local'].unique())

# Filtrar os dados conforme o tipo de local selecionado
df_local = df[df['subtipo_local'] == local_selecionado].groupby('natureza_apurada').size().reset_index(name='total_crimes')

# Verificar se há dados para o local selecionado
if df_local.empty:
    st.warning(f"⚠️ Não foram encontrados dados para o local **{local_selecionado}**.")
else:
    # Gráfico de barras com o total de crimes por tipo
    fig_local = px.bar(df_local, 
                       x='natureza_apurada', 
                       y='total_crimes', 
                       labels={'natureza_apurada': 'Tipo de Crime', 'total_crimes': 'Total de Crimes'}, 
                       title=f"Tipos de Crimes em {local_selecionado}",
                       color='natureza_apurada',  # Adicionando colorização para tornar o gráfico mais dinâmico
                       color_discrete_sequence=px.colors.qualitative.Set2)

    # Atualização do layout para centralizar o título e ajustar o gráfico
    fig_local.update_layout(title_x=0.5, 
                            xaxis_title=None, 
                            yaxis_title=None, 
                            xaxis_tickangle=45)
    
    # Exibindo o gráfico
    st.plotly_chart(fig_local)

    # Detalhamento adicional
    st.write(f"A análise dos crimes no local **{local_selecionado}** revela as seguintes informações:")
    st.write(df_local)



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

# 9. Evolução Anual de Crimes
st.subheader("📊 Evolução Anual de Ocorrências")
crimes_por_ano = df.groupby('ano_estatistica').size().reset_index(name='total_crimes')

fig_ano = px.line(crimes_por_ano, x='ano_estatistica', y='total_crimes', title="Evolução Anual de Crimes", markers=True)
fig_ano.update_layout(title_x=0.5)
st.plotly_chart(fig_ano)

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


# 11. Exportar Dados para PDF
from datetime import datetime

def gerar_pdf():
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Captura a data de geração do relatório
    data_geracao = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

    # Cabeçalho
    p.setFont("Helvetica-Bold", 16)
    p.drawString(40, height - 50, "Relatório de Análise Criminal")

    # Indicadores principais
    p.setFont("Helvetica", 12)
    p.drawString(40, height - 100, f"Total de Ocorrências: {total}")
    p.drawString(40, height - 120, f"Bairro com Mais Casos: {bairro_top}")
    p.drawString(40, height - 140, f"Natureza Mais Comum: {tipo_top}")
    p.drawString(40, height - 160, f"Anos Selecionados: {', '.join(map(str, anos_selecionados))}")
    p.drawString(40, height - 180, f"Local Selecionado: {local_selecionado}")
    p.drawString(40, height - 200, f"Bairro Selecionado: {bairro_escolhido}")
    p.drawString(40, height - 220, f"Crime para Análise Sazonal: {crime_escolhido}")
    p.drawString(40, height - 240, f"Mês com Maior Incidência: {mes_top['mes_nome']} ({mes_top['total_crimes']} casos)")

    # Dados sobre Ocorrências por Dia da Semana
    p.setFont("Helvetica-Bold", 12)
    p.drawString(40, height - 280, "📅 Ocorrências por Dia da Semana:")
    
    p.setFont("Helvetica", 10)
    y_position = height - 300
    for dia, qtd in crimes_por_dia.items():
        p.drawString(40, y_position, f"{dia}: {int(qtd)} ocorrências")
        y_position -= 15

    # Garantir que o texto não saia da página
    if y_position < 60:
        p.showPage()
        p.setFont("Helvetica", 10)
        y_position = height - 50

    # Footer com a data de geração
    p.setFont("Helvetica-Oblique", 8)
    p.drawString(40, 40, f"Relatório gerado em: {data_geracao}")

    # Salvar PDF
    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer


# Botão para baixar o PDF
st.subheader("📥 Exportar Dados para PDF" )
st.write("Clique no botão abaixo para baixar os dados filtrados em PDF.")
pdf_bytes = gerar_pdf()
st.download_button(label="📥 Baixar PDF do Relatório",
                   data=pdf_bytes,
                   file_name="relatorio_analise_criminal.pdf",
                   mime="application/pdf")

# 12. Exportar Relatório Detalhado para PDF
def gerar_relatorio_detalhado(df, total, bairro_top, tipo_top, anos_selecionados, local_selecionado, bairro_escolhido, crime_escolhido, mes_top):
    # Criar buffer para PDF
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Função auxiliar para adicionar texto com controle de altura e páginas
    def add_text_with_page_control(text, font, size, x, y, page_height):
        nonlocal p
        p.setFont(font, size)
        if y < 40:  # Se a posição y for muito baixa, criamos uma nova página
            p.showPage()
            p.setFont(font, size)
            y = page_height - 50  # Reseta a altura para o topo da nova página
        p.drawString(x, y, text)
        return y - 20  # Retorna a nova altura após o texto

    # Cabeçalho
    p.setFont("Helvetica-Bold", 16)
    altura = height - 50
    altura = add_text_with_page_control("Relatório Detalhado de Análise Criminal", "Helvetica-Bold", 16, 40, altura, height)

    # Data e hora do relatório
    data_geracao = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    altura = add_text_with_page_control(f"Data de Geração: {data_geracao}", "Helvetica", 10, 40, altura, height)

    # Indicadores principais
    altura = add_text_with_page_control("Indicadores Principais", "Helvetica-Bold", 12, 40, altura, height)
    altura = add_text_with_page_control(f"Total de Ocorrências: {total}", "Helvetica", 10, 40, altura, height)
    altura = add_text_with_page_control(f"Bairro com Mais Casos: {bairro_top}", "Helvetica", 10, 40, altura, height)
    altura = add_text_with_page_control(f"Natureza Mais Comum: {tipo_top}", "Helvetica", 10, 40, altura, height)
    altura = add_text_with_page_control(f"Anos Selecionados: {', '.join(map(str, anos_selecionados))}", "Helvetica", 10, 40, altura, height)
    altura = add_text_with_page_control(f"Local Selecionado: {local_selecionado}", "Helvetica", 10, 40, altura, height)
    altura = add_text_with_page_control(f"Bairro Selecionado: {bairro_escolhido}", "Helvetica", 10, 40, altura, height)
    altura = add_text_with_page_control(f"Crime para Análise Sazonal: {crime_escolhido}", "Helvetica", 10, 40, altura, height)
    altura = add_text_with_page_control(f"Mês com Maior Incidência: {mes_top['mes_nome']} ({mes_top['total_crimes']} casos)", "Helvetica", 10, 40, altura, height)

    # Tendência de Crimes por Mês
    altura = add_text_with_page_control("Tendência de Crimes por Mês", "Helvetica-Bold", 12, 40, altura, height)
    tendencia = df.groupby(['ano_estatistica', 'mes_estatistica']).size().reset_index(name='total_crimes')
    for i, row in tendencia.iterrows():
        altura = add_text_with_page_control(f"Ano: {row['ano_estatistica']} - Mês: {row['mes_estatistica']} - Crimes: {row['total_crimes']}", "Helvetica", 10, 40, altura, height)

    # Ocorrências por Dia da Semana
    altura = add_text_with_page_control("Ocorrências por Dia da Semana", "Helvetica-Bold", 12, 40, altura, height)
    df['dia_semana'] = pd.to_datetime(df['data_ocorrencia'], errors='coerce').dt.day_name()
    traducao_dias = {'Monday': 'Segunda', 'Tuesday': 'Terça', 'Wednesday': 'Quarta', 'Thursday': 'Quinta', 'Friday': 'Sexta', 'Saturday': 'Sábado', 'Sunday': 'Domingo'}
    df['dia_semana_pt'] = df['dia_semana'].map(traducao_dias)
    crimes_por_dia = df['dia_semana_pt'].value_counts().reindex(['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']).fillna(0)
    for i, (dia, qtd) in enumerate(crimes_por_dia.items()):
        altura = add_text_with_page_control(f"{dia}: {qtd} crimes", "Helvetica", 10, 40, altura, height)

    # Crimes Mais Comuns por Dia da Semana
    altura = add_text_with_page_control("Crimes Mais Comuns por Dia da Semana", "Helvetica-Bold", 12, 40, altura, height)
    top_crimes = df['natureza_apurada'].value_counts().head(5).index
    df_top_crimes = df[df['natureza_apurada'].isin(top_crimes)]
    crimes_dia = df_top_crimes.groupby(['natureza_apurada', 'dia_semana_pt']).size().reset_index(name='total')
    for i, row in crimes_dia.iterrows():
        altura = add_text_with_page_control(f"Crime: {row['natureza_apurada']} - Dia: {row['dia_semana_pt']} - Total: {row['total']}", "Helvetica", 10, 40, altura, height)

    # Detalhamento sobre o bairro escolhido
    altura = add_text_with_page_control(f"Detalhamento para o Bairro: {bairro_escolhido}", "Helvetica-Bold", 12, 40, altura, height)
    df_bairro = df[df['bairro'] == bairro_escolhido]
    tipos_bairro = df_bairro['natureza_apurada'].value_counts().head(10)
    for i, (tipo, qtd) in enumerate(tipos_bairro.items()):
        altura = add_text_with_page_control(f"{tipo}: {qtd} crimes", "Helvetica", 10, 40, altura, height)

    # Finalização do relatório
    p.setFont("Helvetica-Oblique", 8)
    p.drawString(40, 40, "Este relatório foi gerado automaticamente.")

    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer


# Função para o botão de download
def download_relatorio_detalhado():
    pdf_bytes = gerar_relatorio_detalhado(df, total, bairro_top, tipo_top, anos_selecionados, local_selecionado, bairro_escolhido, crime_escolhido, mes_top)
    st.download_button(label="📥 Baixar Relatório Detalhado",
                       data=pdf_bytes,
                       file_name="relatorio_detalhado_analise_criminal.pdf",
                       mime="application/pdf")

# Chamada para download do relatório
st.subheader("📥 Exportar Relatório Detalhado para PDF")
download_relatorio_detalhado()
