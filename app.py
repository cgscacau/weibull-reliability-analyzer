"""
Weibull Reliability Analyzer
Aplicativo para análise de confiabilidade usando distribuição de Weibull
"""
import streamlit as st
from config import APP_CONFIG
from modules.data_handler import FileUploader
from utils.helpers import init_session_state

# Configuração da página
st.set_page_config(**APP_CONFIG)

# Inicialização do session state
init_session_state("data", None)
init_session_state("filename", None)
init_session_state("data_status", "not_loaded")

# Título principal
st.title("📊 Weibull Reliability Analyzer")
st.markdown("### Análise de Confiabilidade para Frotas e Equipamentos")

# Sidebar
with st.sidebar:
    st.image("https://via.placeholder.com/150x50/1f77b4/ffffff?text=WRA", use_container_width=True)
    st.markdown("---")
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
- Upload de dados em múltiplos formatos (CSV, Excel, PDF)
- Análise estatística completa com distribuição de Weibull
- Visualizações interativas e intuitivas
- Cálculo de métricas de confiabilidade (MTBF, taxa de falha, etc.)
- Exportação de relatórios e gráficos
""")

st.markdown("---")

# Upload de arquivo
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
    
    st.success("✅ Dados carregados! Prossiga para a validação na próxima etapa.")

else:
    st.info("👆 Faça o upload de um arquivo para começar a análise.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <small>Weibull Reliability Analyzer © 2025 | Desenvolvido com Streamlit</small>
</div>
""", unsafe_allow_html=True)
