"""
Página de Teoria de Weibull
"""
import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(
    page_title="Teoria Weibull - WRA",
    page_icon="📖",
    layout="wide"
)

st.title("📖 Teoria da Distribuição de Weibull")

st.markdown("""
A distribuição de Weibull é uma das ferramentas mais importantes em análise de confiabilidade 
e engenharia de manutenção. Sua flexibilidade permite modelar diversos tipos de comportamento de falha.
""")

st.markdown("---")

# Introdução
with st.expander("**📌 INTRODUÇÃO**", expanded=True):
    st.markdown("""
    ### O que é a Distribuição de Weibull?
    
    A distribuição de Weibull foi proposta pelo engenheiro sueco Waloddi Weibull em 1951. 
    É uma distribuição de probabilidade contínua amplamente utilizada para:
    
    - **Análise de confiabilidade** de equipamentos e sistemas
    - **Previsão de vida útil** de componentes
    - **Planejamento de manutenção** preventiva
    - **Análise de garantia** de produtos
    - **Estudos de fadiga** de materiais
    
    ### Por que Weibull?
    
    A grande vantagem da distribuição de Weibull é sua **flexibilidade**:
    - Pode modelar taxas de falha decrescentes, constantes ou crescentes
    - Apenas dois parâmetros principais (β e η)
    - Base matemática sólida
    - Amplamente aceita na indústria
    """)

# Função de Distribuição
with st.expander("**📐 FUNÇÕES MATEMÁTICAS**"):
    st.markdown("""
    ### Função de Densidade de Probabilidade (PDF)
    
    A PDF da distribuição de Weibull é dada por:
    """)
    
    st.latex(r"f(t) = \frac{\beta}{\eta} \left(\frac{t}{\eta}\right)^{\beta-1} e^{-(t/\eta)^\beta}")
    
    st.markdown("""
    ### Função de Distribuição Acumulada (CDF)
    
    A probabilidade de falha até o tempo t:
    """)
    
    st.latex(r"F(t) = 1 - e^{-(t/\eta)^\beta}")
    
    st.markdown("""
    ### Função de Confiabilidade
    
    A probabilidade de sobrevivência até o tempo t:
    """)
    
    st.latex(r"R(t) = e^{-(t/\eta)^\beta}")
    
    st.markdown("""
    ### Taxa de Falha (Hazard Function)
    
    A taxa instantânea de falha no tempo t:
    """)
    
    st.latex(r"h(t) = \frac{\beta}{\eta} \left(\frac{t}{\eta}\right)^{\beta-1}")
    
    st.markdown("""
    ### Tempo Médio Até Falha (MTTF)
    
    O tempo médio esperado até a falha:
    """)
    
    st.latex(r"MTTF = \eta \cdot \Gamma\left(1 + \frac{1}{\beta}\right)")
    
    st.markdown("Onde Γ é a função Gamma.")

