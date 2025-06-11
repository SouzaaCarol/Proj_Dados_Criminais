import streamlit as st

st.set_page_config(page_title="Sistema de Segurança Pública", layout="centered")

st.title("🔐 Sistema de Segurança Pública")
st.subheader("Escolha seu perfil de acesso:")

col1, col2 = st.columns(2)

with col1:
    if st.button("👮‍♂️ Autoridades Públicas"):
        st.switch_page("pages/policia.py")

with col2:
   if st.button("📊 Quero ver Tendências"):
        st.switch_page("pages/analise.py")
    
