"""
Constantes utilizadas em todo o aplicativo
"""

# Status de dados
DATA_STATUS = {
    "NOT_LOADED": "not_loaded",
    "LOADED": "loaded",
    "VALIDATED": "validated",
    "PROCESSED": "processed",
    "ANALYZED": "analyzed",
}

# Tipos de censura
CENSORING_TYPES = {
    "RIGHT": "right",  # Censura à direita (mais comum)
    "LEFT": "left",    # Censura à esquerda
    "INTERVAL": "interval",  # Censura intervalar
}

# Tipos de análise
ANALYSIS_TYPES = {
    "WEIBULL_2P": "weibull_2p",  # 2 parâmetros (β, η)
    "WEIBULL_3P": "weibull_3p",  # 3 parâmetros (β, η, γ)
}

# Métodos de estimação
ESTIMATION_METHODS = {
    "MLE": "Maximum Likelihood Estimation",
    "RRX": "Rank Regression on X",
    "RRY": "Rank Regression on Y",
}

# Tipos de gráficos
PLOT_TYPES = {
    "PROBABILITY": "probability_plot",
    "RELIABILITY": "reliability_vs_time",
    "HAZARD": "hazard_rate",
    "PDF": "probability_density",
    "CDF": "cumulative_distribution",
}

# Unidades de tempo
TIME_UNITS = {
    "HOURS": "horas",
    "DAYS": "dias",
    "WEEKS": "semanas",
    "MONTHS": "meses",
    "YEARS": "anos",
    "CYCLES": "ciclos",
    "KM": "quilômetros",
}

# Mensagens de erro
ERROR_MESSAGES = {
    "NO_FILE": "❌ Nenhum arquivo foi carregado.",
    "INVALID_FORMAT": "❌ Formato de arquivo não suportado.",
    "MISSING_COLUMNS": "❌ Colunas obrigatórias não encontradas.",
    "INSUFFICIENT_DATA": "❌ Dados insuficientes para análise (mínimo de 3 falhas).",
    "INVALID_VALUES": "❌ Valores inválidos detectados nos dados.",
    "ANALYSIS_FAILED": "❌ Falha na análise. Verifique os dados.",
}

# Mensagens de sucesso
SUCCESS_MESSAGES = {
    "FILE_LOADED": "✅ Arquivo carregado com sucesso!",
    "DATA_VALIDATED": "✅ Dados validados com sucesso!",
    "ANALYSIS_COMPLETE": "✅ Análise concluída com sucesso!",
}

# Mensagens de aviso
WARNING_MESSAGES = {
    "FEW_SAMPLES": "⚠️ Poucos dados para análise robusta. Resultados podem não ser confiáveis.",
    "HIGH_CENSORING": "⚠️ Alta taxa de censura detectada. Considere coletar mais dados.",
    "OUTLIERS_DETECTED": "⚠️ Possíveis outliers detectados nos dados.",
}
