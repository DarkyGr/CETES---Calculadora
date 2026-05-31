#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
INICIO RÁPIDO - Calculadora de CETES
Ejemplos simples para empezar inmediatamente.
"""

# ============================================================================
# OPCIÓN 1: USO MÁS SIMPLE (Una línea)
# ============================================================================

from src.calculadora import crear_calculadora

resultado = crear_calculadora(250000, 0.0719, 0.0411, tasa_isr=0.15)
print("Ganancia Neta:", resultado['ganancia_neta'])  # $6,545.00
print("Saldo a Favor:", resultado['saldo_a_favor'])  # $1,095.00


# ============================================================================
# OPCIÓN 2: CON SALIDA FORMATEADA
# ============================================================================

from src.calculadora import CalculadoraCETES

calc = CalculadoraCETES(250000, 0.0719, 0.0411, tasa_isr=0.15)
resultado = calc.calcular()
print(calc.resumen_texto())


# ============================================================================
# OPCIÓN 3: COMPARA 3 ESCENARIOS ISR
# ============================================================================

from src.comparador import ComparadorEscenarios

comparador = ComparadorEscenarios()
resultados = comparador.comparar_por_tasa_isr(250000, 0.0719, 0.0411)

for tasa, resultado in resultados.items():
    print(f"{tasa}: ${resultado['ganancia_neta']:,.2f}")


# ============================================================================
# OPCIÓN 4: PROYECTA 5 AÑOS
# ============================================================================

proyecciones = comparador.proyectar_multiples_anos(
    250000, 0.0719, 0.0411, 0.15, anos=5
)

for p in proyecciones:
    print(f"Año {p['ano']}: ${p['capital_final']:,.2f}")


# ============================================================================
# OPCIÓN 5: EXPORTAR A CSV
# ============================================================================

from src.exportador import ExportadorCSV

exportador = ExportadorCSV("./output")
exportador.exportar_resultado(resultado, "mi_inversion")


# ============================================================================
# OPCIÓN 6: MENÚ INTERACTIVO (COMPLETO)
# ============================================================================

if __name__ == "__main__":
    print("¿Ejecutar menú interactivo? Ver main.py")
    # python main.py
