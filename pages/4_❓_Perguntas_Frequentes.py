"""
Página de Perguntas Frequentes (FAQ)
"""
import streamlit as st

st.set_page_config(
    page_title="FAQ - WRA",
    page_icon="❓",
    layout="wide"
)

st.title("❓ Perguntas Frequentes (FAQ)")

st.markdown("""
Encontre respostas rápidas para as dúvidas mais comuns sobre análise de Weibull 
e uso do aplicativo.
""")

# Barra de busca
search = st.text_input("🔍 Buscar pergunta:", placeholder="Digite sua dúvida...")

st.markdown("---")

# Categorias
tab1, tab2, tab3, tab4 = st.tabs([
    "🎯 Uso do Aplicativo",
    "📊 Análise de Dados",
    "📈 Interpretação",
    "🔧 Problemas Técnicos"
])

# TAB 1: Uso do Aplicativo
with tab1:
    st.subheader("Uso do Aplicativo")
    
    with st.expander("**1. Quais formatos de arquivo são aceitos?**"):
        st.markdown("""
        O aplicativo aceita três formatos principais:
        
        - **CSV (.csv)** - Recomendado
          - Separadores: vírgula, ponto-e-vírgula, tab
          - Encodings: UTF-8, Latin-1
        
        - **Excel (.xlsx, .xls)**
          - Múltiplas planilhas suportadas
          - Você pode selecionar qual planilha usar
        
        - **PDF (.pdf)** - Experimental
          - Apenas tabelas bem formatadas
          - Pode não funcionar com PDFs complexos
        
        **Dica:** Para melhores resultados, use CSV ou Excel.
        """)
    
    with st.expander("**2. Quantos dados preciso para uma análise confiável?**"):
        st.markdown("""
        **Mínimo absoluto:** 3 falhas (o aplicativo não permite menos)
        
        **Recomendações:**
        - **5-10 falhas:** Análise preliminar, resultados com alta incerteza
        - **10-20 falhas:** Análise aceitável para decisões operacionais
        - **20-30 falhas:** Boa confiabilidade estatística
        - **30+ falhas:** Excelente confiabilidade, intervalos estreitos
        
        **Importante:** Mais dados = resultados mais confiáveis!
        
        Com poucos dados (< 10), os intervalos de confiança serão muito largos 
        e as conclusões devem ser tomadas com cautela.
        """)
    
    with st.expander("**3. O que é censura e quando devo usá-la?**"):
        st.markdown("""
        **Censura** ocorre quando você sabe que um equipamento operou por um 
        certo tempo, mas não falhou ainda.
        
        **Exemplos de dados censurados:**
        - Equipamento ainda em operação (censura à direita)
        - Teste interrompido antes da falha
        - Equipamento removido do serviço preventivamente
        
        **Como marcar:**
        - Status = 1 → Falha observada
        - Status = 0 → Censurado (não falhou)
        
        **Quando usar:**
        - ✅ Sempre que tiver equipamentos ainda operando
        - ✅ Testes interrompidos
        - ✅ Substituições preventivas
        
        **Benefício:** Aproveita TODOS os dados disponíveis, não só falhas!
        """)
    
    with st.expander("**4. Devo remover outliers?**"):
        st.markdown("""
        **Resposta curta:** Na maioria das vezes, NÃO.
        
        **Quando NÃO remover:**
        - ❌ Outliers são falhas reais
        - ❌ Você não tem certeza da causa
        - ❌ Dados são de campo (não testes)
        
        **Quando considerar remover:**
        - ✅ Erro de medição comprovado
        - ✅ Falha por causa externa identificada (acidente, etc.)
        - ✅ Dados de teste com problema conhecido
        
        **Importante:** Documente sempre que remover outliers e justifique!
        
        **Alternativa:** Faça duas análises (com e sem outliers) e compare.
        """)
    
    with st.expander("**5. Qual método de estimação devo usar: MLE ou RR?**"):
        st.markdown("""
        **Recomendação geral:** Use **MLE (Maximum Likelihood)**
        
        **Use MLE quando:**
        - ✅ Dados têm censura
        - ✅ Análise formal/relatório
        - ✅ Decisões críticas
        - ✅ Quer máxima precisão
        
        **Use RR (Rank Regression) quando:**
        - ✅ Análise exploratória rápida
        - ✅ Não há censura
        - ✅ Poucos dados (< 10)
        - ✅ MLE não convergiu
        
        **Diferença prática:** Para a maioria dos casos, os resultados são similares.
        MLE é mais preciso, especialmente com censura.
        """)
    
    with st.expander("**6. Como interpretar os intervalos de confiança?**"):
        st.markdown("""
        **Intervalos de Confiança (IC)** mostram a incerteza dos parâmetros estimados.
        
        **Exemplo:**
        - β = 2.5 [IC 95%: 2.1 - 2.9]
        - Significa: Temos 95% de confiança que o verdadeiro β está entre 2.1 e 2.9
        
        **Interpretação:**
        - **IC estreito** → Alta precisão, muitos dados
        - **IC largo** → Baixa precisão, poucos dados
        
        **Nível de confiança:**
        - 90% → Intervalos mais estreitos, menos conservador
        - 95% → Padrão, bom equilíbrio
        - 99% → Intervalos mais largos, mais conservador
        
        **Dica:** Se os ICs são muito largos, você precisa de mais dados!
        """)

