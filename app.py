"""
Weibull Reliability Analyzer
Aplicativo para análise de confiabilidade usando distribuição de Weibull
"""
import streamlit as st
import sys
import os
import numpy as np

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from config.settings import APP_CONFIG, TOOLTIPS
from modules.data_handler.file_uploader import FileUploader
from modules.data_handler.data_validator import DataValidator
from modules.data_handler.data_processor import DataProcessor
from modules.analysis.weibull_analysis import WeibullAnalysis
from modules.analysis.reliability_metrics import ReliabilityMetrics
from modules.analysis.statistical_tests import StatisticalTests
from utils.helpers import init_session_state, format_number
from utils.constants import TIME_UNITS

# Configuração da página
st.set_page_config(**APP_CONFIG)

# Inicialização do session state
init_session_state("data", None)
init_session_state("filename", None)
init_session_state("data_status", "not_loaded")
init_session_state("validation_results", None)
init_session_state("processed_data", None)
init_session_state("analysis_results", None)

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
            format="%.2f",
            help="Nível de confiança para intervalos"
        )
    
    if st.button("📈 Executar Análise de Weibull", type="primary"):
        with st.spinner("Executando análise de Weibull..."):
            # Análise de Weibull
            weibull = WeibullAnalysis(st.session_state["processed_data"])
            results = weibull.fit(method=method, confidence_level=confidence_level)
            
            # Métricas de confiabilidade
            metrics_calc = ReliabilityMetrics(weibull)
            metrics = metrics_calc.calculate_all_metrics()
            
            # Testes estatísticos
            tests = StatisticalTests(weibull)
            test_results = tests.run_all_tests()
            
            # Interpretação
            interpretation = weibull.get_interpretation()
            
            # Armazena resultados
            st.session_state["analysis_results"] = {
                "weibull": results,
                "metrics": metrics,
                "tests": test_results,
                "interpretation": interpretation,
                "weibull_obj": weibull,
                "metrics_obj": metrics_calc
            }
            
            st.session_state["data_status"] = "analyzed"
            
            # EXIBE RESULTADOS
            st.success("✅ Análise concluída com sucesso!")
            
            # Parâmetros de Weibull
            st.subheader("📊 Parâmetros de Weibull")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric(
                    label="β (Beta) - Parâmetro de Forma",
                    value=f"{results['beta']:.4f}",
                    help=TOOLTIPS["beta"]
                )
                st.caption(f"IC {confidence_level*100:.0f}%: [{results['beta_ci'][0]:.4f}, {results['beta_ci'][1]:.4f}]")
            
            with col2:
                st.metric(
                    label=f"η (Eta) - Parâmetro de Escala ({results['time_unit']})",
                    value=f"{results['eta']:.2f}",
                    help=TOOLTIPS["eta"]
                )
                st.caption(f"IC {confidence_level*100:.0f}%: [{results['eta_ci'][0]:.2f}, {results['eta_ci'][1]:.2f}]")
            
            # Interpretação
            st.markdown("---")
            st.subheader("🔍 Interpretação dos Resultados")
            
            st.info(f"""
            **Modo de Falha:** {interpretation['failure_mode']}
            
            **Comportamento:** {interpretation['behavior']}
            
            **Recomendação:** {interpretation['recommendation']}
            
            **Valor de β:** {interpretation['beta_value']}
            """)
            
            # Métricas de Confiabilidade
            st.markdown("---")
            st.subheader("📈 Métricas de Confiabilidade")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "MTTF",
                    format_number(metrics["mttf"], 2, results['time_unit']),
                    help=TOOLTIPS["mtbf"]
                )
            
            with col2:
                st.metric(
                    "Vida Mediana",
                    format_number(metrics["median_life"], 2, results['time_unit']),
                    help="Tempo em que 50% das unidades falharam"
                )
            
            with col3:
                st.metric(
                    "B10 Life",
                    format_number(metrics["b10_life"], 2, results['time_unit']),
                    help="Tempo em que 10% das unidades falharam"
                )
            
            with col4:
                st.metric(
                    "Vida Característica",
                    format_number(metrics["characteristic_life"], 2, results['time_unit']),
                    help="Tempo em que 63.2% das unidades falharam (η)"
                )
            
            # Testes Estatísticos
            st.markdown("---")
            st.subheader("🧪 Testes de Adequação")
            
            # R²
            r2_result = test_results["r_squared"]
            st.metric(
                "Coeficiente de Determinação (R²)",
                f"{r2_result['r_squared']:.4f}",
                delta=r2_result['quality'],
                help="Mede a qualidade do ajuste da distribuição aos dados"
            )
            st.caption(r2_result['interpretation'])
            
            # Anderson-Darling
            ad_result = test_results["anderson_darling"]
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Teste Anderson-Darling**")
                st.write(f"Estatística: {ad_result['statistic']:.4f}")
                st.write(f"Valor Crítico: {ad_result['critical_value']:.4f}")
                if ad_result['passed']:
                    st.success("✅ " + ad_result['interpretation'])
                else:
                    st.warning("⚠️ " + ad_result['interpretation'])
            
            # Kolmogorov-Smirnov
            ks_result = test_results["kolmogorov_smirnov"]
            with col2:
                st.write("**Teste Kolmogorov-Smirnov**")
                st.write(f"Estatística: {ks_result['statistic']:.4f}")
                st.write(f"P-valor: {ks_result['p_value']:.4f}")
                if ks_result['passed']:
                    st.success("✅ " + ks_result['interpretation'])
                else:
                    st.warning("⚠️ " + ks_result['interpretation'])

