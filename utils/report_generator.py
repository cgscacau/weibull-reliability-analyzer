"""
Módulo para geração de relatórios
"""
import streamlit as st
import pandas as pd
from datetime import datetime
from typing import Dict, Optional
import io


class ReportGenerator:
    """Classe para gerar relatórios de análise"""
    
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
    
    def generate_markdown_report(self) -> str:
        """
        Gera relatório em formato Markdown
        
        Returns:
            String com relatório em Markdown
        """
        report = f"""# Relatório de Análise de Weibull

## Informações Gerais

**Data da Análise:** {datetime.now().strftime("%d/%m/%Y %H:%M")}  
**Arquivo Analisado:** {self.filename}  
**Método de Estimação:** {self.weibull['method'].upper()}  
**Nível de Confiança:** {self.weibull['confidence_level']*100:.0f}%

---

## 1. Resumo Executivo

### Dados Analisados
- **Total de Observações:** {self.weibull['n_failures'] + self.weibull['n_censored']}
- **Falhas Observadas:** {self.weibull['n_failures']}
- **Dados Censurados:** {self.weibull['n_censored']}
- **Taxa de Censura:** {(self.weibull['n_censored']/(self.weibull['n_failures']+self.weibull['n_censored'])*100):.1f}%

### Parâmetros de Weibull Estimados

**β (Beta) - Parâmetro de Forma:** {self.weibull['beta']:.4f}  
*Intervalo de Confiança {self.weibull['confidence_level']*100:.0f}%:* [{self.weibull['beta_ci'][0]:.4f}, {self.weibull['beta_ci'][1]:.4f}]

**η (Eta) - Parâmetro de Escala:** {self.weibull['eta']:.2f} {self.weibull['time_unit']}  
*Intervalo de Confiança {self.weibull['confidence_level']*100:.0f}%:* [{self.weibull['eta_ci'][0]:.2f}, {self.weibull['eta_ci'][1]:.2f}] {self.weibull['time_unit']}

---

## 2. Interpretação dos Resultados

### Modo de Falha Identificado
**{self.interpretation['failure_mode']}**

### Comportamento Observado
{self.interpretation['behavior']}

### Recomendação
{self.interpretation['recommendation']}

---

## 3. Métricas de Confiabilidade

| Métrica | Valor | Unidade |
|---------|-------|---------|
| MTTF (Tempo Médio até Falha) | {self.metrics['mttf']:.2f} | {self.weibull['time_unit']} |
| Vida Mediana | {self.metrics['median_life']:.2f} | {self.weibull['time_unit']} |
| Vida Característica (η) | {self.metrics['characteristic_life']:.2f} | {self.weibull['time_unit']} |
| Moda | {self.metrics['mode']:.2f} | {self.weibull['time_unit']} |
| Desvio Padrão | {self.metrics['std_dev']:.2f} | {self.weibull['time_unit']} |
| Coeficiente de Variação | {self.metrics['coefficient_of_variation']:.4f} | - |

### B-Life (Percentis de Falha)

| Percentil | Tempo | Interpretação |
|-----------|-------|---------------|
| B10 | {self.metrics['b10_life']:.2f} {self.weibull['time_unit']} | 10% da população falhou |
| B50 | {self.metrics['b50_life']:.2f} {self.weibull['time_unit']} | 50% da população falhou (mediana) |
| B90 | {self.metrics['b90_life']:.2f} {self.weibull['time_unit']} | 90% da população falhou |

---

## 4. Testes de Adequação

### Coeficiente de Determinação (R²)
**Valor:** {self.tests['r_squared']['r_squared']:.4f}  
**Qualidade:** {self.tests['r_squared']['quality']}  
**Interpretação:** {self.tests['r_squared']['interpretation']}

### Teste de Anderson-Darling
**Estatística:** {self.tests['anderson_darling']['statistic']:.4f}  
**Valor Crítico (α=0.05):** {self.tests['anderson_darling']['critical_value']:.4f}  
**Resultado:** {"✅ APROVADO" if self.tests['anderson_darling']['passed'] else "⚠️ NÃO APROVADO"}  
**Interpretação:** {self.tests['anderson_darling']['interpretation']}

### Teste de Kolmogorov-Smirnov
**Estatística:** {self.tests['kolmogorov_smirnov']['statistic']:.4f}  
**P-valor:** {self.tests['kolmogorov_smirnov']['p_value']:.4f}  
**Resultado:** {"✅ APROVADO" if self.tests['kolmogorov_smirnov']['passed'] else "⚠️ NÃO APROVADO"}  
**Interpretação:** {self.tests['kolmogorov_smirnov']['interpretation']}

---

## 5. Aplicações Práticas

### Planejamento de Manutenção Preventiva

Baseado na análise, recomenda-se:

**Intervalo de Manutenção Sugerido:** {self.metrics['b10_life']*0.8:.0f} {self.weibull['time_unit']}  
*(Baseado em 80% do B10 Life)*

**Justificativa:**
- Com β = {self.weibull['beta']:.2f}, o equipamento apresenta {self.interpretation['failure_mode'].lower()}
- A manutenção preventiva neste intervalo deve capturar falhas antes que ocorram
- Aproximadamente 90% dos equipamentos devem sobreviver até este ponto

### Estimativa de Confiabilidade

| Tempo de Operação | Confiabilidade | Risco de Falha |
|-------------------|----------------|----------------|
| {self.metrics['b10_life']*.5:.0f} {self.weibull['time_unit']} | ~95% | Muito Baixo |
| {self.metrics['b10_life']:.0f} {self.weibull['time_unit']} | ~90% | Baixo |
| {self.metrics['median_life']:.0f} {self.weibull['time_unit']} | ~50% | Médio |
| {self.metrics['b90_life']:.0f} {self.weibull['time_unit']} | ~10% | Alto |

---

## 6. Conclusões e Recomendações

### Conclusões Principais

1. **Característica de Falha:** {self.interpretation['failure_mode']}
   - O parâmetro β = {self.weibull['beta']:.2f} indica {self.interpretation['behavior'].lower()}

2. **Vida Útil Esperada:**
   - MTTF: {self.metrics['mttf']:.0f} {self.weibull['time_unit']}
   - Mediana: {self.metrics['median_life']:.0f} {self.weibull['time_unit']}

3. **Qualidade do Ajuste:**
   - R² = {self.tests['r_squared']['r_squared']:.4f} ({self.tests['r_squared']['quality']})
   - Os testes estatísticos {"confirmam" if self.tests['anderson_darling']['passed'] and self.tests['kolmogorov_smirnov']['passed'] else "sugerem revisar"} a adequação da distribuição de Weibull

### Recomendações

**Estratégia de Manutenção:**
{self.interpretation['recommendation']}

**Ações Específicas:**
"""
        
        # Adiciona recomendações baseadas em β
        if self.weibull['beta'] < 1:
            report += """
- Implementar programa de burn-in para novos equipamentos
- Revisar processos de fabricação e instalação
- Considerar seleção mais rigorosa de componentes
- Monitorar falhas precoces de perto
"""
        elif self.weibull['beta'] >= 1 and self.weibull['beta'] < 1.5:
            report += """
- Implementar manutenção baseada em condição
- Monitorar continuamente parâmetros operacionais
- Manter estoque adequado de peças de reposição
- Documentar e analisar modos de falha
"""
        else:
            report += """
- Estabelecer programa de manutenção preventiva baseada em tempo
- Substituir componentes antes do B10 Life
- Monitorar tendências de degradação
- Considerar redesign para aumentar vida útil
"""
        
        report += f"""

**Gestão de Estoques:**
- Manter peças críticas para substituição a cada {self.metrics['b10_life']*0.8:.0f} {self.weibull['time_unit']}
- Prever necessidade de {int((self.weibull['n_failures']/(self.weibull['n_failures']+self.weibull['n_censored']))*100)}% de taxa de falha anual

---

## 7. Limitações e Considerações

### Limitações da Análise

- Análise baseada em {self.weibull['n_failures']} falhas observadas
- Resultados são válidos para as condições operacionais dos dados coletados
- Extrapolação além do range de dados observados deve ser feita com cautela

### Considerações Importantes

- Monitorar continuamente e atualizar análise com novos dados
- Validar premissas periodicamente
- Documentar mudanças em condições operacionais
- Revisar estratégia de manutenção anualmente

---

## 8. Referências

**Método de Análise:** Distribuição de Weibull (2 parâmetros)  
**Método de Estimação:** {self.weibull['method'].upper()}  
**Software:** Weibull Reliability Analyzer v1.0  
**Normas Aplicáveis:** IEC 61649, MIL-HDBK-217

---

*Relatório gerado automaticamente em {datetime.now().strftime("%d/%m/%Y às %H:%M")}*
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
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Relatório Markdown
        markdown_report = generator.generate_markdown_report()
        
        st.download_button(
            label="📥 Baixar Relatório Completo (Markdown)",
            data=markdown_report,
            file_name=f"relatorio_weibull_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
            mime="text/markdown",
            help="Relatório completo em formato Markdown (pode ser convertido para PDF)"
        )
    
    with col2:
        # Tabela Resumo
        summary_table = generator.generate_summary_table()
        csv_summary = summary_table.to_csv(index=False)
        
        st.download_button(
            label="📊 Baixar Resumo (CSV)",
            data=csv_summary,
            file_name=f"resumo_weibull_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
            help="Tabela resumo com principais resultados"
        )
    
    # Preview do relatório
    with st.expander("👁️ Pré-visualizar Relatório", expanded=False):
        st.markdown(markdown_report)
