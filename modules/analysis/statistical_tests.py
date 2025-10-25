"""
Módulo para testes estatísticos
"""
import numpy as np
from scipy import stats
from typing import Dict, Tuple


class StatisticalTests:
    """Classe para testes estatísticos de adequação"""
    
    def __init__(self, weibull_analysis):
        """
        Inicializa com resultados da análise de Weibull
        
        Args:
            weibull_analysis: Instância de WeibullAnalysis
        """
        self.analysis = weibull_analysis
        self.failures = weibull_analysis.failures
        self.results = weibull_analysis.results
    
    def anderson_darling_test(self) -> Dict:
        """
        Teste de Anderson-Darling para adequação
        
        Returns:
            Dicionário com resultados do teste
        """
        beta = self.results["beta"]
        eta = self.results["eta"]
        
        # Transforma dados para distribuição exponencial padrão
        transformed = (self.failures / eta) ** beta
        
        # Aplica teste de Anderson-Darling
        result = stats.anderson(transformed, dist='expon')
        
        # Interpreta resultado
        critical_value = result.critical_values[2]  # 5% significance
        statistic = result.statistic
        
        passed = statistic < critical_value
        
        return {
            "test_name": "Anderson-Darling",
            "statistic": statistic,
            "critical_value": critical_value,
            "significance_level": 0.05,
            "passed": passed,
            "interpretation": "Dados seguem distribuição de Weibull" if passed 
                            else "Dados podem não seguir distribuição de Weibull"
        }
    
    def kolmogorov_smirnov_test(self) -> Dict:
        """
        Teste de Kolmogorov-Smirnov para adequação
        
        Returns:
            Dicionário com resultados do teste
        """
        beta = self.results["beta"]
        eta = self.results["eta"]
        
        # CDF teórica de Weibull
        def weibull_cdf(x):
            return 1 - np.exp(-(x / eta) ** beta)
        
        # Aplica teste KS
        statistic, p_value = stats.kstest(self.failures, weibull_cdf)
        
        passed = p_value > 0.05
        
        return {
            "test_name": "Kolmogorov-Smirnov",
            "statistic": statistic,
            "p_value": p_value,
            "significance_level": 0.05,
            "passed": passed,
            "interpretation": "Dados seguem distribuição de Weibull" if passed 
                            else "Dados podem não seguir distribuição de Weibull"
        }
    
    def coefficient_of_determination(self) -> Dict:
        """
        Calcula R² para avaliar qualidade do ajuste
        
        Returns:
            Dicionário com R² e interpretação
        """
        beta = self.results["beta"]
        eta = self.results["eta"]
        
        # Ordena falhas
        sorted_failures = np.sort(self.failures)
        n = len(sorted_failures)
        
        # Valores observados (median ranks)
        ranks = np.arange(1, n + 1)
        observed = (ranks - 0.3) / (n + 0.4)
        
        # Valores preditos pela Weibull
        predicted = 1 - np.exp(-(sorted_failures / eta) ** beta)
        
        # Calcula R²
        ss_res = np.sum((observed - predicted) ** 2)
        ss_tot = np.sum((observed - np.mean(observed)) ** 2)
        r_squared = 1 - (ss_res / ss_tot)
        
        # Interpretação
        if r_squared > 0.95:
            quality = "Excelente"
        elif r_squared > 0.90:
            quality = "Bom"
        elif r_squared > 0.80:
            quality = "Aceitável"
        else:
            quality = "Pobre"
        
        return {
            "r_squared": r_squared,
            "quality": quality,
            "interpretation": f"Ajuste {quality.lower()} aos dados (R² = {r_squared:.4f})"
        }
    
    def run_all_tests(self) -> Dict:
        """
        Executa todos os testes estatísticos
        
        Returns:
            Dicionário com todos os resultados
        """
        return {
            "anderson_darling": self.anderson_darling_test(),
            "kolmogorov_smirnov": self.kolmogorov_smirnov_test(),
            "r_squared": self.coefficient_of_determination()
        }

