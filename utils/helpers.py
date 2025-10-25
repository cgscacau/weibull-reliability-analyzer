"""
Funções auxiliares gerais
"""
import streamlit as st
import pandas as pd
from typing import Any, Dict, List, Optional
import re


def format_number(value: float, decimals: int = 2, unit: str = "") -> str:
    """
    Formata um número para exibição
    
    Args:
        value: Valor a ser formatado
        decimals: Número de casas decimais
        unit: Unidade de medida (opcional)
    
    Returns:
        String formatada
    """
    if pd.isna(value):
        return "N/A"
    
    formatted = f"{value:,.{decimals}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    if unit:
        return f"{formatted} {unit}"
    return formatted


def create_download_button(data: Any, filename: str, label: str, mime_type: str = "text/csv"):
    """
    Cria um botão de download
    
    Args:
        data: Dados a serem baixados
        filename: Nome do arquivo
        label: Texto do botão
        mime_type: Tipo MIME do arquivo
    """
    st.download_button(
        label=label,
        data=data,
        file_name=filename,
        mime=mime_type,
    )


def normalize_column_name(column: str) -> str:
    """
    Normaliza nome de coluna (remove acentos, espaços, etc)
    
    Args:
        column: Nome da coluna
    
    Returns:
        Nome normalizado
    """
    # Remove acentos
    import unicodedata
    nfkd = unicodedata.normalize('NFKD', column)
    column_normalized = "".join([c for c in nfkd if not unicodedata.combining(c)])
    
    # Converte para minúsculas e substitui espaços
    column_normalized = column_normalized.lower().strip()
    column_normalized = re.sub(r'[^\w\s]', '', column_normalized)
    column_normalized = re.sub(r'\s+', '_', column_normalized)
    
    return column_normalized


def find_column_match(df: pd.DataFrame, possible_names: List[str]) -> Optional[str]:
    """
    Encontra uma coluna no DataFrame baseado em possíveis nomes
    
    Args:
        df: DataFrame
        possible_names: Lista de possíveis nomes
    
    Returns:
        Nome da coluna encontrada ou None
    """
    normalized_columns = {normalize_column_name(col): col for col in df.columns}
    
    for name in possible_names:
        normalized_name = normalize_column_name(name)
        if normalized_name in normalized_columns:
            return normalized_columns[normalized_name]
    
    return None


def display_metric_card(title: str, value: Any, delta: Optional[str] = None, 
                       help_text: Optional[str] = None):
    """
    Exibe uma métrica em formato de card
    
    Args:
        title: Título da métrica
        value: Valor da métrica
        delta: Variação (opcional)
        help_text: Texto de ajuda (opcional)
    """
    st.metric(
        label=title,
        value=value,
        delta=delta,
        help=help_text
    )


def create_info_box(message: str, type: str = "info"):
    """
    Cria uma caixa de informação
    
    Args:
        message: Mensagem a ser exibida
        type: Tipo da mensagem (info, success, warning, error)
    """
    if type == "info":
        st.info(message)
    elif type == "success":
        st.success(message)
    elif type == "warning":
        st.warning(message)
    elif type == "error":
        st.error(message)


def init_session_state(key: str, default_value: Any):
    """
    Inicializa uma variável no session state se não existir
    
    Args:
        key: Chave da variável
        default_value: Valor padrão
    """
    if key not in st.session_state:
        st.session_state[key] = default_value


def clear_session_state(keys: Optional[List[str]] = None):
    """
    Limpa variáveis do session state
    
    Args:
        keys: Lista de chaves a limpar (None limpa todas)
    """
    if keys is None:
        st.session_state.clear()
    else:
        for key in keys:
            if key in st.session_state:
                del st.session_state[key]
