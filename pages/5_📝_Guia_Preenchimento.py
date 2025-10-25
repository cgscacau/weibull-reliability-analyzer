"""
Página de Guia de Preenchimento
"""
import streamlit as st
import pandas as pd
import io

st.set_page_config(
    page_title="Guia de Preenchimento - WRA",
    page_icon="📝",
    layout="wide"
)

st.title("📝 Guia de Preenchimento de Dados")

st.markdown("""
Este guia detalha como preparar seus dados para análise de Weibull. 
Siga estas instruções para garantir resultados precisos e confiáveis.
""")

st.markdown("---")

# Estrutura Básica
with st.expander("**📋 ESTRUTURA BÁSICA DOS DADOS**", expanded=True):
    st.markdown("""
    ### Formato Tabular
    
    Seus dados devem estar organizados em **formato de tabela** (planilha), onde:
    - Cada **linha** representa um equipamento ou observação
    - Cada **coluna** representa uma variável (tempo, status, ID, etc.)
    - A **primeira linha** contém os nomes das colunas (cabeçalho)
    
    ### Colunas Necessárias
    
    **Obrigatória:**
    1. **Tempo até Falha** - Tempo de operação até falha ou censura
    
    **Opcionais (mas recomendadas):**
    2. **Status** - Indica se houve falha (1) ou censura (0)
    3. **Identificação** - ID único do equipamento
    """)
    
    # Exemplo visual
    st.markdown("### ✅ Exemplo de Estrutura Correta")
    
    example_data = pd.DataFrame({
        'tempo': [150, 230, 180, 310, 275, 420, 195, 380, 290, 165],
        'status': [1, 1, 0, 1, 1, 1, 1, 0, 1, 1],
        'equipamento': ['EQ-001', 'EQ-002', 'EQ-003', 'EQ-004', 'EQ-005',
                       'EQ-006', 'EQ-007', 'EQ-008', 'EQ-009', 'EQ-010']
    })
    
    st.dataframe(example_data, use_container_width=True)
    
    st.caption("""
    **Legenda:**
    - `tempo`: Horas de operação
    - `status`: 1 = falhou, 0 = ainda operando (censurado)
    - `equipamento`: Identificador único
    """)

# Coluna de Tempo
with st.expander("**⏱️ COLUNA DE TEMPO ATÉ FALHA**"):
    st.markdown("""
    ### Nomes Aceitos
    
    O aplicativo reconhece automaticamente estes nomes (não diferencia maiúsculas):
    
    **Português:**
    - `tempo`
    - `horas`
    - `tempo_falha`
    - `tempo_ate_falha`
    
    **Inglês:**
    - `time`
    - `hours`
    - `failure_time`
    - `time_to_failure`
    
    ### Formato dos Valores
    
    **✅ Valores Aceitos:**
    - Números positivos: `150`, `230.5`, `1500`
    - Inteiros ou decimais
    - Separador decimal: ponto (`.`) ou vírgula (`,`)
    
    **❌ Valores NÃO Aceitos:**
    - Números negativos: `-50`
    - Texto: `"cento e cinquenta"`
    - Datas: `01/01/2024`
    - Células vazias (serão removidas)
    
    ### Unidades de Tempo
    
    **Escolha a unidade apropriada:**
    
    | Unidade | Quando Usar | Exemplo |
    |---------|-------------|---------|
    | Horas | Operação contínua | Motores, compressores |
    | Dias | Uso diário | Equipamentos de processo |
    | Semanas/Meses | Uso intermitente | Equipamentos de backup |
    | Anos | Análise de garantia | Produtos de consumo |
    | Ciclos | Operação cíclica | Válvulas, atuadores |
    | Quilômetros | Equipamentos móveis | Veículos, correias |
    
    **Importante:** Seja consistente! Todos os valores devem estar na mesma unidade.
    
    ### Exemplos Práticos
    
    **Exemplo 1: Bombas industriais**
    ```
    tempo (horas de operação)
    1250
    2340
    1890
    3120
    ```
    
    **Exemplo 2: Veículos**
    ```
    tempo (quilômetros rodados)
    45000
    67500
    52000
    81000
    ```
    
    **Exemplo 3: Válvulas**
    ```
    tempo (ciclos de abertura/fechamento)
    15000
    23000
    18500
    29000
    ```
    """)

