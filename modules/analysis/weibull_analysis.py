"""
Módulo para análise de Weibull
"""
import numpy as np
import pandas as pd
from scipy import stats
from scipy.special import gamma  # CORREÇÃO: importar gamma da scipy.special
from scipy.optimize import minimize
from typing import Dict, Tuple, Optional
import streamlit as st


class WeibullAnalysis:
    """Classe para análise de Weibull"""
    
    def __init__(self, df: pd.DataFrame):
        """
        Inicializa a análise
        
        Args:
            df: DataFrame processado com colunas 'tempo_falha' e 'status'
        """
        self.df = df
        self.time_unit = df.attrs.get("time_unit", "unidades")
        
        # Separa falhas e censuras
        self.failures = df[df['status'] == 1]['tempo_falha'].values
        self.censored = df[df['status'] == 0]['tempo_falha'].values
        
        # Resultados
        self.results = {}
    
    def fit(self, method: str = "mle", confidence_level: float = 0.95) -> Dict:
        """
        Ajusta a distribuição de Weibull aos dados
        
        Args:
            method: Método de estimação ('mle' ou 'rr')
            confidence_level: Nível de confiança para intervalos
        
        Returns:
            Dicionário com resultados da análise
        """
        if method == "mle":
            beta, eta = self._fit_mle()
        elif method == "rr":
            beta, eta = self._fit_rank_regression()
        else:
            raise ValueError(f"Método desconhecido: {method}")
        
        # Calcula intervalos de confiança
        beta_ci, eta_ci = self._calculate_confidence_intervals(beta, eta, confidence_level)
        
        # Armazena resultados
        self.results = {
            "beta": beta,
            "eta": eta,
            "beta_ci": beta_ci,
            "eta_ci": eta_ci,
            "method": method,
            "confidence_level": confidence_level,
            "n_failures": len(self.failures),
            "n_censored": len(self.censored),
            "time_unit": self.time_unit
        }
        
        return self.results
    
    def _fit_mle(self) -> Tuple[float, float]:
        """
        Estimação por Máxima Verossimilhança (MLE)
        
        Returns:
            Tupla (beta, eta)
        """
        # Função de log-verossimilhança negativa
        def neg_log_likelihood(params):
            beta, eta = params
            
            if beta <= 0 or eta <= 0:
                return np.inf
            
            try:
                # Log-likelihood para falhas
                ll_failures = np.sum(
                    np.log(beta) - beta * np.log(eta) + 
                    (beta - 1) * np.log(self.failures) - 
                    (self.failures / eta) ** beta
                )
                
                # Log-likelihood para censuras (survival function)
                if len(self.censored) > 0:
                    ll_censored = -np.sum((self.censored / eta) ** beta)
                else:
                    ll_censored = 0
                
                return -(ll_failures + ll_censored)
            except:
                return np.inf
        
        # Estimativa inicial usando método dos momentos
        mean_failures = np.mean(self.failures)
        std_failures = np.std(self.failures)
        
        # Aproximação inicial (método simplificado)
        cv = std_failures / mean_failures if mean_failures > 0 else 1
        
        # Estimativa inicial de beta baseada no CV
        if cv < 0.3:
            beta_init = 3.5
        elif cv < 0.5:
            beta_init = 2.5
        elif cv < 0.8:
            beta_init = 1.5
        else:
            beta_init = 1.0
        
        # Estimativa inicial de eta usando função gamma
        eta_init = mean_failures / gamma(1 + 1/beta_init)
        
        # Garante valores positivos
        beta_init = max(0.5, min(beta_init, 10))
        eta_init = max(mean_failures * 0.5, min(eta_init, mean_failures * 2))
        
        # Otimização com múltiplas tentativas
        best_result = None
        best_likelihood = np.inf
        
        # Tenta diferentes pontos iniciais
        for beta_try in [beta_init, 1.0, 2.0]:
            for eta_try in [eta_init, mean_failures, np.median(self.failures)]:
                try:
                    result = minimize(
                        neg_log_likelihood,
                        x0=[beta_try, eta_try],
                        method='Nelder-Mead',
                        options={'maxiter': 1000, 'xatol': 1e-8, 'fatol': 1e-8}
                    )
                    
                    if result.fun < best_likelihood and result.x[0] > 0 and result.x[1] > 0:
                        best_likelihood = result.fun
                        best_result = result
                except:
                    continue
        
        if best_result is None:
            # Fallback para rank regression se MLE falhar
            st.warning("⚠️ MLE falhou, usando Rank Regression como alternativa.")
            return self._fit_rank_regression()
        
        beta, eta = best_result.x
        
        # Valida resultados
        if beta <= 0 or beta > 20 or eta <= 0:
            st.warning("⚠️ Parâmetros MLE fora do intervalo esperado, usando Rank Regression.")
            return self._fit_rank_regression()
        
        return beta, eta
    
    def _fit_rank_regression(self) -> Tuple[float, float]:
        """
        Estimação por Regressão de Ranks (Rank Regression on X)
        
        Returns:
            Tupla (beta, eta)
        """
        # Ordena os tempos de falha
        sorted_failures = np.sort(self.failures)
        n = len(sorted_failures)
        
        # Calcula posições de plotagem (mediana ranks)
        ranks = np.arange(1, n + 1)
        median_ranks = (ranks - 0.3) / (n + 0.4)
        
        # Remove valores muito próximos de 0 ou 1
        valid_idx = (median_ranks > 0.001) & (median_ranks < 0.999)
        median_ranks = median_ranks[valid_idx]
        sorted_failures = sorted_failures[valid_idx]
        
        # Transforma para escala de Weibull
        y = np.log(-np.log(1 - median_ranks))
        x = np.log(sorted_failures)
        
        # Regressão linear
        coeffs = np.polyfit(x, y, 1)
        beta = coeffs[0]
        eta = np.exp(-coeffs[1] / beta)
        
        # Garante valores razoáveis
        beta = max(0.1, min(beta, 10))
        eta = max(np.min(sorted_failures) * 0.5, min(eta, np.max(sorted_failures) * 2))
        
        return beta, eta
    
    def _calculate_confidence_intervals(self, beta: float, eta: float, 
                                       confidence_level: float) -> Tuple[Tuple, Tuple]:
        """
        Calcula intervalos de confiança para os parâmetros
        
        Args:
            beta: Parâmetro de forma
            eta: Parâmetro de escala
            confidence_level: Nível de confiança
        
        Returns:
            Tuplas ((beta_lower, beta_upper), (eta_lower, eta_upper))
        """
        n = len(self.failures)
        
        # Aproximação usando Fisher Information Matrix
        alpha = 1 - confidence_level
        z = stats.norm.ppf(1 - alpha/2)
        
        # Erro padrão aproximado
        se_beta = beta / np.sqrt(n)
        se_eta = eta / np.sqrt(n)
        
        beta_ci = (
            max(0.1, beta - z * se_beta),
            beta + z * se_beta
        )
        
        eta_ci = (
            max(0.1, eta - z * se_eta),
            eta + z * se_eta
        )
        
        return beta_ci, eta_ci
    
    def reliability(self, t: np.ndarray) -> np.ndarray:
        """
        Calcula a confiabilidade R(t)
        
        Args:
            t: Tempos para calcular confiabilidade
        
        Returns:
            Array com valores de confiabilidade
        """
        beta = self.results["beta"]
        eta = self.results["eta"]
        
        return np.exp(-(t / eta) ** beta)
    
    def unreliability(self, t: np.ndarray) -> np.ndarray:
        """
        Calcula a não-confiabilidade F(t) = 1 - R(t)
        
        Args:
            t: Tempos para calcular não-confiabilidade
        
        Returns:
            Array com valores de não-confiabilidade
        """
        return 1 - self.reliability(t)
    
    def pdf(self, t: np.ndarray) -> np.ndarray:
        """
        Calcula a função densidade de probabilidade f(t)
        
        Args:
            t: Tempos para calcular PDF
        
        Returns:
            Array com valores de PDF
        """
        beta = self.results["beta"]
        eta = self.results["eta"]
        
        return (beta / eta) * (t / eta) ** (beta - 1) * np.exp(-(t / eta) ** beta)
    
    def hazard_rate(self, t: np.ndarray) -> np.ndarray:
        """
        Calcula a taxa de falha h(t)
        
        Args:
            t: Tempos para calcular taxa de falha
        
        Returns:
            Array com valores de taxa de falha
        """
        beta = self.results["beta"]
        eta = self.results["eta"]
        
        return (beta / eta) * (t / eta) ** (beta - 1)
    
    def mean_life(self) -> float:
        """
        Calcula a vida média (MTTF - Mean Time To Failure)
        
        Returns:
            Vida média
        """
        beta = self.results["beta"]
        eta = self.results["eta"]
        
        return eta * gamma(1 + 1/beta)
    
    def median_life(self) -> float:
        """
        Calcula a vida mediana
        
        Returns:
            Vida mediana
        """
        eta = self.results["eta"]
        
        return eta * (np.log(2)) ** (1 / self.results["beta"])
    
    def characteristic_life(self) -> float:
        """
        Calcula a vida característica (η)
        
        Returns:
            Vida característica
        """
        return self.results["eta"]
    
    def b_life(self, percentile: float) -> float:
        """
        Calcula B-life (tempo em que X% da população falhou)
        
        Args:
            percentile: Percentil desejado (ex: 10 para B10)
        
        Returns:
            Tempo correspondente ao percentil
        """
        beta = self.results["beta"]
        eta = self.results["eta"]
        
        p = percentile / 100
        return eta * (-np.log(1 - p)) ** (1 / beta)
    
    def get_interpretation(self) -> Dict[str, str]:
        """
        Retorna interpretação dos parâmetros
        
        Returns:
            Dicionário com interpretações
        """
        beta = self.results["beta"]
        
        if beta < 1:
            failure_mode = "Mortalidade Infantil"
            behavior = "Taxa de falha decrescente - falhas precoces são mais comuns"
            recommendation = "Considere burn-in ou seleção de componentes"
        elif 0.9 <= beta <= 1.1:  # Tolerância para beta ≈ 1
            failure_mode = "Vida Útil (Falhas Aleatórias)"
            behavior = "Taxa de falha constante - falhas ocorrem aleatoriamente"
            recommendation = "Manutenção baseada em condição pode ser apropriada"
        else:
            failure_mode = "Desgaste"
            behavior = "Taxa de falha crescente - falhas aumentam com o tempo"
            recommendation = "Manutenção preventiva baseada em tempo é recomendada"
        
        return {
            "failure_mode": failure_mode,
            "behavior": behavior,
            "recommendation": recommendation,
            "beta_value": f"{beta:.3f}"
        }
