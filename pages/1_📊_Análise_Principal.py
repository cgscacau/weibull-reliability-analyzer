"""
Página principal de análise (cópia do app.py com ajustes)
"""
import streamlit as st
import sys
import os
import numpy as np

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config.settings import APP_CONFIG, TOOLTIPS
from modules.data_handler.file_uploader import FileUploader
from modules.data_handler.data_validator import DataValidator
from modules.data_handler.data_processor import DataProcessor
from modules.analysis.weibull_analysis import WeibullAnalysis
from modules.analysis.reliability_metrics import ReliabilityMetrics
from modules.analysis.statistical_tests import StatisticalTests
from modules.visualization.weibull_plots import WeibullPlots
from modules.visualization.reliability_plots import ReliabilityPlots
from utils.helpers import init_session_state, format_number
from utils.constants import TIME_UNITS

# Configuração da página
st.set_page_config(
    page_title="Análise Principal - WRA",
    page_icon="📊",
    layout="wide"
)

# Inicialização do session state
init_session_state("data", None)
init_session_state("filename", None)
init_session_state("data_status", "not_loaded")
init_session_state("validation_results", None)
init_session_state("processed_data", None)
init_session_state("analysis_results", None)

# Título
st.title("📊 Análise Principal")
st.markdown("### Análise Completa de Confiabilidade com Weibull")

# Link para ajuda
col1, col2, col3 = st.columns([1, 1, 1])
with col3:
    st.markdown("**Precisa de ajuda?** 👉 [Ver Tutorial](Tutorial) | [FAQ](Perguntas_Frequentes)")

st.markdown("---")

# ETAPA 1: Upload de arquivo
st.header("1️⃣ Upload de Dados")

with st.expander("ℹ️ Como preparar seus dados", expanded=False):
    st.markdown("""
    **Seus dados devem conter:**
    - Coluna de **tempo até falha** (horas, dias, ciclos, km, etc.)
    - Coluna de **status** (1 = falha, 0 = censurado) - opcional
    - Coluna de **identificação** (ID do equipamento) - opcional
    
    📝 **Veja o [Guia de Preenchimento](Guia_Preenchimento) para mais detalhes**
    """)

uploader = FileUploader()
result = uploader.upload_file()

if result is not None:
    df, filename = result
    st.session_state["data"] = df
    st.session_state["filename"] = filename
    st.session_state["data_status"] = "loaded"
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📝 Total de Registros", len(df))
    with col2:
        st.metric("📊 Número de Colunas", len(df.columns))
    with col3:
        st.metric("📁 Arquivo", filename)

# ETAPA 2: Validação
if st.session_state["data"] is not None:
    st.markdown("---")
    st.header("2️⃣ Validação de Dados")
    
    if st.button("🔍 Validar Dados", type="primary"):
        with st.spinner("Validando dados..."):
            validator = DataValidator(st.session_state["data"])
            validation_results = validator.validate()
            st.session_state["validation_results"] = validation_results
            is_valid = validator.display_validation_results()
            if is_valid:
                st.session_state["data_status"] = "validated"

# ETAPA 3: Processamento
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
            processor.display_processed_data()
            st.success("✅ Dados processados com sucesso!")

