"""
Calculadora de CETES - Paquete principal
"""

from .calculadora import CalculadoraCETES, crear_calculadora
from .exportador import ExportadorCSV
from .comparador import ComparadorEscenarios, AnalizadorSensibilidad
from .tabla_isr import TablaISRMensual
from .calculadora_v2 import (
    CalculadoraCETESV2,
    ComparadorEscenariosPorIngresos,
    proyectar_multiples_ingresos
)

__version__ = "1.0.0"
__author__ = "Calculadora CETES"
__all__ = [
    'CalculadoraCETES',
    'crear_calculadora',
    'ExportadorCSV',
    'ComparadorEscenarios',
    'AnalizadorSensibilidad',
    'TablaISRMensual',
    'CalculadoraCETESV2',
    'ComparadorEscenariosPorIngresos',
    'proyectar_multiples_ingresos'
]