# Parâmetros
with st.expander("**⚙️ PARÂMETROS DA DISTRIBUIÇÃO**"):
    st.markdown("""
    ### β (Beta) - Parâmetro de Forma
    
    O parâmetro β determina a **forma** da distribuição e o **comportamento da taxa de falha**:
    
    **β < 1: Mortalidade Infantil**
    - Taxa de falha **decrescente** com o tempo
    - Falhas precoces são mais comuns
    - Problemas de fabricação ou instalação
    - Exemplo: Defeitos de componentes eletrônicos novos
    
    **β = 1: Vida Útil (Falhas Aleatórias)**
    - Taxa de falha **constante**
    - Falhas ocorrem aleatoriamente
    - Equivalente à distribuição exponencial
    - Exemplo: Falhas causadas por eventos externos aleatórios
    
    **β > 1: Desgaste**
    - Taxa de falha **crescente** com o tempo
    - Falhas aumentam devido ao desgaste
    - Envelhecimento natural do equipamento
    - Exemplo: Desgaste mecânico, fadiga de materiais
    
    **Valores Típicos:**
    - β = 0.5: Forte mortalidade infantil
    - β = 1.0: Falhas aleatórias
    - β = 2.0: Desgaste moderado
    - β = 3.5: Desgaste acentuado (fadiga)
    
    ### η (Eta) - Parâmetro de Escala
    
    O parâmetro η representa a **vida característica**:
    
    - **Unidade**: Mesma unidade do tempo (horas, dias, etc.)
    - **Significado**: Tempo em que aproximadamente 63,2% das unidades falharam
    - **Interpretação**: Quanto maior η, maior a vida útil
    - **Independente de β**: Escala a distribuição sem mudar sua forma
    
    **Relação com MTTF:**
    - Para β = 1: η = MTTF
    - Para β ≠ 1: η ≠ MTTF (depende da função Gamma)
    """)
    
    # Gráfico interativo mostrando efeito dos parâmetros
    st.markdown("### 📊 Visualização Interativa dos Parâmetros")
    
    col1, col2 = st.columns(2)
    with col1:
        beta_demo = st.slider("β (Beta)", 0.5, 3.0, 1.5, 0.1, key="beta_demo")
    with col2:
        eta_demo = st.slider("η (Eta)", 50.0, 200.0, 100.0, 10.0, key="eta_demo")
    
    t = np.linspace(0.1, 300, 200)
    pdf = (beta_demo/eta_demo) * (t/eta_demo)**(beta_demo-1) * np.exp(-(t/eta_demo)**beta_demo)
    h = (beta_demo/eta_demo) * (t/eta_demo)**(beta_demo-1)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t, y=pdf, name='PDF', line=dict(color='blue', width=2)))
    fig.add_trace(go.Scatter(x=t, y=h, name='Taxa de Falha', line=dict(color='red', width=2)))
    
    fig.update_layout(
        title=f'Distribuição de Weibull (β={beta_demo:.1f}, η={eta_demo:.0f})',
        xaxis_title='Tempo',
        yaxis_title='Valor',
        height=400,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Aplicações
with st.expander("**🏭 APLICAÇÕES PRÁTICAS**"):
    st.markdown("""
    ### Engenharia de Confiabilidade
    
    **Análise de Falhas:**
    - Identificar modos de falha dominantes
    - Estimar vida útil de componentes
    - Comparar confiabilidade de diferentes designs
    
    **Planejamento de Manutenção:**
    - Determinar intervalos ótimos de manutenção preventiva
    - Calcular custos de manutenção vs. substituição
    - Otimizar estoques de peças de reposição
    
    **Garantia e Qualidade:**
    - Definir períodos de garantia baseados em dados
    - Estimar custos de garantia
    - Identificar problemas de qualidade precocemente
    
    ### Indústrias que Utilizam Weibull
    
    - **Aeroespacial**: Análise de fadiga, vida de motores
    - **Automotiva**: Garantia de componentes, recalls
    - **Eletrônica**: Confiabilidade de circuitos, baterias
    - **Energia**: Turbinas eólicas, equipamentos de geração
    - **Manufatura**: Ferramentas de corte, equipamentos de produção
    - **Óleo & Gás**: Válvulas, bombas, compressores
    """)

# Métodos de Estimação
with st.expander("**🔬 MÉTODOS DE ESTIMAÇÃO DE PARÂMETROS**"):
    st.markdown("""
    ### Maximum Likelihood Estimation (MLE)
    
    **Descrição:**
    - Método estatístico que maximiza a verossimilhança dos dados observados
    - Encontra os parâmetros que tornam os dados mais prováveis
    
    **Vantagens:**
    - ✅ Estatisticamente ótimo (propriedades assintóticas)
    - ✅ Funciona bem com dados censurados
    - ✅ Fornece intervalos de confiança precisos
    - ✅ Recomendado pela maioria dos padrões
    
    **Desvantagens:**
    - ⚠️ Requer otimização numérica (mais lento)
    - ⚠️ Pode não convergir com poucos dados
    - ⚠️ Sensível a valores iniciais
    
    **Quando Usar:**
    - Dados com censura
    - Análises críticas
    - Relatórios formais
    
    ### Rank Regression (RR)
    
    **Descrição:**
    - Método gráfico baseado em regressão linear
    - Transforma dados para escala de Weibull
    - Ajusta uma linha reta aos pontos transformados
    
    **Vantagens:**
    - ✅ Rápido e simples
    - ✅ Intuitivo (visualização gráfica)
    - ✅ Bom para dados sem censura
    - ✅ Sempre converge
    
    **Desvantagens:**
    - ⚠️ Menos preciso com censura
    - ⚠️ Viés em amostras pequenas
    - ⚠️ Intervalos de confiança aproximados
    
    **Quando Usar:**
    - Análises preliminares
    - Dados sem censura
    - Necessidade de rapidez
    
    ### Comparação
    
    | Aspecto | MLE | Rank Regression |
    |---------|-----|-----------------|
    | Precisão | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
    | Velocidade | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
    | Com Censura | ⭐⭐⭐⭐⭐ | ⭐⭐ |
    | Simplicidade | ⭐⭐ | ⭐⭐⭐⭐⭐ |
    
    **Recomendação Geral:** Use MLE para análises finais e RR para exploração inicial.
    """)

# Testes de Adequação
with st.expander("**✅ TESTES DE ADEQUAÇÃO (GOODNESS OF FIT)**"):
    st.markdown("""
    ### Por que Testar o Ajuste?
    
    É importante verificar se a distribuição de Weibull é apropriada para seus dados:
    - Nem todos os dados seguem Weibull
    - Validar premissas da análise
    - Garantir confiabilidade dos resultados
    
    ### Teste de Anderson-Darling
    
    **Descrição:**
    - Teste estatístico de adequação
    - Compara distribuição empírica com teórica
    - Dá mais peso às caudas da distribuição
    
    **Interpretação:**
    - Estatística < Valor Crítico → Bom ajuste ✅
    - Estatística > Valor Crítico → Ajuste questionável ⚠️
    
    **Nível de Significância:** Tipicamente 5% (0.05)
    
    ### Teste de Kolmogorov-Smirnov
    
    **Descrição:**
    - Teste não-paramétrico
    - Mede máxima diferença entre CDFs
    - Mais conservador que Anderson-Darling
    
    **Interpretação:**
    - p-valor > 0.05 → Não rejeita Weibull ✅
    - p-valor < 0.05 → Rejeita Weibull ❌
    
    ### Coeficiente de Determinação (R²)
    
    **Descrição:**
    - Mede qualidade do ajuste linear
    - Varia de 0 a 1
    - Mais intuitivo que testes formais
    
    **Interpretação:**
    - R² > 0.95 → Excelente ajuste ⭐⭐⭐⭐⭐
    - R² > 0.90 → Bom ajuste ⭐⭐⭐⭐
    - R² > 0.80 → Aceitável ⭐⭐⭐
    - R² < 0.80 → Pobre ⭐
    
    ### O que Fazer se o Ajuste for Ruim?
    
    1. **Verificar os dados:**
       - Outliers
       - Erros de medição
       - Dados de diferentes populações
    
    2. **Considerar outras distribuições:**
       - Lognormal
       - Exponencial
       - Gamma
    
    3. **Segmentar os dados:**
       - Por modo de falha
       - Por período de tempo
       - Por condições de operação
    """)

# Interpretação Prática
with st.expander("**💼 INTERPRETAÇÃO PRÁTICA DOS RESULTADOS**"):
    st.markdown("""
    ### Como Interpretar β (Beta)
    
    **β = 0.5 (Mortalidade Infantil Severa)**
    - **Significado:** Defeitos de fabricação graves
    - **Ação:** Implementar burn-in, melhorar controle de qualidade
    - **Exemplo:** Componentes eletrônicos com defeitos de solda
    
    **β = 0.8 (Mortalidade Infantil Moderada)**
    - **Significado:** Problemas de instalação ou ajuste
    - **Ação:** Melhorar procedimentos de instalação e comissionamento
    - **Exemplo:** Equipamentos mal ajustados
    
    **β = 1.0 (Vida Útil)**
    - **Significado:** Falhas aleatórias, taxa constante
    - **Ação:** Manutenção baseada em condição
    - **Exemplo:** Falhas causadas por eventos externos
    
    **β = 2.0 (Desgaste Normal)**
    - **Significado:** Desgaste gradual esperado
    - **Ação:** Manutenção preventiva baseada em tempo
    - **Exemplo:** Desgaste de rolamentos
    
    **β = 3.5 (Desgaste Rápido)**
    - **Significado:** Fadiga ou desgaste acelerado
    - **Ação:** Reduzir intervalos de manutenção, investigar causas
    - **Exemplo:** Fadiga de materiais sob alta carga
    
    ### Como Usar η (Eta)
    
    **Para Planejamento:**
    - η = 1000 horas → Planejar manutenção antes de 1000h
    - Considerar fator de segurança (ex: 80% de η)
    
    **Para Comparação:**
    - Equipamento A: η = 5000h
    - Equipamento B: η = 3000h
    - Equipamento A tem vida 67% maior
    
    **Para Custos:**
    - Estimar custos de manutenção ao longo da vida
    - Calcular custo por hora de operação
    - Otimizar política de substituição
    
    ### Métricas Derivadas
    
    **MTTF (Mean Time To Failure):**
    - Vida média esperada
    - Útil para planejamento de longo prazo
    - Base para cálculos de disponibilidade
    
    **B10 Life:**
    - Tempo em que 10% falharam
    - Usado em especificações de rolamentos
    - Conservador para planejamento
    
    **Mediana:**
    - Tempo em que 50% falharam
    - Menos sensível a outliers que MTTF
    - Útil para comunicação com não-técnicos
    """)

# Referências
st.markdown("---")
st.subheader("📚 Referências e Leitura Adicional")

st.markdown("""
### Livros Recomendados

1. **"The Weibull Distribution: A Handbook"** - Horst Rinne
   - Referência completa sobre a distribuição

2. **"Reliability Engineering"** - Elsayed A. Elsayed
   - Aplicações práticas em engenharia

3. **"Statistical Methods for Reliability Data"** - Meeker & Escobar
   - Métodos estatísticos avançados

### Normas Técnicas

- **IEC 61649**: Análise de confiabilidade de Weibull
- **MIL-HDBK-217**: Confiabilidade de equipamentos eletrônicos
- **ISO 12107**: Fadiga - Procedimentos estatísticos

### Artigos Originais

- Weibull, W. (1951). "A Statistical Distribution Function of Wide Applicability"
- Journal of Applied Mechanics, 18(3), 293-297

### Recursos Online

- NIST/SEMATECH e-Handbook of Statistical Methods
- ReliaSoft Weibull Analysis
- Reliability Analytics Corporation
""")

st.markdown("---")
st.info("""
**💡 Dica:** A teoria é importante, mas a prática é essencial! 
Experimente com seus próprios dados na [Análise Principal](Análise_Principal).
""")