# ETAPA 4: Análise de Weibull
if st.session_state.get("processed_data") is not None:
    st.markdown("---")
    st.header("4️⃣ Análise de Weibull")
    
    col1, col2 = st.columns(2)
    with col1:
        method = st.selectbox(
            "Método de Estimação",
            options=["mle", "rr"],
            format_func=lambda x: "Maximum Likelihood (MLE)" if x == "mle" else "Rank Regression (RR)",
            help="MLE é geralmente mais preciso, mas RR é mais rápido"
        )
    with col2:
        confidence_level = st.slider(
            "Nível de Confiança",
            min_value=0.80,
            max_value=0.99,
            value=0.95,
            step=0.01,
            format="%.2f"
        )
    
    if st.button("📈 Executar Análise de Weibull", type="primary"):
        with st.spinner("Executando análise..."):
            weibull = WeibullAnalysis(st.session_state["processed_data"])
            results = weibull.fit(method=method, confidence_level=confidence_level)
            metrics_calc = ReliabilityMetrics(weibull)
            metrics = metrics_calc.calculate_all_metrics()
            tests = StatisticalTests(weibull)
            test_results = tests.run_all_tests()
            interpretation = weibull.get_interpretation()
            
            st.session_state["analysis_results"] = {
                "weibull": results,
                "metrics": metrics,
                "tests": test_results,
                "interpretation": interpretation,
                "weibull_obj": weibull,
                "metrics_obj": metrics_calc
            }
            st.session_state["data_status"] = "analyzed"
            st.success("✅ Análise concluída!")
            
            # Exibe resultados
            st.subheader("📊 Parâmetros de Weibull")
            col1, col2 = st.columns(2)
            with col1:
                st.metric(
                    "β (Beta) - Forma",
                    f"{results['beta']:.4f}",
                    help=TOOLTIPS["beta"]
                )
                st.caption(f"IC {confidence_level*100:.0f}%: [{results['beta_ci'][0]:.4f}, {results['beta_ci'][1]:.4f}]")
            with col2:
                st.metric(
                    f"η (Eta) - Escala ({results['time_unit']})",
                    f"{results['eta']:.2f}",
                    help=TOOLTIPS["eta"]
                )
                st.caption(f"IC {confidence_level*100:.0f}%: [{results['eta_ci'][0]:.2f}, {results['eta_ci'][1]:.2f}]")
            
            st.markdown("---")
            st.subheader("🔍 Interpretação")
            st.info(f"""
            **Modo de Falha:** {interpretation['failure_mode']}
            
            **Comportamento:** {interpretation['behavior']}
            
            **Recomendação:** {interpretation['recommendation']}
            """)
            
            st.markdown("---")
            st.subheader("📈 Métricas de Confiabilidade")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("MTTF", format_number(metrics["mttf"], 2, results['time_unit']), help=TOOLTIPS["mtbf"])
            with col2:
                st.metric("Vida Mediana", format_number(metrics["median_life"], 2, results['time_unit']))
            with col3:
                st.metric("B10 Life", format_number(metrics["b10_life"], 2, results['time_unit']))
            with col4:
                st.metric("Vida Característica", format_number(metrics["characteristic_life"], 2, results['time_unit']))
            
            st.markdown("---")
            st.subheader("🧪 Testes de Adequação")
            r2_result = test_results["r_squared"]
            st.metric("R²", f"{r2_result['r_squared']:.4f}", delta=r2_result['quality'])

# ETAPA 5: Visualizações
if st.session_state.get("analysis_results") is not None:
    st.markdown("---")
    st.header("5️⃣ Visualizações")
    
    analysis_results = st.session_state["analysis_results"]
    weibull_obj = analysis_results["weibull_obj"]
    metrics_obj = analysis_results["metrics_obj"]
    
    weibull_plots = WeibullPlots(weibull_obj, metrics_obj)
    reliability_plots = ReliabilityPlots(weibull_obj, metrics_obj)
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Principais",
        "📈 Detalhada", 
        "📉 Métricas",
        "🔍 Completa"
    ])
    
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(weibull_plots.probability_plot(), use_container_width=True)
        with col2:
            st.plotly_chart(weibull_plots.reliability_vs_time(), use_container_width=True)
    
    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(weibull_plots.hazard_rate_plot(), use_container_width=True)
        with col2:
            st.plotly_chart(reliability_plots.failure_distribution_histogram(), use_container_width=True)
        st.plotly_chart(weibull_plots.pdf_cdf_plot(), use_container_width=True)
    
    with tab3:
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(reliability_plots.b_life_chart(), use_container_width=True)
        with col2:
            st.plotly_chart(reliability_plots.metrics_comparison(), use_container_width=True)
    
    with tab4:
        st.plotly_chart(weibull_plots.combined_analysis_plot(), use_container_width=True)
        
        st.markdown("---")
        st.subheader("🧮 Calculadora de Confiabilidade")
        col1, col2 = st.columns(2)
        with col1:
            calc_time = st.number_input(
                f"Tempo ({analysis_results['weibull']['time_unit']})",
                min_value=0.0,
                value=float(analysis_results['metrics']['median_life']),
                step=10.0
            )
        with col2:
            if st.button("🔄 Calcular"):
                metrics_at_time = metrics_obj.reliability_at_time(calc_time)
                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric("Confiabilidade", f"{metrics_at_time['reliability']*100:.2f}%")
                    st.metric("PDF", f"{metrics_at_time['pdf']:.6f}")
                with col_b:
                    st.metric("Não-Confiabilidade", f"{metrics_at_time['unreliability']*100:.2f}%")
                    st.metric("Taxa de Falha", f"{metrics_at_time['hazard_rate']:.6f}")

if st.session_state["data"] is None:
    st.info("👆 Faça o upload de um arquivo para começar.")
