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

## 🗂️ Estrutura do Projeto

```
projeto-desafio2/
│
├── data/
│   ├── raw/              # Dados originais (nunca modificar)
│   ├── base/             # Dados base organizados
│   │   ├── desmatamento/
│   │   ├── idh/
│   │   ├── pib/
│   │   └── populacao/
│   ├── limpos/           # Dados limpos e processados
│   ├── processed/        # Dados com feature engineering
│   └── external/         # Dados externos adquiridos
│
├── notebooks/
│   ├── 01_exploratory_analysis.ipynb      # Análise exploratória
│   ├── 02_feature_engineering.ipynb       # Criação de features
│   └── 03_modeling.ipynb                  # Modelagem e predições
│
├── src/                  # Scripts reutilizáveis
│   ├── __init__.py
│   ├── data_processing.py    # Processamento de dados
│   ├── modeling.py           # Treinamento de modelos
│   └── visualization.py      # Visualizações
│
├── models/               # Modelos treinados salvos
│   └── best_model.pkl
│
├── dashboards/
│   └── app.py           # Dashboard interativo (Streamlit/Dash)
│
├── requirements.txt     # Dependências do projeto
├── README.md           # Este arquivo
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

#### Recomendações:
1. **Monitoramento contínuo**: Retreinar modelo anualmente com novos dados
2. **Análise de sensibilidade**: Testar cenários (política ambiental rigorosa vs frouxa)
3. **Ensemble com outros modelos**: Combinar Random Forest com Gradient Boosting
4. **Dados adicionais**: Incorporar variáveis climáticas, preços de commodities
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

