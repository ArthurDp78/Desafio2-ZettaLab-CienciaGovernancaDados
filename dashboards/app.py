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

# ========== SEÇÃO 1: VISÃO GERAL ==========
st.header("📊 Visão Geral")

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_desmatamento = df_filtrado['desmatamento_km2'].sum()
    st.metric("Desmatamento Total", f"{total_desmatamento:,.0f} km²")

with col2:
    media_anual = df_filtrado.groupby('ano')['desmatamento_km2'].sum().mean()
    st.metric("Média Anual", f"{media_anual:,.0f} km²")

with col3:
    pib_medio = df_filtrado['pib_bilhoes'].mean()
    st.metric("PIB Médio", f"R$ {pib_medio:.1f}bi")

with col4:
    idh_medio = df_filtrado['IDH'].mean()
    st.metric("IDH Médio", f"{idh_medio:.3f}")

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

# ========== SEÇÃO 3: COMPARAÇÃO ENTRE ESTADOS ==========
st.header("🗺️ Comparação entre Estados")

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

# ========== SEÇÃO 4: CORRELAÇÕES ==========
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

# ========== SEÇÃO 5: PREDIÇÕES FUTURAS ==========
if df_predicoes is not None:
    st.header("🔮 Predições Futuras (2022-2026)")
    
    # Filtra predições para estados selecionados
    df_pred_filtrado = df_predicoes[df_predicoes['UF'].isin(estados_selecionados)]
    
    # Combina histórico + predições
    df_historico_estados = df_historico[df_historico['UF'].isin(estados_selecionados)][['UF', 'ano', 'desmatamento_km2']]
    df_historico_estados['tipo'] = 'Histórico'
    
    df_pred_plot = df_pred_filtrado.copy()
    df_pred_plot['desmatamento_km2'] = df_pred_plot['desmatamento_predito_km2']
    df_pred_plot['tipo'] = 'Predição'
    df_pred_plot = df_pred_plot[['UF', 'ano', 'desmatamento_km2', 'tipo']]
    
    df_completo = pd.concat([df_historico_estados, df_pred_plot], ignore_index=True)
    
    # Gráfico histórico + predições
    fig_pred = px.line(
        df_completo,
        x='ano',
        y='desmatamento_km2',
        color='UF',
        line_dash='tipo',
        markers=True,
        title='Histórico e Predições de Desmatamento (2012-2026)',
        labels={'desmatamento_km2': 'Desmatamento (km²)', 'ano': 'Ano', 'tipo': 'Tipo'}
    )
    fig_pred.add_vline(x=2021.5, line_dash="dot", line_color="red", 
                       annotation_text="Início das Predições", annotation_position="top")
    fig_pred.update_layout(height=500)
    st.plotly_chart(fig_pred, use_container_width=True)
    
    # Tabela de predições
    st.subheader("📋 Tabela de Predições")
    predicoes_pivot = df_pred_filtrado.pivot(index='ano', columns='UF', values='desmatamento_predito_km2')
    predicoes_pivot['TOTAL'] = predicoes_pivot.sum(axis=1)
    st.dataframe(predicoes_pivot.style.format("{:.0f}"), use_container_width=True)
    
    # Tendência das predições
    total_2021 = df_historico[df_historico['ano'] == 2021]['desmatamento_km2'].sum()
    total_2026_pred = df_predicoes[df_predicoes['ano'] == 2026]['desmatamento_predito_km2'].sum()
    variacao_pct = ((total_2026_pred - total_2021) / total_2021) * 100
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Desmatamento 2021 (Real)", f"{total_2021:,.0f} km²")
    with col2:
        st.metric("Desmatamento 2026 (Predito)", f"{total_2026_pred:,.0f} km²")
    with col3:
        st.metric("Variação Esperada", f"{variacao_pct:+.1f}%", delta_color="inverse")

else:
    st.info("ℹ️ Execute o notebook **03_modeling.ipynb** para gerar as predições futuras.")

st.markdown("---")

# ========== SEÇÃO 6: TABELA DE DADOS ==========
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
