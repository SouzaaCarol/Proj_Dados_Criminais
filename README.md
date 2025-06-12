# 🚨 Sistema de Gestão de Segurança Pública  
🔍 Dados que salvam vidas

Este projeto foi desenvolvido como parte de um trabalho acadêmico com o objetivo de tornar os **dados de ocorrências criminais** mais acessíveis, organizados e úteis para a tomada de decisões por parte de **governos, sociedade civil, jornalistas e forças de segurança pública**.

---

##💡 Objetivo

Criar uma solução tecnológica que permita:

- Organizar grandes volumes de dados brutos sobre segurança pública
- Tratar e padronizar esses dados para uma base de dados confiável
- Visualizar informações por meio de dashboards interativos
- Apoiar políticas públicas com **dados reais e estruturados**

---

## 🧠 Tecnologias Utilizadas

- **[Python](https://www.python.org/)** – linguagem principal  
- **[Streamlit](https://streamlit.io/)** – criação do painel web  
- **[Pandas](https://pandas.pydata.org/)** – manipulação de dados  
- **[Plotly Express](https://plotly.com/python/plotly-express/)** – gráficos interativos  
- **[ReportLab](https://www.reportlab.com/)** – geração de arquivos PDF  
- **[SQLAlchemy](https://www.sqlalchemy.org/)** – conexão com banco de dados  
- **[MySQL](https://www.mysql.com/)** – sistema de gerenciamento do banco de dados utilizado  
- **[Base64](https://docs.python.org/3/library/base64.html)** – codificação para download  
- **[Datetime](https://docs.python.org/3/library/datetime.html)** – manipulação de datas  
- **[os](https://docs.python.org/3/library/os.html)** – manipulação de variáveis de ambiente e arquivos  


---

## 👩‍💻 Etapas Técnicas

### 🗂️ Modelagem
- Criação do **DER**, **MER** e **Dicionário de Dados**
- Definição das entidades: `Departamento`, `Seccional`, `Delegacia`, `Município`, `Ocorrência`, `Localização`, `Natureza Apurada` e `Ocorrência_Natureza`

### 🔄 Migração de Dados (Python)
- Leitura dos dados a partir de planilhas Excel (CSV)
- Mapeamento de colunas com **padronização de nomes**
- Tratamento de inconsistências (campos vazios, dados inválidos, coordenadas incorretas)
- Inserção otimizada dos dados em lotes no banco **MySQL**

### 🔐 Segurança
- Controle de acesso com **perfis personalizados**:
  - Jornalistas
  - Sociedade civil
  - Forças policiais

---

## 📊 Principais Visualizações no Dashboard

- Número total de ocorrências
- Mapa de calor por bairro e município
- Dias da semana com maior número de crimes
- Tipos de crime por local (via pública, loja, residência etc.)
- Categorias criminais mais recorrentes (furto, roubo, lesão corporal…)

---

## 🤝 Colaboração

Projeto desenvolvido por:  
- Ana Carolina Martins Souza
- Bianca Mangueira Porto
- Dell Isola Silva
- Fernando Matos de Sousa
- Gabriel Pereira Cesar
- Gustavo Camargo Dantas de Souza
- Guilherme Nicacio de Assis Pereira
- Matheus Francisco da Silva Barbosa
- Mayara Caroline Alves Pereira
- Vinicius Peixoto Morais
---

## ✨ Contribuições

Contribuições são super bem-vindas! 💜

Se você quiser sugerir melhorias, relatar bugs ou colaborar com o código.




