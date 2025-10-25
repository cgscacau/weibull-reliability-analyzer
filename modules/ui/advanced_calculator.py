"""
Calculadora avançada de confiabilidade
"""
import streamlit as st
import numpy as np
import plotly.graph_objects as go
from typing import Dict

from config.settings import COLORS


class AdvancedCalculator:
    """Calculadora avançada de confiabilidade"""
    
    def __init__(self, weibull_analysis, metrics_calculator):
        """
        Inicializa calculadora
        
        Args:
            weibull_analysis: Objeto WeibullAnalysis
            metrics_calculator: Objeto ReliabilityMetrics
        """
        self.analysis = weibull_analysis
        self.metrics = metrics_calculator
        self.results = weibull_analysis.results
    
    def mission_analysis(self, mission_time: float, required_reliability: float) -> Dict:
        """
        Análise de missão
        
        Args:
            mission_time: Tempo da missão
            required_reliability: Confiabilidade requerida (0-1)
        
        Returns:
            Dicionário com resultados
        """
        return self.metrics.mission_reliability(mission_time, required_reliability)
    
    def maintenance_planning(self, target_reliability: float = 0.90) -> Dict:
        """
        Planejamento de manutenção
        
        Args:
            target_reliability: Confiabilidade alvo
        
        Returns:
            Dicionário com recomendações
        """
        beta = self.results['beta']
        eta = self.results['eta']
        
        # Calcula intervalo para atingir confiabilidade alvo
        interval = eta * (-np.log(target_reliability)) ** (1/beta)
        
        # Aplica fatores de segurança
        conservative_interval = interval * 0.8
        moderate_interval = interval * 0.9
        aggressive_interval = interval * 0.95
        
        return {
            'target_reliability': target_reliability,
            'calculated_interval': interval,
            'conservative': conservative_interval,
            'moderate': moderate_interval,
            'aggressive': aggressive_interval,
            'recommendation': 'conservative' if beta > 2 else 'moderate'
        }
    
    def spare_parts_analysis(self, fleet_size: int, time_period: float) -> Dict:
        """
        Análise de peças de reposição
        
        Args:
            fleet_size: Tamanho da frota
            time_period: Período de tempo
        
        Returns:
            Dicionário com estimativas
        """
        # Probabilidade de falha no período
        F = self.analysis.unreliability(np.array([time_period]))[0]
        
        # Número esperado de falhas
        expected_failures = fleet_size * F
        
        # Intervalo de confiança (Poisson)
        from scipy import stats
        lambda_param = expected_failures
        
        # 90% de confiança
        lower_90 = stats.poisson.ppf(0.05, lambda_param)
        upper_90 = stats.poisson.ppf(0.95, lambda_param)
        
        # 95% de confiança
        lower_95 = stats.poisson.ppf(0.025, lambda_param)
        upper_95 = stats.poisson.ppf(0.975, lambda_param)
        
        return {
            'fleet_size': fleet_size,
            'time_period': time_period,
            'failure_probability': F,
            'expected_failures': expected_failures,
            'confidence_90': (int(lower_90), int(upper_90)),
            'confidence_95': (int(lower_95), int(upper_95)),
            'recommended_spares_90': int(upper_90),
            'recommended_spares_95': int(upper_95)
        }
    
    def cost_analysis(self, 
                     maintenance_cost: float,
                     failure_cost: float,
                     downtime_cost_per_hour: float,
                     mttr: float) -> Dict:
        """
        Análise de custos
        
        Args:
            maintenance_cost: Custo de manutenção preventiva
            failure_cost: Custo de reparo de falha
            downtime_cost_per_hour: Custo de parada por hora
            mttr: Mean Time To Repair (horas)
        
        Returns:
            Dicionário com análise de custos
        """
        mttf = self.analysis.mean_life()
        
        # Custo de falha total
        total_failure_cost = failure_cost + (downtime_cost_per_hour * mttr)
        
        # Custo por hora - estratégia reativa
        reactive_cost_per_hour = total_failure_cost / mttf
        
        # Custo por hora - estratégia preventiva (assumindo manutenção a cada 80% do MTTF)
        pm_interval = mttf * 0.8
        preventive_cost_per_hour = maintenance_cost / pm_interval
        
        # Economia
        savings_per_hour = reactive_cost_per_hour - preventive_cost_per_hour
        savings_percent = (savings_per_hour / reactive_cost_per_hour) * 100
        
        return {
            'mttf': mttf,
            'pm_interval': pm_interval,
            'reactive_cost_per_hour': reactive_cost_per_hour,
            'preventive_cost_per_hour': preventive_cost_per_hour,
            'savings_per_hour': savings_per_hour,
            'savings_percent': savings_percent,
            'recommendation': 'Manutenção Preventiva' if savings_per_hour > 0 else 'Manutenção Reativa'
        }
