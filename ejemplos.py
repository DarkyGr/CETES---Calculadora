#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ejemplos de uso de la Calculadora de CETES.
Ejecuta este archivo para ver ejemplos precargados.
"""

from src.calculadora import CalculadoraCETES
from src.comparador import ComparadorEscenarios, AnalizadorSensibilidad
from src.exportador import ExportadorCSV


def ejemplo_1_caso_base():
    """Ejemplo 1: Caso base del problema original."""
    print("\n" + "="*70)
    print("EJEMPLO 1: CASO BASE (Capital: $250,000, CETES: 7.19%, ISR: 15%)")
    print("="*70)
    
    calc = CalculadoraCETES(
        capital=250000,
        tasa_cetes=0.0719,
        tasa_inflacion=0.0411,
        tasa_isr=0.15
    )
    
    resultado = calc.calcular()
    print(calc.resumen_texto())


def ejemplo_2_comparativa_isr():
    """Ejemplo 2: Comparar diferentes tasas ISR."""
    print("\n" + "="*70)
    print("EJEMPLO 2: COMPARATIVA DE TASAS ISR (10%, 15%, 21%)")
    print("="*70)
    
    comparador = ComparadorEscenarios()
    resultados = comparador.comparar_por_tasa_isr(250000, 0.0719, 0.0411)
    
    print("\n📋 TABLA COMPARATIVA")
    print("-"*70)
    print(f"{'ISR':<8} {'Ganancia Neta':<20} {'Rentabilidad':<15} {'Saldo':<15}")
    print("-"*70)
    
    for tasa_nombre, resultado in resultados.items():
        saldo = resultado['saldo_a_favor'] - resultado['saldo_a_pagar']
        print(f"{tasa_nombre:<8} ${resultado['ganancia_neta']:>16,.2f} "
              f"{resultado['rentabilidad_efectiva']:>13.2f}% ${saldo:>12,.2f}")
    
    # Identificar mejor escenario
    mejor = max(resultados.items(), key=lambda x: x[1]['ganancia_neta'])
    print(f"\n✅ Mejor escenario: {mejor[0]} (Ganancia: ${mejor[1]['ganancia_neta']:,.2f})")


def ejemplo_3_proyeccion_anos():
    """Ejemplo 3: Proyectar inversión a 5 años."""
    print("\n" + "="*70)
    print("EJEMPLO 3: PROYECCIÓN DE 5 AÑOS")
    print("="*70)
    
    comparador = ComparadorEscenarios()
    proyecciones = comparador.proyectar_multiples_anos(
        capital_inicial=250000,
        tasa_cetes_anual=0.0719,
        tasa_inflacion_anual=0.0411,
        tasa_isr=0.15,
        anos=5
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
    print(f"Rentabilidad Total: {(proyecciones[-1]['ganancia_acumulada']/250000)*100:.2f}%")


def ejemplo_4_sensibilidad_tasa_cetes():
    """Ejemplo 4: Análisis de sensibilidad de tasa CETES."""
    print("\n" + "="*70)
    print("EJEMPLO 4: SENSIBILIDAD DE TASA CETES (±2%)")
    print("="*70)
    
    variaciones = AnalizadorSensibilidad.variar_tasa_cetes(
        capital=250000,
        tasa_base=0.0719,
        tasa_inflacion=0.0411,
        tasa_isr=0.15,
        rango_variacion=0.02,
        pasos=5
    )
    
    print("\n📈 VARIACIÓN DE TASA CETES")
    print("-"*80)
    print(f"{'Tasa CETES':<15} {'Ganancia Neta':<20} {'Rentabilidad':<15} {'Cambio':<15}")
    print("-"*80)
    
    ganancia_base = variaciones[2]['ganancia_neta']  # Valor central
    
    for var in variaciones:
        cambio = var['ganancia_neta'] - ganancia_base
        simbolo = "↑" if cambio > 0 else "↓" if cambio < 0 else "→"
        print(f"{var['tasa_variada']*100:>6.2f}%        ${var['ganancia_neta']:>15,.2f} "
              f"{var['rentabilidad_efectiva']:>13.2f}% {simbolo} ${cambio:>11,.2f}")


def ejemplo_5_sensibilidad_inflacion():
    """Ejemplo 5: Análisis de sensibilidad de inflación."""
    print("\n" + "="*70)
    print("EJEMPLO 5: SENSIBILIDAD DE INFLACIÓN (±2%)")
    print("="*70)
    
    variaciones = AnalizadorSensibilidad.variar_inflacion(
        capital=250000,
        tasa_cetes=0.0719,
        inflacion_base=0.0411,
        tasa_isr=0.15,
        rango_variacion=0.02,
        pasos=5
    )
    
    print("\n📈 VARIACIÓN DE INFLACIÓN")
    print("-"*80)
    print(f"{'Inflación':<15} {'Ganancia Neta':<20} {'Rentabilidad':<15} {'Cambio':<15}")
    print("-"*80)
    
    ganancia_base = variaciones[2]['ganancia_neta']  # Valor central
    
    for var in variaciones:
        cambio = var['ganancia_neta'] - ganancia_base
        simbolo = "↑" if cambio > 0 else "↓" if cambio < 0 else "→"
        print(f"{var['inflacion_variada']*100:>6.2f}%        ${var['ganancia_neta']:>15,.2f} "
              f"{var['rentabilidad_efectiva']:>13.2f}% {simbolo} ${cambio:>11,.2f}")


def ejemplo_6_exportar_csv():
    """Ejemplo 6: Exportar resultados a CSV."""
    print("\n" + "="*70)
    print("EJEMPLO 6: EXPORTAR A CSV")
    print("="*70)
    
    # Calcular resultado
    calc = CalculadoraCETES(250000, 0.0719, 0.0411, tasa_isr=0.15)
    resultado = calc.calcular()
    
    # Exportar
    exportador = ExportadorCSV("./output")
    ruta = exportador.exportar_resultado(resultado, "ejemplo_caso_base")
    print(f"\n✅ Resultado exportado a: {ruta}")
    
    # Exportar comparativa
    resultados_multi = [resultado]  # Podría haber múltiples
    ruta_comp = exportador.exportar_comparativa(resultados_multi, "ejemplo_comparativa")
    print(f"✅ Comparativa exportada a: {ruta_comp}")


def ejemplo_7_multiples_escenarios():
    """Ejemplo 7: Comparar múltiples escenarios personalizados."""
    print("\n" + "="*70)
    print("EJEMPLO 7: MÚLTIPLES ESCENARIOS PERSONALIZADOS")
    print("="*70)
    
    comparador = ComparadorEscenarios()
    
    # Agregar escenarios
    comparador.agregar_escenario(
        "Conservador",
        capital=250000,
        tasa_cetes=0.0619,  # 6.19%
        tasa_inflacion=0.0411,
        tasa_isr=0.21  # Ingresos altos
    )
    
    comparador.agregar_escenario(
        "Base",
        capital=250000,
        tasa_cetes=0.0719,  # 7.19%
        tasa_inflacion=0.0411,
        tasa_isr=0.15  # Ingresos medios
    )
    
    comparador.agregar_escenario(
        "Optimista",
        capital=250000,
        tasa_cetes=0.0819,  # 8.19%
        tasa_inflacion=0.0311,  # Inflación baja
        tasa_isr=0.10  # Ingresos bajos
    )
    
    comparador.calcular_todos()
    print(comparador.generar_resumen_comparativa())
    
    # Mejor y peor
    mejor = comparador.obtener_mejor_escenario()
    peor = comparador.obtener_peor_escenario()
    
    print(f"\n🏆 Mejor escenario: {mejor[0]}")
    print(f"   Ganancia Neta: ${mejor[1]['ganancia_neta']:,.2f}")
    print(f"\n📉 Peor escenario: {peor[0]}")
    print(f"   Ganancia Neta: ${peor[1]['ganancia_neta']:,.2f}")


def main():
    """Ejecuta todos los ejemplos."""
    print("\n" + "="*70)
    print("EJEMPLOS DE USO - CALCULADORA DE CETES")
    print("="*70)
    
    ejemplo_1_caso_base()
    ejemplo_2_comparativa_isr()
    ejemplo_3_proyeccion_anos()
    ejemplo_4_sensibilidad_tasa_cetes()
    ejemplo_5_sensibilidad_inflacion()
    ejemplo_6_exportar_csv()
    ejemplo_7_multiples_escenarios()
    
    print("\n" + "="*70)
    print("✅ EJEMPLOS COMPLETADOS")
    print("="*70)
    print("\n💡 Para más información, revisa el README.md o ejecuta: python main.py\n")


if __name__ == "__main__":
    main()
