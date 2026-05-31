#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script principal - VARIATION 1
Calculadora de CETES con cálculo automático de ISR desde ingresos mensuales.
"""

from src.calculadora_v2 import (
    CalculadoraCETESV2,
    ComparadorEscenariosPorIngresos,
    proyectar_multiples_ingresos
)
from src.tabla_isr import TablaISRMensual
from src.exportador import ExportadorCSV


def mostrar_menu_principal():
    """Muestra el menú principal."""
    print("\n" + "="*70)
    print("CALCULADORA DE INVERSIÓN EN CETES - VARIATION 1")
    print("(Con cálculo automático de ISR desde ingresos mensuales)")
    print("="*70)
    print("\n¿Qué deseas hacer?")
    print("  1. Calcular inversión (con tu ingreso mensual)")
    print("  2. Ver tabla de ISR vigente")
    print("  3. Comparar diferentes ingresos mensuales")
    print("  4. Proyectar para múltiples niveles de ingreso")
    print("  5. Volver a Calculadora Original (sin ingresos)")
    print("  6. Salir")
    print("-"*70)


def calcular_con_ingreso_mensual():
    """Calcula inversión solicitando ingreso mensual bruto."""
    print("\n📊 CÁLCULO CON INGRESO MENSUAL")
    print("-"*70)
    
    try:
        capital = float(input("Capital inicial (MXN): $"))
        tasa_cetes = float(input("Tasa CETES (ej: 7.19 para 7.19%): ")) / 100
        tasa_inflacion = float(input("Tasa Inflación (ej: 4.11 para 4.11%): ")) / 100
        ingreso_mensual = float(input("Tu ingreso bruto mensual (antes de impuestos) (MXN): $"))
        
        # Verificar si hay tabla para el año actual
        try:
            ano_tabla = TablaISRMensual.obtener_ano_tabla_actual()
            print(f"\n✓ Usando tabla ISR del año {ano_tabla}")
        except ValueError as e:
            print(f"⚠️  Advertencia: {e}")
            ano_tabla = None
        
        # Crear calculadora
        calc = CalculadoraCETESV2(
            capital=capital,
            tasa_cetes=tasa_cetes,
            tasa_inflacion=tasa_inflacion,
            ingreso_bruto_mensual=ingreso_mensual,
            ano=ano_tabla
        )
        
        # Calcular
        resultado = calc.calcular()
        
        # Mostrar resumen detallado
        print(calc.resumen_texto_detallado())
        
        # Opción de exportar
        exportar = input("\n¿Deseas exportar a CSV? (s/n): ").lower() == 's'
        if exportar:
            exportador = ExportadorCSV()
            ruta = exportador.exportar_resultado(resultado, "inversion_con_ingreso")
            print(f"✅ Archivo guardado en: {ruta}")
        
        return resultado
    
    except ValueError as e:
        print(f"❌ Error: {e}")
        return None


def mostrar_tabla_isr():
    """Muestra la tabla de ISR vigente."""
    print("\n📋 TABLA DE ISR VIGENTE")
    print("-"*70)
    
    try:
        ano = TablaISRMensual.obtener_ano_tabla_actual()
        print(TablaISRMensual.resumen_tabla(ano))
        
        anos_disponibles = TablaISRMensual.listar_anos_disponibles()
        print(f"\n✓ Años con tablas disponibles: {', '.join(map(str, anos_disponibles))}")
    
    except ValueError as e:
        print(f"❌ Error: {e}")


def comparar_ingresos():
    """Compara escenarios con diferentes ingresos mensuales."""
    print("\n📊 COMPARATIVA DE INGRESOS MENSUALES")
    print("-"*70)
    
    try:
        capital = float(input("Capital inicial (MXN): $"))
        tasa_cetes = float(input("Tasa CETES (ej: 7.19): ")) / 100
        tasa_inflacion = float(input("Tasa Inflación (ej: 4.11): ")) / 100
        
        comparador = ComparadorEscenariosPorIngresos()
        
        # Agregar escenarios
        print("\n💰 Ingresa diferentes ingresos mensuales (escribe 'listo' para terminar):")
        contador = 1
        
        while True:
            ingreso_input = input(f"Ingreso mensual #{contador} (MXN) o 'listo': $")
            
            if ingreso_input.lower() == 'listo':
                break
            
            try:
                ingreso = float(ingreso_input)
                comparador.agregar_escenario_por_ingreso(
                    nombre=f"Ingreso ${ingreso:,.0f}/mes",
                    capital=capital,
                    tasa_cetes=tasa_cetes,
                    tasa_inflacion=tasa_inflacion,
                    ingreso_bruto_mensual=ingreso
                )
                contador += 1
            except ValueError:
                print("❌ Valor inválido. Intenta de nuevo.")
        
        if contador == 1:
            print("❌ No ingresaste ningún valor.")
            return
        
        # Mostrar comparativa
        print("\n" + comparador.generar_resumen())
        
        # Exportar
        exportar = input("\n¿Deseas exportar a CSV? (s/n): ").lower() == 's'
        if exportar:
            exportador = ExportadorCSV()
            resultados = comparador.calcular_todos()
            ruta = exportador.exportar_comparativa(
                list(resultados.values()),
                "comparativa_ingresos"
            )
            print(f"✅ Archivo guardado en: {ruta}")
    
    except ValueError as e:
        print(f"❌ Error: {e}")


def proyectar_multiples_niveles():
    """Proyecta inversión para múltiples niveles de ingreso."""
    print("\n📈 PROYECCIÓN PARA MÚLTIPLES NIVELES DE INGRESO")
    print("-"*70)
    
    try:
        capital = float(input("Capital inicial (MXN): $"))
        tasa_cetes = float(input("Tasa CETES (ej: 7.19): ")) / 100
        tasa_inflacion = float(input("Tasa Inflación (ej: 4.11): ")) / 100
        
        print("\n💰 Define el rango de ingresos mensuales:")
        ingreso_minimo = float(input("Ingreso mínimo (MXN): $"))
        ingreso_maximo = float(input("Ingreso máximo (MXN): $"))
        cantidad_niveles = int(input("¿Cuántos niveles deseas comparar?: "))
        
        # Generar ingresos equidistantes
        paso = (ingreso_maximo - ingreso_minimo) / (cantidad_niveles - 1) if cantidad_niveles > 1 else 0
        ingresos = [ingreso_minimo + (paso * i) for i in range(cantidad_niveles)]
        
        # Proyectar
        resultados = proyectar_multiples_ingresos(
            capital=capital,
            tasa_cetes=tasa_cetes,
            tasa_inflacion=tasa_inflacion,
            ingresos_mensuales=ingresos
        )
        
        # Mostrar resultados
        print("\n📊 PROYECCIÓN POR NIVEL DE INGRESO")
        print("-"*100)
        print(f"{'Ingreso/ISR':<30} {'Ganancia Neta':<20} {'Rentabilidad':<15} {'Saldo':<15}")
        print("-"*100)
        
        for label, resultado in resultados.items():
            saldo = resultado['saldo_a_favor'] - resultado['saldo_a_pagar']
            print(f"{label:<30} ${resultado['ganancia_neta']:>15,.2f} "
                  f"{resultado['rentabilidad_efectiva']:>13.2f}% ${saldo:>12,.2f}")
        
        print("-"*100)
        
        # Exportar
        exportar = input("\n¿Deseas exportar a CSV? (s/n): ").lower() == 's'
        if exportar:
            exportador = ExportadorCSV()
            ruta = exportador.exportar_comparativa(
                list(resultados.values()),
                "proyeccion_multiples_ingresos"
            )
            print(f"✅ Archivo guardado en: {ruta}")
    
    except ValueError as e:
        print(f"❌ Error: {e}")


def volver_calculadora_original():
    """Retorna a la calculadora original."""
    print("\n✓ Volviendo a la calculadora original...")
    print("Ejecuta: python main.py")


def main():
    """Función principal."""
    while True:
        mostrar_menu_principal()
        opcion = input("Selecciona una opción (1-6): ").strip()
        
        if opcion == "1":
            calcular_con_ingreso_mensual()
        
        elif opcion == "2":
            mostrar_tabla_isr()
        
        elif opcion == "3":
            comparar_ingresos()
        
        elif opcion == "4":
            proyectar_multiples_niveles()
        
        elif opcion == "5":
            volver_calculadora_original()
            break
        
        elif opcion == "6":
            print("\n¡Hasta luego! 👋")
            break
        
        else:
            print("❌ Opción no válida. Intenta de nuevo.")


if __name__ == "__main__":
    main()
