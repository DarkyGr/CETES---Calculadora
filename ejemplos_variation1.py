#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ejemplos de uso - VARIATION 1
Demuestra cálculos de CETES con ISR automático desde ingresos mensuales.
"""

from src.calculadora_v2 import (
    CalculadoraCETESV2,
    ComparadorEscenariosPorIngresos,
    proyectar_multiples_ingresos
)
from src.tabla_isr import TablaISRMensual


def ejemplo_1_tabla_isr():
    """Ejemplo 1: Ver la tabla de ISR 2026."""
    print("\n" + "="*70)
    print("EJEMPLO 1: TABLA DE ISR 2026")
    print("="*70)
    print(TablaISRMensual.resumen_tabla(2026))


def ejemplo_2_ingreso_bajo():
    """Ejemplo 2: Inversión con ingreso mensual bajo."""
    print("\n" + "="*70)
    print("EJEMPLO 2: INGRESO MENSUAL BAJO ($10,000/mes)")
    print("="*70)
    
    calc = CalculadoraCETESV2(
        capital=250000,
        tasa_cetes=0.0719,
        tasa_inflacion=0.0411,
        ingreso_bruto_mensual=10000,
        ano=2026
    )
    
    resultado = calc.calcular()
    print(calc.resumen_texto_detallado())


def ejemplo_3_ingreso_medio():
    """Ejemplo 3: Inversión con ingreso mensual medio."""
    print("\n" + "="*70)
    print("EJEMPLO 3: INGRESO MENSUAL MEDIO ($25,000/mes)")
    print("="*70)
    
    calc = CalculadoraCETESV2(
        capital=250000,
        tasa_cetes=0.0719,
        tasa_inflacion=0.0411,
        ingreso_bruto_mensual=25000,
        ano=2026
    )
    
    resultado = calc.calcular()
    print(calc.resumen_texto_detallado())


def ejemplo_4_ingreso_alto():
    """Ejemplo 4: Inversión con ingreso mensual alto."""
    print("\n" + "="*70)
    print("EJEMPLO 4: INGRESO MENSUAL ALTO ($80,000/mes)")
    print("="*70)
    
    calc = CalculadoraCETESV2(
        capital=250000,
        tasa_cetes=0.0719,
        tasa_inflacion=0.0411,
        ingreso_bruto_mensual=80000,
        ano=2026
    )
    
    resultado = calc.calcular()
    print(calc.resumen_texto_detallado())


def ejemplo_5_comparativa_ingresos():
    """Ejemplo 5: Comparar tres niveles de ingresos."""
    print("\n" + "="*70)
    print("EJEMPLO 5: COMPARATIVA DE TRES NIVELES DE INGRESO")
    print("="*70)
    
    comparador = ComparadorEscenariosPorIngresos()
    
    # Agregar tres escenarios
    comparador.agregar_escenario_por_ingreso(
        "Ingreso Bajo",
        capital=250000,
        tasa_cetes=0.0719,
        tasa_inflacion=0.0411,
        ingreso_bruto_mensual=15000,
        ano=2026
    )
    
    comparador.agregar_escenario_por_ingreso(
        "Ingreso Medio",
        capital=250000,
        tasa_cetes=0.0719,
        tasa_inflacion=0.0411,
        ingreso_bruto_mensual=40000,
        ano=2026
    )
    
    comparador.agregar_escenario_por_ingreso(
        "Ingreso Alto",
        capital=250000,
        tasa_cetes=0.0719,
        tasa_inflacion=0.0411,
        ingreso_bruto_mensual=120000,
        ano=2026
    )
    
    print(comparador.generar_resumen())


def ejemplo_6_rango_ingresos():
    """Ejemplo 6: Proyectar para rango de ingresos."""
    print("\n" + "="*70)
    print("EJEMPLO 6: PROYECCIÓN PARA RANGO DE INGRESOS")
    print("Simulando ingresos de $5,000 a $150,000 mensuales")
    print("="*70)
    
    # Generar 7 niveles de ingresos
    ingresos = [5000, 15000, 25000, 40000, 60000, 100000, 150000]
    
    resultados = proyectar_multiples_ingresos(
        capital=250000,
        tasa_cetes=0.0719,
        tasa_inflacion=0.0411,
        ingresos_mensuales=ingresos,
        ano=2026
    )
    
    print("\n📊 RESULTADOS POR NIVEL DE INGRESO")
    print("-"*100)
    print(f"{'Ingreso (MXN)':<20} {'ISR %':<10} {'Ganancia Neta':<20} {'Rentabilidad %':<15} {'Saldo':<15}")
    print("-"*100)
    
    for label, resultado in resultados.items():
        saldo = resultado['saldo_a_favor'] - resultado['saldo_a_pagar']
        ingreso_str = label.split(" ")[1].replace("$", "").replace("/mes", "")
        isr_str = f"{resultado['tasa_isr']*100:.1f}%"
        
        print(f"{ingreso_str:<20} {isr_str:<10} ${resultado['ganancia_neta']:>15,.2f} "
              f"{resultado['rentabilidad_efectiva']:>13.2f}% ${saldo:>12,.2f}")
    
    print("-"*100)
    
    # Análisis
    print("\n🔍 ANÁLISIS:")
    valores = list(resultados.values())
    mejor = max(valores, key=lambda x: x['ganancia_neta'])
    peor = min(valores, key=lambda x: x['ganancia_neta'])
    
    mejor_isr = max(valores, key=lambda x: x['tasa_isr'])
    print(f"  • Mayor ganancia: ${mejor['ganancia_neta']:,.2f} (con ISR {mejor['tasa_isr']*100:.1f}%)")
    print(f"  • Menor ganancia: ${peor['ganancia_neta']:,.2f} (con ISR {peor['tasa_isr']*100:.1f}%)")
    print(f"  • Mayor ISR: {mejor_isr['tasa_isr']*100:.1f}%")


def ejemplo_7_como_funciona():
    """Ejemplo 7: Explicación detallada del cálculo."""
    print("\n" + "="*70)
    print("EJEMPLO 7: CÓMO FUNCIONA EL CÁLCULO DE ISR AUTOMÁTICO")
    print("="*70)
    
    ingreso_mensual = 35000
    print(f"\n📍 Ingreso Bruto Mensual: ${ingreso_mensual:,.2f}")
    
    # Obtener info de ISR
    info_isr = TablaISRMensual.calcular_isr_desde_ingreso_mensual(ingreso_mensual, 2026)
    
    print(f"\n1️⃣  LOCALIZAR EN LA TABLA ISR:")
    print(f"   • Límite Inferior: ${info_isr['limite_inferior']:,.2f}")
    print(f"   • Límite Superior: ${info_isr['limite_superior']:,.2f}")
    print(f"   → Tu ingreso (${ingreso_mensual:,.2f}) está entre estos límites ✓")
    
    print(f"\n2️⃣  OBTENER DATOS DEL TRAMO:")
    print(f"   • Cuota Fija: ${info_isr['cuota_fija']:,.2f}")
    print(f"   • % Sobre Excedente: {info_isr['porcentaje_excedente']*100:.2f}%")
    
    print(f"\n3️⃣  USAR COMO TASA ISR EN CETES:")
    print(f"   • Tasa ISR = {info_isr['porcentaje_excedente']*100:.2f}%")
    
    print(f"\n4️⃣  EJEMPLO PRÁCTICO CON ESTOS DATOS:")
    calc = CalculadoraCETESV2(
        capital=250000,
        tasa_cetes=0.0719,
        tasa_inflacion=0.0411,
        ingreso_bruto_mensual=ingreso_mensual,
        ano=2026
    )
    
    resultado = calc.calcular()
    
    print(f"\n   Capital Invertido: ${resultado['capital_inicial']:,.2f}")
    print(f"   Interés Real Gravable: ${resultado['interes_real']:,.2f}")
    print(f"   ISR a Pagar (15.6%): ${resultado['impuesto_definitivo']:,.2f}")
    print(f"   → Ganancia Neta: ${resultado['ganancia_neta']:,.2f}")


def main():
    """Ejecuta todos los ejemplos."""
    print("\n" + "="*70)
    print("EJEMPLOS - CALCULADORA CETES VARIATION 1")
    print("(Con cálculo automático de ISR desde ingresos mensuales)")
    print("="*70)
    
    ejemplo_1_tabla_isr()
    ejemplo_2_ingreso_bajo()
    ejemplo_3_ingreso_medio()
    ejemplo_4_ingreso_alto()
    ejemplo_5_comparativa_ingresos()
    ejemplo_6_rango_ingresos()
    ejemplo_7_como_funciona()
    
    print("\n" + "="*70)
    print("✅ EJEMPLOS COMPLETADOS")
    print("="*70)
    print("\n💡 Para usar interactivamente, ejecuta:")
    print("   python main_variation1.py")
    print()


if __name__ == "__main__":
    main()
