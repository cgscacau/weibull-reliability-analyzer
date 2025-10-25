"""
Módulo para processamento de dados
"""
import pandas as pd
import numpy as np
from typing import Dict, Optional, Tuple
import streamlit as st

from utils.constants import TIME_UNITS


class DataProcessor:
    """Classe para processar e preparar dados para análise"""
    
    def __init__(self, df: pd.DataFrame, column_mapping: Dict[str, str]):
        """
        Inicializa o processador
        
        Args:
            df: DataFrame original
            column_mapping: Mapeamento de colunas
        """
        self.df_original = df.copy()
        self.column_mapping = column_mapping
        self.df_processed = None
    
    def process(self, time_unit: str = "horas", 
                remove_outliers: bool = False,
                handle_duplicates: str = "keep_first") -> pd.DataFrame:
        """
        Processa os dados
        
        Args:
            time_unit: Unidade de tempo dos dados
            remove_outliers: Se deve remover outliers
            handle_duplicates: Como tratar duplicatas
        
        Returns:
            DataFrame processado
        """
        df = self.df_original.copy()
        
        # 1. Renomeia colunas para padrão
        df = self._rename_columns(df)
        
        # 2. Remove valores nulos
        df = self._remove_nulls(df)
        
        # 3. Trata duplicatas
        df = self._handle_duplicates(df, handle_duplicates)
        
        # 4. Adiciona coluna de status se não existir
        df = self._add_status_column(df)
        
        # 5. Remove outliers se solicitado
        if remove_outliers:
            df = self._remove_outliers(df)
        
        # 6. Ordena por tempo
        df = df.sort_values("tempo_falha").reset_index(drop=True)
        
        # 7. Adiciona metadados
        df.attrs["time_unit"] = time_unit
        df.attrs["processed"] = True
        
        self.df_processed = df
        
        return df
    
    def _rename_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Renomeia colunas para padrão"""
        rename_map = {}
        
        if "tempo_falha" in self.column_mapping:
            rename_map[self.column_mapping["tempo_falha"]] = "tempo_falha"
        
        if "status" in self.column_mapping:
            rename_map[self.column_mapping["status"]] = "status"
        
        if "equipamento" in self.column_mapping:
            rename_map[self.column_mapping["equipamento"]] = "equipamento"
        
        df = df.rename(columns=rename_map)
        
        return df
    
    def _remove_nulls(self, df: pd.DataFrame) -> pd.DataFrame:
        """Remove valores nulos da coluna de tempo"""
        initial_count = len(df)
        df = df.dropna(subset=["tempo_falha"])
        removed_count = initial_count - len(df)
        
        if removed_count > 0:
            st.info(f"ℹ️ {removed_count} registros com tempo nulo foram removidos.")
        
        return df
    
    def _handle_duplicates(self, df: pd.DataFrame, method: str) -> pd.DataFrame:
        """
        Trata registros duplicados
        
        Args:
            df: DataFrame
            method: Método de tratamento (keep_first, keep_last, remove_all)
        """
        initial_count = len(df)
        
        if method == "keep_first":
            df = df.drop_duplicates(subset=["tempo_falha"], keep="first")
        elif method == "keep_last":
            df = df.drop_duplicates(subset=["tempo_falha"], keep="last")
        elif method == "remove_all":
            df = df.drop_duplicates(subset=["tempo_falha"], keep=False)
        
        removed_count = initial_count - len(df)
        
        if removed_count > 0:
            st.info(f"ℹ️ {removed_count} registros duplicados foram tratados.")
        
        return df
    
    def _add_status_column(self, df: pd.DataFrame) -> pd.DataFrame:
        """Adiciona coluna de status se não existir"""
        if "status" not in df.columns:
            # Assume todas como falhas
            df["status"] = 1
            st.info("ℹ️ Coluna de status criada. Todos os registros marcados como falhas.")
        else:
            # Garante que status é 0 ou 1
            df["status"] = df["status"].apply(lambda x: 1 if x != 0 else 0)
        
        return df
    
    def _remove_outliers(self, df: pd.DataFrame, method: str = "iqr") -> pd.DataFrame:
        """
        Remove outliers dos dados
        
        Args:
            df: DataFrame
            method: Método de detecção (iqr, zscore)
        """
        initial_count = len(df)
        
        if method == "iqr":
            Q1 = df["tempo_falha"].quantile(0.25)
            Q3 = df["tempo_falha"].quantile(0.75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - 3 * IQR
            upper_bound = Q3 + 3 * IQR
            
            df = df[(df["tempo_falha"] >= lower_bound) & (df["tempo_falha"] <= upper_bound)]
        
        elif method == "zscore":
            from scipy import stats
            z_scores = np.abs(stats.zscore(df["tempo_falha"]))
            df = df[z_scores < 3]
        
        removed_count = initial_count - len(df)
        
        if removed_count > 0:
            st.warning(f"⚠️ {removed_count} outliers foram removidos dos dados.")
        
        return df
    
    def get_summary(self) -> Dict:
        """Retorna resumo do processamento"""
        if self.df_processed is None:
            return {}
        
        return {
            "original_count": len(self.df_original),
            "processed_count": len(self.df_processed),
            "removed_count": len(self.df_original) - len(self.df_processed),
            "failures": int((self.df_processed["status"] == 1).sum()),
            "censored": int((self.df_processed["status"] == 0).sum()),
            "time_unit": self.df_processed.attrs.get("time_unit", "N/A")
        }
    
    def display_processed_data(self):
        """Exibe os dados processados"""
        if self.df_processed is None:
            st.error("Dados ainda não foram processados.")
            return
        
        st.subheader("✅ Dados Processados")
        
        # Resumo
        summary = self.get_summary()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Registros Processados", summary["processed_count"])
        with col2:
            st.metric("Falhas", summary["failures"])
        with col3:
            st.metric("Censurados", summary["censored"])
        
        # Preview dos dados
        with st.expander("👁️ Visualizar Dados Processados", expanded=True):
            st.dataframe(self.df_processed, use_container_width=True)
            
            # Botão de download
            csv = self.df_processed.to_csv(index=False)
            st.download_button(
                label="📥 Baixar Dados Processados (CSV)",
                data=csv,
                file_name="dados_processados.csv",
                mime="text/csv"
            )

