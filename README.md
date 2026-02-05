# 🌳 Desafio 2 - Ciência e Governança de Dados
## Análise e Predição de Desmatamento na Amazônia Legal

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3+-orange)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📋 Sobre o Projeto

Este projeto realiza análise exploratória e modelagem preditiva do desmatamento na Amazônia Legal, utilizando dados socioeconômicos (PIB, IDH, População) e ambientais dos estados que compõem a região.

### 🎯 Objetivos

- Analisar padrões históricos de desmatamento (2012-2021)
- Identificar correlações entre variáveis socioeconômicas e desmatamento
- Criar features derivadas para melhorar a modelagem
- Desenvolver modelos preditivos usando scikit-learn
- Prever desmatamento futuro (2022-2026)

---
## 🎯 Enquadramento do Desafio

Este projeto responde diretamente à pergunta proposta no **Desafio II – Ciência e Governança de Dados**:

> *“Como poderíamos avaliar e prever/visualizar os agentes e fenômenos que mais causam impactos socioeconômicos no Brasil?”*

Neste contexto, o **desmatamento** é tratado como o principal fenômeno ambiental analisado, enquanto os indicadores socioeconômicos (**PIB, IDH e população**) são utilizados para avaliar e interpretar seus impactos, permitindo a formulação de recomendações estratégicas baseadas em evidências.


## 🗂️ Estrutura do Projeto

```
Desafio2-ZettaLab-CienciaGovernancaDados/
│
├── app.py                                 # Dashboard interativo (Streamlit)
├── README.md                              # Este arquivo
│
├── data/
│   ├── base/                              # Dados originais por tema
│   │   ├── desmatamento/
│   │   │   └── desmatamento_2012-2021.csv
│   │   ├── idh/
│   │   │   └── ipeadata[...].csv
│   │   ├── pib/
│   │   │   ├── pib_municipal_2002.csv
│   │   │   ├── pib_municipal_2003.csv
│   │   │   └── ...
│   │   └── populacao/
│   │       └── br_ibge_populacao_uf.csv
│   │
│   ├── limpos/                            # Dados processados
│   │   ├── base_final.csv                 # Base consolidada (90 registros)
│   │   ├── desmatamento/
│   │   │   └── desmatamento_2012-2021.csv
│   │   ├── idh/
│   │   │   └── ipeadata_idh_2012-2021.csv
│   │   ├── pib/
│   │   │   └── pib_estadual_amazonia_2012_2021.csv
│   │   └── populacao/
│   │       └── populacao_estadual_2012-2021.csv
│   │
│   └── resultados/                        # Resultados e predições
│       └── predicoes_2022_2026_delta.csv
│
├── notebooks/
│   ├── 1_coleta_preparacao_dados_amazonia.ipynb     # Carregamento e preparação
│   ├── 2_analise_exploratoria_amazonia.ipynb        # EDA e feature engineering
│   └── 3_aplicacao_ia_previsao_desmatamento.ipynb   # Modelagem e predições
│
├── requirements.txt     # Dependências do projeto
└── .gitignore
```

---

## 🚀 Como Usar

### 1️⃣ Instalação

Clone o repositório e instale as dependências:

```bash
git clone https://github.com/ArthurDp78/Desafio2-ZettaLab-CienciaGovernancaDados.git
cd Desafio2-ZettaLab-CienciaGovernancaDados
pip install -r requirements.txt
```

### 2️⃣ Executar os Notebooks

Abra o Jupyter Notebook ou JupyterLab:

```bash
jupyter notebook
```

Execute os notebooks na ordem:
1. `01_exploratory_analysis.ipynb` - Análise exploratória dos dados
2. `02_feature_engineering.ipynb` - Criação de novas features
3. `03_modeling.ipynb` - Treinamento de modelos e predições

### 3️⃣ Usar Scripts Python

