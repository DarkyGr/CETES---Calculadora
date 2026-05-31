#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests unitarios para la Calculadora de CETES.
"""

import unittest
import sys
from pathlib import Path

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.calculadora import CalculadoraCETES
from src.comparador import ComparadorEscenarios, AnalizadorSensibilidad


class TestCalculadoraCETES(unittest.TestCase):
    """Tests para la clase CalculadoraCETES."""
    
    def setUp(self):
        """Configuración inicial para cada test."""
        self.calc = CalculadoraCETES(250000, 0.0719, 0.0411, tasa_isr=0.15)
    
    def test_inicializacion(self):
        """Test de inicialización correcta."""
        self.assertEqual(self.calc.capital, 250000)
        self.assertEqual(self.calc.tasa_cetes, 0.0719)
        self.assertEqual(self.calc.tasa_inflacion, 0.0411)
    
    def test_calculo_rendimiento_bruto(self):
        """Test de cálculo de rendimiento bruto."""
        resultado = self.calc.calcular()
        rendimiento_esperado = 250000 * 0.0719
        self.assertAlmostEqual(resultado['rendimiento_bruto'], rendimiento_esperado, places=2)
    
    def test_calculo_interes_real(self):
        """Test de cálculo de interés real."""
        resultado = self.calc.calcular()
        rendimiento_bruto = 250000 * 0.0719
        inflacion = 250000 * 0.0411
        interes_real_esperado = rendimiento_bruto - inflacion
        self.assertAlmostEqual(resultado['interes_real'], interes_real_esperado, places=2)
    
    def test_calculo_impuesto_definitivo(self):
        """Test de cálculo del impuesto definitivo."""
        resultado = self.calc.calcular()
        rendimiento_bruto = 250000 * 0.0719
        inflacion = 250000 * 0.0411
        interes_real = rendimiento_bruto - inflacion
        impuesto_esperado = interes_real * 0.15
        self.assertAlmostEqual(resultado['impuesto_definitivo'], impuesto_esperado, places=2)
    
    def test_saldo_a_favor(self):
        """Test de cálculo de saldo a favor."""
        resultado = self.calc.calcular()
        # La retención (2250) es mayor que el impuesto (1155), por lo tanto hay saldo a favor
        self.assertGreater(resultado['saldo_a_favor'], 0)
    
    def test_capital_final(self):
        """Test de cálculo del capital final."""
        resultado = self.calc.calcular()
        capital_final_esperado = resultado['capital_inicial'] + resultado['ganancia_neta']
        self.assertAlmostEqual(resultado['capital_final'], capital_final_esperado, places=2)
    
    def test_validacion_parametros_invalidos(self):
        """Test de validación de parámetros."""
        with self.assertRaises(ValueError):
            CalculadoraCETES(-100, 0.0719, 0.0411)  # Capital negativo
        
        with self.assertRaises(ValueError):
            CalculadoraCETES(250000, -0.05, 0.0411)  # Tasa CETES negativa
    
    def test_resumen_texto(self):
        """Test de generación de resumen en texto."""
        self.calc.calcular()
        resumen = self.calc.resumen_texto()
        self.assertIn("RESUMEN DE INVERSIÓN", resumen)
        self.assertIn("Capital Inicial", resumen)


class TestComparadorEscenarios(unittest.TestCase):
    """Tests para la clase ComparadorEscenarios."""
    
    def setUp(self):
        """Configuración inicial."""
        self.comparador = ComparadorEscenarios()
    
    def test_agregar_escenario(self):
        """Test de agregar escenarios."""
        self.comparador.agregar_escenario("Base", 250000, 0.0719, 0.0411, 0.15)
        self.assertIn("Base", self.comparador.escenarios)
    
    def test_comparar_por_tasa_isr(self):
        """Test de comparativa por tasa ISR."""
        resultados = self.comparador.comparar_por_tasa_isr(250000, 0.0719, 0.0411)
        self.assertEqual(len(resultados), 3)  # 3 tasas (10%, 15%, 21%)
        self.assertIn('10%', resultados)
        self.assertIn('15%', resultados)
        self.assertIn('21%', resultados)
    
    def test_comparar_tasas_diferentes(self):
        """Test que tasas ISR diferentes generan ganancias diferentes."""
        resultados = self.comparador.comparar_por_tasa_isr(250000, 0.0719, 0.0411)
        ganancia_10 = resultados['10%']['ganancia_neta']
        ganancia_21 = resultados['21%']['ganancia_neta']
        # Mayor tasa ISR debe resultar en menor ganancia neta
        self.assertGreater(ganancia_10, ganancia_21)


class TestAnalizadorSensibilidad(unittest.TestCase):
    """Tests para la clase AnalizadorSensibilidad."""
    
    def test_variar_tasa_cetes(self):
        """Test de análisis de sensibilidad de tasa CETES."""
        variaciones = AnalizadorSensibilidad.variar_tasa_cetes(
            250000, 0.0719, 0.0411, 0.15, rango_variacion=0.02, pasos=5
        )
        self.assertEqual(len(variaciones), 5)
        # Mayor tasa CETES debe resultar en mayor ganancia
        self.assertGreater(variaciones[-1]['ganancia_neta'], variaciones[0]['ganancia_neta'])
    
    def test_variar_inflacion(self):
        """Test de análisis de sensibilidad de inflación."""
        variaciones = AnalizadorSensibilidad.variar_inflacion(
            250000, 0.0719, 0.0411, 0.15, rango_variacion=0.02, pasos=5
        )
        self.assertEqual(len(variaciones), 5)
        # Mayor inflación debe resultar en menor ganancia
        self.assertGreater(variaciones[0]['ganancia_neta'], variaciones[-1]['ganancia_neta'])


class TestCasosLimite(unittest.TestCase):
    """Tests de casos límite."""
    
    def test_capital_cero(self):
        """Test con capital zero."""
        with self.assertRaises(ValueError):
            CalculadoraCETES(0, 0.0719, 0.0411)
    
    def test_tasa_isr_maxima(self):
        """Test con tasa ISR máxima."""
        calc = CalculadoraCETES(250000, 0.0719, 0.0411, tasa_isr=1.0)
        resultado = calc.calcular()
        # Si tasa ISR es 100%, impuesto debe ser igual al interés real
        self.assertAlmostEqual(resultado['impuesto_definitivo'], resultado['interes_real'], places=2)
    
    def test_sin_inflacion(self):
        """Test sin inflación."""
        calc = CalculadoraCETES(250000, 0.0719, 0, tasa_isr=0.15)
        resultado = calc.calcular()
        # Sin inflación, interés real debe igual al rendimiento bruto
        self.assertAlmostEqual(resultado['interes_real'], resultado['rendimiento_bruto'], places=2)


def run_tests():
    """Ejecuta todos los tests."""
    # Crear suite de tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Agregar tests
    suite.addTests(loader.loadTestsFromTestCase(TestCalculadoraCETES))
    suite.addTests(loader.loadTestsFromTestCase(TestComparadorEscenarios))
    suite.addTests(loader.loadTestsFromTestCase(TestAnalizadorSensibilidad))
    suite.addTests(loader.loadTestsFromTestCase(TestCasosLimite))
    
    # Ejecutar tests
    runner = unittest.TextTestRunner(verbosity=2)
    resultado = runner.run(suite)
    
    return resultado.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
