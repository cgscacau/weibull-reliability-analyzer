"""
Módulo para comparação de análises
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from typing import List, Dict
import numpy as np

from config.settings import COLORS


class AnalysisComparison:
    """Classe para comparar múltiplas análises"""
    
    def __init__(self):
        """Inicializa comparador"""
        self.analyses = []
    
    def add_analysis(self, name: str, weibull_obj, label: str = None):
        """
        Adiciona uma análise para comparação
        
        Args:
            name: Nome identificador
            weibull_obj: Objeto WeibullAnalysis
            label: Label para exibição (opcional)
        """
        self.analyses.append({
            'name': name,
            'label': label or name,
            'weibull': weibull_obj,
            'results': weibull_obj.results
        })
    
    def compare_parameters(self) -> go.Figure:
        """
        Compara parâmetros de Weibull
        
        Returns:
            Figura Plotly
        """
        if len(self.analyses) < 2:
            st.warning("Adicione pelo menos 2 análises para comparar")
            return None
        
        labels = [a['label'] for a in self.analyses]
        betas = [a['results']['beta'] for a in self.analyses]
        etas = [a['results']['eta'] for a in self.analyses]
        
        fig = go.Figure()
        
        # Beta
        fig.add_trace(go.Bar(
            name='β (Beta)',
            x=labels,
            y=betas,
            marker_color=COLORS['primary'],
            text=[f'{b:.3f}' for b in betas],
            textposition='outside'
        ))
        
        # Eta (em escala secundária)
        fig.add_trace(go.Bar(
            name='η (Eta)',
            x=labels,
            y=etas,
            marker_color=COLORS['secondary'],
            text=[f'{e:.1f}' for e in etas],
            textposition='outside',
            yaxis='y2'
        ))
        
        fig.update_layout(
            title='<b>Comparação de Parâmetros de Weibull</b>',
            xaxis_title='Análises',
            yaxis=dict(title='β (Beta)', side='left'),
            yaxis2=dict(title='η (Eta)', side='right', overlaying='y'),
            barmode='group',
            height=500,
            showlegend=True
        )
        
        return fig
    
    def compare_reliability(self, time_points: np.ndarray = None) -> go.Figure:
        """
        Compara curvas de confiabilidade
        
        Args:
            time_points: Pontos de tempo para plotar
        
        Returns:
            Figura Plotly
        """
        if len(self.analyses) < 2:
            return None
        
        # Define pontos de tempo se não fornecidos
        if time_points is None:
            max_time = max([a['weibull'].failures.max() for a in self.analyses])
            time_points = np.linspace(0, max_time * 1.5, 200)
        
        fig = go.Figure()
        
        colors = [COLORS['primary'], COLORS['secondary'], COLORS['success'], 
                 COLORS['danger'], COLORS['warning'], COLORS['info']]
        
        for i, analysis in enumerate(self.analyses):
            R = analysis['weibull'].reliability(time_points)
            
            fig.add_trace(go.Scatter(
                x=time_points,
                y=R * 100,
                mode='lines',
                name=analysis['label'],
                line=dict(color=colors[i % len(colors)], width=3),
                hovertemplate='<b>%{fullData.name}</b><br>' +
                             'Tempo: %{x:.1f}<br>' +
                             'Confiabilidade: %{y:.2f}%<br>' +
                             '<extra></extra>'
            ))
        
        fig.update_layout(
            title='<b>Comparação de Confiabilidade</b>',
            xaxis_title='Tempo',
            yaxis_title='Confiabilidade R(t) (%)',
            height=500,
            hovermode='x unified',
            legend=dict(
                orientation="v",
                yanchor="top",
                y=0.98,
                xanchor="right",
                x=0.98
            )
        )
        
        return fig
    
    def compare_metrics_table(self) -> pd.DataFrame:
        """
        Cria tabela comparativa de métricas
        
        Returns:
            DataFrame com comparação
        """
        from modules.analysis.reliability_metrics import ReliabilityMetrics
        
        data = []
        
        for analysis in self.analyses:
            metrics_calc = ReliabilityMetrics(analysis['weibull'])
            metrics = metrics_calc.calculate_all_metrics()
            
            data.append({
                'Análise': analysis['label'],
                'β': f"{analysis['results']['beta']:.4f}",
                'η': f"{analysis['results']['eta']:.2f}",
                'MTTF': f"{metrics['mttf']:.2f}",
                'Mediana': f"{metrics['median_life']:.2f}",
                'B10': f"{metrics['b10_life']:.2f}",
                'B90': f"{metrics['b90_life']:.2f}",
                'Modo': analysis['weibull'].get_interpretation()['failure_mode']
            })
        
        return pd.DataFrame(data)
