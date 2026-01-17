import os
import re
import glob
import sys
import argparse
import logging
from pathlib import Path

# Bibliotecas de manipulação de dados
import pandas as pd
import geopandas as gpd

# Bibliotecas de visualização
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression
import numpy as np


# Caminho da base original
caminho = "base/desmatamento/desmatamento_por_estado.csv"

# UFs da Amazônia Legal
AMAZONIA_LEGAL_UFS = {"AC", "AM", "AP", "MA", "MT", "PA", "RO", "RR", "TO"}

# Arquivo de saída
output = Path("limpos/desmatamento/desmatamento_2012-2021.csv")
output.parent.mkdir(parents=True, exist_ok=True)

print("Iniciando processamento do desmatamento...")

# 1️⃣ Ler a base (tratando BOM/encoding)
try:
    df = pd.read_csv(caminho, encoding='utf-8-sig', low_memory=False)
except Exception:
    df = pd.read_csv(caminho, encoding='latin-1', low_memory=False)
print("✅ Base carregada com sucesso!", f"(linhas={len(df)})")

# 2️⃣ Detectar e normalizar colunas esperadas com fallback
col_candidates = {
    'state': ['state', 'estado', 'uf', 'UF', 'State'],
    'year': ['year', 'ano', 'Year', 'YEAR'],
    'area': ['area_km', 'area', 'area_km2', 'area__km']
}

col_map = {}
for target, candidates in col_candidates.items():
    for c in candidates:
        if c in df.columns:
            col_map[c] = target
            break

if not any(v == 'state' for v in col_map.values()) and 'state' not in df.columns and 'estado' not in df.columns:
    # try common column names
    if 'UF' in df.columns:
        df = df.rename(columns={'UF': 'state'})
        col_map['state'] = 'state'

# Apply renames to standard names
rename_map = {}
if any(k for k,v in col_map.items() if v == 'state'):
    src = next(k for k,v in col_map.items() if v == 'state')
    rename_map[src] = 'UF'
if any(k for k,v in col_map.items() if v == 'year'):
    src = next(k for k,v in col_map.items() if v == 'year')
    rename_map[src] = 'ano'
if any(k for k,v in col_map.items() if v == 'area'):
    src = next(k for k,v in col_map.items() if v == 'area')
    rename_map[src] = 'area_km'

if not rename_map:
    raise KeyError('Colunas esperadas não encontradas. Procure por state/estado/UF, year/ano e area_km/area.')

df = df.rename(columns=rename_map)
print('🔹 Colunas após normalização:', list(df.columns))

# 3️⃣ Converter tipos
if 'ano' in df.columns:
    df['ano'] = pd.to_numeric(df['ano'], errors='coerce')
else:
    raise KeyError('Coluna "ano" não encontrada após normalização.')

if 'area_km' in df.columns:
    df['area_km'] = pd.to_numeric(df['area_km'], errors='coerce')
else:
    raise KeyError('Coluna "area_km" não encontrada após normalização.')

# 4️⃣ Remover linhas inválidas e filtrar anos
before = len(df)
df = df.dropna(subset=['ano', 'area_km', 'UF'])
df['ano'] = df['ano'].astype(int)
df['UF'] = df['UF'].astype(str).str.strip().str.upper()
df = df[(df['ano'] >= 2012) & (df['ano'] <= 2021)]
print(f'Linhas removidas por inválidos/fora de intervalo: {before - len(df)}')

# 5️⃣ Filtrar apenas UFs da Amazônia Legal
ufs_found = sorted(df['UF'].unique())
extra_ufs = [u for u in ufs_found if u not in AMAZONIA_LEGAL_UFS]
if extra_ufs:
    print('⚠️  Foram encontrados UFs fora da Amazônia Legal e serão removidos:', extra_ufs)
    df = df[df['UF'].isin(AMAZONIA_LEGAL_UFS)]

# 6️⃣ Agregar total de área desmatada por estado e ano
df_estado = df.groupby(['UF', 'ano'], as_index=False)['area_km'].sum()

# 7️⃣ Salvar versão agregada
df_estado.to_csv(output, index=False, encoding='utf-8-sig')
print('✅ Base agregada por estado salva com sucesso em', output)