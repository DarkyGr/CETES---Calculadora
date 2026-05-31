#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script principal de la Calculadora de CETES.
Interfaz interactiva para realizar cálculos y análisis.
"""

from src.calculadora import CalculadoraCETES
from src.exportador import ExportadorCSV
from src.comparador import ComparadorEscenarios, AnalizadorSensibilidad


def mostrar_menu_principal():
    """Muestra el menú principal."""
    print("\n" + "="*60)
    print("CALCULADORA DE INVERSIÓN EN CETES (México)")
    print("="*60)
    print("\n¿Qué deseas hacer?")
    print("  1. Calcular inversión única")
    print("  2. Comparar diferentes tasas ISR")
    print("  3. Proyectar múltiples años")
    print("  4. Analizar sensibilidad de tasas")
    print("  5. Salir")
    print("-"*60)


def calcular_inversion_unica():
    """Calcula una inversión única."""
    print("\n📊 CÁLCULO DE INVERSIÓN ÚNICA")
    print("-"*60)
    
    try:
        capital = float(input("Capital inicial (MXN): $"))
        tasa_cetes = float(input("Tasa CETES (ej: 7.19 para 7.19%): ")) / 100
        tasa_inflacion = float(input("Tasa Inflación (ej: 4.11 para 4.11%): ")) / 100
        tasa_isr = float(input("Tasa ISR (ej: 15 para 15%, enter para 15%): ") or 15) / 100
        
        calc = CalculadoraCETES(capital, tasa_cetes, tasa_inflacion, tasa_isr=tasa_isr)
        resultado = calc.calcular()
        
        print("\n" + calc.resumen_texto())
        
        # Opción de exportar
        exportar = input("\n¿Deseas exportar a CSV? (s/n): ").lower() == 's'
        if exportar:
            exportador = ExportadorCSV()
            ruta = exportador.exportar_resultado(resultado, "inversion_unica")
            print(f"✅ Archivo guardado en: {ruta}")
        
        return resultado
    
    except ValueError as e:
        print(f"❌ Error: {e}")
        return None


def comparar_tasas_isr():
    """Compara diferentes tasas ISR."""
    print("\n📊 COMPARATIVA DE TASAS ISR")
    print("-"*60)
    
    try:
        capital = float(input("Capital inicial (MXN): $"))
        tasa_cetes = float(input("Tasa CETES (ej: 7.19): ")) / 100
        tasa_inflacion = float(input("Tasa Inflación (ej: 4.11): ")) / 100
        
        comparador = ComparadorEscenarios()
        resultados = comparador.comparar_por_tasa_isr(capital, tasa_cetes, tasa_inflacion)
        
        print("\n" + comparador.generar_resumen_comparativa())
        
        # Tabla comparativa simple
        print("\n📋 TABLA COMPARATIVA")
        print("-"*80)
        print(f"{'ISR':<8} {'Ganancia Neta':<20} {'Rentabilidad':<15} {'Saldo':<15}")
        print("-"*80)
        
        for tasa_nombre, resultado in resultados.items():
            saldo = "A Favor" if resultado['saldo_a_favor'] > 0 else "A Pagar"
            print(f"{tasa_nombre:<8} ${resultado['ganancia_neta']:>16,.2f} "
                  f"{resultado['rentabilidad_efectiva']:>13.2f}% {saldo:>15}")
        
        # Exportar
        exportar = input("\n¿Deseas exportar a CSV? (s/n): ").lower() == 's'
        if exportar:
            exportador = ExportadorCSV()
            lista_res = list(resultados.values())
            ruta = exportador.exportar_comparativa(lista_res, "comparativa_isr")
            print(f"✅ Archivo guardado en: {ruta}")
    
    except ValueError as e:
        print(f"❌ Error: {e}")


def proyectar_multiples_anos():
    """Proyecta inversión a lo largo de varios años."""
    print("\n📊 PROYECCIÓN MULTI-AÑO")
    print("-"*60)
    
    try:
        capital = float(input("Capital inicial (MXN): $"))
        tasa_cetes = float(input("Tasa CETES anual (ej: 7.19): ")) / 100
        tasa_inflacion = float(input("Tasa Inflación anual (ej: 4.11): ")) / 100
        tasa_isr = float(input("Tasa ISR (ej: 15, enter para 15%): ") or 15) / 100
        anos = int(input("¿Cuántos años proyectar?: "))
        
        comparador = ComparadorEscenarios()
        proyecciones = comparador.proyectar_multiples_anos(
            capital, tasa_cetes, tasa_inflacion, tasa_isr, anos
        )
        
        print("\n📈 PROYECCIÓN POR AÑO")
        print("-"*100)
        print(f"{'Año':<5} {'Capital Inicio':<18} {'Ganancia':<18} {'Capital Final':<18} {'Acumulado':<15}")
        print("-"*100)
        
        for p in proyecciones:
            print(f"{p['ano']:<5} ${p['capital_inicial_ano']:>15,.2f} "
                  f"${p['ganancia_neta']:>15,.2f} ${p['capital_final']:>15,.2f} "
                  f"${p['ganancia_acumulada']:>12,.2f}")
        
        print("-"*100)
        print(f"Capital Final Total: ${proyecciones[-1]['capital_final']:,.2f} MXN")
        print(f"Ganancia Acumulada: ${proyecciones[-1]['ganancia_acumulada']:,.2f} MXN")
        
        # Exportar
        exportar = input("\n¿Deseas exportar a CSV? (s/n): ").lower() == 's'
        if exportar:
            exportador = ExportadorCSV()
            ruta = exportador.exportar_comparativa(proyecciones, f"proyeccion_{anos}anos")
            print(f"✅ Archivo guardado en: {ruta}")
    
    except ValueError as e:
        print(f"❌ Error: {e}")


def analizar_sensibilidad():
    """Analiza sensibilidad de parámetros."""
    print("\n📊 ANÁLISIS DE SENSIBILIDAD")
    print("-"*60)
    
    try:
        capital = float(input("Capital inicial (MXN): $"))
        tasa_cetes = float(input("Tasa CETES base (ej: 7.19): ")) / 100
        tasa_inflacion = float(input("Tasa Inflación (ej: 4.11): ")) / 100
        tasa_isr = float(input("Tasa ISR (ej: 15, enter para 15%): ") or 15) / 100
        
        print("\n¿Qué deseas analizar?")
        print("  1. Sensibilidad de Tasa CETES")
        print("  2. Sensibilidad de Inflación")
        
        opcion = input("Selecciona (1-2): ").strip()
        
        if opcion == "1":
            variaciones = AnalizadorSensibilidad.variar_tasa_cetes(
                capital, tasa_cetes, tasa_inflacion, tasa_isr
            )
            print("\n📈 VARIACIÓN DE TASA CETES")
            print("-"*80)
            print(f"{'Tasa CETES':<15} {'Ganancia Neta':<20} {'Rentabilidad':<15} {'Saldo':<15}")
            print("-"*80)
            
            for var in variaciones:
                saldo = var['saldo_a_favor'] - var['saldo_a_pagar']
                print(f"{var['tasa_variada']*100:>6.2f}%        ${var['ganancia_neta']:>15,.2f} "
                      f"{var['rentabilidad_efectiva']:>13.2f}% ${saldo:>12,.2f}")
        
        elif opcion == "2":
            variaciones = AnalizadorSensibilidad.variar_inflacion(
                capital, tasa_cetes, tasa_inflacion, tasa_isr
            )
            print("\n📈 VARIACIÓN DE INFLACIÓN")
            print("-"*80)
            print(f"{'Inflación':<15} {'Ganancia Neta':<20} {'Rentabilidad':<15} {'Saldo':<15}")
            print("-"*80)
            
            for var in variaciones:
                saldo = var['saldo_a_favor'] - var['saldo_a_pagar']
                print(f"{var['inflacion_variada']*100:>6.2f}%        ${var['ganancia_neta']:>15,.2f} "
                      f"{var['rentabilidad_efectiva']:>13.2f}% ${saldo:>12,.2f}")
    
    except ValueError as e:
        print(f"❌ Error: {e}")


def main():
    """Función principal."""
    while True:
        mostrar_menu_principal()
        opcion = input("Selecciona una opción (1-5): ").strip()
        
        if opcion == "1":
            calcular_inversion_unica()
        
        elif opcion == "2":
            comparar_tasas_isr()
        
        elif opcion == "3":
            proyectar_multiples_anos()
        
        elif opcion == "4":
            analizar_sensibilidad()
        
        elif opcion == "5":
            print("\n¡Hasta luego! 👋")
            break
        
        else:
            print("❌ Opción no válida. Intenta de nuevo.")


if __name__ == "__main__":
    main()
