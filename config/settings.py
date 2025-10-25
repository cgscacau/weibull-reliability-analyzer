"""
Configurações globais do aplicativo
"""

# Configurações da aplicação
APP_CONFIG = {
    "page_title": "Weibull Reliability Analyzer",
    "page_icon": "📊",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
}

# Cores do tema
COLORS = {
    "primary": "#1f77b4",
    "secondary": "#ff7f0e",
    "success": "#2ca02c",
    "danger": "#d62728",
    "warning": "#ff9800",
    "info": "#17a2b8",
    "light": "#f8f9fa",
    "dark": "#343a40",
    "background": "#ffffff",
    "text": "#262730",
}

# Configurações de gráficos
PLOT_CONFIG = {
    "template": "plotly_white",
    "height": 500,
    "margin": dict(l=50, r=50, t=80, b=50),
    "font_size": 12,
    "title_font_size": 16,
    "showlegend": True,
}

# Formatos de arquivo suportados
SUPPORTED_FORMATS = {
    "csv": [".csv"],
    "excel": [".xlsx", ".xls"],
    "pdf": [".pdf"],
}

# Colunas esperadas nos dados
REQUIRED_COLUMNS = {
    "tempo_falha": ["tempo", "time", "tempo_falha", "failure_time", "hours", "horas"],
    "status": ["status", "censura", "censored", "event", "evento"],
    "equipamento": ["equipamento", "equipment", "id", "asset", "ativo"],
}

# Configurações de análise Weibull
WEIBULL_CONFIG = {
    "confidence_level": 0.95,
    "min_samples": 3,
    "max_iterations": 1000,
    "tolerance": 1e-6,
}

# Mensagens de ajuda e tooltips
TOOLTIPS = {
    "beta": """
    **Parâmetro de Forma (β)**
    
    - β < 1: Taxa de falha decrescente (mortalidade infantil)
    - β = 1: Taxa de falha constante (vida útil)
    - β > 1: Taxa de falha crescente (desgaste)
    """,
    
    "eta": """
    **Parâmetro de Escala (η)**
    
    Representa a vida característica do equipamento.
    É o tempo em que aproximadamente 63,2% das unidades falharam.
    """,
    
    "mtbf": """
    **MTBF (Mean Time Between Failures)**
    
    Tempo médio entre falhas. Indica o tempo esperado
    de operação antes de uma falha ocorrer.
    """,
    
    "reliability": """
    **Confiabilidade R(t)**
    
    Probabilidade de um equipamento funcionar sem falhas
    até um determinado tempo t.
    """,
    
    "hazard_rate": """
    **Taxa de Falha h(t)**
    
    Taxa instantânea de falha em um determinado tempo,
    dado que o equipamento sobreviveu até esse momento.
    """,
}

# Textos explicativos
EXPLANATIONS = {
    "weibull_intro": """
    A distribuição de Weibull é amplamente utilizada em análise de confiabilidade
    e engenharia de manutenção. Ela é flexível e pode modelar diferentes tipos
    de comportamento de falha através de seus parâmetros.
    """,
    
    "data_format": """
    Seus dados devem conter pelo menos:
    - **Tempo até falha**: tempo de operação até a falha ou censura
    - **Status**: indicador se houve falha (1) ou censura (0)
    - **Identificador** (opcional): ID do equipamento ou componente
    """,
}

# Configurações de validação
VALIDATION_CONFIG = {
    "min_failure_time": 0,
    "max_failure_time": 1e10,
    "allow_negative_times": False,
    "require_status_column": True,
}
