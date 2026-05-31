#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo para análisis multi-año y comparativa de escenarios.
Permite proyectar inversiones a lo largo de varios años.
"""

from .calculadora import CalculadoraCETES


class ComparadorEscenarios:
    """Compara múltiples escenarios de inversión."""
    
    def __init__(self):
        """Inicializa el comparador."""
        self.escenarios = {}
        self.resultados_comparativa = []
    
    def agregar_escenario(self, nombre, capital, tasa_cetes, tasa_inflacion, 
                         tasa_isr=0.15):
        """
        Agrega un escenario a la comparación.
        
        Args:
            nombre (str): Nombre descriptivo del escenario
            capital (float): Capital invertido
            tasa_cetes (float): Tasa CETES
            tasa_inflacion (float): Tasa inflación
            tasa_isr (float): Tasa ISR
        """
        calc = CalculadoraCETES(capital, tasa_cetes, tasa_inflacion, tasa_isr=tasa_isr)
        self.escenarios[nombre] = {
            'calculadora': calc,
            'parametros': {
                'capital': capital,
                'tasa_cetes': tasa_cetes,
                'tasa_inflacion': tasa_inflacion,
                'tasa_isr': tasa_isr
            }
        }
    
    def calcular_todos(self):
        """Calcula todos los escenarios."""
        self.resultados_comparativa = {}
        for nombre, escenario in self.escenarios.items():
            resultado = escenario['calculadora'].calcular()
            self.resultados_comparativa[nombre] = resultado
        return self.resultados_comparativa
    
    def comparar_por_tasa_isr(self, capital, tasa_cetes, tasa_inflacion):
        """
        Compara el mismo escenario con diferentes tasas ISR.
        
        Args:
            capital (float): Capital invertido
            tasa_cetes (float): Tasa CETES
            tasa_inflacion (float): Tasa inflación
        
        Returns:
            dict: Comparativa por tasa ISR
        """
        tasas = {'10%': 0.10, '15%': 0.15, '21%': 0.21}
        resultados = {}
        
        for nombre_tasa, tasa_isr in tasas.items():
            calc = CalculadoraCETES(capital, tasa_cetes, tasa_inflacion, tasa_isr=tasa_isr)
            resultados[nombre_tasa] = calc.calcular()
        
        return resultados
    
    def proyectar_multiples_anos(self, capital_inicial, tasa_cetes_anual, 
                                tasa_inflacion_anual, tasa_isr, anos=5):
        """
        Proyecta la inversión a lo largo de múltiples años.
        
        Args:
            capital_inicial (float): Capital inicial
            tasa_cetes_anual (float): Tasa CETES anual
            tasa_inflacion_anual (float): Tasa inflación anual
            tasa_isr (float): Tasa ISR
            anos (int): Número de años a proyectar
        
        Returns:
            list: Lista de resultados por año
        """
        proyecciones = []
        capital_actual = capital_inicial
        ganancia_acumulada = 0
        
        for ano in range(1, anos + 1):
            calc = CalculadoraCETES(capital_actual, tasa_cetes_anual, 
                                   tasa_inflacion_anual, tasa_isr=tasa_isr)
            resultado = calc.calcular()
            
            # Agregar información de año
            resultado['ano'] = ano
            resultado['capital_inicial_ano'] = capital_actual
            resultado['ganancia_acumulada'] = ganancia_acumulada + resultado['ganancia_neta']
            
            proyecciones.append(resultado)
            
            # Capital para el siguiente año es el capital final del año actual
            capital_actual = resultado['capital_final']
            ganancia_acumulada = resultado['ganancia_acumulada']
        
        return proyecciones
    
    def generar_resumen_comparativa(self):
        """Genera un resumen en texto de la comparativa."""
        if not self.resultados_comparativa:
            self.calcular_todos()
        
        lineas = ["COMPARATIVA DE ESCENARIOS", "=" * 80]
        
        for nombre, resultado in self.resultados_comparativa.items():
            lineas.append(f"\n📊 {nombre.upper()}")
            lineas.append("-" * 80)
            lineas.append(f"  Capital Inicial:      ${resultado['capital_inicial']:>12,.2f} MXN")
            lineas.append(f"  Tasa CETES:           {resultado['tasa_cetes']*100:>12.2f}%")
            lineas.append(f"  Tasa ISR:             {resultado['tasa_isr']*100:>12.0f}%")
            lineas.append(f"  Ganancia Neta:        ${resultado['ganancia_neta']:>12,.2f} MXN")
            lineas.append(f"  Rentabilidad Efectiva:{resultado['rentabilidad_efectiva']:>12.2f}%")
            lineas.append(f"  Saldo a Favor:        ${resultado['saldo_a_favor']:>12,.2f} MXN")
        
        return "\n".join(lineas)
    
    def obtener_mejor_escenario(self):
        """Retorna el escenario con mayor ganancia neta."""
        if not self.resultados_comparativa:
            self.calcular_todos()
        
        mejor = max(self.resultados_comparativa.items(),
                   key=lambda x: x[1]['ganancia_neta'])
        return mejor
    
    def obtener_peor_escenario(self):
        """Retorna el escenario con menor ganancia neta."""
        if not self.resultados_comparativa:
            self.calcular_todos()
        
        peor = min(self.resultados_comparativa.items(),
                  key=lambda x: x[1]['ganancia_neta'])
        return peor


class AnalizadorSensibilidad:
    """Analiza cómo cambian los resultados con variaciones en parámetros."""
    
    @staticmethod
    def variar_tasa_cetes(capital, tasa_base, tasa_inflacion, tasa_isr, 
                         rango_variacion=0.02, pasos=5):
        """
        Varía la tasa CETES y muestra cómo impacta en los resultados.
        
        Args:
            capital (float): Capital invertido
            tasa_base (float): Tasa CETES base
            tasa_inflacion (float): Tasa inflación
            tasa_isr (float): Tasa ISR
            rango_variacion (float): Rango de variación (±)
            pasos (int): Número de pasos
        
        Returns:
            list: Resultados para cada variación
        """
        resultados = []
        paso_tamano = rango_variacion / (pasos - 1) if pasos > 1 else 0
        
        for i in range(pasos):
            tasa = tasa_base - rango_variacion + (paso_tamano * i)
            calc = CalculadoraCETES(capital, tasa, tasa_inflacion, tasa_isr=tasa_isr)
            resultado = calc.calcular()
            resultado['tasa_variada'] = tasa
            resultados.append(resultado)
        
        return resultados
    
    @staticmethod
    def variar_inflacion(capital, tasa_cetes, inflacion_base, tasa_isr,
                        rango_variacion=0.02, pasos=5):
        """Varía la tasa de inflación y analiza impacto."""
        resultados = []
        paso_tamano = rango_variacion / (pasos - 1) if pasos > 1 else 0
        
        for i in range(pasos):
            inflacion = inflacion_base - rango_variacion + (paso_tamano * i)
            calc = CalculadoraCETES(capital, tasa_cetes, inflacion, tasa_isr=tasa_isr)
            resultado = calc.calcular()
            resultado['inflacion_variada'] = inflacion
            resultados.append(resultado)
        
        return resultados