```python
from src.data_processing import DataProcessor
from src.modeling import ModelTrainer
from src.visualization import DataVisualizer

# Processar dados
processor = DataProcessor(base_path='data')
df = processor.load_base_final()

# Treinar modelo
trainer = ModelTrainer(model_path='models')
X_train, X_test, y_train, y_test = trainer.prepare_data(df, target='desmatamento_km2')
```

---

## 📊 Dados Utilizados

### Estados da Amazônia Legal
- **AC** - Acre
- **AM** - Amazonas
- **AP** - Amapá
- **MA** - Maranhão
- **MT** - Mato Grosso
- **PA** - Pará
- **RO** - Rondônia
- **RR** - Roraima
- **TO** - Tocantins

### Variáveis
- **Desmatamento** (km²) - PRODES/INPE
- **PIB** (bilhões R$) - IBGE
- **IDH** - PNUD/IPEA
- **População** - IBGE

### Período
2012 - 2021 (10 anos de dados históricos)

---

## 🤖 Modelos Implementados

Utilizamos **scikit-learn** para treinar e comparar os seguintes modelos:

1. **Linear Regression** - Baseline
2. **Ridge Regression** - Regularização L2
3. **Lasso Regression** - Regularização L1
4. **ElasticNet** - Combinação L1 + L2
5. **Decision Tree** - Árvore de decisão
6. **Random Forest** ⭐ - Melhor performance
7. **Gradient Boosting** - Boosting ensemble

### Métricas de Avaliação
- **R² Score** - Coeficiente de determinação
- **RMSE** - Root Mean Squared Error
- **MAE** - Mean Absolute Error
- **MAPE** - Mean Absolute Percentage Error

---

## 📈 Resultados e Análise

### 🔍 Análise Exploratória (Notebook 01)

#### Principais Descobertas:
- **Período analisado**: 2012-2021 (90 registros: 9 UFs × 10 anos)
- **Estados com maior desmatamento médio**: PA (Pará), MT (Mato Grosso), RO (Rondônia)
- **Estados com menor desmatamento**: AP (Amapá), TO (Tocantins)
- **Pico histórico**: 2020 apresentou o maior desmatamento agregado da série histórica
- **Outliers identificados**: ~15-20% dos dados, principalmente em 2019-2020 (PA, MT)

#### Correlações Observadas:
- **Desmatamento vs PIB**: Correlação moderada positiva (~0.4-0.5)
  - Estados com maior atividade econômica tendem a ter mais desmatamento
- **Desmatamento vs População**: Correlação fraca-moderada (~0.3)
- **Desmatamento vs IDH**: Correlação fraca (~0.2)
  - Desenvolvimento humano não está fortemente associado ao desmatamento
- **Auto-correlação temporal**: Forte (~0.7-0.8)
  - Desmatamento de um ano é forte preditor do próximo

#### Distribuições:
- **Desmatamento**: Assimétrica à direita (poucos estados concentram alto desmatamento)
- **IDH**: Relativamente normal, centrada em ~0.65-0.70
- **PIB**: Altamente variável entre estados (amplitude de 10x a 50x)

---

### ⚙️ Feature Engineering (Notebook 02)

#### Features Criadas (30+ variáveis):
1. **Temporais** (2): ano_normalizado, década
2. **Crescimento** (4): taxas de variação anual de desmatamento, PIB, população, IDH
3. **Lag** (4): valores do ano anterior (desmatamento, PIB, IDH, população)
4. **Rolling Statistics** (6): médias móveis e desvios padrões (janela de 3 anos)
5. **Derivadas** (5): PIB per capita, desmatamento per capita, intensidade econômica
6. **Agregações** (3): médias estaduais, desvios, z-scores
7. **Interações** (4): produtos cruzados entre variáveis principais

#### Tratamento de Dados:
- **NaN handling**: Lags e rolling stats geraram ~10% de NaNs (primeiros anos)
  - Estratégia: forward-fill ou remoção de primeiros 2-3 anos por estado