# Coluna de Status
with st.expander("**🔄 COLUNA DE STATUS/CENSURA**"):
    st.markdown("""
    ### Nomes Aceitos
    
    **Português:**
    - `status`
    - `censura`
    - `evento`
    - `falha`
    
    **Inglês:**
    - `status`
    - `censored`
    - `event`
    - `failure`
    
    ### Valores Permitidos
    
    **Codificação padrão:**
    - `1` = **Falha observada** (evento ocorreu)
    - `0` = **Censurado** (equipamento ainda operando ou removido sem falha)
    
    **Outras codificações aceitas:**
    - `"sim"` / `"não"`
    - `"true"` / `"false"`
    - `"falha"` / `"censura"`
    
    O aplicativo converte automaticamente para 0 e 1.
    
    ### O que é Censura?
    
    **Censura à direita (mais comum):**
    - Equipamento ainda está operando
    - Teste foi interrompido antes da falha
    - Equipamento foi removido preventivamente
    
    **Exemplo:**
    ```
    Equipamento A: Operou 1500h e falhou → status = 1
    Equipamento B: Operou 2000h e ainda funciona → status = 0
    Equipamento C: Operou 1800h e foi substituído preventivamente → status = 0
    ```
    
    ### Quando Não Há Coluna de Status
    
    Se você **não incluir** esta coluna:
    - O aplicativo assume que **todos os dados são falhas** (status = 1)
    - Isso é OK se você só tem dados de falhas
    - Mas você perde informação valiosa de equipamentos censurados
    
    **Recomendação:** Sempre inclua dados censurados quando disponíveis!
    
    ### Benefícios de Incluir Censura
    
    ✅ **Aproveita todos os dados disponíveis**
    - Equipamentos que não falharam ainda têm informação útil
    
    ✅ **Resultados mais precisos**
    - Intervalos de confiança mais estreitos
    - Estimativas menos enviesadas
    
    ✅ **Análise mais realista**
    - Reflete a população real de equipamentos
    
    ### Exemplo Completo
    
    ```csv
    tempo,status,equipamento
    1250,1,Bomba-01    # Falhou em 1250h
    2340,0,Bomba-02    # Ainda operando após 2340h
    1890,1,Bomba-03    # Falhou em 1890h
    3120,0,Bomba-04    # Removida preventivamente em 3120h
    2750,1,Bomba-05    # Falhou em 2750h
    ```
    """)

# Coluna de Identificação
with st.expander("**🏷️ COLUNA DE IDENTIFICAÇÃO (OPCIONAL)**"):
    st.markdown("""
    ### Nomes Aceitos
    
    **Português:**
    - `equipamento`
    - `id`
    - `ativo`
    - `identificacao`
    
    **Inglês:**
    - `equipment`
    - `id`
    - `asset`
    - `identifier`
    
    ### Formato dos Valores
    
    **Pode ser:**
    - Texto: `"Bomba-01"`, `"Motor-A"`, `"EQ-12345"`
    - Número: `1`, `2`, `3`, ...
    - Código alfanumérico: `"A1B2C3"`, `"2024-001"`
    
    **Requisito:** Cada equipamento deve ter ID único.
    
    ### Para Que Serve?
    
    A coluna de ID é **opcional**, mas útil para:
    - Rastreabilidade dos dados
    - Identificar equipamentos problemáticos
    - Documentação e relatórios
    - Análises futuras
    
    **Exemplo:**
    ```csv
    tempo,status,equipamento,localizacao
    1250,1,Bomba-01,Setor-A
    2340,0,Bomba-02,Setor-B
    1890,1,Bomba-03,Setor-A
    ```
    
    Neste exemplo, `localizacao` seria ignorada pelo aplicativo, 
    mas pode ser útil para sua própria análise.
    """)

# Formatos de Arquivo
with st.expander("**💾 FORMATOS DE ARQUIVO ACEITOS**"):
    st.markdown("""
    ### CSV (Recomendado)
    
    **Vantagens:**
    - ✅ Formato universal
    - ✅ Leve e rápido
    - ✅ Compatível com qualquer software
    
    **Como criar CSV no Excel:**
    1. Prepare seus dados no Excel
    2. Arquivo → Salvar Como
    3. Escolha "CSV (Separado por vírgulas) (*.csv)"
    4. **Importante:** Selecione encoding UTF-8 se disponível
    
    **Separadores aceitos:**
    - Vírgula (`,`) - padrão internacional
    - Ponto-e-vírgula (`;`) - padrão brasileiro
    - Tab (`\t`) - menos comum
    - Pipe (`|`) - menos comum
    
    O aplicativo detecta automaticamente o separador.
    
    **Exemplo de CSV:**
    ```
    tempo,status,equipamento
    150,1,EQ-001
    230,1,EQ-002
    180,0,EQ-003
    ```
    
    ### Excel (XLSX, XLS)
    
    **Vantagens:**
    - ✅ Formato familiar
    - ✅ Mantém formatação
    - ✅ Suporta múltiplas planilhas
    
    **Dicas:**
    - Use a primeira planilha para os dados
    - Se houver múltiplas planilhas, você pode escolher qual usar
    - Evite fórmulas (use apenas valores)
    - Não use células mescladas
    
    **Estrutura recomendada:**
    - Linha 1: Cabeçalhos (nomes das colunas)
    - Linhas 2+: Dados
    - Sem linhas vazias entre dados
    - Sem formatação condicional complexa
    
    ### PDF (Experimental)
    
    **Limitações:**
    - ⚠️ Apenas tabelas bem formatadas
    - ⚠️ Pode não funcionar com PDFs complexos
    - ⚠️ Requer Java instalado (no servidor)
    
    **Recomendação:** Converta PDF para CSV ou Excel antes.
    
    **Se precisar usar PDF:**
    - Certifique-se que é uma tabela simples
    - Sem células mescladas
    - Texto selecionável (não imagem)
    """)

