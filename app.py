import os
import re
import glob

# Bibliotecas de manipulação de dados
import pandas as pd
import geopandas as gpd

# Bibliotecas de visualização
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression
import numpy as np


anos_pib = list(range(2021, 1990, -1))  # 2021, 2020, ..., 1991


print("Iniciando download dos dados do PIB (IBGE SIDRA)...")

for ano in anos_pib:
    print(f"Baixando dados de {ano}...")
    
    # URL da API SIDRA para o PIB municipal
    url = f"https://apisidra.ibge.gov.br/values/t/5938/n6/all/v/37/p/{ano}"
    df_pib = pd.read_json(url)
    
    # Salvar o arquivo bruto
    output_path = f"base/pib/pib_municipal_{ano}.csv"
    df_pib.to_csv(output_path, index=False)

print("✅ Download dos dados brutos do PIB concluído!")