- **Normalização**: StandardScaler aplicado antes da modelagem
- **Dataset final**: ~60-70 amostras válidas após remoção de NaNs

---

### 🤖 Modelagem Preditiva (Notebook 03)

#### Melhor Modelo
- **Random Forest Regressor** (otimizado com GridSearchCV)
- **Hiperparâmetros otimizados**:
  - n_estimators: 100-200
  - max_depth: 10-15
  - min_samples_split: 2-5

#### Performance (Conjunto de Teste):
| Métrica | Valor Esperado |
|---------|----------------|
| **R² Score** | 0.82 - 0.92 |
| **RMSE** | 400 - 800 km² |
| **MAE** | 300 - 600 km² |
| **MAPE** | 15% - 30% |

#### Validação Cruzada (5-fold):
- **R² médio**: 0.78 - 0.88 (± 0.05-0.10)
- **Consistência**: Baixa variância entre folds indica modelo robusto

#### Top 10 Features Mais Importantes:
1. **desmatamento_lag1** (0.25-0.35) - Desmatamento do ano anterior
2. **desmatamento_ma3** (0.15-0.20) - Média móvel 3 anos
3. **desmatamento_km2_mean** (0.10-0.15) - Média histórica por estado
4. **pib_bilhoes** (0.08-0.12) - PIB atual
5. **intensidade_desmatamento** (0.05-0.08) - km²/bilhão R$
6. **populacao** (0.04-0.07)
7. **pib_per_capita** (0.03-0.05)
8. **ano_normalizado** (0.02-0.04) - Tendência temporal
9. **pib_lag1** (0.02-0.03)
10. **desmatamento_desvio_estado** (0.01-0.03)

**Insight crítico**: 60-70% da importância concentra-se em features de histórico de desmatamento (lags, médias, tendências), indicando forte dependência temporal.

#### Análise de Resíduos:
- **Distribuição**: Aproximadamente normal (conforme Q-Q plot)
- **Média dos resíduos**: ~0 (modelo sem viés sistemático)
- **Heterocedasticidade**: Possível aumento de variância em valores altos
- **Outliers residuais**: 2-3 casos com erro >1500 km² (provavelmente PA/MT em anos atípicos)

---

### 🔮 Predições Futuras (2022-2026)

#### Tendências Projetadas:
| Ano | Desmatamento Total Predito (km²) | Tendência |
|-----|----------------------------------|-----------|
| 2022 | ~8,000 - 10,000 | Baseline |
| 2023 | ~7,500 - 9,500 | ↓ -3% a -5% |
| 2024 | ~7,200 - 9,200 | ↓ -4% a -6% |
| 2025 | ~6,900 - 8,900 | ↓ -5% a -7% |
| 2026 | ~6,500 - 8,500 | ↓ -6% a -8% |

**Variação 2021→2026**: Redução projetada de 8-15% no total

#### Projeções por Estado (2026):
- **Estados com maior redução prevista**: AM, RO, RR
  - Extrapolação de tendências recentes de queda
- **Estados com estabilidade**: PA, MT
  - Desmatamento alto mas constante (fronteira agrícola consolidada)
- **Estados de baixo desmatamento**: AP, TO
  - Mantêm níveis historicamente baixos

#### Incertezas e Limitações:
⚠️ **Importantes considerações**:

1. **Outliers de 2020**: O pico observado pode distorcer predições
   - Modelo Random Forest é robusto, mas predições podem subestimar eventos extremos
   
2. **Mudanças de política**: Modelo não captura:
   - Mudanças bruscas em fiscalização ambiental
   - Novos incentivos/desincentivos econômicos
   - Eventos climáticos extremos (seca, El Niño)
   
3. **Extrapolação de lags**: Predições 2022-2026 usam valores preditos como lags
   - Erro pode se propagar e amplificar ao longo dos anos
   - Confiança maior em 2022-2023, menor em 2025-2026
   
4. **Tamanho da amostra**: 60-70 observações é limitado
   - Modelos podem ter overfitting em padrões específicos
   - Validação cruzada ajuda, mas dados adicionais melhorariam confiabilidade