# Boas Práticas
with st.expander("**✨ BOAS PRÁTICAS E DICAS**"):
    st.markdown("""
    ### Preparação dos Dados
    
    **✅ FAÇA:**
    
    1. **Organize seus dados antes de importar**
       - Remova linhas e colunas desnecessárias
       - Verifique se não há células vazias nos dados
    
    2. **Use nomes de colunas claros**
       - Preferencialmente em português ou inglês
       - Sem caracteres especiais (evite: ã, ç, @, #, etc.)
       - Sem espaços (use underscore: `tempo_falha`)
    
    3. **Verifique os dados**
       - Sem valores negativos em tempo
       - Status é 0 ou 1
       - Todos na mesma unidade de tempo
    
    4. **Documente suas premissas**
       - Qual unidade de tempo usou
       - Como tratou censura
       - Quais dados foram excluídos e por quê
    
    5. **Mantenha backup dos dados originais**
       - Antes de qualquer limpeza
       - Para auditoria e rastreabilidade
    
    **❌ EVITE:**
    
    1. **Misturar diferentes populações**
       - Não misture tipos de equipamentos diferentes
       - Não misture condições operacionais diferentes
    
    2. **Incluir dados duvidosos**
       - Se não tem certeza, exclua
       - Melhor ter menos dados confiáveis que muitos duvidosos
    
    3. **Remover outliers sem investigar**
       - Outliers podem ser falhas reais importantes
       - Investigue antes de remover
    
    4. **Esquecer de documentar**
       - Sempre anote decisões tomadas
       - Explique tratamento de dados especiais
    
    ### Quantidade de Dados
    
    **Mínimos recomendados:**
    
    | Situação | Mínimo | Ideal |
    |----------|--------|-------|
    | Análise preliminar | 5 falhas | 10+ falhas |
    | Análise operacional | 10 falhas | 20+ falhas |
    | Análise formal/crítica | 20 falhas | 30+ falhas |
    | Pesquisa/publicação | 30 falhas | 50+ falhas |
    
    **Lembre-se:** Mais dados = resultados mais confiáveis!
    
    ### Checklist Antes de Importar
    
    - [ ] Dados estão em formato tabular (linhas e colunas)
    - [ ] Primeira linha contém nomes das colunas
    - [ ] Coluna de tempo está presente e com valores positivos
    - [ ] Coluna de status (se aplicável) tem valores 0 ou 1
    - [ ] Não há células vazias nos dados importantes
    - [ ] Todos os tempos estão na mesma unidade
    - [ ] Arquivo está em formato aceito (CSV, Excel, PDF)
    - [ ] Nome do arquivo não tem caracteres especiais
    - [ ] Tenho backup dos dados originais
    """)

# Templates
st.markdown("---")
st.subheader("📥 Templates e Exemplos")

st.markdown("""
Baixe templates prontos para começar rapidamente:
""")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 📄 Template Básico")
    
    # Cria template básico
    template_basic = pd.DataFrame({
        'tempo': [150, 230, 180, 310, 275],
        'status': [1, 1, 0, 1, 1],
        'equipamento': ['EQ-001', 'EQ-002', 'EQ-003', 'EQ-004', 'EQ-005']
    })
    
    csv_basic = template_basic.to_csv(index=False)
    st.download_button(
        label="⬇️ Baixar Template Básico (CSV)",
        data=csv_basic,
        file_name="template_basico_weibull.csv",
        mime="text/csv"
    )
    
    st.caption("Apenas colunas essenciais")

with col2:
    st.markdown("### 📊 Template Completo")
    
    # Cria template completo
    template_full = pd.DataFrame({
        'tempo': [150, 230, 180, 310, 275, 420, 195, 380, 290, 165],
        'status': [1, 1, 0, 1, 1, 1, 1, 0, 1, 1],
        'equipamento': ['EQ-001', 'EQ-002', 'EQ-003', 'EQ-004', 'EQ-005',
                       'EQ-006', 'EQ-007', 'EQ-008', 'EQ-009', 'EQ-010'],
        'localizacao': ['Setor-A', 'Setor-B', 'Setor-A', 'Setor-C', 'Setor-B',
                       'Setor-A', 'Setor-C', 'Setor-B', 'Setor-A', 'Setor-C']
    })
    
    csv_full = template_full.to_csv(index=False)
    st.download_button(
        label="⬇️ Baixar Template Completo (CSV)",
        data=csv_full,
        file_name="template_completo_weibull.csv",
        mime="text/csv"
    )
    
    st.caption("Com colunas adicionais")

