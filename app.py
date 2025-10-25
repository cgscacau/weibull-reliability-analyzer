"""
Weibull Reliability Analyzer
Aplicativo para análise de confiabilidade usando distribuição de Weibull
"""
import streamlit as st
import sys
import os

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from config.settings import APP_CONFIG
from modules.data_handler.file_uploader import FileUploader
from modules.data_handler.data_validator import DataValidator
from modules.data_handler.data_processor import DataProcessor
from utils.helpers import init_session_state
from utils.constants import TIME_UNITS

# Configuração da página
st.set_page_config(**APP_CONFIG)

# Inicialização do session state
init_session_state("data", None)
init_session_state("filename", None)
init_session_state("data_status", "not_loaded")
init_session_state("validation_results", None)
init_session_state("processed_data", None)

# Título principal
st.title("📊 Weibull Reliability Analyzer")
st.markdown("### Análise de Confiabilidade para Frotas e Equipamentos")

# Sidebar
with st.sidebar:
    st.markdown("### 🎯 Navegação")
    st.markdown("""
    - 📊 **Análise Principal**: Upload e análise de dados
    - 📚 **Tutorial**: Aprenda a usar o aplicativo
    - 📖 **Teoria Weibull**: Fundamentos teóricos
    - ❓ **FAQ**: Perguntas frequentes
    - 📝 **Guia**: Como preparar seus dados
    """)
    st.markdown("---")
    st.markdown("### ℹ️ Sobre")
    st.markdown("""
    **Versão:** 1.0.0  
    **Desenvolvido para:** Análise de confiabilidade industrial
    """)

# Conteúdo principal
st.markdown("""
Bem-vindo ao **Weibull Reliability Analyzer**! Este aplicativo permite realizar análises 
completas de confiabilidade utilizando a distribuição de Weibull.

**Funcionalidades principais:**
- Upload de dados em múltiplos formatos (CSV, Excel)
- Análise estatística completa com distribuição de Weibull
- Visualizações interativas e intuitivas
- Cálculo de métricas de confiabilidade (MTBF, taxa de falha, etc.)
- Exportação de relatórios e gráficos
""")

st.markdown("---")

# ETAPA 1: Upload de arquivo
st.header("1️⃣ Upload de Dados")
uploader = FileUploader()
result = uploader.upload_file()

if result is not None:
    df, filename = result
    st.session_state["data"] = df
    st.session_state["filename"] = filename
    st.session_state["data_status"] = "loaded"
    
    # Informações sobre os dados
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📝 Total de Registros", len(df))
    with col2:
        st.metric("📊 Número de Colunas", len(df.columns))
    with col3:
        st.metric("📁 Arquivo", filename)

# ETAPA 2: Validação de dados
if st.session_state["data"] is not None:
    st.markdown("---")
    st.header("2️⃣ Validação de Dados")
    
    if st.button("🔍 Validar Dados", type="primary"):
        with st.spinner("Validando dados..."):
            validator = DataValidator(st.session_state["data"])
            validation_results = validator.validate()
            st.session_state["validation_results"] = validation_results
            
            # Exibe resultados
            is_valid = validator.display_validation_results()
            
            if is_valid:
                st.session_state["data_status"] = "validated"

# ETAPA 3: Processamento de dados
if st.session_state.get("validation_results") and st.session_state["validation_results"]["is_valid"]:
    st.markdown("---")
    st.header("3️⃣ Processamento de Dados")
    
    col1, col2 = st.columns(2)
    
    with col1:
        time_unit = st.selectbox(
            "Unidade de Tempo",
            options=list(TIME_UNITS.keys()),
            format_func=lambda x: TIME_UNITS[x],
            help="Selecione a unidade de tempo dos seus dados"
        )
    
    with col2:
        remove_outliers = st.checkbox(
            "Remover Outliers",
            value=False,
            help="Remove valores extremos que podem afetar a análise"
        )
    
    if st.button("⚙️ Processar Dados", type="primary"):
        with st.spinner("Processando dados..."):
            validation_results = st.session_state["validation_results"]
            processor = DataProcessor(
                st.session_state["data"],
                validation_results["column_mapping"]
            )
            
            processed_df = processor.process(
                time_unit=TIME_UNITS[time_unit],
                remove_outliers=remove_outliers
            )
            
            st.session_state["processed_data"] = processed_df
            st.session_state["data_status"] = "processed"
            
            # Exibe dados processados
            processor.display_processed_data()
            
            st.success("✅ Dados processados com sucesso! Pronto para análise.")

# Mensagem inicial
if st.session_state["data"] is None:
    st.info("👆 Faça o upload de um arquivo para começar a análise.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <small>Weibull Reliability Analyzer © 2025 | Desenvolvido com Streamlit</small>
</div>
""", unsafe_allow_html=True)
