"""
Módulo para gráficos de Weibull
"""
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Dict, Optional
import streamlit as st

from config.settings import COLORS, PLOT_CONFIG


class WeibullPlots:
    """Classe para criar gráficos de Weibull"""
    
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
    
    def probability_plot(self) -> go.Figure:
        """
        Cria gráfico de probabilidade de Weibull
        
        Returns:
            Figura Plotly
        """
        # Dados observados
        sorted_failures = np.sort(self.analysis.failures)
        n = len(sorted_failures)
        
        # Median ranks
        ranks = np.arange(1, n + 1)
        median_ranks = (ranks - 0.3) / (n + 0.4)
        
        # Linha teórica de Weibull
        t_theory = np.linspace(sorted_failures.min() * 0.5, 
                              sorted_failures.max() * 1.2, 100)
        F_theory = self.analysis.unreliability(t_theory)
        
        # Cria figura
        fig = go.Figure()
        
        # Pontos observados
        fig.add_trace(go.Scatter(
            x=sorted_failures,
            y=median_ranks * 100,
            mode='markers',
            name='Dados Observados',
            marker=dict(
                size=8,
                color=COLORS["primary"],
                symbol='circle',
                line=dict(width=1, color='white')
            ),
            hovertemplate='<b>Tempo:</b> %{x:.2f} ' + self.time_unit + '<br>' +
                         '<b>Probabilidade:</b> %{y:.2f}%<br>' +
                         '<extra></extra>'
        ))
        
        # Linha teórica
        fig.add_trace(go.Scatter(
            x=t_theory,
            y=F_theory * 100,
            mode='lines',
            name='Ajuste Weibull',
            line=dict(
                color=COLORS["danger"],
                width=2,
                dash='solid'
            ),
            hovertemplate='<b>Tempo:</b> %{x:.2f} ' + self.time_unit + '<br>' +
                         '<b>Probabilidade Teórica:</b> %{y:.2f}%<br>' +
                         '<extra></extra>'
        ))
        
        # Intervalos de confiança
        beta_lower = self.results["beta_ci"][0]
        beta_upper = self.results["beta_ci"][1]
        eta = self.results["eta"]
        
        F_lower = 1 - np.exp(-(t_theory / eta) ** beta_lower)
        F_upper = 1 - np.exp(-(t_theory / eta) ** beta_upper)
        
        fig.add_trace(go.Scatter(
            x=np.concatenate([t_theory, t_theory[::-1]]),
            y=np.concatenate([F_lower * 100, F_upper[::-1] * 100]),
            fill='toself',
            fillcolor='rgba(31, 119, 180, 0.2)',
            line=dict(color='rgba(255,255,255,0)'),
            name=f'IC {self.results["confidence_level"]*100:.0f}%',
            showlegend=True,
            hoverinfo='skip'
        ))
        
        # Layout
        fig.update_layout(
            title=dict(
                text='<b>Gráfico de Probabilidade de Weibull</b>',
                font=dict(size=PLOT_CONFIG["title_font_size"])
            ),
            xaxis=dict(
                title=f'Tempo até Falha ({self.time_unit})',
                type='log',
                showgrid=True,
                gridcolor='lightgray'
            ),
            yaxis=dict(
                title='Probabilidade de Falha (%)',
                showgrid=True,
                gridcolor='lightgray'
            ),
            template=PLOT_CONFIG["template"],
            height=PLOT_CONFIG["height"],
            hovermode='closest',
            legend=dict(
                orientation="v",
                yanchor="bottom",
                y=0.02,
                xanchor="right",
                x=0.98
            )
        )
        
        return fig
    
    def reliability_vs_time(self) -> go.Figure:
        """
        Cria gráfico de confiabilidade vs tempo
        
        Returns:
            Figura Plotly
        """
        # Gera pontos de tempo
        t_max = max(self.analysis.failures) * 1.5
        t = np.linspace(0, t_max, 200)
        
        # Calcula confiabilidade
        R = self.analysis.reliability(t)
        
        # Cria figura
        fig = go.Figure()
        
        # Curva de confiabilidade
        fig.add_trace(go.Scatter(
            x=t,
            y=R * 100,
            mode='lines',
            name='Confiabilidade R(t)',
            line=dict(
                color=COLORS["success"],
                width=3
            ),
            fill='tozeroy',
            fillcolor='rgba(44, 160, 44, 0.2)',
            hovertemplate='<b>Tempo:</b> %{x:.2f} ' + self.time_unit + '<br>' +
                         '<b>Confiabilidade:</b> %{y:.2f}%<br>' +
                         '<extra></extra>'
        ))
        
        # Adiciona linhas de referência
        for reliability_level in [90, 50, 10]:
            time_at_level = self.analysis.b_life(100 - reliability_level)
            
            if time_at_level <= t_max:
                fig.add_hline(
                    y=reliability_level,
                    line_dash="dash",
                    line_color="gray",
                    opacity=0.5,
                    annotation_text=f"R = {reliability_level}%",
                    annotation_position="right"
                )
                
                fig.add_vline(
                    x=time_at_level,
                    line_dash="dash",
                    line_color="gray",
                    opacity=0.5,
                    annotation_text=f"t = {time_at_level:.1f}",
                    annotation_position="top"
                )
        
        # Layout
        fig.update_layout(
            title=dict(
                text='<b>Confiabilidade vs Tempo</b>',
                font=dict(size=PLOT_CONFIG["title_font_size"])
            ),
            xaxis=dict(
                title=f'Tempo ({self.time_unit})',
                showgrid=True,
                gridcolor='lightgray'
            ),
            yaxis=dict(
                title='Confiabilidade R(t) (%)',
                range=[0, 105],
                showgrid=True,
                gridcolor='lightgray'
            ),
            template=PLOT_CONFIG["template"],
            height=PLOT_CONFIG["height"],
            hovermode='x unified'
        )
        
        return fig
    
    def hazard_rate_plot(self) -> go.Figure:
        """
        Cria gráfico de taxa de falha
        
        Returns:
            Figura Plotly
        """
        # Gera pontos de tempo
        t_max = max(self.analysis.failures) * 1.5
        t = np.linspace(0.01, t_max, 200)
        
        # Calcula taxa de falha
        h = self.analysis.hazard_rate(t)
        
        # Cria figura
        fig = go.Figure()
        
        # Curva de taxa de falha
        fig.add_trace(go.Scatter(
            x=t,
            y=h,
            mode='lines',
            name='Taxa de Falha h(t)',
            line=dict(
                color=COLORS["danger"],
                width=3
            ),
            fill='tozeroy',
            fillcolor='rgba(214, 39, 40, 0.2)',
            hovertemplate='<b>Tempo:</b> %{x:.2f} ' + self.time_unit + '<br>' +
                         '<b>Taxa de Falha:</b> %{y:.4f}<br>' +
                         '<extra></extra>'
        ))
        
        # Determina comportamento
        beta = self.results["beta"]
        
        if beta < 1:
            behavior_text = "Taxa Decrescente (β < 1)<br>Mortalidade Infantil"
            behavior_color = COLORS["warning"]
        elif 0.9 <= beta <= 1.1:
            behavior_text = "Taxa Constante (β ≈ 1)<br>Vida Útil"
            behavior_color = COLORS["info"]
        else:
            behavior_text = "Taxa Crescente (β > 1)<br>Desgaste"
            behavior_color = COLORS["danger"]
        
        # Adiciona anotação
        fig.add_annotation(
            x=t_max * 0.7,
            y=max(h) * 0.8,
            text=behavior_text,
            showarrow=False,
            bgcolor=behavior_color,
            opacity=0.8,
            font=dict(color="white", size=12),
            borderpad=10
        )
        
        # Layout
        fig.update_layout(
            title=dict(
                text='<b>Taxa de Falha vs Tempo</b>',
                font=dict(size=PLOT_CONFIG["title_font_size"])
            ),
            xaxis=dict(
                title=f'Tempo ({self.time_unit})',
                showgrid=True,
                gridcolor='lightgray'
            ),
            yaxis=dict(
                title='Taxa de Falha h(t)',
                showgrid=True,
                gridcolor='lightgray'
            ),
            template=PLOT_CONFIG["template"],
            height=PLOT_CONFIG["height"],
            hovermode='x unified'
        )
        
        return fig
    
    def pdf_cdf_plot(self) -> go.Figure:
        """
        Cria gráfico combinado de PDF e CDF
        
        Returns:
            Figura Plotly com subplots
        """
        # Gera pontos de tempo
        t_max = max(self.analysis.failures) * 1.5
        t = np.linspace(0.01, t_max, 200)
        
        # Calcula PDF e CDF
        pdf = self.analysis.pdf(t)
        cdf = self.analysis.unreliability(t)
        
        # Cria subplots
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Função Densidade de Probabilidade (PDF)', 
                          'Função Distribuição Acumulada (CDF)')
        )
        
        # PDF
        fig.add_trace(
            go.Scatter(
                x=t,
                y=pdf,
                mode='lines',
                name='PDF f(t)',
                line=dict(color=COLORS["primary"], width=3),
                fill='tozeroy',
                fillcolor='rgba(31, 119, 180, 0.2)',
                hovertemplate='<b>Tempo:</b> %{x:.2f}<br>' +
                             '<b>PDF:</b> %{y:.4f}<br>' +
                             '<extra></extra>'
            ),
            row=1, col=1
        )
        
        # CDF
        fig.add_trace(
            go.Scatter(
                x=t,
                y=cdf * 100,
                mode='lines',
                name='CDF F(t)',
                line=dict(color=COLORS["secondary"], width=3),
                fill='tozeroy',
                fillcolor='rgba(255, 127, 14, 0.2)',
                hovertemplate='<b>Tempo:</b> %{x:.2f}<br>' +
                             '<b>CDF:</b> %{y:.2f}%<br>' +
                             '<extra></extra>'
            ),
            row=1, col=2
        )
        
        # Adiciona moda no PDF
        metrics = self.metrics.calculate_all_metrics()
        if metrics["mode"] > 0:
            mode_pdf = self.analysis.pdf(np.array([metrics["mode"]]))[0]
            fig.add_trace(
                go.Scatter(
                    x=[metrics["mode"]],
                    y=[mode_pdf],
                    mode='markers',
                    name='Moda',
                    marker=dict(size=12, color=COLORS["danger"], symbol='diamond'),
                    showlegend=False,
                    hovertemplate='<b>Moda:</b> %{x:.2f}<br>' +
                                 '<extra></extra>'
                ),
                row=1, col=1
            )
        
        # Layout
        fig.update_xaxes(title_text=f'Tempo ({self.time_unit})', row=1, col=1)
        fig.update_xaxes(title_text=f'Tempo ({self.time_unit})', row=1, col=2)
        fig.update_yaxes(title_text='Densidade de Probabilidade', row=1, col=1)
        fig.update_yaxes(title_text='Probabilidade Acumulada (%)', row=1, col=2)
        
        fig.update_layout(
            title=dict(
                text='<b>Distribuição de Weibull - PDF e CDF</b>',
                font=dict(size=PLOT_CONFIG["title_font_size"])
            ),
            template=PLOT_CONFIG["template"],
            height=PLOT_CONFIG["height"],
            showlegend=False,
            hovermode='closest'
        )
        
        return fig
    
    def combined_analysis_plot(self) -> go.Figure:
        """
        Cria gráfico combinado com múltiplas visualizações
        
        Returns:
            Figura Plotly com subplots
        """
        # Gera pontos de tempo
        t_max = max(self.analysis.failures) * 1.5
        t = np.linspace(0.01, t_max, 200)
        
        # Cria subplots 2x2
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                'Confiabilidade R(t)',
                'Taxa de Falha h(t)',
                'PDF f(t)',
                'Dados vs Ajuste'
            ),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # 1. Confiabilidade
        R = self.analysis.reliability(t)
        fig.add_trace(
            go.Scatter(x=t, y=R*100, name='R(t)', 
                      line=dict(color=COLORS["success"], width=2),
                      showlegend=False),
            row=1, col=1
        )
        
        # 2. Taxa de Falha
        h = self.analysis.hazard_rate(t)
        fig.add_trace(
            go.Scatter(x=t, y=h, name='h(t)',
                      line=dict(color=COLORS["danger"], width=2),
                      showlegend=False),
            row=1, col=2
        )
        
        # 3. PDF
        pdf = self.analysis.pdf(t)
        fig.add_trace(
            go.Scatter(x=t, y=pdf, name='f(t)',
                      line=dict(color=COLORS["primary"], width=2),
                      fill='tozeroy',
                      showlegend=False),
            row=2, col=1
        )
        
        # 4. Dados vs Ajuste
        sorted_failures = np.sort(self.analysis.failures)
        n = len(sorted_failures)
        ranks = np.arange(1, n + 1)
        median_ranks = (ranks - 0.3) / (n + 0.4)
        
        fig.add_trace(
            go.Scatter(x=sorted_failures, y=median_ranks*100,
                      mode='markers', name='Dados',
                      marker=dict(color=COLORS["primary"], size=6),
                      showlegend=False),
            row=2, col=2
        )
        
        F_theory = self.analysis.unreliability(t)
        fig.add_trace(
            go.Scatter(x=t, y=F_theory*100, name='Ajuste',
                      line=dict(color=COLORS["danger"], width=2),
                      showlegend=False),
            row=2, col=2
        )
        
        # Atualiza eixos
        fig.update_xaxes(title_text=f'Tempo ({self.time_unit})', row=1, col=1)
        fig.update_xaxes(title_text=f'Tempo ({self.time_unit})', row=1, col=2)
        fig.update_xaxes(title_text=f'Tempo ({self.time_unit})', row=2, col=1)
        fig.update_xaxes(title_text=f'Tempo ({self.time_unit})', row=2, col=2)
        
        fig.update_yaxes(title_text='R(t) (%)', row=1, col=1)
        fig.update_yaxes(title_text='h(t)', row=1, col=2)
        fig.update_yaxes(title_text='f(t)', row=2, col=1)
        fig.update_yaxes(title_text='F(t) (%)', row=2, col=2)
        
        # Layout
        fig.update_layout(
            title=dict(
                text='<b>Análise Completa de Weibull</b>',
                font=dict(size=PLOT_CONFIG["title_font_size"])
            ),
            template=PLOT_CONFIG["template"],
            height=800,
            showlegend=False
        )
        
        return fig