with col3:
    st.markdown("### 📈 Dados de Exemplo")
    
    # Cria dados de exemplo realistas
    np.random.seed(42)
    beta_ex = 2.5
    eta_ex = 1000
    n_samples = 30
    
    times_ex = eta_ex * (-np.log(1 - np.random.rand(n_samples))) ** (1/beta_ex)
    status_ex = np.random.choice([0, 1], size=n_samples, p=[0.2, 0.8])
    
    example_data_full = pd.DataFrame({
        'tempo': times_ex.round(0).astype(int),
        'status': status_ex,
        'equipamento': [f'BOMBA-{i:03d}' for i in range(1, n_samples+1)]
    })
    
    csv_example = example_data_full.to_csv(index=False)
    st.download_button(
        label="⬇️ Baixar Dados de Exemplo (CSV)",
        data=csv_example,
        file_name="exemplo_dados_weibull.csv",
        mime="text/csv"
    )
    
    st.caption("30 amostras realistas")

# Exemplos Específicos
st.markdown("---")
st.subheader("🎯 Exemplos por Tipo de Equipamento")

tab1, tab2, tab3 = st.tabs(["⚙️ Equipamentos Rotativos", "🔌 Eletrônicos", "🚗 Veículos"])

with tab1:
    st.markdown("""
    ### Equipamentos Rotativos (Bombas, Motores, Compressores)
    
    **Unidade recomendada:** Horas de operação
    
    **Exemplo de dados:**
    """)
    
    rotating_example = pd.DataFrame({
        'horas_operacao': [8750, 12340, 9890, 15120, 11275, 18420, 10195],
        'status': [1, 1, 0, 1, 1, 1, 0],
        'equipamento': ['BOMBA-01', 'MOTOR-02', 'COMP-03', 'BOMBA-04', 
                       'MOTOR-05', 'COMP-06', 'BOMBA-07'],
        'tipo_falha': ['Rolamento', 'Enrolamento', 'N/A', 'Selo mecânico',
                      'Rolamento', 'Válvula', 'N/A']
    })
    
    st.dataframe(rotating_example, use_container_width=True)

with tab2:
    st.markdown("""
    ### Equipamentos Eletrônicos
    
    **Unidade recomendada:** Horas de uso ou Ciclos liga/desliga
    
    **Exemplo de dados:**
    """)
    
    electronic_example = pd.DataFrame({
        'horas_uso': [2450, 3890, 1920, 5230, 4180],
        'status': [1, 0, 1, 1, 0],
        'equipamento': ['PLC-001', 'PLC-002', 'PLC-003', 'PLC-004', 'PLC-005'],
        'ambiente': ['Industrial', 'Escritório', 'Industrial', 'Industrial', 'Escritório']
    })
    
    st.dataframe(electronic_example, use_container_width=True)

with tab3:
    st.markdown("""
    ### Veículos e Equipamentos Móveis
    
    **Unidade recomendada:** Quilômetros ou Horas de motor
    
    **Exemplo de dados:**
    """)
    
    vehicle_example = pd.DataFrame({
        'quilometros': [125000, 89000, 156000, 203000, 178000],
        'status': [1, 0, 1, 1, 0],
        'veiculo': ['CAMINHAO-01', 'CAMINHAO-02', 'CAMINHAO-03', 
                   'CAMINHAO-04', 'CAMINHAO-05'],
        'componente': ['Transmissão', 'N/A', 'Motor', 'Embreagem', 'N/A']
    })
    
    st.dataframe(vehicle_example, use_container_width=True)

# Validação Final
st.markdown("---")
st.subheader("✅ Validação Final")

st.info("""
**Antes de fazer upload, verifique:**

1. ✅ Seus dados seguem a estrutura recomendada
2. ✅ Coluna de tempo tem apenas valores positivos
3. ✅ Coluna de status (se presente) tem apenas 0 e 1
4. ✅ Não há células vazias nos dados importantes
5. ✅ Arquivo está em formato aceito (CSV preferencial)
6. ✅ Você tem pelo menos 5 falhas (idealmente 10+)
7. ✅ Todos os tempos estão na mesma unidade
8. ✅ Você documentou suas premissas e decisões

**Pronto para começar?** Vá para [Análise Principal](Análise_Principal) e faça o upload!
""")
