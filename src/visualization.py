"""
Módulo para visualização de dados e resultados
Desafio 2 - Ciência e Governança de Dados
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from typing import List, Tuple, Optional

# Configurações de estilo
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")


class DataVisualizer:
    """Classe para criar visualizações dos dados e resultados"""
    
    def __init__(self, figsize: Tuple[int, int] = (12, 6), style: str = 'seaborn-v0_8-darkgrid'):
        """
        Inicializa o visualizador
        
        Args:
            figsize: Tamanho padrão das figuras
            style: Estilo do matplotlib
        """
        self.figsize = figsize
        plt.style.use(style)
        
        # Cores para estados da Amazônia
        self.uf_colors = {
            'AC': '#FF6B6B', 'AM': '#4ECDC4', 'AP': '#45B7D1',
            'MA': '#FFA07A', 'MT': '#98D8C8', 'PA': '#F7DC6F',
            'RO': '#BB8FCE', 'RR': '#85C1E2', 'TO': '#F8B195'
        }
    
    def plot_time_series(self, df: pd.DataFrame, 
                        x: str = 'ano',
                        y: str = 'desmatamento_km2',
                        hue: str = 'UF',
                        title: str = None,
                        ylabel: str = None,
                        figsize: Tuple[int, int] = None) -> plt.Figure:
        """
        Plota série temporal por estado
        
        Args:
            df: DataFrame com dados
            x: Coluna do eixo x
            y: Coluna do eixo y
            hue: Coluna para cores
            title: Título do gráfico
            ylabel: Label do eixo y
            figsize: Tamanho da figura
            
        Returns:
            Figure do matplotlib
        """
        if figsize is None:
            figsize = self.figsize
        
        fig, ax = plt.subplots(figsize=figsize)
        
        for uf in df[hue].unique():
            data = df[df[hue] == uf]
            color = self.uf_colors.get(uf, None)
            ax.plot(data[x], data[y], marker='o', label=uf, 
                   linewidth=2, markersize=6, color=color)
        
        ax.set_xlabel('Ano', fontsize=12, fontweight='bold')
        ax.set_ylabel(ylabel or y, fontsize=12, fontweight='bold')
        ax.set_title(title or f'{y} ao longo do tempo', fontsize=14, fontweight='bold')
        ax.legend(title='UF', bbox_to_anchor=(1.05, 1), loc='upper left')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def plot_correlation_matrix(self, df: pd.DataFrame, 
                               columns: List[str] = None,
                               title: str = 'Matriz de Correlação',
                               figsize: Tuple[int, int] = (10, 8)) -> plt.Figure:
        """
        Plota matriz de correlação
        
        Args:
            df: DataFrame
            columns: Colunas para incluir (None = todas numéricas)
            title: Título
            figsize: Tamanho da figura
            
        Returns:
            Figure do matplotlib
        """
        if columns is None:
            columns = df.select_dtypes(include=[np.number]).columns.tolist()
        
        corr = df[columns].corr()
        
        fig, ax = plt.subplots(figsize=figsize)
        
        mask = np.triu(np.ones_like(corr, dtype=bool))
        sns.heatmap(corr, mask=mask, annot=True, fmt='.2f', 
                   cmap='coolwarm', center=0, square=True,
                   linewidths=1, cbar_kws={"shrink": 0.8}, ax=ax)
        
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        plt.tight_layout()
        
        return fig
    
    def plot_distribution(self, df: pd.DataFrame, 
                         column: str,
                         bins: int = 30,
                         title: str = None,
                         figsize: Tuple[int, int] = None) -> plt.Figure:
        """
        Plota distribuição de uma variável
        
        Args:
            df: DataFrame
            column: Coluna para plotar
            bins: Número de bins
            title: Título
            figsize: Tamanho da figura
            
        Returns:
            Figure do matplotlib
        """
        if figsize is None:
            figsize = self.figsize
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
        
        # Histograma
        ax1.hist(df[column].dropna(), bins=bins, edgecolor='black', alpha=0.7)
        ax1.set_xlabel(column, fontsize=11, fontweight='bold')
        ax1.set_ylabel('Frequência', fontsize=11, fontweight='bold')
        ax1.set_title('Histograma', fontsize=12, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        
        # Boxplot
        ax2.boxplot(df[column].dropna(), vert=True)
        ax2.set_ylabel(column, fontsize=11, fontweight='bold')
        ax2.set_title('Boxplot', fontsize=12, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        
        fig.suptitle(title or f'Distribuição de {column}', 
                    fontsize=14, fontweight='bold', y=1.02)
        
        plt.tight_layout()
        return fig
    
    def plot_scatter(self, df: pd.DataFrame,
                    x: str, y: str,
                    hue: str = None,
                    title: str = None,
                    figsize: Tuple[int, int] = None) -> plt.Figure:
        """
        Plota scatter plot
        
        Args:
            df: DataFrame
            x: Coluna do eixo x
            y: Coluna do eixo y
            hue: Coluna para cores
            title: Título
            figsize: Tamanho da figura
            
        Returns:
            Figure do matplotlib
        """
        if figsize is None:
            figsize = self.figsize
        
        fig, ax = plt.subplots(figsize=figsize)
        
        if hue:
            for category in df[hue].unique():
                data = df[df[hue] == category]
                color = self.uf_colors.get(category, None)
                ax.scatter(data[x], data[y], label=category, alpha=0.6, 
                          s=100, edgecolors='black', linewidth=0.5, color=color)
            ax.legend(title=hue, bbox_to_anchor=(1.05, 1), loc='upper left')
        else:
            ax.scatter(df[x], df[y], alpha=0.6, s=100, 
                      edgecolors='black', linewidth=0.5)
        
        ax.set_xlabel(x, fontsize=12, fontweight='bold')
        ax.set_ylabel(y, fontsize=12, fontweight='bold')
        ax.set_title(title or f'{y} vs {x}', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def plot_bar_comparison(self, df: pd.DataFrame,
                           x: str, y: str,
                           title: str = None,
                           figsize: Tuple[int, int] = None,
                           horizontal: bool = False) -> plt.Figure:
        """
        Plota gráfico de barras para comparação
        
        Args:
            df: DataFrame
            x: Coluna do eixo x
            y: Coluna do eixo y
            title: Título
            figsize: Tamanho da figura
            horizontal: Se True, barras horizontais
            
        Returns:
            Figure do matplotlib
        """
        if figsize is None:
            figsize = self.figsize
        
        fig, ax = plt.subplots(figsize=figsize)
        
        colors = [self.uf_colors.get(uf, '#95A5A6') for uf in df[x]]
        
        if horizontal:
            ax.barh(df[x], df[y], color=colors, edgecolor='black', linewidth=1.2)
            ax.set_xlabel(y, fontsize=12, fontweight='bold')
            ax.set_ylabel(x, fontsize=12, fontweight='bold')
        else:
            ax.bar(df[x], df[y], color=colors, edgecolor='black', linewidth=1.2)
            ax.set_xlabel(x, fontsize=12, fontweight='bold')
            ax.set_ylabel(y, fontsize=12, fontweight='bold')
            plt.xticks(rotation=45, ha='right')
        
        ax.set_title(title or f'{y} por {x}', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y' if not horizontal else 'x')
        
        plt.tight_layout()
        return fig
    
    def plot_predictions_vs_actual(self, y_true: np.ndarray, 
                                   y_pred: np.ndarray,
                                   title: str = 'Valores Reais vs Predições',
                                   figsize: Tuple[int, int] = None) -> plt.Figure:
        """
        Plota valores reais vs predições
        
        Args:
            y_true: Valores reais
            y_pred: Valores preditos
            title: Título
            figsize: Tamanho da figura
            
        Returns:
            Figure do matplotlib
        """
        if figsize is None:
            figsize = (10, 6)
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
        
        # Scatter plot
        ax1.scatter(y_true, y_pred, alpha=0.6, s=50, edgecolors='black', linewidth=0.5)
        
        # Linha de referência (predição perfeita)
        min_val = min(y_true.min(), y_pred.min())
        max_val = max(y_true.max(), y_pred.max())
        ax1.plot([min_val, max_val], [min_val, max_val], 
                'r--', linewidth=2, label='Predição Perfeita')
        
        ax1.set_xlabel('Valores Reais', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Valores Preditos', fontsize=12, fontweight='bold')
        ax1.set_title('Scatter Plot', fontsize=12, fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Resíduos
        residuals = y_true - y_pred
        ax2.scatter(y_pred, residuals, alpha=0.6, s=50, edgecolors='black', linewidth=0.5)
        ax2.axhline(y=0, color='r', linestyle='--', linewidth=2)
        ax2.set_xlabel('Valores Preditos', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Resíduos', fontsize=12, fontweight='bold')
        ax2.set_title('Gráfico de Resíduos', fontsize=12, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        
        fig.suptitle(title, fontsize=14, fontweight='bold', y=1.02)
        plt.tight_layout()
        
        return fig
    
    def plot_feature_importance(self, importance_df: pd.DataFrame,
                               top_n: int = 10,
                               title: str = 'Importância das Features',
                               figsize: Tuple[int, int] = None) -> plt.Figure:
        """
        Plota importância das features
        
        Args:
            importance_df: DataFrame com colunas 'Feature' e 'Importance'
            top_n: Número de features mais importantes para mostrar
            title: Título
            figsize: Tamanho da figura
            
        Returns:
            Figure do matplotlib
        """
        if figsize is None:
            figsize = (10, 6)
        
        # Seleciona top N features
        top_features = importance_df.head(top_n)
        
        fig, ax = plt.subplots(figsize=figsize)
        
        ax.barh(range(len(top_features)), top_features['Importance'], 
               color='steelblue', edgecolor='black', linewidth=1.2)
        ax.set_yticks(range(len(top_features)))
        ax.set_yticklabels(top_features['Feature'])
        ax.set_xlabel('Importância', fontsize=12, fontweight='bold')
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='x')
        
        # Inverte eixo y para maior importância no topo
        ax.invert_yaxis()
        
        plt.tight_layout()
        return fig
    
    def plot_metrics_comparison(self, metrics_df: pd.DataFrame,
                               metric_columns: List[str] = None,
                               title: str = 'Comparação de Modelos',
                               figsize: Tuple[int, int] = None) -> plt.Figure:
        """
        Plota comparação de métricas entre modelos
        
        Args:
            metrics_df: DataFrame com métricas (coluna 'Model' e métricas)
            metric_columns: Colunas de métricas para plotar
            title: Título
            figsize: Tamanho da figura
            
        Returns:
            Figure do matplotlib
        """
        if figsize is None:
            figsize = (14, 6)
        
        if metric_columns is None:
            metric_columns = [col for col in metrics_df.columns if col != 'Model']
        
        n_metrics = len(metric_columns)
        fig, axes = plt.subplots(1, n_metrics, figsize=figsize)
        
        if n_metrics == 1:
            axes = [axes]
        
        for i, metric in enumerate(metric_columns):
            ax = axes[i]
            
            ax.barh(metrics_df['Model'], metrics_df[metric], 
                   color='coral', edgecolor='black', linewidth=1.2)
            ax.set_xlabel(metric, fontsize=11, fontweight='bold')
            ax.set_title(metric, fontsize=12, fontweight='bold')
            ax.grid(True, alpha=0.3, axis='x')
            
            if i > 0:
                ax.set_yticklabels([])
        
        fig.suptitle(title, fontsize=14, fontweight='bold', y=1.02)
        plt.tight_layout()
        
        return fig
    
    def save_figure(self, fig: plt.Figure, filename: str, 
                   output_dir: str = 'outputs', dpi: int = 300):
        """
        Salva figura em arquivo
        
        Args:
            fig: Figure do matplotlib
            filename: Nome do arquivo
            output_dir: Diretório de saída
            dpi: Resolução
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        filepath = output_path / filename
        fig.savefig(filepath, dpi=dpi, bbox_inches='tight')
        print(f"✅ Figura salva em: {filepath}")
