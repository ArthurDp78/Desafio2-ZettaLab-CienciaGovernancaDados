"""
Módulo para processamento e limpeza de dados
Desafio 2 - Ciência e Governança de Dados
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import List, Dict, Tuple


class DataProcessor:
    """Classe para processar e limpar dados da Amazônia Legal"""
    
    AMAZONIA_LEGAL_UFS = {"AC", "AM", "AP", "MA", "MT", "PA", "RO", "RR", "TO"}
    
    def __init__(self, base_path: str = "data"):
        """
        Inicializa o processador de dados
        
        Args:
            base_path: Caminho base para os dados
        """
        self.base_path = Path(base_path)
        self.raw_path = self.base_path / "raw"
        self.processed_path = self.base_path / "processed"
        
    def load_base_final(self) -> pd.DataFrame:
        """
        Carrega a base final consolidada
        
        Returns:
            DataFrame com dados consolidados
        """
        file_path = self.processed_path / "base_final.csv"
        df = pd.read_csv(file_path)
        return df
    
    def filter_amazonia_legal(self, df: pd.DataFrame, uf_column: str = 'UF') -> pd.DataFrame:
        """
        Filtra apenas estados da Amazônia Legal
        
        Args:
            df: DataFrame a ser filtrado
            uf_column: Nome da coluna com UF
            
        Returns:
            DataFrame filtrado
        """
        return df[df[uf_column].isin(self.AMAZONIA_LEGAL_UFS)].copy()
    
    def check_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Verifica valores faltantes no DataFrame
        
        Args:
            df: DataFrame para verificar
            
        Returns:
            DataFrame com estatísticas de valores faltantes
        """
        missing = pd.DataFrame({
            'Total_Missing': df.isnull().sum(),
            'Percent_Missing': (df.isnull().sum() / len(df) * 100).round(2)
        })
        missing = missing[missing['Total_Missing'] > 0].sort_values('Total_Missing', ascending=False)
        return missing
    
    def remove_outliers_iqr(self, df: pd.DataFrame, column: str, factor: float = 1.5) -> pd.DataFrame:
        """
        Remove outliers usando método IQR
        
        Args:
            df: DataFrame
            column: Coluna para remover outliers
            factor: Fator multiplicador do IQR (padrão 1.5)
            
        Returns:
            DataFrame sem outliers
        """
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - factor * IQR
        upper_bound = Q3 + factor * IQR
        
        mask = (df[column] >= lower_bound) & (df[column] <= upper_bound)
        return df[mask].copy()
    
    def create_time_features(self, df: pd.DataFrame, year_column: str = 'ano') -> pd.DataFrame:
        """
        Cria features temporais
        
        Args:
            df: DataFrame
            year_column: Nome da coluna de ano
            
        Returns:
            DataFrame com novas features temporais
        """
        df = df.copy()
        
        # Ano como variável categórica
        df['ano_categorico'] = df[year_column].astype(str)
        
        # Ano normalizado (0-1)
        df['ano_normalizado'] = (df[year_column] - df[year_column].min()) / (df[year_column].max() - df[year_column].min())
        
        # Década
        df['decada'] = (df[year_column] // 10) * 10
        
        return df
    
    def aggregate_by_year(self, df: pd.DataFrame, 
                         group_cols: List[str],
                         agg_dict: Dict[str, List[str]]) -> pd.DataFrame:
        """
        Agrega dados por ano e outras colunas
        
        Args:
            df: DataFrame
            group_cols: Colunas para agrupar
            agg_dict: Dicionário com agregações
            
        Returns:
            DataFrame agregado
        """
        return df.groupby(group_cols).agg(agg_dict).reset_index()
    
    def calculate_growth_rate(self, df: pd.DataFrame, 
                             value_column: str,
                             group_column: str = 'UF',
                             year_column: str = 'ano') -> pd.DataFrame:
        """
        Calcula taxa de crescimento ano a ano
        
        Args:
            df: DataFrame
            value_column: Coluna com valores
            group_column: Coluna para agrupar
            year_column: Coluna de ano
            
        Returns:
            DataFrame com taxa de crescimento
        """
        df = df.copy()
        df = df.sort_values([group_column, year_column])
        
        # Calcula variação percentual
        df[f'{value_column}_growth_rate'] = df.groupby(group_column)[value_column].pct_change() * 100
        
        return df
    
    def normalize_column(self, df: pd.DataFrame, column: str, 
                        method: str = 'minmax') -> pd.DataFrame:
        """
        Normaliza uma coluna
        
        Args:
            df: DataFrame
            column: Coluna para normalizar
            method: Método ('minmax' ou 'zscore')
            
        Returns:
            DataFrame com coluna normalizada
        """
        df = df.copy()
        
        if method == 'minmax':
            df[f'{column}_normalized'] = (df[column] - df[column].min()) / (df[column].max() - df[column].min())
        elif method == 'zscore':
            df[f'{column}_normalized'] = (df[column] - df[column].mean()) / df[column].std()
        
        return df
    
    def save_processed_data(self, df: pd.DataFrame, filename: str):
        """
        Salva dados processados
        
        Args:
            df: DataFrame para salvar
            filename: Nome do arquivo
        """
        self.processed_path.mkdir(parents=True, exist_ok=True)
        output_path = self.processed_path / filename
        df.to_csv(output_path, index=False)
        print(f"✅ Dados salvos em: {output_path}")
        
    def get_year_range(self, df: pd.DataFrame, year_column: str = 'ano') -> Tuple[int, int]:
        """
        Retorna o intervalo de anos nos dados
        
        Args:
            df: DataFrame
            year_column: Coluna de ano
            
        Returns:
            Tupla (ano_inicial, ano_final)
        """
        return df[year_column].min(), df[year_column].max()
    
    def pivot_by_state_year(self, df: pd.DataFrame, 
                           value_column: str,
                           index: str = 'ano',
                           columns: str = 'UF') -> pd.DataFrame:
        """
        Cria tabela pivot por estado e ano
        
        Args:
            df: DataFrame
            value_column: Coluna com valores
            index: Coluna para índice
            columns: Coluna para colunas
            
        Returns:
            DataFrame pivotado
        """
        return df.pivot(index=index, columns=columns, values=value_column)