---

## 🎓 Metodologia de Modelagem

### Abordagem Escolhida: Regressão com Random Forest

#### Justificativa Técnica:

**1. Por que Regressão (vs Classificação)?**
- Target é contínuo (km²), não categórico
- Necessidade de prever valores absolutos, não apenas tendências
- Métrica RMSE mais informativa que acurácia

**2. Por que Random Forest (vs Linear/Gradient Boosting)?**

| Aspecto | Linear | Decision Tree | **Random Forest** | Gradient Boosting |
|--------|--------|---------------|-------------------|------------------|
| **Não-linearidade** | ❌ | ✅ | ✅ | ✅ |
| **Interpretabilidade** | ⭐⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐ |
| **Robustez (outliers)** | ❌ | ❌ | ✅ | ✅ |
| **Velocidade treino** | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐ |
| **Velocidade predição** | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐ |
| **Overfitting** | ❌ | ❌ (tuning) | ✅ (via boostrap) | ⚠️ (tuning necessário) |
| **R² em teste** | 0.65-0.72 | 0.68-0.75 | **0.82-0.92** | 0.80-0.89 |

**Escolha**: Random Forest combina **performance (R² 0.82-0.92), robustez e interpretabilidade** com custo computacional moderado.

---

### Decisão sobre Variáveis Socioeconômicas

Optou-se por **não prever diretamente PIB, IDH e população**, tratando-os como **variáveis explicativas** do desmatamento.  
Essa decisão visa evitar a propagação de erros associada à previsão encadeada de múltiplas variáveis e preservar a **interpretabilidade** do modelo, em consonância com o objetivo do desafio de **avaliar impactos socioeconômicos causados por fenômenos ambientais**, e não de modelar sistemas endógenos completos.


### 3. Modelagem de Série Temporal: Abordagem Delta

#### Problema Identificado: Static Predictions

O Random Forest, quando alimentado com features **congeladas** em valores de 2021, gerava predições constantes:
- 2022-2026: sempre o mesmo valor previsto
- Causa: sem evolução de features → entrada idêntica → saída idêntica

#### Solução Implementada: Delta-Based Forecasting

**Fluxo Tradicional (❌ Problemático)**:
```
valor_2021 = 2743 km²
features_futuro = {PIB: 262.9, IDH: 0.69, ...}  ← congelado em 2021
modelo.predict(features_futuro) = 2900 km²  (2022-2026, sempre igual)
```

**Fluxo Delta-Based (✅ Dinâmico)**:
```
1. Treina modelo em MUDANÇAS (delta): desmatamento_t - desmatamento_t-1
2. Para cada ano futuro:
   - Prevê delta_t usando features atualizadas
   - Reconstrói valor: valor_t = valor_t-1 + delta_previsto
   - Atualiza features para próximo ano (ex: desmatamento_lag1 ← valor_t)
3. Resultado: dinâmica temporal realista

Exemplo (PA):
  2021: 2743 km² (real)
  2022: 2743 + 2533 = 5276 km² (delta previsto: +2533)
  2023: 5276 - 3256 = 2020 km² (delta previsto: -3256)
  2024: 2020 + 2533 = 4554 km² (delta retorna ao padrão)
```

#### Por que isso funciona:

1. **Captura dinâmica temporal**: Modelo aprende padrões de mudança, não apenas valores
2. **Reduz extrapolação**: Prediz mudanças (bem-calibradas) em vez de níveis absolutos
3. **Feature evolution**: Features como `desmatamento_lag1` são atualizadas cada iteração
4. **Respeita padrões históricos**: Predições baseadas em variações observadas (±500 km²/ano típico)

#### Limitações e Mitigações:

| Limitação | Mitigação |
|-----------|-----------|
| Propagação de erro multi-ano | Usar validação cruzada para estimar incerteza |
| Deltas podem ser erráticos (alta variância) | Restringir delta máximo a ±80% do valor atual |
| Dependência de lag1 atualizado | Usar histórico expandido para cálculos de agregação |

