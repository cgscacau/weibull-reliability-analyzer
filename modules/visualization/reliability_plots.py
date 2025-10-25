"""
Módulo para gráficos de confiabilidade adicionais
"""
import numpy as np
import plotly.graph_objects as go
from typing import Dict, List
import pandas as pd

from config.settings import COLORS, PLOT_CONFIG


class ReliabilityPlots:
    """Classe para gráficos de confiabilidade adicionais"""
    
    def __init__(self, weibull_analysis, metrics_calculator):
        """
        Inicializa com resultados da análise
        
        Args:
            weibull_analysis: Instância de WeibullAnalysis
            metrics_calculator: Instância de ReliabilityMetrics
        """
        self.analysis = weibull_analysis
        self.metrics = metrics_calculator
        self.results = weibull_analysis.results
        self.time_unit = self.results["time_unit"]
    
    def b_life_chart(self) -> go.Figure:
        """
        Cria gráfico de B-life (B10, B50, B90, etc)
        
        Returns:
            Figura Plotly
        """
        # Percentis para calcular
        percentiles = [1, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 99]
        b_lives = [self.analysis.b_life(p) for p in percentiles]
        
        # Cria figura
        fig = go.Figure()
        
        # Barras
        fig.add_trace(go.Bar(
            x=[f'B{p}' for p in percentiles],
            y=b_lives,
            marker=dict(
                color=b_lives,
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title=f"Tempo<br>({self.time_unit})")
            ),
            text=[f'{b:.1f}' for b in b_lives],
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>' +
                         f'Tempo: %{{y:.2f}} {self.time_unit}<br>' +
                         '<extra></extra>'
        ))
        
        # Layout
        fig.update_layout(
            title=dict(
                text='<b>B-Life: Tempo de Falha por Percentil</b>',
                font=dict(size=PLOT_CONFIG["title_font_size"])
            ),
            xaxis=dict(
                title='Percentil de Falha',
                showgrid=False
            ),
            yaxis=dict(
                title=f'Tempo até Falha ({self.time_unit})',
                showgrid=True,
                gridcolor='lightgray'
            ),
            template=PLOT_CONFIG["template"],
            height=PLOT_CONFIG["height"],
            showlegend=False
        )
        
        return fig
    
    def metrics_comparison(self) -> go.Figure:
        """
        Cria gráfico comparativo de métricas principais
        
        Returns:
            Figura Plotly
        """
        metrics = self.metrics.calculate_all_metrics()
        
        # Seleciona métricas principais
        metric_names = ['MTTF', 'Mediana', 'B10', 'B90', 'Vida\nCaracterística']
        metric_values = [
            metrics['mttf'],
            metrics['median_life'],
            metrics['b10_life'],
            metrics['b90_life'],
            metrics['characteristic_life']
        ]
        
        # Cria figura
        fig = go.Figure()
        
        # Barras horizontais
        fig.add_trace(go.Bar(
            y=metric_names,
            x=metric_values,
            orientation='h',
            marker=dict(
                color=[COLORS["primary"], COLORS["success"], COLORS["warning"],
                      COLORS["danger"], COLORS["info"]],
            ),
            text=[f'{v:.1f}' for v in metric_values],
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>' +
                         f'Valor: %{{x:.2f}} {self.time_unit}<br>' +
                         '<extra></extra>'
        ))
        
        # Layout
        fig.update_layout(
            title=dict(
                text='<b>Comparação de Métricas de Vida</b>',
                font=dict(size=PLOT_CONFIG["title_font_size"])
            ),
            xaxis=dict(
                title=f'Tempo ({self.time_unit})',
                showgrid=True,
                gridcolor='lightgray'
            ),
            yaxis=dict(
                showgrid=False
            ),
            template=PLOT_CONFIG["template"],
            height=400,
            showlegend=False
        )
        
        return fig
    
    def failure_distribution_histogram(self) -> go.Figure:
        """
        Cria histograma dos tempos de falha
        
        Returns:
            Figura Plotly
        """
        failures = self.analysis.failures
        
        # Cria figura
        fig = go.Figure()
        
        # Histograma
        fig.add_trace(go.Histogram(
            x=failures,
            nbinsx=20,
            name='Falhas Observadas',
            marker=dict(
                color=COLORS["primary"],
                line=dict(color='white', width=1)
            ),
            opacity=0.7,
            hovertemplate='<b>Intervalo:</b> %{x}<br>' +
                         '<b>Frequência:</b> %{y}<br>' +
                         '<extra></extra>'
        ))
        
        # Curva PDF teórica sobreposta
        t = np.linspace(failures.min(), failures.max(), 100)
        pdf = self.analysis.pdf(t)
        
        # Escala PDF para combinar com histograma
        hist_counts, _ = np.histogram(failures, bins=20)
        scale_factor = max(hist_counts) / max(pdf) if max(pdf) > 0 else 1
        
        fig.add_trace(go.Scatter(
            x=t,
            y=pdf * scale_factor,
            mode='lines',
            name='Distribuição Teórica',
            line=dict(
                color=COLORS["danger"],
                width=3
            ),
            hovertemplate='<b>Tempo:</b> %{x:.2f}<br>' +
                         '<b>Densidade (escala):</b> %{y:.2f}<br>' +
                         '<extra></extra>'
        ))
        
        # Layout
        fig.update_layout(
            title=dict(
                text='<b>Distribuição dos Tempos de Falha</b>',
                font=dict(size=PLOT_CONFIG["title_font_size"])
            ),
            xaxis=dict(
                title=f'Tempo até Falha ({self.time_unit})',
                showgrid=True,
                gridcolor='lightgray'
            ),
            yaxis=dict(
                title='Frequência',
                showgrid=True,
                gridcolor='lightgray'
            ),
            template=PLOT_CONFIG["template"],
            height=PLOT_CONFIG["height"],
            barmode='overlay',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        return fig