# TAB 2: Análise de Dados
with tab2:
    st.subheader("Análise de Dados")
    
    with st.expander("**7. Meus dados têm colunas com nomes diferentes. O que fazer?**"):
        st.markdown("""
        **Não se preocupe!** O aplicativo detecta automaticamente nomes comuns.
        
        **Nomes reconhecidos automaticamente:**
        
        **Para tempo:**
        - tempo, time, hours, horas, tempo_falha, failure_time
        
        **Para status:**
        - status, censura, censored, event, evento
        
        **Para ID:**
        - equipamento, equipment, id, asset, ativo
        
        **Se não funcionar:**
        1. Renomeie as colunas no seu arquivo
        2. Use nomes simples em português ou inglês
        3. Evite caracteres especiais
        
        **Exemplo de bom formato:**
        ```
        tempo,status,equipamento
        150,1,EQ-001
        230,1,EQ-002
        ```
        """)
    
    with st.expander("**8. Posso misturar diferentes tipos de falha?**"):
        st.markdown("""
        **Resposta curta:** Depende!
        
        **NÃO misture se:**
        - ❌ Modos de falha têm causas diferentes
        - ❌ Comportamentos são claramente distintos
        - ❌ Um é mortalidade infantil e outro desgaste
        
        **PODE misturar se:**
        - ✅ Falhas são do mesmo sistema
        - ✅ Causas raiz são similares
        - ✅ Interesse é na confiabilidade geral do sistema
        
        **Melhor prática:**
        1. Analise cada modo de falha separadamente
        2. Compare os parâmetros β
        3. Se β são similares (diferença < 20%), pode combinar
        4. Se β são muito diferentes, mantenha separado
        
        **Exemplo:**
        - Falha de rolamento (β=2.5) + Falha de vedação (β=2.3) → OK combinar
        - Falha eletrônica (β=0.8) + Falha mecânica (β=3.2) → NÃO combinar
        """)
    
    with st.expander("**9. O que fazer se o R² for baixo (< 0.90)?**"):
        st.markdown("""
        **R² baixo indica que Weibull pode não ser a melhor distribuição.**
        
        **Possíveis causas:**
        1. **Dados de múltiplas populações**
           - Solução: Segmente os dados
        
        2. **Outliers influentes**
           - Solução: Investigue e considere remover se justificado
        
        3. **Distribuição não é Weibull**
           - Solução: Tente outras distribuições (lognormal, exponencial)
        
        4. **Poucos dados**
           - Solução: Colete mais dados
        
        5. **Erros de medição**
           - Solução: Revise os dados originais
        
        **Ações práticas:**
        - Verifique o gráfico de probabilidade visualmente
        - Se pontos seguem aproximadamente a linha, pode usar
        - Se há padrão claro de desvio, não use Weibull
        - Documente a limitação nos relatórios
        """)
    
    with st.expander("**10. Como lidar com dados de diferentes condições operacionais?**"):
        st.markdown("""
        **Problema:** Equipamentos operaram em condições diferentes (carga, temperatura, etc.)
        
        **Soluções:**
        
        **1. Segmentação (Recomendado)**
        - Separe dados por condição
        - Analise cada grupo separadamente
        - Compare os parâmetros
        
        **2. Normalização**
        - Ajuste tempos por fator de aceleração
        - Exemplo: 1 hora a 80°C = 2 horas a 60°C
        - Requer conhecimento técnico
        
        **3. Análise Conservadora**
        - Use apenas dados da condição mais severa
        - Mais conservador, mas mais seguro
        
        **4. Modelo de Regressão Weibull**
        - Avançado: incorpora covariáveis
        - Fora do escopo deste aplicativo
        
        **Exemplo prático:**
        ```
        Condição A (normal): 50 falhas, β=2.5, η=1000h
        Condição B (severa): 30 falhas, β=2.3, η=600h
        → Use Condição B para planejamento conservador
        ```
        """)
    
    with st.expander("**11. Qual unidade de tempo devo usar?**"):
        st.markdown("""
        **A unidade de tempo deve refletir como você mede a vida do equipamento.**
        
        **Escolha baseada em:**
        
        **Horas de operação:**
        - Equipamentos que operam continuamente
        - Exemplo: Motores, compressores, bombas
        
        **Dias/Meses/Anos:**
        - Equipamentos com uso intermitente
        - Análise de garantia
        - Exemplo: Eletrodomésticos, veículos pessoais
        
        **Ciclos:**
        - Equipamentos com operação cíclica
        - Exemplo: Prensas, válvulas, atuadores
        
        **Quilômetros:**
        - Veículos e equipamentos móveis
        - Exemplo: Caminhões, correias transportadoras
        
        **Importante:** 
        - Seja consistente em toda a análise
        - Documente a unidade escolhida
        - Considere qual é mais útil para manutenção
        
        **Conversão:** Você pode converter depois se necessário
        - 1 ano = 8760 horas (operação contínua)
        - 1 mês = 730 horas (operação contínua)
        """)