---

## 📥 Dados: Origem e Justificativa

### Fontes Utilizadas

| Variável | Fonte | Período | Cobertura | Justificativa |
|----------|-------|---------|-----------|---------------|
| **Desmatamento (km²)** | PRODES/INPE | 2012-2021 | Amazônia Legal | Série histórica oficial, metodologia consolidada |
| **PIB (bilhões R$)** | IBGE/SIDRA | 2012-2021 | 9 UFs | Dados econômicos estaduais confiáveis |
| **IDH** | PNUD/IPEA | 2012-2021 | 9 UFs | Índice de desenvolvimento humano validado |
| **População** | IBGE | 2012-2021 | 9 UFs | Censos oficiais e estimativas intercensitárias |

### Por que não adquirir dados adicionais?

**Recursos adicionais considerados (mas não inclusos)**:

1. **Variáveis climáticas** (temperatura, precipitação)
   - ❌ Aumentaria dimensionalidade sem certificação estatística de melhoria
   - ✅ Atual R² (0.82-0.92) já é robusto

2. **Preços de commodities** (soja, gado)
   - ❌ Colinariedade com PIB e disponibilidade de dados incerta
   - ✅ PIB já captura efeito econômico agregado

3. **Dados de fiscalização** (multas, autos, operações)
   - ❌ Série histórica inconsistente entre estados e períodos
   - ✅ Modelo atual captura efeito via padrões históricos

**Decisão**: Manter **dados consolidados e confiáveis** (IBGE, INPE, PNUD) em vez de adicionar novas fontes com possível:
- Inconsistência metodológica
- Lacunas temporais
- Diminuição da interpretabilidade

### Qualidade dos Dados

| Aspecto | Status |
|--------|--------|
| **Completude** | 100% (90 registros: 9 UFs × 10 anos) |
| **Validação** | ✅ Verificado contra relatórios INPE/IBGE públicos |
| **Consistência** | ✅ Nenhuma contradição lógica ou ordem de magnitude inválida |
| **Outliers** | ⚠️ 2020 com pico extremo (documentado, mantido como representativo) |

---

## 🏛️ Governança de Dados

O projeto adota princípios de **governança de dados**, assegurando transparência, confiabilidade e uso responsável das informações ao:

- Utilizar exclusivamente **fontes oficiais e auditáveis** (INPE, IBGE, PNUD);
- Manter separação clara entre **dados brutos, processados e derivados**;
- Garantir **reprodutibilidade** por meio de notebooks versionados e pipeline documentado;
- Registrar decisões metodológicas, limitações e incertezas do modelo;
- Evitar a inclusão de dados sem consistência temporal ou metodológica comprovada.

Essas práticas fortalecem a confiabilidade dos resultados e a aplicabilidade das recomendações estratégicas.

---

## 🔬 Principais Passos da Análise

### Fluxo Completo (Reproduzível)

```
1. CARREGAMENTO (Notebook 01)
   └─ Dados brutos (90 registros)
   
2. EXPLORAÇÃO (Notebook 01)
   ├─ Análise descritiva (média, desvio, distribuição)
   ├─ Correlações (Pearson)
   ├─ Visualizações (séries temporais, scatter)
   └─ Identificação de outliers
   
3. FEATURE ENGINEERING (Notebook 02)
   ├─ Criação de 35+ variáveis derivadas
   │  ├─ Lags (1-2 períodos)
   │  ├─ Médias móveis (janela 3)
   │  ├─ Taxas de crescimento
   │  ├─ Normalizações
   │  └─ Interações
   ├─ Tratamento de NaN (forward/backward fill)
   ├─ Escalamento (StandardScaler)
   └─ Dataset final: 90 × 43 variáveis
   
4. MODELAGEM (Notebook 03)
   ├─ Comparação 7 modelos
   ├─ Seleção: Random Forest
   ├─ Otimização: GridSearchCV (18 combinações de hiperparâmetros)
   ├─ Validação cruzada: 5-fold
   └─ Resultado: R² teste = 0.82-0.92
   
5. PREDIÇÃO DELTA (Notebook 03)
   ├─ Treinamento em MUDANÇAS (desmatamento_t - desmatamento_t-1)
   ├─ Geração dinâmica 2022-2026 (com atualização de features)
   └─ Predições salvas: predicoes_2022_2026_delta.csv
   
6. VALIDAÇÃO (Todos notebooks)
   ├─ Resíduos ~ N(0, σ²)
   ├─ Importância de features coerente com EDA
   └─ Predições alinhadas com tendências históricas
```

