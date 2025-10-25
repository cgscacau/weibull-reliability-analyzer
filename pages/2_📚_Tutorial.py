"""
Página de Tutorial
"""
import streamlit as st

st.set_page_config(
    page_title="Tutorial - WRA",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Tutorial: Como Usar o Weibull Reliability Analyzer")

# Introdução
st.markdown("""
Este tutorial vai guiá-lo através de todos os passos necessários para realizar 
uma análise completa de confiabilidade usando a distribuição de Weibull.
""")

st.markdown("---")

# Passo 1
with st.expander("**1️⃣ PREPARAÇÃO DOS DADOS**", expanded=True):
    st.markdown("""
    ### Formato dos Dados
    
    Seus dados devem estar em formato tabular (planilha) com as seguintes colunas:
    
    **Colunas Obrigatórias:**
    - **Tempo até Falha**: Tempo de operação até a falha ou censura
      - Exemplos de nomes: `tempo`, `hours`, `horas`, `time`, `tempo_falha`
      - Valores: números positivos (ex: 100, 250.5, 1500)
    
    **Colunas Opcionais:**
    - **Status/Censura**: Indica se houve falha ou censura
      - Exemplos de nomes: `status`, `censura`, `event`, `censored`
      - Valores: 1 (falha) ou 0 (censurado)
      - Se não fornecida, assume-se que todos são falhas
    
    - **Identificação**: ID do equipamento
      - Exemplos de nomes: `equipamento`, `id`, `asset`, `equipment`
      - Valores: texto ou número identificador
    
    ### Exemplo de Dados Válidos
    
    | tempo | status | equipamento |
    |-------|--------|-------------|
    | 150   | 1      | EQ-001      |
    | 230   | 1      | EQ-002      |
    | 180   | 0      | EQ-003      |
    | 310   | 1      | EQ-004      |
    | 275   | 1      | EQ-005      |
    
    ### Formatos Aceitos
    - **CSV** (.csv) - Recomendado
    - **Excel** (.xlsx, .xls)
    - **PDF** (.pdf) - Experimental
    """)

# Passo 2
with st.expander("**2️⃣ UPLOAD E VALIDAÇÃO**"):
    st.markdown("""
    ### Upload do Arquivo
    
    1. Clique em **"Browse files"** ou arraste seu arquivo
    2. Aguarde o processamento
    3. Visualize o preview dos dados
    
    ### Validação Automática
    
    O sistema irá:
    - ✅ Identificar automaticamente as colunas
    - ✅ Verificar tipos de dados
    - ✅ Detectar valores inválidos
    - ✅ Calcular estatísticas básicas
    - ✅ Identificar possíveis problemas
    
    ### Possíveis Avisos
    
    - **⚠️ Poucos dados**: Menos de 10 falhas pode gerar resultados não confiáveis
    - **⚠️ Outliers detectados**: Valores muito diferentes da média
    - **⚠️ Alta censura**: Mais de 50% dos dados censurados
    
    **Dica:** Se houver erros, revise seu arquivo e tente novamente.
    """)

# Passo 3
with st.expander("**3️⃣ PROCESSAMENTO**"):
    st.markdown("""
    ### Configurações de Processamento
    
    **Unidade de Tempo:**
    - Selecione a unidade correta dos seus dados
    - Opções: horas, dias, semanas, meses, anos, ciclos, quilômetros
    - Importante para interpretação correta dos resultados
    
    **Remover Outliers:**
    - ☑️ Marcado: Remove valores extremos automaticamente
    - ☐ Desmarcado: Mantém todos os dados
    - Recomendação: Deixe desmarcado a menos que tenha certeza
    
    ### O que Acontece no Processamento
    
    1. Renomeia colunas para padrão interno
    2. Remove valores nulos
    3. Trata duplicatas
    4. Adiciona coluna de status se necessário
    5. Remove outliers (se solicitado)
    6. Ordena dados por tempo
    
    **Resultado:** Dados limpos e prontos para análise
    """)

# Passo 4
with st.expander("**4️⃣ ANÁLISE DE WEIBULL**"):
    st.markdown("""
    ### Método de Estimação
    
    **MLE (Maximum Likelihood Estimation):**
    - ✅ Mais preciso estatisticamente
    - ✅ Recomendado para dados com censura
    - ⚠️ Pode ser mais lento
    
    **RR (Rank Regression):**
    - ✅ Mais rápido
    - ✅ Bom para dados sem censura
    - ⚠️ Menos preciso com censura
    
    **Recomendação:** Use MLE na maioria dos casos
    
    ### Nível de Confiança
    
    - Padrão: 95% (0.95)
    - Determina a largura dos intervalos de confiança
    - Maior confiança = intervalos mais largos
    
    ### Interpretação dos Parâmetros
    
    **β (Beta) - Parâmetro de Forma:**
    - β < 1: Mortalidade infantil (falhas precoces)
    - β ≈ 1: Vida útil (falhas aleatórias)
    - β > 1: Desgaste (falhas aumentam com tempo)
    
    **η (Eta) - Parâmetro de Escala:**
    - Vida característica
    - Tempo em que ~63.2% falharam
    - Maior η = maior vida útil
    
    ### Métricas Calculadas
    
    - **MTTF**: Tempo médio até falha
    - **Mediana**: Tempo em que 50% falharam
    - **B10**: Tempo em que 10% falharam
    - **B90**: Tempo em que 90% falharam
    """)

# Passo 5
with st.expander("**5️⃣ VISUALIZAÇÕES**"):
    st.markdown("""
    ### Gráficos Principais
    
    **Probability Plot:**
    - Mostra ajuste dos dados à distribuição
    - Pontos próximos à linha = bom ajuste
    - Inclui intervalos de confiança
    
    **Confiabilidade vs Tempo:**
    - Curva R(t)
    - Mostra probabilidade de sobrevivência
    - Útil para planejamento de manutenção
    
    **Taxa de Falha:**
    - Curva h(t)
    - Mostra como falhas evoluem no tempo
    - Identifica fase de vida do equipamento
    
    ### Análise Detalhada
    
    - **PDF**: Densidade de probabilidade
    - **CDF**: Distribuição acumulada
    - **Histograma**: Distribuição observada
    
    ### Gráficos de Métricas
    
    - **B-Life Chart**: Percentis de falha
    - **Comparação de Métricas**: Visualização de MTTF, mediana, etc.
    
    ### Calculadora Interativa
    
    - Digite um tempo específico
    - Obtenha confiabilidade, taxa de falha, etc.
    - Útil para análises "e se"
    """)

# Passo 6
with st.expander("**6️⃣ EXPORTAÇÃO E RELATÓRIOS**"):
    st.markdown("""
    ### Opções de Exportação
    
    **Dados Processados:**
    - Botão "📥 Baixar Dados Processados"
    - Formato: CSV
    - Contém dados limpos e padronizados
    
    **Gráficos:**
    - Clique no ícone 📷 em cada gráfico
    - Formatos: PNG, SVG, PDF
    - Alta resolução para relatórios
    
    **Dica:** Use PNG para apresentações e SVG para documentos editáveis
    """)

st.markdown("---")

# Dicas e Melhores Práticas
st.subheader("💡 Dicas e Melhores Práticas")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### ✅ Faça
    
    - Tenha pelo menos 10 falhas para análise confiável
    - Use dados reais de campo
    - Documente a unidade de tempo
    - Verifique outliers manualmente
    - Compare diferentes métodos de estimação
    - Salve os gráficos para relatórios
    """)

with col2:
    st.markdown("""
    ### ❌ Evite
    
    - Misturar diferentes tipos de falha
    - Usar dados insuficientes (< 5 falhas)
    - Ignorar avisos do sistema
    - Remover outliers sem investigar
    - Esquecer de documentar premissas
    - Usar dados de diferentes populações
    """)

st.markdown("---")

# Vídeo Tutorial (placeholder)
st.subheader("🎥 Vídeo Tutorial")
st.info("📹 Em breve: Tutorial em vídeo passo a passo")

st.markdown("---")

# Próximos Passos
st.subheader("🎯 Próximos Passos")

st.markdown("""
Agora que você conhece o processo, experimente:

1. 📝 **[Guia de Preenchimento](Guia_Preenchimento)** - Detalhes sobre formato de dados
2. 📖 **[Teoria Weibull](Teoria_Weibull)** - Entenda a matemática por trás
3. ❓ **[FAQ](Perguntas_Frequentes)** - Respostas para dúvidas comuns
4. 📊 **[Análise Principal](Análise_Principal)** - Comece sua análise!
""")

# Suporte
st.markdown("---")
st.info("""
**Precisa de ajuda?**

Se encontrou algum problema ou tem dúvidas:
- Consulte a seção de **FAQ**
- Revise o **Guia de Preenchimento**
- Verifique se seus dados estão no formato correto
""")