# TAB 3: Interpretação
with tab3:
    st.subheader("Interpretação dos Resultados")
    
    with st.expander("**12. O que significa β = 1.05? É mortalidade infantil ou desgaste?**"):
        st.markdown("""
        **β muito próximo de 1 está na zona de transição.**
        
        **Interpretação prática:**
        
        **β entre 0.9 e 1.1:**
        - Considere como **taxa de falha aproximadamente constante**
        - Falhas são essencialmente aleatórias
        - Diferença de 0.9 para 1.1 é estatisticamente pequena
        
        **Recomendação:**
        - Verifique os intervalos de confiança
        - Se IC inclui 1.0, trate como taxa constante
        - Manutenção baseada em condição é apropriada
        
        **Exemplo:**
        - β = 1.05 [IC: 0.92 - 1.18]
        - IC inclui 1.0 → Trate como exponencial (β=1)
        
        **Ação prática:**
        - Não force manutenção preventiva baseada em tempo
        - Monitore condição do equipamento
        - Substitua sob demanda
        """)
    
    with st.expander("**13. Como usar MTTF para planejamento de manutenção?**"):
        st.markdown("""
        **MTTF = Mean Time To Failure (Tempo Médio Até Falha)**
        
        **O que NÃO fazer:**
        - ❌ Agendar manutenção exatamente no MTTF
        - ❌ Assumir que todos falharão no MTTF
        - ❌ Usar MTTF como única métrica
        
        **O que fazer:**
        
        **1. Use como referência:**
        - MTTF dá uma ideia da ordem de grandeza
        - Exemplo: MTTF = 5000h → Vida útil é de milhares de horas
        
        **2. Combine com outras métricas:**
        - B10 (10% falharam) → Mais conservador
        - Mediana (50% falharam) → Ponto médio
        - MTTF → Média (afetada por outliers)
        
        **3. Aplique fator de segurança:**
        - Manutenção preventiva: 50-70% do MTTF
        - Exemplo: MTTF = 10000h → Manutenção a cada 6000h
        
        **4. Considere β:**
        - Se β < 1: MTTF é menos útil (falhas precoces)
        - Se β ≈ 1: MTTF é bom indicador
        - Se β > 1: Use B10 ou mediana (mais conservador)
        
        **Exemplo prático:**
        ```
        MTTF = 8000h, β = 2.5 (desgaste)
        B10 = 3500h
        → Agende manutenção preventiva a cada 3000h
        ```
        """)
    
    with st.expander("**14. O que é B10 Life e quando devo usá-lo?**"):
        st.markdown("""
        **B10 Life = Tempo em que 10% da população falhou**
        
        **Também chamado de:**
        - L10 (em rolamentos)
        - Vida de 10%
        - Percentil 10
        
        **Por que B10?**
        - Métrica conservadora
        - Amplamente usada em especificações de rolamentos
        - Boa para planejamento de manutenção preventiva
        
        **Interpretação:**
        - B10 = 5000h → 10% falharão antes de 5000h
        - Ou: 90% sobreviverão até 5000h
        
        **Quando usar:**
        
        **Para planejamento de manutenção:**
        - Estabeleça intervalos em torno do B10
        - Exemplo: Manutenção a cada 80% do B10
        
        **Para especificações:**
        - "Equipamento deve ter B10 > 10000h"
        - Comum em compras técnicas
        
        **Para comparação:**
        - Fornecedor A: B10 = 8000h
        - Fornecedor B: B10 = 6000h
        - Fornecedor A é 33% melhor
        
        **Outras métricas B-Life:**
        - **B1:** 1% falharam (muito conservador)
        - **B5:** 5% falharam (conservador)
        - **B50:** 50% falharam (= mediana)
        - **B90:** 90% falharam (otimista)
        """)
    
    with st.expander("**15. Como explicar resultados de Weibull para não-técnicos?**"):
        st.markdown("""
        **Dicas de comunicação:**
        
        **1. Evite jargão técnico:**
        ❌ "O parâmetro de forma β é 2.5, indicando desgaste"
        ✅ "O equipamento desgasta com o tempo, falhas aumentam com a idade"
        
        **2. Use analogias:**
        - β < 1: "Como mortalidade infantil em humanos"
        - β = 1: "Como acidentes de carro - aleatórios"
        - β > 1: "Como envelhecimento - aumenta com idade"
        
        **3. Foque em ações:**
        ❌ "MTTF é 5000 horas"
        ✅ "Devemos fazer manutenção a cada 3000 horas"
        
        **4. Use visualizações:**
        - Mostre o gráfico de confiabilidade
        - "Veja como a chance de falha aumenta com o tempo"
        
        **5. Dê contexto:**
        ❌ "R(5000h) = 0.85"
        ✅ "85% dos equipamentos funcionarão por 5000 horas sem falha"
        
        **Exemplo de apresentação:**
        ```
        "Analisamos 50 falhas de bombas. Descobrimos que:
        
        1. As falhas aumentam com o tempo (desgaste)
        2. Metade das bombas falha antes de 4000 horas
        3. Recomendamos manutenção preventiva a cada 3000 horas
        4. Isso deve reduzir falhas inesperadas em 70%"
        ```
        """)
    
    with st.expander("**16. Quando devo considerar substituição vs. manutenção?**"):
        st.markdown("""
        **Decisão baseada em análise de Weibull:**
        
        **Substitua quando:**
        
        **1. β alto (> 3):**
        - Desgaste rápido
        - Manutenção não é efetiva
        - Custo de reparo próximo ao de substituição
        
        **2. Equipamento velho:**
        - Já passou da vida característica (η)
        - Taxa de falha está muito alta
        - Confiabilidade inaceitável
        
        **3. Análise de custo:**
        ```
        Custo de manutenção anual > 60% do custo de substituição
        → Considere substituir
        ```
        
        **Mantenha quando:**
        
        **1. β baixo ou moderado (< 2.5):**
        - Manutenção preventiva é efetiva
        - Vida útil ainda é longa
        
        **2. Equipamento novo:**
        - Ainda na fase de vida útil
        - Longe da vida característica
        
        **3. Manutenção é econômica:**
        - Peças disponíveis e baratas
        - Mão de obra é simples
        
        **Análise econômica:**
        
        **Calcule:**
        1. **Custo de manter:** Manutenção + Falhas + Downtime
        2. **Custo de substituir:** Equipamento novo + Instalação
        3. **Período de análise:** Típico 5-10 anos
        
        **Decisão:**
        - Se Custo Anual de Manter > 15% do Custo de Substituir
        - → Considere substituição
        
        **Exemplo:**
        ```
        Bomba: η = 8000h, β = 3.5, já operou 7000h
        
        Opção A (Manter):
        - Manutenção anual: $5,000
        - Falhas esperadas: 3/ano × $2,000 = $6,000
        - Total anual: $11,000
        
        Opção B (Substituir):
        - Bomba nova: $25,000
        - Vida útil: 8 anos
        - Custo anual equivalente: $3,125
        
        → Substituir é mais econômico!
        ```
        """)