# ETAPA 5: Visualizações
if st.session_state.get("analysis_results") is not None:
    st.markdown("---")
    st.header("5️⃣ Visualizações")
    
    analysis_results = st.session_state["analysis_results"]
    weibull_obj = analysis_results["weibull_obj"]
    metrics_obj = analysis_results["metrics_obj"]
    
    # Importa classes de visualização
    from modules.visualization.weibull_plots import WeibullPlots
    from modules.visualization.reliability_plots import ReliabilityPlots
    
    # Cria objetos de visualização
    weibull_plots = WeibullPlots(weibull_obj, metrics_obj)
    reliability_plots = ReliabilityPlots(weibull_obj, metrics_obj)
    
    # Tabs para diferentes visualizações
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Gráficos Principais",
        "📈 Análise Detalhada", 
        "📉 Métricas",
        "🔍 Análise Completa"
    ])
    
    with tab1:
        st.subheader("Gráficos Principais de Weibull")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(
                weibull_plots.probability_plot(),
                use_container_width=True,
                key="prob_plot"
            )
        
        with col2:
            st.plotly_chart(
                weibull_plots.reliability_vs_time(),
                use_container_width=True,
                key="reliability_plot"
            )
    
    with tab2:
        st.subheader("Análise Detalhada")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(
                weibull_plots.hazard_rate_plot(),
                use_container_width=True,
                key="hazard_plot"
            )
        
        with col2:
            st.plotly_chart(
                reliability_plots.failure_distribution_histogram(),
                use_container_width=True,
                key="histogram_plot"
            )
        
        st.plotly_chart(
            weibull_plots.pdf_cdf_plot(),
            use_container_width=True,
            key="pdf_cdf_plot"
        )
    
    with tab3:
        st.subheader("Métricas Visuais")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(
                reliability_plots.b_life_chart(),
                use_container_width=True,
                key="blife_chart"
            )
        
        with col2:
            st.plotly_chart(
                reliability_plots.metrics_comparison(),
                use_container_width=True,
                key="metrics_comparison"
            )
    
    with tab4:
        st.subheader("Visão Geral Completa")
        st.plotly_chart(
            weibull_plots.combined_analysis_plot(),
            use_container_width=True,
            key="combined_plot"
        )
        
        # Calculadora interativa
        st.markdown("---")
        st.subheader("🧮 Calculadora de Confiabilidade")
        
        col1, col2 = st.columns(2)
        
        with col1:
            calc_time = st.number_input(
                f"Tempo para análise ({analysis_results['weibull']['time_unit']})",
                min_value=0.0,
                value=float(analysis_results['metrics']['median_life']),
                step=10.0
            )
        
        with col2:
            if st.button("🔄 Calcular Métricas", type="primary"):
                metrics_at_time = metrics_obj.reliability_at_time(calc_time)
                
                st.markdown("#### Resultados:")
                col_a, col_b = st.columns(2)
                
                with col_a:
                    st.metric(
                        "Confiabilidade",
                        f"{metrics_at_time['reliability']*100:.2f}%",
                        help="Probabilidade de funcionar até este tempo"
                    )
                    st.metric(
                        "PDF",
                        f"{metrics_at_time['pdf']:.6f}",
                        help="Densidade de probabilidade neste tempo"
                    )
                
                with col_b:
                    st.metric(
                        "Não-Confiabilidade",
                        f"{metrics_at_time['unreliability']*100:.2f}%",
                        help="Probabilidade de falhar até este tempo"
                    )
                    st.metric(
                        "Taxa de Falha",
                        f"{metrics_at_time['hazard_rate']:.6f}",
                        help="Taxa instantânea de falha neste tempo"
                    )



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