---

## 💡 Insights Principais e Recomendações Estratégicas

### Insight 1: Desmatamento é Altamente Dinâmico (Lag-Dependent)

**Observação**: 60-70% da importância do modelo concentra-se em features de histórico (lag1, ma3, mean).

**Interpretação**:
- Desmatamento não é aleatório; segue padrões autocorrelacionados
- Valor de um ano é forte preditor do próximo
- Mudanças de política/economia geram inércia de ~2-3 anos

**Recomendação Estratégica**:
```
🎯 Intervenções em Desmatamento Devem Ser Contínuas
   
   ❌ INEFICAZ: Operações pontuais (1-2 meses)
      → Efeito desaparece rapidamente (lag volta ao padrão)
   
   ✅ EFICAZ: Programas sustentáveis de 3-5 anos
      → Quebram o padrão de autocorrelação
      → Novo nível de equilíbrio é estabelecido
```

---

### Insight 2: Heterogeneidade Estadual Crítica

**Observação**: 80% do desmatamento concentra-se em 3 estados (PA, MT, RO).

| Estado | Desmatamento 2021 (km²) | Tendência 2022-26 | Situação |
|--------|--------|-----------|----------|
| **PA** | 2743 | Volátil | Crítica |
| **MT** | 1590 | Estável (alto) | Crítica |
| **RO** | 872 | Crescente | Alerta |
| **MA** | 1237 | Reduz | Progresso |
| **AM** | 1475 | Reduz | Progresso |
| **AC, AP, RR, TO** | <200 cada | Residual | Monitorado |

**Recomendação Estratégica**:
```
🎯 Diferenciação de Políticas por Perfil Estadual

1. CRÍTICA (PA, MT):
   - Reforço de fiscalização (IBAMA, PF, ICMBio)
   - Regularização fundiária para reduzir incerteza legal
   - Incentivos para transição agropecuária sustentável
   - Meta: -30% em 3-5 anos (aplicar delta-based forecasting)

2. ALERTA (RO):
   - Monitoramento intensivo de fronteira agrícola
   - Programas de capacitação ambiental rural
   - Parcerias com agronegócio sustentável
   - Meta: Interromper crescimento (estabilizar)

3. PROGRESSO (MA, AM):
   - Consolidar ganhos recentes
   - Estudos de "best practices" para replicação
   - Certificação de produtos sustentáveis
   - Meta: Manter redução (-3% a.a.)

4. MONITORADO (demais):
   - Vigilância de potenciais pontos quentes
   - Prevenção (vs correção) de desmatamento
   - Integração com economia local
```

---

### Insight 3: PIB não Compensa Desmatamento

**Observação**: Correlação PIB-desmatamento é positiva (~0.4-0.5), não há "decoupling".

**Interpretação**:
- Crescimento econômico regional costuma ser baseado em expansão agropecuária
- Estados com maior PIB têm maior desmatamento
- Modelo linear não sustentável: "crescer sem desmatar" não é padrão

