"""
Módulo para cálculo de métricas de confiabilidade
"""
import numpy as np
from typing import Dict
from scipy import stats


class ReliabilityMetrics:
    """Classe para calcular métricas de confiabilidade"""
    
    def __init__(self, weibull_analysis):
        """
        Inicializa com resultados da análise de Weibull
        
        Args:
            weibull_analysis: Instância de WeibullAnalysis
        """
        self.analysis = weibull_analysis
        self.results = weibull_analysis.results
    
    def calculate_all_metrics(self) -> Dict:
        """
        Calcula todas as métricas de confiabilidade
        
        Returns:
            Dicionário com todas as métricas
        """
        metrics = {
            "mttf": self.analysis.mean_life(),
            "median_life": self.analysis.median_life(),
            "characteristic_life": self.analysis.characteristic_life(),
            "b10_life": self.analysis.b_life(10),
            "b50_life": self.analysis.b_life(50),
            "b90_life": self.analysis.b_life(90),
            "mode": self._calculate_mode(),
            "variance": self._calculate_variance(),
            "std_dev": self._calculate_std_dev(),
            "coefficient_of_variation": self._calculate_cv(),
        }
        
        return metrics
    
    def _calculate_mode(self) -> float:
        """Calcula a moda da distribuição"""
        beta = self.results["beta"]
        eta = self.results["eta"]
        
        if beta > 1:
            return eta * ((beta - 1) / beta) ** (1 / beta)
        else:
            return 0.0
    
    def _calculate_variance(self) -> float:
        """Calcula a variância"""
        beta = self.results["beta"]
        eta = self.results["eta"]
        
        return eta**2 * (stats.gamma(1 + 2/beta) - stats.gamma(1 + 1/beta)**2)
    
    def _calculate_std_dev(self) -> float:
        """Calcula o desvio padrão"""
        return np.sqrt(self._calculate_variance())
    
    def _calculate_cv(self) -> float:
        """Calcula o coeficiente de variação"""
        mean = self.analysis.mean_life()
        std = self._calculate_std_dev()
        
        return std / mean if mean > 0 else 0.0
    
    def reliability_at_time(self, t: float) -> Dict:
        """
        Calcula métricas de confiabilidade em um tempo específico
        
        Args:
            t: Tempo específico
        
        Returns:
            Dicionário com métricas no tempo t
        """
        return {
            "time": t,
            "reliability": self.analysis.reliability(np.array([t]))[0],
            "unreliability": self.analysis.unreliability(np.array([t]))[0],
            "pdf": self.analysis.pdf(np.array([t]))[0],
            "hazard_rate": self.analysis.hazard_rate(np.array([t]))[0],
        }
    
    def mission_reliability(self, mission_time: float, 
                           required_reliability: float = 0.90) -> Dict:
        """
        Analisa confiabilidade para uma missão específica
        
        Args:
            mission_time: Tempo da missão
            required_reliability: Confiabilidade requerida
        
        Returns:
            Dicionário com análise da missão
        """
        actual_reliability = self.analysis.reliability(np.array([mission_time]))[0]
        meets_requirement = actual_reliability >= required_reliability
        
        # Calcula tempo para atingir confiabilidade requerida
        if required_reliability < 1.0:
            beta = self.results["beta"]
            eta = self.results["eta"]
            time_for_required = eta * (-np.log(required_reliability)) ** (1 / beta)
        else:
            time_for_required = 0.0
        
        return {
            "mission_time": mission_time,
            "required_reliability": required_reliability,
            "actual_reliability": actual_reliability,
            "meets_requirement": meets_requirement,
            "reliability_margin": actual_reliability - required_reliability,
            "time_for_required_reliability": time_for_required
        }