# TAB 4: Problemas Técnicos
with tab4:
    st.subheader("Problemas Técnicos")
    
    with st.expander("**17. O upload falhou. O que fazer?**"):
        st.markdown("""
        **Possíveis causas e soluções:**
        
        **1. Arquivo muito grande:**
        - Limite: ~200 MB
        - Solução: Reduza o tamanho, remova colunas desnecessárias
        
        **2. Formato incompatível:**
        - Verifique se é CSV, XLSX, XLS ou PDF
        - Solução: Converta para CSV
        
        **3. Caracteres especiais:**
        - Acentos ou símbolos no nome do arquivo
        - Solução: Renomeie sem caracteres especiais
        
        **4. Arquivo corrompido:**
        - Arquivo pode estar danificado
        - Solução: Abra e salve novamente no Excel
        
        **5. Separador incorreto (CSV):**
        - O aplicativo tenta detectar automaticamente
        - Solução: Use vírgula ou ponto-e-vírgula
        
        **Dica:** Tente salvar como CSV (UTF-8) no Excel.
        """)
    
    with st.expander("**18. A análise não convergiu. O que significa?**"):
        st.markdown("""
        **"Não convergiu" significa que o algoritmo MLE não encontrou solução.**
        
        **Causas comuns:**
        
        **1. Poucos dados:**
        - < 5 falhas é muito pouco para MLE
        - Solução: Use Rank Regression ou colete mais dados
        
        **2. Dados problemáticos:**
        - Muitos valores iguais
        - Outliers extremos
        - Solução: Revise os dados
        
        **3. Censura excessiva:**
        - > 80% dos dados censurados
        - Solução: Aguarde mais falhas ou use RR
        
        **O que o aplicativo faz:**
        - Automaticamente tenta Rank Regression
        - Você verá aviso: "MLE falhou, usando RR"
        
        **Ações:**
        1. Aceite os resultados do RR (geralmente OK)
        2. Ou colete mais dados
        3. Verifique qualidade dos dados
        """)
    
    with st.expander("**19. Os gráficos não aparecem. Como resolver?**"):
        st.markdown("""
        **Soluções rápidas:**
        
        **1. Atualize a página:**
        - Pressione F5 ou Ctrl+R
        - Ou use o botão "Rerun" do Streamlit
        
        **2. Limpe o cache:**
        - Menu (☰) → Settings → Clear cache
        - Recarregue a página
        
        **3. Verifique o navegador:**
        - Use Chrome, Firefox ou Edge (atualizados)
        - Evite Internet Explorer
        
        **4. Desabilite bloqueadores:**
        - Ad-blockers podem interferir
        - Desabilite temporariamente
        
        **5. JavaScript habilitado:**
        - Gráficos Plotly requerem JavaScript
        - Verifique se está habilitado
        
        **Se persistir:**
        - Tente em modo anônimo/privado
        - Teste em outro navegador
        - Verifique sua conexão de internet
        """)
    
    with st.expander("**20. Como salvar/exportar meus resultados?**"):
        st.markdown("""
        **Opções de exportação:**
        
        **1. Dados Processados:**
        - Botão "📥 Baixar Dados Processados"
        - Formato: CSV
        - Contém dados limpos usados na análise
        
        **2. Gráficos individuais:**
        - Passe o mouse sobre o gráfico
        - Clique no ícone de câmera 📷
        - Escolha formato: PNG, SVG, PDF
        
        **3. Captura de tela:**
        - Use ferramenta de captura do sistema
        - Windows: Win + Shift + S
        - Mac: Cmd + Shift + 4
        
        **4. Relatório completo:**
        - Copie métricas principais
        - Salve gráficos importantes
        - Monte relatório no Word/PowerPoint
        
        **Dica para relatórios:**
        1. Capture aba "Análise Completa" (visão geral)
        2. Salve gráficos principais em alta resolução
        3. Copie tabela de parâmetros e métricas
        4. Adicione interpretação e recomendações
        
        **Formatos recomendados:**
        - **PNG**: Para apresentações (PowerPoint)
        - **SVG**: Para documentos editáveis
        - **PDF**: Para relatórios formais
        """)
    
    with st.expander("**21. Posso usar este aplicativo offline?**"):
        st.markdown("""
        **Resposta:** Não diretamente, mas há alternativas.
        
        **Este aplicativo:**
        - Roda na nuvem (Streamlit Cloud)
        - Requer conexão com internet
        - Seus dados NÃO são armazenados no servidor
        
        **Para uso offline:**
        
        **Opção 1: Instalação local (avançado)**
        ```bash
        # Requer Python instalado
        git clone [repositório]
        pip install -r requirements.txt
        streamlit run app.py
        ```
        
        **Opção 2: Software comercial**
        - ReliaSoft Weibull++
        - Minitab
        - JMP
        
        **Opção 3: R ou Python**
        - Pacotes: WeibullR, lifelines, reliability
        - Requer conhecimento de programação
        
        **Segurança dos dados:**
        - Seus dados são processados apenas no navegador
        - Nada é enviado para servidores externos
        - Dados são apagados ao fechar a página
        """)

st.markdown("---")

# Seção de ajuda adicional
st.subheader("🆘 Não encontrou sua resposta?")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    **📚 Consulte:**
    - [Tutorial](Tutorial)
    - [Teoria Weibull](Teoria_Weibull)
    - [Guia de Preenchimento](Guia_Preenchimento)
    """)

with col2:
    st.markdown("""
    **🔍 Recursos:**
    - Exemplos de dados
    - Vídeos tutoriais (em breve)
    - Documentação técnica
    """)

with col3:
    st.markdown("""
    **💬 Suporte:**
    - Revise os logs de erro
    - Verifique a documentação
    - Consulte normas técnicas
    """)

st.markdown("---")
st.info("💡 **Dica:** Use a busca no topo desta página para encontrar respostas rapidamente!")