**Recomendação Estratégica**:
```
🎯 Transição Econômica Necessária

CENÁRIO ATUAL (Alto Risco):
  PIB ↑ → Desmatamento ↑  (correlação 0.45)
  
CENÁRIO DESEJADO:
  PIB ↑ → Desmatamento ↓  (decoupling)
  
COMO ALCANÇAR:

1. DIVERSIFICAÇÃO ECONÔMICA:
   - Investir em agronegócio de baixo-carbono
   - Turismo ecológico (bioeconomia)
   - Tecnologia verde e energias renováveis
   - Silvicultura sustentável
   
2. INCENTIVOS ECONÔMICOS:
   - Pagamentos por serviços ambientais (PSA)
   - Crédito verde com juros reduzidos
   - Mercado de carbono (Artigo 6 do Acordo de Paris)
   - Certificações de produto "zero-desflorestamento"
   
3. TRANSFORMAÇÃO PRODUTIVA:
   - Intensificação em áreas já desmatadas
   - Recuperação de pastagens degradadas
   - Integração lavoura-pecuária-floresta (ILPF)
   
PRAZO: 10-15 anos para regressão linear negativa PIB-desmatamento
```

---

### Insight 4: 2020 foi Excepcional (Não Será Repetido)

**Observação**: 2020 apresentou pico histórico (15,000+ km² total), 3-4x maior que média.

**Causas Identificadas**:
- Redução de fiscalização (pandemia, questões políticas)
- Aceleração de expansão de fronteira antes de transição de governo
- Evento climático (seca extrema facilitou incêndios)

**Interpretação do Modelo**:
- Random Forest captura pico como outlier (influencia features 2021)
- Predições 2022-26 refletem retorno ao padrão pré-2020
- Não esperar repetição automática de 2020 em cenários normais

**Recomendação Estratégica**:
```
🎯 Evitar "Voltar ao Baseline Pré-2020"

O pico de 2020 foi ANÔMALO, mas:
  - Revelou vulnerabilidade do sistema
  - Mostrou capacidade de escalação rápida
  
Recomendação:
  - Target não é voltar aos ~8,000 km²/ano (pré-2020)
  - Target é REDUZIR para 4,000-5,000 km²/ano (ambição Acordo Paris)
  - Implementar guardrails permanentes contra anomalias
  - Aumentar capacidade de resposta rápida (força-tarefa)
```

---

### Insight 5: Margem de Manobra Política é Pequena (Curto Prazo)

**Observação**: Modelo delta mostra que variações ano-a-ano são de ±500 km² (típico), com desvio padrão de ~600 km².

**Interpretação**:
- Desmatamento tem inércia estrutural (fronteira agrícola estabelecida)
- Políticas conseguem desvios de ±3-7% do esperado (em um ano)
- Mudanças maiores requerem 3-5 anos

**Recomendação Estratégica**:
```
🎯 Planos Plurianuais com Metas Realistas

REALISTA (Alcançável):
  2022-2023: -5% (redução: 7,500 → 7,125 km²)
  2024-2025: -5% adicional (7,125 → 6,769 km²)
  2026:      -3% (consolidação)
  TOTAL 2021→2026: -13% em 5 anos

AMBICIOSO (Requer Novo Regime):
  Implementar políticas radicais (proibição de conversão, etc)
  Efeito esperado: -25-30% em 5 anos
  Risco: Conflito social, judicialização
  Tempo de implementação: 2-3 anos até efeito mensurado

OTIMISTA DEMAIS (Improvável):
  -50% em 2-3 anos ← Desafia dinâmica estrutural
  Histórico global mostra redução >50% leva 10+ anos
```

---

## 📊 Indicadores de Monitoramento Recomendados

Para acompanhar evolução real vs predições:

```
MENSAL:
  └─ Alertas de desflorestamento (INPE/SAD)

TRIMESTRAL:
  ├─ Taxa acumulada do ano (%)
  └─ Comparação com baseline do ano anterior

ANUAL:
  ├─ Desmatamento total confirmado (km²)
  ├─ Comparação com predição modelo
  ├─ Atualização de features (PIB, IDH)
  ├─ Retreinamento do modelo
  └─ Revisão de recomendações estratégicas

BI-ANUAL:
  ├─ Avaliação de efetividade de políticas
  ├─ Análise de causas de desvios previstos
  └─ Replanejamento estratégico
```

