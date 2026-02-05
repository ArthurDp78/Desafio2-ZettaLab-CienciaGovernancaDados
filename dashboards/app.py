"""
Dashboard Interativo - Desmatamento na Amazônia Legal
Desafio 2 - Ciência e Governança de Dados

Execute: streamlit run dashboards/app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# Configuração da página
st.set_page_config(
    page_title="Desmatamento Amazônia Legal",
    page_icon="🌳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título principal
st.title("🌳 Análise e Predição de Desmatamento na Amazônia Legal")
st.markdown("### Desafio 2 - Ciência e Governança de Dados")
st.markdown("---")

# Cache para carregar dados (evita recarregar a cada interação)
@st.cache_data
def load_data():
    """Carrega dados históricos e predições"""
    try:
        # Caminho base do projeto (sobe um nível da pasta dashboards)
        base_path = Path(__file__).parent.parent
        
        # Dados históricos
        df_hist = pd.read_csv(base_path / 'data' / 'processed' / 'base_final.csv')
        
        # Dados com features (se existir)
        try:
            df_eng = pd.read_csv(base_path / 'data' / 'processed' / 'base_final_engineered.csv')
        except:
            df_eng = None
        
        # Predições futuras (tenta DELTA primeiro, depois original)
        try:
            df_pred = pd.read_csv(base_path / 'data' / 'processed' / 'predicoes_2022_2026_delta.csv')
            # Renomeia coluna para padronizar
            if 'desmatamento_previsto_km2' in df_pred.columns:
                df_pred = df_pred.rename(columns={'desmatamento_previsto_km2': 'desmatamento_predito_km2'})
        except:
            try:
                df_pred = pd.read_csv(base_path / 'data' / 'processed' / 'predicoes_2022_2026.csv')
            except:
                df_pred = None
        
        return df_hist, df_eng, df_pred
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return None, None, None

# Carrega dados
df_historico, df_engineered, df_predicoes = load_data()

if df_historico is None:
    st.error("⚠️ Não foi possível carregar os dados. Verifique se os arquivos estão na pasta correta.")
    st.stop()

# Sidebar - Filtros
st.sidebar.header("🔧 Filtros")

# Filtro de estados
estados_disponiveis = sorted(df_historico['UF'].unique())
estados_selecionados = st.sidebar.multiselect(
    "Selecione os Estados:",
    options=estados_disponiveis,
    default=estados_disponiveis[:3]  # Primeiros 3 por padrão
)

# Filtro de período
ano_min = int(df_historico['ano'].min())
ano_max = int(df_historico['ano'].max())
periodo_selecionado = st.sidebar.slider(
    "Período Histórico:",
    min_value=ano_min,
    max_value=ano_max,
    value=(ano_min, ano_max)
)

# Filtra dados
df_filtrado = df_historico[
    (df_historico['UF'].isin(estados_selecionados)) &
    (df_historico['ano'] >= periodo_selecionado[0]) &
    (df_historico['ano'] <= periodo_selecionado[1])
]

# Se nenhum estado selecionado
if len(estados_selecionados) == 0:
    st.warning("⚠️ Selecione pelo menos um estado no menu lateral.")
    st.stop()

# ========== SEÇÃO 1: VISÃO GERAL COM KPI CARDS ==========
st.header("📊 Visão Geral e KPIs")

# Calcula tendência
anos_recentes = sorted(df_filtrado['ano'].unique())[-3:] if len(df_filtrado['ano'].unique()) >= 3 else sorted(df_filtrado['ano'].unique())
df_2anos_recentes = df_filtrado[df_filtrado['ano'].isin(anos_recentes)]
desmat_2anos = df_2anos_recentes.groupby('ano')['desmatamento_km2'].sum().sort_index()

col1, col2, col3, col4 = st.columns(4)

# KPI 1: Desmatamento Total com Tendência
with col1:
    total_desmatamento = df_filtrado['desmatamento_km2'].sum()
    if len(desmat_2anos) >= 2:
        tendencia_total = desmat_2anos.iloc[-1] - desmat_2anos.iloc[-2]
        delta_text = f"{tendencia_total:+,.0f} km² (vs ano anterior)"
    else:
        delta_text = None
    st.metric("Desmatamento Total", f"{total_desmatamento:,.0f} km²", delta=delta_text, delta_color="inverse")

# KPI 2: Média Anual com Tendência
with col2:
    media_anual = df_filtrado.groupby('ano')['desmatamento_km2'].sum().mean()
    if len(desmat_2anos) >= 2:
        media_recente = desmat_2anos.iloc[-1]
        delta_media = f"{media_recente - media_anual:+,.0f} km²"
    else:
        delta_media = None
    st.metric("Média Histórica", f"{media_anual:,.0f} km²", delta=delta_media)

# KPI 3: PIB Médio
with col3:
    pib_medio = df_filtrado['pib_bilhoes'].mean()
    pib_2021 = df_historico[df_historico['ano'] == 2021]['pib_bilhoes'].mean()
    pib_2020 = df_historico[df_historico['ano'] == 2020]['pib_bilhoes'].mean()
    if pib_2020 > 0:
        delta_pib = f"{((pib_2021 - pib_2020) / pib_2020 * 100):+.1f}%"
    else:
        delta_pib = None
    st.metric("PIB Médio", f"R$ {pib_medio:.1f}bi", delta=delta_pib)

# KPI 4: IDH Médio
with col4:
    idh_medio = df_filtrado['IDH'].mean()
    idh_2021 = df_historico[df_historico['ano'] == 2021]['IDH'].mean()
    idh_2020 = df_historico[df_historico['ano'] == 2020]['IDH'].mean()
    if idh_2020 > 0:
        delta_idh = f"{((idh_2021 - idh_2020) / idh_2020 * 100):+.1f}%"
    else:
        delta_idh = None
    st.metric("IDH Médio", f"{idh_medio:.3f}", delta=delta_idh)

# Gráfico de tendência de cores
st.markdown("#### 📉 Tendência Recente")
tendencia_dados = df_historico[df_historico['UF'].isin(estados_selecionados)].copy()
tendencia_anual = tendencia_dados.groupby('ano')['desmatamento_km2'].sum().reset_index()
tendencia_anual['Cor'] = tendencia_anual['desmatamento_km2'].apply(
    lambda x: 'Acima' if x > tendencia_anual['desmatamento_km2'].mean() else 'Abaixo'
)

fig_tendencia = px.bar(
    tendencia_anual,
    x='ano',
    y='desmatamento_km2',
    color='Cor',
    color_discrete_map={'Acima': '#d62728', 'Abaixo': '#2ca02c'},
    title='Desmatamento vs Média Histórica',
    labels={'desmatamento_km2': 'Desmatamento (km²)', 'ano': 'Ano'}
)
fig_tendencia.update_layout(height=250, showlegend=False)
st.plotly_chart(fig_tendencia, use_container_width=True)

st.markdown("---")

# ========== SEÇÃO 2: EVOLUÇÃO TEMPORAL ==========
st.header("📈 Evolução Temporal do Desmatamento")

# Gráfico de linha por estado
fig_temporal = px.line(
    df_filtrado,
    x='ano',
    y='desmatamento_km2',
    color='UF',
    markers=True,
    title='Desmatamento por Estado ao Longo do Tempo',
    labels={'desmatamento_km2': 'Desmatamento (km²)', 'ano': 'Ano', 'UF': 'Estado'}
)
fig_temporal.update_layout(height=500)
st.plotly_chart(fig_temporal, use_container_width=True)

# Desmatamento total por ano
desmat_total_ano = df_filtrado.groupby('ano')['desmatamento_km2'].sum().reset_index()
fig_total = px.bar(
    desmat_total_ano,
    x='ano',
    y='desmatamento_km2',
    title='Desmatamento Total por Ano (Estados Selecionados)',
    labels={'desmatamento_km2': 'Desmatamento Total (km²)', 'ano': 'Ano'},
    color='desmatamento_km2',
    color_continuous_scale='Reds'
)
fig_total.update_layout(height=400)
st.plotly_chart(fig_total, use_container_width=True)

st.markdown("---")

# ========== SEÇÃO 3A: ANÁLISE DETALHADA POR ESTADO (NOVO) ==========
st.header("🔍 Análise Detalhada por Estado")

# Seletor de estado para análise profunda
estado_analise = st.selectbox(
    "Selecione um estado para análise detalhada:",
    options=sorted(df_historico['UF'].unique()),
    index=0
)

df_estado = df_historico[df_historico['UF'] == estado_analise].sort_values('ano')

# KPIs do estado selecionado
st.markdown(f"### {estado_analise} - Indicadores")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    desmat_total_estado = df_estado['desmatamento_km2'].sum()
    st.metric("Total Desmat.", f"{desmat_total_estado:,.0f} km²")

with col2:
    desmat_media_estado = df_estado['desmatamento_km2'].mean()
    st.metric("Média Anual", f"{desmat_media_estado:,.0f} km²")

with col3:
    desmat_max_ano = df_estado.loc[df_estado['desmatamento_km2'].idxmax(), 'ano']
    desmat_max = df_estado['desmatamento_km2'].max()
    st.metric("Pico Histórico", f"{desmat_max:,.0f} km²", f"({int(desmat_max_ano)})")

with col4:
    desmat_2021 = df_estado[df_estado['ano'] == 2021]['desmatamento_km2'].values
    desmat_2012 = df_estado[df_estado['ano'] == 2012]['desmatamento_km2'].values
    if len(desmat_2021) > 0 and len(desmat_2012) > 0:
        variacao_periodo = ((desmat_2021[0] - desmat_2012[0]) / desmat_2012[0] * 100)
        st.metric("Variação 2012-21", f"{variacao_periodo:+.1f}%", delta_color="inverse")

with col5:
    pib_2021 = df_estado[df_estado['ano'] == 2021]['pib_bilhoes'].values
    if len(pib_2021) > 0:
        st.metric("PIB 2021", f"R$ {pib_2021[0]:.1f}bi")

# Grid de 2 colunas para análise detalhada
col1, col2 = st.columns(2)

with col1:
    # Série temporal do estado
    fig_estado_serie = px.line(
        df_estado,
        x='ano',
        y='desmatamento_km2',
        markers=True,
        title=f'Série Histórica de Desmatamento - {estado_analise}',
        labels={'desmatamento_km2': 'Desmatamento (km²)', 'ano': 'Ano'},
        line_shape='spline'
    )
    fig_estado_serie.update_traces(line=dict(color='#d62728', width=3), marker=dict(size=8))
    fig_estado_serie.update_layout(height=400)
    st.plotly_chart(fig_estado_serie, use_container_width=True)

with col2:
    # Comparação com média amazônia
    media_amazonia = df_historico.groupby('ano')['desmatamento_km2'].mean()
    df_comparacao = pd.DataFrame({
        'Ano': df_estado['ano'],
        estado_analise: df_estado['desmatamento_km2'].values,
        'Média Amazônia': [media_amazonia[ano] if ano in media_amazonia.index else 0 for ano in df_estado['ano'].values]
    })
    
    fig_comparacao = px.line(
        df_comparacao,
        x='Ano',
        y=[estado_analise, 'Média Amazônia'],
        markers=True,
        title=f'{estado_analise} vs Média da Amazônia',
        labels={'value': 'Desmatamento (km²)'}
    )
    fig_comparacao.update_layout(height=400)
    st.plotly_chart(fig_comparacao, use_container_width=True)

# Análise de correlações do estado
st.markdown(f"### 🔗 Correlações para {estado_analise}")

col1, col2, col3 = st.columns(3)

with col1:
    corr_pib = df_estado['desmatamento_km2'].corr(df_estado['pib_bilhoes'])
    fig_corr_pib = px.scatter(
        df_estado,
        x='pib_bilhoes',
        y='desmatamento_km2',
        hover_data=['ano'],
        title=f'PIB vs Desmatamento (r={corr_pib:.2f})',
        labels={'pib_bilhoes': 'PIB (Bilhões R$)', 'desmatamento_km2': 'Desmatamento (km²)'},
        trendline='ols',
        color_discrete_sequence=['#ff7f0e']
    )
    fig_corr_pib.update_layout(height=350)
    st.plotly_chart(fig_corr_pib, use_container_width=True)

with col2:
    corr_idh = df_estado['desmatamento_km2'].corr(df_estado['IDH'])
    fig_corr_idh = px.scatter(
        df_estado,
        x='IDH',
        y='desmatamento_km2',
        hover_data=['ano'],
        title=f'IDH vs Desmatamento (r={corr_idh:.2f})',
        labels={'IDH': 'IDH', 'desmatamento_km2': 'Desmatamento (km²)'},
        trendline='ols',
        color_discrete_sequence=['#2ca02c']
    )
    fig_corr_idh.update_layout(height=350)
    st.plotly_chart(fig_corr_idh, use_container_width=True)

with col3:
    corr_pop = df_estado['desmatamento_km2'].corr(df_estado['populacao'])
    fig_corr_pop = px.scatter(
        df_estado,
        x='populacao',
        y='desmatamento_km2',
        hover_data=['ano'],
        title=f'População vs Desmatamento (r={corr_pop:.2f})',
        labels={'populacao': 'População', 'desmatamento_km2': 'Desmatamento (km²)'},
        trendline='ols',
        color_discrete_sequence=['#1f77b4']
    )
    fig_corr_pop.update_layout(height=350)
    st.plotly_chart(fig_corr_pop, use_container_width=True)

# Tabela de dados do estado
st.markdown(f"### 📋 Dados do {estado_analise}")
df_estado_display = df_estado[['ano', 'desmatamento_km2', 'pib_bilhoes', 'IDH', 'populacao']].copy()
df_estado_display.columns = ['Ano', 'Desmatamento (km²)', 'PIB (bilhões R$)', 'IDH', 'População']
st.dataframe(df_estado_display.style.format({
    'Desmatamento (km²)': '{:,.0f}',
    'PIB (bilhões R$)': '{:.2f}',
    'IDH': '{:.4f}',
    'População': '{:,.0f}'
}), use_container_width=True)

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    # Média por estado
    media_estado = df_filtrado.groupby('UF')['desmatamento_km2'].mean().sort_values(ascending=False).reset_index()
    fig_media = px.bar(
        media_estado,
        x='UF',
        y='desmatamento_km2',
        title='Desmatamento Médio por Estado',
        labels={'desmatamento_km2': 'Desmatamento Médio (km²)', 'UF': 'Estado'},
        color='desmatamento_km2',
        color_continuous_scale='Oranges'
    )
    st.plotly_chart(fig_media, use_container_width=True)

with col2:
    # Total por estado
    total_estado = df_filtrado.groupby('UF')['desmatamento_km2'].sum().sort_values(ascending=False).reset_index()
    fig_pizza = px.pie(
        total_estado,
        values='desmatamento_km2',
        names='UF',
        title='Distribuição do Desmatamento Total',
        hole=0.4
    )
    st.plotly_chart(fig_pizza, use_container_width=True)

st.markdown("---")

# ========== SEÇÃO 5: CORRELAÇÕES ==========
st.header("🔗 Correlações entre Variáveis")

col1, col2 = st.columns(2)

with col1:
    # Scatter PIB vs Desmatamento
    fig_pib = px.scatter(
        df_filtrado,
        x='pib_bilhoes',
        y='desmatamento_km2',
        color='UF',
        size='populacao',
        hover_data=['ano'],
        title='PIB vs Desmatamento',
        labels={'pib_bilhoes': 'PIB (Bilhões R$)', 'desmatamento_km2': 'Desmatamento (km²)'},
        trendline='ols'
    )
    st.plotly_chart(fig_pib, use_container_width=True)

with col2:
    # Scatter IDH vs Desmatamento
    fig_idh = px.scatter(
        df_filtrado,
        x='IDH',
        y='desmatamento_km2',
        color='UF',
        size='populacao',
        hover_data=['ano'],
        title='IDH vs Desmatamento',
        labels={'IDH': 'IDH', 'desmatamento_km2': 'Desmatamento (km²)'},
        trendline='ols'
    )
    st.plotly_chart(fig_idh, use_container_width=True)

st.markdown("---")

# ========== SEÇÃO 5: PREDIÇÕES FUTURAS COM COMPARAÇÃO REALIZADO VS PREDITO ==========
if df_predicoes is not None:
    st.header("🔮 Predições Futuras (2022-2026) - Realizado vs Predito")
    
    # Filtra predições para estados selecionados
    df_pred_filtrado = df_predicoes[df_predicoes['UF'].isin(estados_selecionados)]
    
    # Combina histórico + predições
    df_historico_estados = df_historico[df_historico['UF'].isin(estados_selecionados)][['UF', 'ano', 'desmatamento_km2']]
    df_historico_estados['tipo'] = 'Histórico'
    df_historico_estados['status'] = 'Realizado'
    
    df_pred_plot = df_pred_filtrado.copy()
    df_pred_plot['desmatamento_km2'] = df_pred_plot['desmatamento_predito_km2']
    df_pred_plot['tipo'] = 'Predição'
    df_pred_plot['status'] = 'Predito'
    df_pred_plot = df_pred_plot[['UF', 'ano', 'desmatamento_km2', 'tipo', 'status']]
    
    df_historico_estados['status'] = 'Realizado'
    df_completo = pd.concat([df_historico_estados, df_pred_plot], ignore_index=True)
    
    # Gráfico de linha com cor diferenciada
    fig_pred = px.line(
        df_completo,
        x='ano',
        y='desmatamento_km2',
        color='UF',
        line_dash='tipo',
        markers=True,
        title='Histórico e Predições de Desmatamento (2012-2026)',
        labels={'desmatamento_km2': 'Desmatamento (km²)', 'ano': 'Ano', 'tipo': 'Tipo'},
        line_shape='spline'
    )
    fig_pred.add_vline(x=2021.5, line_dash="dot", line_color="red", annotation_text="Início das Predições", annotation_position="top")
    fig_pred.update_layout(height=500, hovermode='x unified')
    st.plotly_chart(fig_pred, use_container_width=True)
    
    # NOVO: Comparação visual Realizado vs Predito
    st.markdown("#### 📊 Comparação: Realizado vs Predito")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Desmatamento total histórico
        desmat_hist_total = df_historico[df_historico['UF'].isin(estados_selecionados)].groupby('ano')['desmatamento_km2'].sum().reset_index()
        desmat_hist_total['Tipo'] = 'Realizado'
        
        # Desmatamento total predito
        desmat_pred_total = df_pred_filtrado.groupby('ano')['desmatamento_predito_km2'].sum().reset_index()
        desmat_pred_total.columns = ['ano', 'desmatamento_km2']
        desmat_pred_total['Tipo'] = 'Predito'
        
        # Combine
        desmat_comparacao = pd.concat([
            desmat_hist_total[desmat_hist_total['ano'] >= 2018],
            desmat_pred_total
        ], ignore_index=True)
        
        fig_comparacao_total = px.bar(
            desmat_comparacao,
            x='ano',
            y='desmatamento_km2',
            color='Tipo',
            barmode='group',
            title='Desmatamento Total: Histórico vs Predições',
            labels={'desmatamento_km2': 'Desmatamento (km²)', 'ano': 'Ano'},
            color_discrete_map={'Realizado': '#1f77b4', 'Predito': '#ff7f0e'},
            opacity=0.8
        )
        fig_comparacao_total.update_layout(height=400)
        st.plotly_chart(fig_comparacao_total, use_container_width=True)
    
    with col2:
        # Diferença entre realizado e predito (média)
        desmat_2021_real = df_historico[df_historico['ano'] == 2021]['desmatamento_km2'].sum()
        desmat_2022_pred = df_predicoes[df_predicoes['ano'] == 2022]['desmatamento_predito_km2'].sum()
        desmat_2026_pred = df_predicoes[df_predicoes['ano'] == 2026]['desmatamento_predito_km2'].sum()
        
        tendencia_data = {
            'Período': ['2021\n(Real)', '2022\n(Pred.)', '2026\n(Pred.)'],
            'Desmatamento': [desmat_2021_real, desmat_2022_pred, desmat_2026_pred],
            'Tipo': ['Realizado', 'Predito', 'Predito']
        }
        df_tendencia_comparacao = pd.DataFrame(tendencia_data)
        
        fig_tendencia_comp = px.bar(
            df_tendencia_comparacao,
            x='Período',
            y='Desmatamento',
            color='Tipo',
            title='Trajetória: 2021 Real → 2022-2026 Predito',
            labels={'Desmatamento': 'Desmatamento (km²)'},
            color_discrete_map={'Realizado': '#2ca02c', 'Predito': '#d62728'},
            opacity=0.8
        )
        
        # Adiciona linha de tendência
        fig_tendencia_comp.add_hline(y=desmat_2021_real, line_dash="dash", line_color="gray", 
                                    annotation_text="Baseline 2021", annotation_position="right")
        
        fig_tendencia_comp.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_tendencia_comp, use_container_width=True)
    
    # Tabela de predições com comparação
    st.subheader("📋 Comparação Detalhada de Predições")
    
    # Agrupa por estado e ano
    comparacao_detalhada = []
    for estado in estados_selecionados:
        df_estado_pred = df_pred_filtrado[df_pred_filtrado['UF'] == estado]
        for _, row in df_estado_pred.iterrows():
            comparacao_detalhada.append({
                'UF': estado,
                'Ano': int(row['ano']),
                'Predito (km²)': row['desmatamento_predito_km2'],
                'vs 2021 (%)': ((row['desmatamento_predito_km2'] - desmat_2021_real / len(estados_selecionados)) / (desmat_2021_real / len(estados_selecionados)) * 100)
            })
    
    df_comparacao_tabela = pd.DataFrame(comparacao_detalhada)
    
    st.dataframe(
        df_comparacao_tabela.style.format({
            'Predito (km²)': '{:,.0f}',
            'vs 2021 (%)': '{:+.1f}%'
        }),
        use_container_width=True
    )
    
    # Insights da predição
    st.markdown("### 💡 Insights das Predições")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        reducao_total = desmat_2021_real - desmat_2026_pred
        reducao_pct = (reducao_total / desmat_2021_real) * 100
        st.metric(
            "Redução Esperada (2021→2026)",
            f"{reducao_total:,.0f} km²",
            f"{reducao_pct:.1f}%",
            delta_color="inverse"
        )
    
    with col2:
        variacao_anual_media = (desmat_2026_pred - desmat_2021_real) / 5
        st.metric(
            "Variação Média Anual",
            f"{variacao_anual_media:+,.0f} km²",
            "por ano",
            delta_color="inverse"
        )
    
    with col3:
        maior_volatilidade = df_pred_filtrado.groupby('UF')['desmatamento_predito_km2'].std().max()
        estado_volatil = df_pred_filtrado.groupby('UF')['desmatamento_predito_km2'].std().idxmax()
        st.metric(
            "Maior Volatilidade",
            f"{estado_volatil}",
            f"σ = {maior_volatilidade:.0f} km²"
        )
else:
    st.info("ℹ️ Execute o notebook **03_modeling.ipynb** para gerar as predições futuras.")

st.markdown("---")

# ========== SEÇÃO 7: TABELA DE DADOS ==========
with st.expander("📋 Ver Tabela de Dados Completa"):
    st.dataframe(df_filtrado, use_container_width=True)
    
    # Download CSV
    csv = df_filtrado.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Baixar Dados em CSV",
        data=csv,
        file_name='dados_desmatamento_filtrados.csv',
        mime='text/csv'
    )

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
        🌳 Dashboard de Análise de Desmatamento na Amazônia Legal<br>
        Desafio 2 - ZettaLab | Dados: INPE, IBGE, IPEA
    </div>
    """,
    unsafe_allow_html=True
)
