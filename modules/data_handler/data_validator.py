"""
Módulo para validação de dados
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
import streamlit as st

from config.settings import REQUIRED_COLUMNS, VALIDATION_CONFIG
from utils.constants import ERROR_MESSAGES, WARNING_MESSAGES, SUCCESS_MESSAGES


class DataValidator:
    """Classe para validar dados de entrada"""
    
    def __init__(self, df: pd.DataFrame):
        """
        Inicializa o validador
        
        Args:
            df: DataFrame a ser validado
        """
        self.df = df.copy()
        self.validation_results = {
            "is_valid": False,
            "errors": [],
            "warnings": [],
            "column_mapping": {},
            "stats": {}
        }
    
    def validate(self) -> Dict:
        """
        Executa todas as validações
        
        Returns:
            Dicionário com resultados da validação
        """
        # 1. Verifica se o DataFrame não está vazio
        if not self._check_not_empty():
            return self.validation_results
        
        # 2. Tenta mapear as colunas automaticamente
        self._map_columns()
        
        # 3. Verifica colunas obrigatórias
        if not self._check_required_columns():
            return self.validation_results
        
        # 4. Valida tipos de dados
        self._validate_data_types()
        
        # 5. Verifica valores inválidos
        self._check_invalid_values()
        
        # 6. Calcula estatísticas básicas
        self._calculate_statistics()
        
        # 7. Verifica quantidade mínima de dados
        self._check_minimum_samples()
        
        # Define se é válido (sem erros críticos)
        self.validation_results["is_valid"] = len(self.validation_results["errors"]) == 0
        
        return self.validation_results
    
    def _check_not_empty(self) -> bool:
        """Verifica se o DataFrame não está vazio"""
        if self.df.empty:
            self.validation_results["errors"].append(ERROR_MESSAGES["INSUFFICIENT_DATA"])
            return False
        return True
    
    def _map_columns(self):
        """Tenta mapear automaticamente as colunas necessárias"""
        from utils.helpers import find_column_match
        
        mapping = {}
        
        # Tenta encontrar coluna de tempo
        tempo_col = find_column_match(self.df, REQUIRED_COLUMNS["tempo_falha"])
        if tempo_col:
            mapping["tempo_falha"] = tempo_col
        
        # Tenta encontrar coluna de status/censura
        status_col = find_column_match(self.df, REQUIRED_COLUMNS["status"])
        if status_col:
            mapping["status"] = status_col
        
        # Tenta encontrar coluna de identificação
        id_col = find_column_match(self.df, REQUIRED_COLUMNS["equipamento"])
        if id_col:
            mapping["equipamento"] = id_col
        
        self.validation_results["column_mapping"] = mapping
    
    def _check_required_columns(self) -> bool:
        """Verifica se as colunas obrigatórias foram encontradas"""
        mapping = self.validation_results["column_mapping"]
        
        if "tempo_falha" not in mapping:
            self.validation_results["errors"].append(
                "❌ Coluna de tempo até falha não encontrada. "
                "Esperado: tempo, time, tempo_falha, failure_time, hours, horas"
            )
            return False
        
        if VALIDATION_CONFIG["require_status_column"] and "status" not in mapping:
            self.validation_results["warnings"].append(
                "⚠️ Coluna de status/censura não encontrada. "
                "Assumindo que todos os dados são falhas (não censurados)."
            )
        
        return True
    
    def _validate_data_types(self):
        """Valida os tipos de dados das colunas"""
        mapping = self.validation_results["column_mapping"]
        
        # Valida coluna de tempo
        if "tempo_falha" in mapping:
            tempo_col = mapping["tempo_falha"]
            try:
                # Tenta converter para numérico
                self.df[tempo_col] = pd.to_numeric(self.df[tempo_col], errors='coerce')
                
                # Verifica se há valores não numéricos
                null_count = self.df[tempo_col].isna().sum()
                if null_count > 0:
                    self.validation_results["warnings"].append(
                        f"⚠️ {null_count} valores não numéricos encontrados na coluna de tempo. "
                        "Estes registros serão removidos."
                    )
            except Exception as e:
                self.validation_results["errors"].append(
                    f"❌ Erro ao converter coluna de tempo para numérico: {str(e)}"
                )
        
        # Valida coluna de status
        if "status" in mapping:
            status_col = mapping["status"]
            try:
                # Tenta converter para numérico
                self.df[status_col] = pd.to_numeric(self.df[status_col], errors='coerce')
                
                # Verifica valores únicos
                unique_values = self.df[status_col].dropna().unique()
                if not all(v in [0, 1] for v in unique_values):
                    self.validation_results["warnings"].append(
                        f"⚠️ Coluna de status contém valores diferentes de 0 e 1: {unique_values}. "
                        "Esperado: 0 (censurado) e 1 (falha)."
                    )
            except Exception as e:
                self.validation_results["errors"].append(
                    f"❌ Erro ao processar coluna de status: {str(e)}"
                )
    
    def _check_invalid_values(self):
        """Verifica valores inválidos nos dados"""
        mapping = self.validation_results["column_mapping"]
        
        if "tempo_falha" in mapping:
            tempo_col = mapping["tempo_falha"]
            
            # Remove valores nulos
            valid_times = self.df[tempo_col].dropna()
            
            # Verifica valores negativos
            if not VALIDATION_CONFIG["allow_negative_times"]:
                negative_count = (valid_times < 0).sum()
                if negative_count > 0:
                    self.validation_results["errors"].append(
                        f"❌ {negative_count} valores negativos encontrados na coluna de tempo. "
                        "Tempos devem ser positivos."
                    )
            
            # Verifica valores muito pequenos (próximos de zero)
            near_zero_count = ((valid_times > 0) & (valid_times < 0.001)).sum()
            if near_zero_count > 0:
                self.validation_results["warnings"].append(
                    f"⚠️ {near_zero_count} valores muito próximos de zero encontrados. "
                    "Verifique se a unidade de tempo está correta."
                )
            
            # Verifica valores muito grandes
            if valid_times.max() > VALIDATION_CONFIG["max_failure_time"]:
                self.validation_results["warnings"].append(
                    "⚠️ Valores de tempo muito grandes detectados. "
                    "Verifique se a unidade de tempo está correta."
                )
            
            # Verifica outliers usando IQR
            Q1 = valid_times.quantile(0.25)
            Q3 = valid_times.quantile(0.75)
            IQR = Q3 - Q1
            outliers = ((valid_times < (Q1 - 3 * IQR)) | (valid_times > (Q3 + 3 * IQR))).sum()
            
            if outliers > 0:
                outlier_pct = (outliers / len(valid_times)) * 100
                if outlier_pct > 5:
                    self.validation_results["warnings"].append(
                        f"⚠️ {outliers} possíveis outliers detectados ({outlier_pct:.1f}% dos dados). "
                        "Considere revisar estes valores."
                    )
    
    def _calculate_statistics(self):
        """Calcula estatísticas básicas dos dados"""
        mapping = self.validation_results["column_mapping"]
        
        stats = {
            "total_records": len(self.df),
            "valid_records": 0,
            "failures": 0,
            "censored": 0,
            "censoring_rate": 0.0
        }
        
        if "tempo_falha" in mapping:
            tempo_col = mapping["tempo_falha"]
            valid_data = self.df[tempo_col].dropna()
            stats["valid_records"] = len(valid_data)
            
            if len(valid_data) > 0:
                stats["min_time"] = float(valid_data.min())
                stats["max_time"] = float(valid_data.max())
                stats["mean_time"] = float(valid_data.mean())
                stats["median_time"] = float(valid_data.median())
                stats["std_time"] = float(valid_data.std())
        
        if "status" in mapping:
            status_col = mapping["status"]
            valid_status = self.df[status_col].dropna()
            
            stats["failures"] = int((valid_status == 1).sum())
            stats["censored"] = int((valid_status == 0).sum())
            
            if len(valid_status) > 0:
                stats["censoring_rate"] = (stats["censored"] / len(valid_status)) * 100
        else:
            # Se não há coluna de status, assume todas como falhas
            stats["failures"] = stats["valid_records"]
            stats["censored"] = 0
            stats["censoring_rate"] = 0.0
        
        self.validation_results["stats"] = stats
    
    def _check_minimum_samples(self):
        """Verifica se há quantidade mínima de amostras"""
        from config.settings import WEIBULL_CONFIG
        
        stats = self.validation_results["stats"]
        min_samples = WEIBULL_CONFIG["min_samples"]
        
        if stats["failures"] < min_samples:
            self.validation_results["errors"].append(
                f"❌ Quantidade insuficiente de falhas. "
                f"Mínimo necessário: {min_samples}. Encontrado: {stats['failures']}"
            )
        elif stats["failures"] < 10:
            self.validation_results["warnings"].append(
                WARNING_MESSAGES["FEW_SAMPLES"]
            )
        
        # Verifica taxa de censura
        if stats["censoring_rate"] > 50:
            self.validation_results["warnings"].append(
                WARNING_MESSAGES["HIGH_CENSORING"]
            )
    
    def display_validation_results(self):
        """Exibe os resultados da validação na interface"""
        results = self.validation_results
        
        # Exibe erros
        if results["errors"]:
            st.error("### ❌ Erros Encontrados")
            for error in results["errors"]:
                st.error(error)
        
        # Exibe avisos
        if results["warnings"]:
            st.warning("### ⚠️ Avisos")
            for warning in results["warnings"]:
                st.warning(warning)
        
        # Se válido, exibe sucesso e estatísticas
        if results["is_valid"]:
            st.success(SUCCESS_MESSAGES["DATA_VALIDATED"])
            
            # Exibe estatísticas
            st.subheader("📊 Estatísticas dos Dados")
            
            stats = results["stats"]
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "Total de Registros",
                    stats["total_records"],
                    help="Número total de linhas no arquivo"
                )
            
            with col2:
                st.metric(
                    "Registros Válidos",
                    stats["valid_records"],
                    help="Registros com dados válidos para análise"
                )
            
            with col3:
                st.metric(
                    "Falhas",
                    stats["failures"],
                    help="Número de eventos de falha observados"
                )
            
            with col4:
                st.metric(
                    "Censurados",
                    stats["censored"],
                    delta=f"{stats['censoring_rate']:.1f}%",
                    help="Registros censurados (sem falha observada)"
                )
            
            # Estatísticas de tempo
            if "mean_time" in stats:
                st.markdown("#### Estatísticas de Tempo")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Mínimo", f"{stats['min_time']:.2f}")
                with col2:
                    st.metric("Média", f"{stats['mean_time']:.2f}")
                with col3:
                    st.metric("Mediana", f"{stats['median_time']:.2f}")
                with col4:
                    st.metric("Máximo", f"{stats['max_time']:.2f}")
        
        return results["is_valid"]