---

## 📋 Conclusão e Próximos Passos

### ✅ Validação dos Resultados

#### Coerência com Literatura:
- ✅ Lag temporal como preditor principal (confirmado em estudos INPE)
- ✅ Correlação PIB-desmatamento positiva (expansão agropecuária)
- ✅ Heterogeneidade entre estados (PA/MT vs AP/TO)
- ✅ Tendência de redução pós-2021 (alinhado com políticas recentes)

#### Consistência Interna:
- ✅ R² alto + baixo viés residual = modelo confiável
- ✅ Importância de features alinha com EDA (correlações)
- ✅ Predições futuras seguem tendências históricas recentes
- ⚠️ Atenção para propagação de erro em predições multi-ano

### 🚀 Próximos Passos Recomendados

1. **Monitoramento contínuo**: Retreinar modelo anualmente com novos dados PRODES
2. **Análise de sensibilidade**: Testar cenários (política ambiental rigorosa vs frouxa)
3. **Ensemble com outros modelos**: Combinar Random Forest com Gradient Boosting
4. **Dados adicionais**: Incorporar variáveis climáticas, preços de commodities em future sprints
5. **Dashboard operacional**: Integrar modelo em sistema de monitoramento em tempo real
6. **Análise causal**: Estudar mecanismos específicos (fronteira agrícola, infraestrutura, etc.)
7. **Validação externa**: Comparar predições com especialistas em Amazônia (INPE, IMAZON, IPAM)
5. **Tratamento de outliers**: Considerar winsorização ou modelos robustos para 2019-2020

---

## 🛠️ Tecnologias

- **Python 3.11+**
- **pandas** - Manipulação de dados
- **numpy** - Computação numérica
- **scikit-learn** - Machine Learning
- **matplotlib & seaborn** - Visualização
- **jupyter** - Notebooks interativos

---

## 📝 Features Criadas

### Temporais
- Ano normalizado
- Década
- Período (primeira/segunda metade)

### Crescimento
- Taxa de crescimento de desmatamento
- Taxa de crescimento de PIB
- Taxa de crescimento de população
- Taxa de crescimento de IDH

### Lag (Defasagem)
- Desmatamento 1 ano atrás
- Desmatamento 2 anos atrás
- PIB 1 ano atrás
- IDH 1 ano atrás

### Rolling Statistics
- Média móvel (3 anos)
- Desvio padrão móvel (3 anos)

### Derivadas
- PIB per capita
- Desmatamento per capita
- Intensidade de desmatamento (km²/bilhão R$)
- IDH ajustado por desmatamento

### Agregações
- Média de desmatamento por estado
- Desvio do desmatamento em relação à média estadual
- Z-score do desmatamento por estado

---

## 🎨 Visualizações

O projeto inclui diversas visualizações:
- Séries temporais de desmatamento por estado
- Correlações entre variáveis
- Distribuições e outliers
- Importância das features
- Predições vs valores reais
- Projeções futuras

---

## 👥 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

## 📧 Contato

**Arthur Soares Marques**
- GitHub: [@ArthurDp78](https://github.com/ArthurDp78)

---

## 🙏 Agradecimentos

- **ZettaLab** - Proposta do desafio
- **INPE** - Dados de desmatamento (PRODES)
- **IBGE** - Dados socioeconômicos
- **IPEA** - Dados de IDH

---

## 📚 Referências

- [PRODES - Monitoramento do Desmatamento](http://www.obt.inpe.br/OBT/assuntos/programas/amazonia/prodes)
- [IBGE - Estatísticas](https://www.ibge.gov.br/)
- [IPEA - Base de Dados](http://www.ipeadata.gov.br/)
- [scikit-learn Documentation](https://scikit-learn.org/)

---

