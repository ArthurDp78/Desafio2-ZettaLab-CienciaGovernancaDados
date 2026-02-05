"""
Módulo para criação e avaliação de modelos de Machine Learning
Desafio 2 - Ciência e Governança de Dados
"""

import pandas as pd
import numpy as np
from pathlib import Path
import pickle
from typing import Tuple, Dict, List, Any

from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import (mean_squared_error, mean_absolute_error, 
                             r2_score, mean_absolute_percentage_error)


class ModelTrainer:
    """Classe para treinar e avaliar modelos de Machine Learning"""
    
    def __init__(self, model_path: str = "models"):
        """
        Inicializa o treinador de modelos
        
        Args:
            model_path: Caminho para salvar modelos
        """
        self.model_path = Path(model_path)
        self.model_path.mkdir(parents=True, exist_ok=True)
        
        self.scaler = None
        self.best_model = None
        self.feature_names = None
        self.target_name = None
        
    def prepare_data(self, df: pd.DataFrame, 
                    target: str,
                    features: List[str] = None,
                    test_size: float = 0.2,
                    random_state: int = 42,
                    scale: bool = True) -> Tuple:
        """
        Prepara dados para treinamento
        
        Args:
            df: DataFrame com dados
            target: Nome da variável alvo
            features: Lista de features (se None, usa todas exceto target)
            test_size: Proporção do conjunto de teste
            random_state: Seed para reprodutibilidade
            scale: Se True, aplica padronização
            
        Returns:
            Tupla (X_train, X_test, y_train, y_test)
        """
        # Remove linhas com valores faltantes
        df_clean = df.dropna()
        
        # Define features
        if features is None:
            features = [col for col in df_clean.columns if col != target]
        
        self.feature_names = features
        self.target_name = target
        
        X = df_clean[features]
        y = df_clean[target]
        
        # Divide em treino e teste
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )
        
        # Aplica escalonamento se solicitado
        if scale:
            self.scaler = StandardScaler()
            X_train = self.scaler.fit_transform(X_train)
            X_test = self.scaler.transform(X_test)
            
            # Converte de volta para DataFrame para manter nomes
            X_train = pd.DataFrame(X_train, columns=features)
            X_test = pd.DataFrame(X_test, columns=features)
        
        return X_train, X_test, y_train, y_test
    
    def train_multiple_models(self, X_train, y_train, X_test, y_test) -> pd.DataFrame:
        """
        Treina múltiplos modelos e compara resultados
        
        Args:
            X_train: Features de treino
            y_train: Target de treino
            X_test: Features de teste
            y_test: Target de teste
            
        Returns:
            DataFrame com métricas de cada modelo
        """
        models = {
            'Linear Regression': LinearRegression(),
            'Ridge': Ridge(alpha=1.0),
            'Lasso': Lasso(alpha=1.0),
            'ElasticNet': ElasticNet(alpha=1.0),
            'Decision Tree': DecisionTreeRegressor(random_state=42, max_depth=10),
            'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42, max_depth=10),
            'Gradient Boosting': GradientBoostingRegressor(n_estimators=100, random_state=42)
        }
        
        results = []
        
        for name, model in models.items():
            print(f"Treinando {name}...")
            
            # Treina o modelo
            model.fit(X_train, y_train)
            
            # Predições
            y_pred_train = model.predict(X_train)
            y_pred_test = model.predict(X_test)
            
            # Métricas
            metrics = {
                'Model': name,
                'R2_Train': r2_score(y_train, y_pred_train),
                'R2_Test': r2_score(y_test, y_pred_test),
                'RMSE_Train': np.sqrt(mean_squared_error(y_train, y_pred_train)),
                'RMSE_Test': np.sqrt(mean_squared_error(y_test, y_pred_test)),
                'MAE_Train': mean_absolute_error(y_train, y_pred_train),
                'MAE_Test': mean_absolute_error(y_test, y_pred_test),
                'MAPE_Test': mean_absolute_percentage_error(y_test, y_pred_test) * 100
            }
            
            results.append(metrics)
        
        results_df = pd.DataFrame(results)
        results_df = results_df.sort_values('R2_Test', ascending=False)
        
        return results_df
    
    def tune_hyperparameters(self, X_train, y_train, model_type: str = 'random_forest') -> Any:
        """
        Otimiza hiperparâmetros usando GridSearch
        
        Args:
            X_train: Features de treino
            y_train: Target de treino
            model_type: Tipo do modelo ('random_forest', 'gradient_boosting', 'ridge')
            
        Returns:
            Melhor modelo encontrado
        """
        if model_type == 'random_forest':
            model = RandomForestRegressor(random_state=42)
            param_grid = {
                'n_estimators': [50, 100, 200],
                'max_depth': [5, 10, 15, None],
                'min_samples_split': [2, 5, 10],
                'min_samples_leaf': [1, 2, 4]
            }
        elif model_type == 'gradient_boosting':
            model = GradientBoostingRegressor(random_state=42)
            param_grid = {
                'n_estimators': [50, 100, 200],
                'learning_rate': [0.01, 0.05, 0.1],
                'max_depth': [3, 5, 7],
                'min_samples_split': [2, 5, 10]
            }
        elif model_type == 'ridge':
            model = Ridge()
            param_grid = {
                'alpha': [0.01, 0.1, 1.0, 10.0, 100.0]
            }
        else:
            raise ValueError(f"Tipo de modelo não suportado: {model_type}")
        
        print(f"Otimizando hiperparâmetros para {model_type}...")
        grid_search = GridSearchCV(
            model, param_grid, cv=5, 
            scoring='r2', n_jobs=-1, verbose=1
        )
        
        grid_search.fit(X_train, y_train)
        
        print(f"✅ Melhores parâmetros: {grid_search.best_params_}")
        print(f"✅ Melhor score (R2): {grid_search.best_score_:.4f}")
        
        self.best_model = grid_search.best_estimator_
        return grid_search.best_estimator_
    
    def evaluate_model(self, model, X_test, y_test) -> Dict[str, float]:
        """
        Avalia um modelo
        
        Args:
            model: Modelo treinado
            X_test: Features de teste
            y_test: Target de teste
            
        Returns:
            Dicionário com métricas
        """
        y_pred = model.predict(X_test)
        
        metrics = {
            'R2': r2_score(y_test, y_pred),
            'RMSE': np.sqrt(mean_squared_error(y_test, y_pred)),
            'MAE': mean_absolute_error(y_test, y_pred),
            'MAPE': mean_absolute_percentage_error(y_test, y_pred) * 100
        }
        
        return metrics
    
    def cross_validate_model(self, model, X, y, cv: int = 5) -> Dict[str, np.ndarray]:
        """
        Validação cruzada
        
        Args:
            model: Modelo para validar
            X: Features
            y: Target
            cv: Número de folds
            
        Returns:
            Dicionário com scores
        """
        scores = {
            'R2': cross_val_score(model, X, y, cv=cv, scoring='r2'),
            'RMSE': -cross_val_score(model, X, y, cv=cv, scoring='neg_root_mean_squared_error'),
            'MAE': -cross_val_score(model, X, y, cv=cv, scoring='neg_mean_absolute_error')
        }
        
        return scores
    
    def get_feature_importance(self, model, feature_names: List[str] = None) -> pd.DataFrame:
        """
        Extrai importância das features (para modelos tree-based)
        
        Args:
            model: Modelo treinado
            feature_names: Nomes das features
            
        Returns:
            DataFrame com importância ordenada
        """
        if feature_names is None:
            feature_names = self.feature_names
        
        if hasattr(model, 'feature_importances_'):
            importance = pd.DataFrame({
                'Feature': feature_names,
                'Importance': model.feature_importances_
            })
            importance = importance.sort_values('Importance', ascending=False)
            return importance
        else:
            print("⚠️ Modelo não possui feature_importances_")
            return None
    
    def save_model(self, model, filename: str):
        """
        Salva modelo treinado
        
        Args:
            model: Modelo para salvar
            filename: Nome do arquivo
        """
        filepath = self.model_path / filename
        
        # Salva o modelo
        with open(filepath, 'wb') as f:
            pickle.dump(model, f)
        
        # Salva também o scaler se existir
        if self.scaler is not None:
            scaler_path = self.model_path / f"scaler_{filename}"
            with open(scaler_path, 'wb') as f:
                pickle.dump(self.scaler, f)
        
        print(f"✅ Modelo salvo em: {filepath}")
    
    def load_model(self, filename: str):
        """
        Carrega modelo salvo
        
        Args:
            filename: Nome do arquivo
            
        Returns:
            Modelo carregado
        """
        filepath = self.model_path / filename
        
        with open(filepath, 'rb') as f:
            model = pickle.load(f)
        
        # Tenta carregar scaler
        scaler_path = self.model_path / f"scaler_{filename}"
        if scaler_path.exists():
            with open(scaler_path, 'rb') as f:
                self.scaler = pickle.load(f)
        
        print(f"✅ Modelo carregado de: {filepath}")
        return model
    
    def predict_future(self, model, last_year_data: pd.DataFrame, 
                       years_ahead: int = 5) -> pd.DataFrame:
        """
        Faz predições para anos futuros
        
        Args:
            model: Modelo treinado
            last_year_data: Dados do último ano
            years_ahead: Quantos anos prever
            
        Returns:
            DataFrame com predições
        """
        predictions = []
        
        for i in range(1, years_ahead + 1):
            # Cria novo registro com ano incrementado
            new_data = last_year_data.copy()
            new_data['ano'] = new_data['ano'] + i
            
            # Ajusta outras features temporais se existirem
            if 'ano_normalizado' in new_data.columns:
                new_data['ano_normalizado'] = (new_data['ano'] - 2012) / (2021 - 2012 + i)
            
            # Prepara features para predição
            X_pred = new_data[self.feature_names]
            
            if self.scaler is not None:
                X_pred = self.scaler.transform(X_pred)
            
            # Faz predição
            y_pred = model.predict(X_pred)
            
            result = new_data.copy()
            result[self.target_name] = y_pred
            predictions.append(result)
        
        return pd.concat(predictions, ignore_index=True)
