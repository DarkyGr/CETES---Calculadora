#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Calculadora CETES V2 - Con cálculo automático de ISR basado en ingresos.
Hereda de CalculadoraCETES y agrega funcionalidad de ingresos mensuales.
"""

from .calculadora import CalculadoraCETES
from .tabla_isr import TablaISRMensual


class CalculadoraCETESV2(CalculadoraCETES):
    """Versión mejorada con cálculo automático de ISR desde ingresos mensuales."""
    
    def __init__(self, capital, tasa_cetes, tasa_inflacion, 
                 ingreso_bruto_mensual=None, tasa_isr=None, 
                 tasa_retencion=None, ano=None):
        """
        Inicializa la calculadora con soporte para ingresos mensuales.
        
        Args:
            capital (float): Capital invertido en MXN
            tasa_cetes (float): Tasa CETES anual
            tasa_inflacion (float): Tasa inflación anual
            ingreso_bruto_mensual (float, optional): Ingreso bruto mensual
                Si se proporciona, calcula automáticamente tasa_isr
            tasa_isr (float, optional): Tasa ISR manual (si ingreso_bruto_mensual no se proporciona)
            tasa_retencion (float, optional): Tasa retención (default 0.90%)
            ano (int, optional): Año para tabla de ISR (default año actual)
        
        Raises:
            ValueError: Si parámetros no son válidos
        """
        self.ingreso_bruto_mensual = ingreso_bruto_mensual
        self.ano = ano
        self.info_isr = None
        
        # Si se proporciona ingreso, calcular tasa_isr automáticamente
        if ingreso_bruto_mensual is not None:
            self.info_isr = TablaISRMensual.calcular_isr_desde_ingreso_mensual(
                ingreso_bruto_mensual, ano
            )
            tasa_isr_calculada = self.info_isr['tasa_isr']
        else:
            tasa_isr_calculada = tasa_isr or 0.15
        
        # Llamar al constructor padre
        super().__init__(
            capital=capital,
            tasa_cetes=tasa_cetes,
            tasa_inflacion=tasa_inflacion,
            tasa_retencion=tasa_retencion,
            tasa_isr=tasa_isr_calculada
        )
    
    def obtener_informacion_isr(self):
        """Retorna información detallada sobre el cálculo de ISR."""
        return self.info_isr
    
    def resumen_texto_detallado(self):
        """Retorna resumen completo incluyendo información de ingresos e ISR."""
        lineas = []
        
        # Información de ingresos si está disponible
        if self.ingreso_bruto_mensual is not None and self.info_isr:
            lineas.append("\n" + "="*60)
            lineas.append("CÁLCULO DE ISR DESDE INGRESOS MENSUALES")
            lineas.append("="*60)
            lineas.append(f"Ingreso Bruto Mensual:  ${self.ingreso_bruto_mensual:,.2f} MXN")
            lineas.append(f"Año de Tabla:           {self.info_isr['ano']}")
            lineas.append(f"Límite Inferior:        ${self.info_isr['limite_inferior']:,.2f}")
            lineas.append(f"Límite Superior:        ${self.info_isr['limite_superior']:,.2f}")
            lineas.append(f"Cuota Fija:             ${self.info_isr['cuota_fija']:,.2f}")
            lineas.append(f"% Sobre Excedente:      {self.info_isr['porcentaje_excedente']*100:.2f}%")
            lineas.append(f"\n➜ Tasa ISR Determinada: {self.tasa_isr*100:.2f}%")
        
        # Resumen estándar de CETES
        lineas.append("\n" + super().resumen_texto())
        
        return "\n".join(lineas)
    
    @staticmethod
    def crear_desde_ingresos(capital, tasa_cetes, tasa_inflacion, 
                             ingreso_bruto_mensual, ano=None):
        """
        Función de conveniencia para crear calculadora desde ingresos mensuales.
        
        Returns:
            dict: Resultados del cálculo
        """
        calc = CalculadoraCETESV2(
            capital=capital,
            tasa_cetes=tasa_cetes,
            tasa_inflacion=tasa_inflacion,
            ingreso_bruto_mensual=ingreso_bruto_mensual,
            ano=ano
        )
        return calc.calcular()


class ComparadorEscenariosPorIngresos:
    """Compara escenarios de inversión basados en diferentes ingresos mensuales."""
    
    def __init__(self):
        """Inicializa el comparador."""
        self.escenarios = {}
    
    def agregar_escenario_por_ingreso(self, nombre, capital, tasa_cetes, 
                                      tasa_inflacion, ingreso_bruto_mensual, ano=None):
        """
        Agrega un escenario usando ingreso mensual bruto.
        
        Args:
            nombre (str): Nombre descriptivo del escenario
            capital (float): Capital invertido
            tasa_cetes (float): Tasa CETES
            tasa_inflacion (float): Tasa inflación
            ingreso_bruto_mensual (float): Ingreso bruto mensual
            ano (int, optional): Año de tabla
        """
        calc = CalculadoraCETESV2(
            capital=capital,
            tasa_cetes=tasa_cetes,
            tasa_inflacion=tasa_inflacion,
            ingreso_bruto_mensual=ingreso_bruto_mensual,
            ano=ano
        )
        
        self.escenarios[nombre] = {
            'calculadora': calc,
            'ingreso_mensual': ingreso_bruto_mensual,
            'info_isr': calc.obtener_informacion_isr()
        }
    
    def calcular_todos(self):
        """Calcula todos los escenarios."""
        resultados = {}
        for nombre, escenario in self.escenarios.items():
            resultado = escenario['calculadora'].calcular()
            resultado['ingreso_mensual'] = escenario['ingreso_mensual']
            resultado['info_isr'] = escenario['info_isr']
            resultados[nombre] = resultado
        
        return resultados
    
    def generar_resumen(self):
        """Genera resumen detallado de todos los escenarios."""
        resultados = self.calcular_todos()
        lineas = ["COMPARATIVA DE ESCENARIOS POR INGRESO", "="*90]
        
        for nombre, resultado in resultados.items():
            lineas.append(f"\n📊 {nombre.upper()}")
            lineas.append("-"*90)
            lineas.append(f"  Ingreso Mensual Bruto: ${resultado['ingreso_mensual']:>12,.2f} MXN")
            lineas.append(f"  Tasa ISR (automática): {resultado['tasa_isr']*100:>12.2f}%")
            lineas.append(f"  Capital Invertido:    ${resultado['capital_inicial']:>12,.2f} MXN")
            lineas.append(f"  Ganancia Neta:        ${resultado['ganancia_neta']:>12,.2f} MXN")
            lineas.append(f"  Rentabilidad Efectiva:{resultado['rentabilidad_efectiva']:>12.2f}%")
            lineas.append(f"  Saldo a Favor:        ${resultado['saldo_a_favor']:>12,.2f} MXN")
        
        return "\n".join(lineas)


def proyectar_multiples_ingresos(capital, tasa_cetes, tasa_inflacion, 
                                 ingresos_mensuales, ano=None):
    """
    Proyecta múltiples escenarios de inversión basados en diferentes ingresos.
    
    Args:
        capital (float): Capital invertido
        tasa_cetes (float): Tasa CETES
        tasa_inflacion (float): Tasa inflación
        ingresos_mensuales (list): Lista de ingresos mensuales a proyectar
        ano (int, optional): Año de tabla
    
    Returns:
        dict: Resultados para cada nivel de ingresos
    """
    resultados = {}
    
    for ingreso in ingresos_mensuales:
        try:
            calc = CalculadoraCETESV2(
                capital=capital,
                tasa_cetes=tasa_cetes,
                tasa_inflacion=tasa_inflacion,
                ingreso_bruto_mensual=ingreso,
                ano=ano
            )
            resultado = calc.calcular()
            
            label = f"${ingreso:,.0f}/mes ({resultado['tasa_isr']*100:.0f}% ISR)"
            resultados[label] = resultado
        
        except ValueError as e:
            print(f"⚠️  Error con ingreso ${ingreso:,.2f}: {e}")
    
    return resultados
