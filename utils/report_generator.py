"""
Módulo para geração de relatórios com gráficos
"""
import streamlit as st
import pandas as pd
from datetime import datetime
from typing import Dict, Optional
import io
import base64
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

from config.settings import COLORS


class ReportGenerator:
    """Classe para gerar relatórios de análise com gráficos"""
    
    def __init__(self, analysis_results: Dict, filename: str):
        """
        Inicializa o gerador de relatórios
        
        Args:
            analysis_results: Resultados da análise completa
            filename: Nome do arquivo original
        """
        self.results = analysis_results
        self.filename = filename
        self.weibull = analysis_results['weibull']
        self.metrics = analysis_results['metrics']
        self.tests = analysis_results['tests']
        self.interpretation = analysis_results['interpretation']
        self.weibull_obj = analysis_results['weibull_obj']
        self.metrics_obj = analysis_results['metrics_obj']
    
    def _create_probability_plot_html(self) -> str:
        """Cria gráfico de probabilidade em HTML"""
        from modules.visualization.weibull_plots import WeibullPlots
        
        plotter = WeibullPlots(self.weibull_obj, self.metrics_obj)
        fig = plotter.probability_plot()
        
        return fig.to_html(include_plotlyjs='cdn', full_html=False)
    
    def _create_reliability_plot_html(self) -> str:
        """Cria gráfico de confiabilidade em HTML"""
        from modules.visualization.weibull_plots import WeibullPlots
        
        plotter = WeibullPlots(self.weibull_obj, self.metrics_obj)
        fig = plotter.reliability_vs_time()
        
        return fig.to_html(include_plotlyjs='cdn', full_html=False)
    
    def _create_hazard_plot_html(self) -> str:
        """Cria gráfico de taxa de falha em HTML"""
        from modules.visualization.weibull_plots import WeibullPlots
        
        plotter = WeibullPlots(self.weibull_obj, self.metrics_obj)
        fig = plotter.hazard_rate_plot()
        
        return fig.to_html(include_plotlyjs='cdn', full_html=False)
    
    def _create_blife_plot_html(self) -> str:
        """Cria gráfico B-Life em HTML"""
        from modules.visualization.reliability_plots import ReliabilityPlots
        
        plotter = ReliabilityPlots(self.weibull_obj, self.metrics_obj)
        fig = plotter.b_life_chart()
        
        return fig.to_html(include_plotlyjs='cdn', full_html=False)
    
    def _create_combined_plot_html(self) -> str:
        """Cria gráfico combinado em HTML"""
        from modules.visualization.weibull_plots import WeibullPlots
        
        plotter = WeibullPlots(self.weibull_obj, self.metrics_obj)
        fig = plotter.combined_analysis_plot()
        
        return fig.to_html(include_plotlyjs='cdn', full_html=False)
    
    def generate_html_report(self) -> str:
        """
        Gera relatório completo em HTML com gráficos interativos
        
        Returns:
            String com HTML completo
        """
        # Gera gráficos
        prob_plot = self._create_probability_plot_html()
        rel_plot = self._create_reliability_plot_html()
        hazard_plot = self._create_hazard_plot_html()
        blife_plot = self._create_blife_plot_html()
        combined_plot = self._create_combined_plot_html()
        
        # Calcula taxa de censura
        censoring_rate = (self.weibull['n_censored']/(self.weibull['n_failures']+self.weibull['n_censored'])*100)
        
        # Gera HTML
        html = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Relatório de Análise de Weibull</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .header h1 {{
            margin: 0;
            font-size: 2.5em;
        }}
        .header p {{
            margin: 10px 0 0 0;
            font-size: 1.1em;
            opacity: 0.9;
        }}
        .section {{
            background: white;
            padding: 25px;
            margin-bottom: 25px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .section h2 {{
            color: #667eea;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
            margin-top: 0;
        }}
        .section h3 {{
            color: #764ba2;
            margin-top: 20px;
        }}
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        .metric-card {{
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }}
        .metric-card h4 {{
            margin: 0 0 10px 0;
            color: #555;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        .metric-card .value {{
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
            margin: 0;
        }}
        .metric-card .unit {{
            font-size: 0.9em;
            color: #777;
            margin-top: 5px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th {{
            background-color: #667eea;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: 600;
        }}
        td {{
            padding: 12px;
            border-bottom: 1px solid #ddd;
        }}
        tr:hover {{
            background-color: #f5f5f5;
        }}
        .alert {{
            padding: 15px;
            margin: 20px 0;
            border-radius: 5px;
            border-left: 5px solid;
        }}
        .alert-info {{
            background-color: #e3f2fd;
            border-color: #2196F3;
            color: #0d47a1;
        }}
        .alert-success {{
            background-color: #e8f5e9;
            border-color: #4caf50;
            color: #1b5e20;
        }}
        .alert-warning {{
            background-color: #fff3e0;
            border-color: #ff9800;
            color: #e65100;
        }}
        .badge {{
            display: inline-block;
            padding: 5px 10px;
            border-radius: 12px;
            font-size: 0.85em;
            font-weight: 600;
        }}
        .badge-success {{
            background-color: #4caf50;
            color: white;
        }}
        .badge-warning {{
            background-color: #ff9800;
            color: white;
        }}
        .badge-danger {{
            background-color: #f44336;
            color: white;
        }}
        .plot-container {{
            margin: 30px 0;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .footer {{
            text-align: center;
            margin-top: 40px;
            padding: 20px;
            color: #777;
            font-size: 0.9em;
            border-top: 2px solid #ddd;
        }}
        @media print {{
            body {{
                background-color: white;
            }}
            .section {{
                box-shadow: none;
                page-break-inside: avoid;
            }}
            .plot-container {{
                page-break-inside: avoid;
            }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 Relatório de Análise de Weibull</h1>
        <p>Análise de Confiabilidade e Vida Útil</p>
    </div>

    <!-- Informações Gerais -->
    <div class="section">
        <h2>📋 Informações Gerais</h2>
        <table>
            <tr>
                <th>Parâmetro</th>
                <th>Valor</th>
            </tr>
            <tr>
                <td><strong>Data da Análise</strong></td>
                <td>{datetime.now().strftime("%d/%m/%Y às %H:%M")}</td>
            </tr>
            <tr>
                <td><strong>Arquivo Analisado</strong></td>
                <td>{self.filename}</td>
            </tr>
            <tr>
                <td><strong>Método de Estimação</strong></td>
                <td>{self.weibull['method'].upper()}</td>
            </tr>
            <tr>
                <td><strong>Nível de Confiança</strong></td>
                <td>{self.weibull['confidence_level']*100:.0f}%</td>
            </tr>
        </table>
    </div>

    <!-- Resumo Executivo -->
    <div class="section">
        <h2>📊 Resumo Executivo</h2>
        
        <h3>Dados Analisados</h3>
        <div class="metrics-grid">
            <div class="metric-card">
                <h4>Total de Observações</h4>
                <p class="value">{self.weibull['n_failures'] + self.weibull['n_censored']}</p>
            </div>
            <div class="metric-card">
                <h4>Falhas Observadas</h4>
                <p class="value">{self.weibull['n_failures']}</p>
            </div>
            <div class="metric-card">
                <h4>Dados Censurados</h4>
                <p class="value">{self.weibull['n_censored']}</p>
            </div>
            <div class="metric-card">
                <h4>Taxa de Censura</h4>
                <p class="value">{censoring_rate:.1f}%</p>
            </div>
        </div>

        <h3>Parâmetros de Weibull</h3>
        <div class="metrics-grid">
            <div class="metric-card">
                <h4>β (Beta) - Forma</h4>
                <p class="value">{self.weibull['beta']:.4f}</p>
                <p class="unit">IC {self.weibull['confidence_level']*100:.0f}%: [{self.weibull['beta_ci'][0]:.4f}, {self.weibull['beta_ci'][1]:.4f}]</p>
            </div>
            <div class="metric-card">
                <h4>η (Eta) - Escala</h4>
                <p class="value">{self.weibull['eta']:.2f}</p>
                <p class="unit">{self.weibull['time_unit']}</p>
                <p class="unit">IC {self.weibull['confidence_level']*100:.0f}%: [{self.weibull['eta_ci'][0]:.2f}, {self.weibull['eta_ci'][1]:.2f}]</p>
            </div>
        </div>
    </div>

    <!-- Interpretação -->
    <div class="section">
        <h2>🔍 Interpretação dos Resultados</h2>
        
        <div class="alert alert-info">
            <h3>Modo de Falha Identificado</h3>
            <p><strong>{self.interpretation['failure_mode']}</strong></p>
        </div>

        <div class="alert alert-warning">
            <h3>Comportamento Observado</h3>
            <p>{self.interpretation['behavior']}</p>
        </div>

        <div class="alert alert-success">
            <h3>Recomendação</h3>
            <p>{self.interpretation['recommendation']}</p>
        </div>
    </div>

    <!-- Métricas de Confiabilidade -->
    <div class="section">
        <h2>📈 Métricas de Confiabilidade</h2>
        
        <table>
            <tr>
                <th>Métrica</th>
                <th>Valor</th>
                <th>Unidade</th>
            </tr>
            <tr>
                <td><strong>MTTF (Tempo Médio até Falha)</strong></td>
                <td>{self.metrics['mttf']:.2f}</td>
                <td>{self.weibull['time_unit']}</td>
            </tr>
            <tr>
                <td><strong>Vida Mediana</strong></td>
                <td>{self.metrics['median_life']:.2f}</td>
                <td>{self.weibull['time_unit']}</td>
            </tr>
            <tr>
                <td><strong>Vida Característica (η)</strong></td>
                <td>{self.metrics['characteristic_life']:.2f}</td>
                <td>{self.weibull['time_unit']}</td>
            </tr>
            <tr>
                <td><strong>Moda</strong></td>
                <td>{self.metrics['mode']:.2f}</td>
                <td>{self.weibull['time_unit']}</td>
            </tr>
            <tr>
                <td><strong>Desvio Padrão</strong></td>
                <td>{self.metrics['std_dev']:.2f}</td>
                <td>{self.weibull['time_unit']}</td>
            </tr>
        </table>

        <h3>B-Life (Percentis de Falha)</h3>
        <div class="metrics-grid">
            <div class="metric-card">
                <h4>B10 Life</h4>
                <p class="value">{self.metrics['b10_life']:.2f}</p>
                <p class="unit">{self.weibull['time_unit']}</p>
                <p class="unit">10% falharam</p>
            </div>
            <div class="metric-card">
                <h4>B50 Life</h4>
                <p class="value">{self.metrics['b50_life']:.2f}</p>
                <p class="unit">{self.weibull['time_unit']}</p>
                <p class="unit">50% falharam</p>
            </div>
            <div class="metric-card">
                <h4>B90 Life</h4>
                <p class="value">{self.metrics['b90_life']:.2f}</p>
                <p class="unit">{self.weibull['time_unit']}</p>
                <p class="unit">90% falharam</p>
            </div>
        </div>
    </div>

    <!-- Gráficos -->
    <div class="section">
        <h2>📊 Gráficos de Análise</h2>
        
        <h3>Gráfico de Probabilidade de Weibull</h3>
        <div class="plot-container">
            {prob_plot}
        </div>

        <h3>Confiabilidade vs Tempo</h3>
        <div class="plot-container">
            {rel_plot}
        </div>

        <h3>Taxa de Falha vs Tempo</h3>
        <div class="plot-container">
            {hazard_plot}
        </div>

        <h3>B-Life Chart</h3>
        <div class="plot-container">
            {blife_plot}
        </div>

        <h3>Análise Completa</h3>
        <div class="plot-container">
            {combined_plot}
        </div>
    </div>

    <!-- Testes de Adequação -->
    <div class="section">
        <h2>🧪 Testes de Adequação</h2>
        
        <h3>Coeficiente de Determinação (R²)</h3>
        <table>
            <tr>
                <th>Métrica</th>
                <th>Valor</th>
            </tr>
            <tr>
                <td><strong>R²</strong></td>
                <td>{self.tests['r_squared']['r_squared']:.4f} <span class="badge badge-{'success' if self.tests['r_squared']['r_squared'] > 0.95 else 'warning' if self.tests['r_squared']['r_squared'] > 0.90 else 'danger'}">{self.tests['r_squared']['quality']}</span></td>
            </tr>
            <tr>
                <td><strong>Interpretação</strong></td>
                <td>{self.tests['r_squared']['interpretation']}</td>
            </tr>
        </table>

        <h3>Teste de Anderson-Darling</h3>
        <table>
            <tr>
                <th>Métrica</th>
                <th>Valor</th>
            </tr>
            <tr>
                <td><strong>Estatística</strong></td>
                <td>{self.tests['anderson_darling']['statistic']:.4f}</td>
            </tr>
            <tr>
                <td><strong>Valor Crítico (α=0.05)</strong></td>
                <td>{self.tests['anderson_darling']['critical_value']:.4f}</td>
            </tr>
            <tr>
                <td><strong>Resultado</strong></td>
                <td><span class="badge badge-{'success' if self.tests['anderson_darling']['passed'] else 'warning'}">{"✅ APROVADO" if self.tests['anderson_darling']['passed'] else "⚠️ NÃO APROVADO"}</span></td>
            </tr>
            <tr>
                <td><strong>Interpretação</strong></td>
                <td>{self.tests['anderson_darling']['interpretation']}</td>
            </tr>
        </table>

        <h3>Teste de Kolmogorov-Smirnov</h3>
        <table>
            <tr>
                <th>Métrica</th>
                <th>Valor</th>
            </tr>
            <tr>
                <td><strong>Estatística</strong></td>
                <td>{self.tests['kolmogorov_smirnov']['statistic']:.4f}</td>
            </tr>
            <tr>
                <td><strong>P-valor</strong></td>
                <td>{self.tests['kolmogorov_smirnov']['p_value']:.4f}</td>
            </tr>
            <tr>
                <td><strong>Resultado</strong></td>
                <td><span class="badge badge-{'success' if self.tests['kolmogorov_smirnov']['passed'] else 'warning'}">{"✅ APROVADO" if self.tests['kolmogorov_smirnov']['passed'] else "⚠️ NÃO APROVADO"}</span></td>
            </tr>
            <tr>
                <td><strong>Interpretação</strong></td>
                <td>{self.tests['kolmogorov_smirnov']['interpretation']}</td>
            </tr>
        </table>
    </div>

    <!-- Aplicações Práticas -->
    <div class="section">
        <h2>💼 Aplicações Práticas</h2>
        
        <h3>Planejamento de Manutenção Preventiva</h3>
        <div class="alert alert-success">
            <p><strong>Intervalo de Manutenção Sugerido:</strong> {self.metrics['b10_life']*0.8:.0f} {self.weibull['time_unit']}</p>
            <p><em>Baseado em 80% do B10 Life</em></p>
        </div>

        <p><strong>Justificativa:</strong></p>
        <ul>
            <li>Com β = {self.weibull['beta']:.2f}, o equipamento apresenta {self.interpretation['failure_mode'].lower()}</li>
            <li>A manutenção preventiva neste intervalo deve capturar falhas antes que ocorram</li>
            <li>Aproximadamente 90% dos equipamentos devem sobreviver até este ponto</li>
        </ul>

        <h3>Estimativa de Confiabilidade</h3>
        <table>
            <tr>
                <th>Tempo de Operação</th>
                <th>Confiabilidade</th>
                <th>Risco de Falha</th>
            </tr>
            <tr>
                <td>{self.metrics['b10_life']*.5:.0f} {self.weibull['time_unit']}</td>
                <td>~95%</td>
                <td><span class="badge badge-success">Muito Baixo</span></td>
            </tr>
            <tr>
                <td>{self.metrics['b10_life']:.0f} {self.weibull['time_unit']}</td>
                <td>~90%</td>
                <td><span class="badge badge-success">Baixo</span></td>
            </tr>
            <tr>
                <td>{self.metrics['median_life']:.0f} {self.weibull['time_unit']}</td>
                <td>~50%</td>
                <td><span class="badge badge-warning">Médio</span></td>
            </tr>
            <tr>
                <td>{self.metrics['b90_life']:.0f} {self.weibull['time_unit']}</td>
                <td>~10%</td>
                <td><span class="badge badge-danger">Alto</span></td>
            </tr>
        </table>
    </div>

    <!-- Conclusões -->
    <div class="section">
        <h2>✅ Conclusões e Recomendações</h2>
        
        <h3>Conclusões Principais</h3>
        <ol>
            <li><strong>Característica de Falha:</strong> {self.interpretation['failure_mode']}
                <br>O parâmetro β = {self.weibull['beta']:.2f} indica {self.interpretation['behavior'].lower()}
            </li>
            <li><strong>Vida Útil Esperada:</strong>
                <ul>
                    <li>MTTF: {self.metrics['mttf']:.0f} {self.weibull['time_unit']}</li>
                    <li>Mediana: {self.metrics['median_life']:.0f} {self.weibull['time_unit']}</li>
                </ul>
            </li>
            <li><strong>Qualidade do Ajuste:</strong>
                <br>R² = {self.tests['r_squared']['r_squared']:.4f} ({self.tests['r_squared']['quality']})
                <br>Os testes estatísticos {"confirmam" if self.tests['anderson_darling']['passed'] and self.tests['kolmogorov_smirnov']['passed'] else "sugerem revisar"} a adequação da distribuição de Weibull
            </li>
        </ol>

        <h3>Recomendações</h3>
        <div class="alert alert-info">
            <p><strong>Estratégia de Manutenção:</strong></p>
            <p>{self.interpretation['recommendation']}</p>
        </div>
    </div>

    <!-- Rodapé -->
    <div class="footer">
        <p><strong>Weibull Reliability Analyzer v1.0</strong></p>
        <p>Relatório gerado automaticamente em {datetime.now().strftime("%d/%m/%Y às %H:%M")}</p>
        <p>© 2025 - Análise de Confiabilidade Industrial</p>
    </div>
</body>
</html>
"""
        
        return html
    
    def generate_markdown_report(self) -> str:
        """
        Gera relatório em formato Markdown (versão simplificada sem gráficos)
        
        Returns:
            String com relatório em Markdown
        """
        # Mantém a versão Markdown anterior para compatibilidade
        report = f"""# Relatório de Análise de Weibull

## Informações Gerais

**Data da Análise:** {datetime.now().strftime("%d/%m/%Y %H:%M")}  
**Arquivo Analisado:** {self.filename}  
**Método de Estimação:** {self.weibull['method'].upper()}  
**Nível de Confiança:** {self.weibull['confidence_level']*100:.0f}%

---

## Resumo Executivo

### Parâmetros de Weibull

**β (Beta):** {self.weibull['beta']:.4f} [IC: {self.weibull['beta_ci'][0]:.4f}, {self.weibull['beta_ci'][1]:.4f}]  
**η (Eta):** {self.weibull['eta']:.2f} {self.weibull['time_unit']} [IC: {self.weibull['eta_ci'][0]:.2f}, {self.weibull['eta_ci'][1]:.2f}]

### Interpretação

**Modo de Falha:** {self.interpretation['failure_mode']}  
**Recomendação:** {self.interpretation['recommendation']}

### Métricas Principais

- **MTTF:** {self.metrics['mttf']:.2f} {self.weibull['time_unit']}
- **Mediana:** {self.metrics['median_life']:.2f} {self.weibull['time_unit']}
- **B10:** {self.metrics['b10_life']:.2f} {self.weibull['time_unit']}

---

*Relatório gerado em {datetime.now().strftime("%d/%m/%Y às %H:%M")}*
"""
        
        return report
    
    def generate_summary_table(self) -> pd.DataFrame:
        """
        Gera tabela resumo dos resultados
        
        Returns:
            DataFrame com resumo
        """
        summary_data = {
            'Parâmetro': [
                'β (Beta)',
                'η (Eta)',
                'MTTF',
                'Vida Mediana',
                'B10 Life',
                'B50 Life',
                'B90 Life',
                'R²',
                'Modo de Falha'
            ],
            'Valor': [
                f"{self.weibull['beta']:.4f}",
                f"{self.weibull['eta']:.2f}",
                f"{self.metrics['mttf']:.2f}",
                f"{self.metrics['median_life']:.2f}",
                f"{self.metrics['b10_life']:.2f}",
                f"{self.metrics['b50_life']:.2f}",
                f"{self.metrics['b90_life']:.2f}",
                f"{self.tests['r_squared']['r_squared']:.4f}",
                self.interpretation['failure_mode']
            ],
            'Unidade': [
                '-',
                self.weibull['time_unit'],
                self.weibull['time_unit'],
                self.weibull['time_unit'],
                self.weibull['time_unit'],
                self.weibull['time_unit'],
                self.weibull['time_unit'],
                '-',
                '-'
            ]
        }
        
        return pd.DataFrame(summary_data)


def display_report_section(analysis_results: Dict, filename: str):
    """
    Exibe seção de relatórios no Streamlit
    
    Args:
        analysis_results: Resultados da análise
        filename: Nome do arquivo
    """
    st.subheader("📄 Exportar Relatório")
    
    generator = ReportGenerator(analysis_results, filename)
    
    # Opções de exportação
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Relatório HTML com gráficos
        html_report = generator.generate_html_report()
        
        st.download_button(
            label="📊 Relatório Completo (HTML com Gráficos)",
            data=html_report,
            file_name=f"relatorio_weibull_{datetime.now().strftime('%Y%m%d_%H%M')}.html",
            mime="text/html",
            help="Relatório interativo com gráficos (abra no navegador ou converta para PDF)"
        )
    
    with col2:
        # Relatório Markdown
        markdown_report = generator.generate_markdown_report()
        
        st.download_button(
            label="📝 Relatório Resumido (Markdown)",
            data=markdown_report,
            file_name=f"relatorio_weibull_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
            mime="text/markdown",
            help="Relatório em texto com formatação Markdown"
        )
    
    with col3:
        # Tabela Resumo
        summary_table = generator.generate_summary_table()
        csv_summary = summary_table.to_csv(index=False)
        
        st.download_button(
            label="📊 Tabela Resumo (CSV)",
            data=csv_summary,
            file_name=f"resumo_weibull_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
            help="Tabela com principais resultados em CSV"
        )
    
    # Informações adicionais
    st.info("""
    **💡 Dica:** O relatório HTML pode ser:
    - Aberto diretamente no navegador para visualização interativa
    - Impresso como PDF (Ctrl+P → Salvar como PDF)
    - Convertido para PDF usando ferramentas online
    - Os gráficos são interativos no navegador!
    """)
    
    # Preview do relatório HTML
    with st.expander("👁️ Pré-visualizar Relatório HTML", expanded=False):
        st.components.v1.html(html_report, height=800, scrolling=True)
