#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuración de rama protegida Variation1

Para proteger esta rama en GitHub/GitLab, usa:

GitHub:
1. Ve a Settings > Branches > Branch protection rules
2. Crea nueva regla para "Variation1"
3. Habilita:
   - Require a pull request before merging
   - Require status checks to pass before merging
   - Require branches to be up to date before merging
   - Require code reviews before merging

GitLab:
1. Ve a Settings > Repository > Protected Branches
2. Crea nueva rama protegida "Variation1"
3. Configura permisos:
   - Allowed to merge: Maintainers
   - Allowed to push: No one

Comandos útiles:

# Ver rama actual
git branch

# Cambiar a Variation1
git checkout Variation1

# Ver commits
git log --oneline

# Hacer push (requiere autenticación)
git push origin Variation1

# Fusionar con main (después de PR aprobado)
git checkout main
git pull origin main
git merge Variation1
git push origin main
"""

# Información de la rama
RAMA_NOMBRE = "Variation1"
RAMA_DESCRIPCION = "Cálculo automático de ISR desde ingresos mensuales"
FECHA_CREACION = "2026-05-31"

CAMBIOS_PRINCIPALES = [
    "Tabla ISR Mensual 2026 (tabla_isr.py)",
    "CalculadoraCETESV2 con soporte de ingresos (calculadora_v2.py)",
    "Menú interactivo main_variation1.py",
    "7 ejemplos completos ejemplos_variation1.py",
]

FUNCIONALIDADES_NUEVAS = [
    "Usuario ingresa ingreso bruto mensual",
    "Sistema identifica tramo ISR automáticamente",
    "Calcula tasa ISR desde '% sobre excedente'",
    "Comparación de múltiples ingresos",
    "Proyección de múltiples niveles de ingreso",
    "Soporte para años futuro de tabla ISR",
]

def mostrar_informacion():
    """Muestra información sobre la rama protegida."""
    print(f"""
    ╔═══════════════════════════════════════════════════════════════════╗
    ║          RAMA PROTEGIDA: {RAMA_NOMBRE:<45}║
    ╚═══════════════════════════════════════════════════════════════════╝
    
    Descripción: {RAMA_DESCRIPCION}
    Fecha de Creación: {FECHA_CREACION}
    
    ═══════════════════════════════════════════════════════════════════
    CAMBIOS PRINCIPALES:
    ═══════════════════════════════════════════════════════════════════
    """)
    
    for cambio in CAMBIOS_PRINCIPALES:
        print(f"    ✓ {cambio}")
    
    print("""
    ═══════════════════════════════════════════════════════════════════
    FUNCIONALIDADES NUEVAS:
    ═══════════════════════════════════════════════════════════════════
    """)
    
    for func in FUNCIONALIDADES_NUEVAS:
        print(f"    ✓ {func}")
    
    print("""
    ═══════════════════════════════════════════════════════════════════
    ARCHIVOS CREADOS/MODIFICADOS:
    ═══════════════════════════════════════════════════════════════════
    
    src/tabla_isr.py
        → TablaISRMensual con tabla 2026
        → calcular_isr_desde_ingreso_mensual()
        → agregar_tabla() para años futuros
    
    src/calculadora_v2.py
        → CalculadoraCETESV2 (hereda de CalculadoraCETES)
        → ComparadorEscenariosPorIngresos
        → proyectar_multiples_ingresos()
    
    main_variation1.py
        → Menú interactivo con 6 opciones
        → Calcular con ingreso mensual
        → Ver tabla ISR vigente
        → Comparar diferentes ingresos
        → Proyectar múltiples niveles
    
    ejemplos_variation1.py
        → 7 ejemplos completos
        → Explicación de cálculo
        → Resultados para diferentes ingresos
    
    src/__init__.py
        → Actualizado con nuevas clases
    
    ═══════════════════════════════════════════════════════════════════
    CÓMO USAR:
    ═══════════════════════════════════════════════════════════════════
    
    # Menú interactivo
    python main_variation1.py
    
    # Ver ejemplos
    python ejemplos_variation1.py
    
    # Usar en código
    from src.calculadora_v2 import CalculadoraCETESV2
    
    calc = CalculadoraCETESV2(
        capital=250000,
        tasa_cetes=0.0719,
        tasa_inflacion=0.0411,
        ingreso_bruto_mensual=35000,  # ← Automáticamente calcula ISR
        ano=2026
    )
    print(calc.resumen_texto_detallado())
    
    ═══════════════════════════════════════════════════════════════════
    PROTECCIÓN DE RAMA:
    ═══════════════════════════════════════════════════════════════════
    
    Esta rama debe protegerse para evitar cambios accidentales.
    
    Requisitos recomendados:
    • Pull Request requerido antes de fusionar
    • Revisión de código (1+ aprobadores)
    • Tests deben pasar
    • Rama debe estar actualizada
    • No permitir pushes directo a la rama
    
    Ver BRANCH_PROTECTION.py para instrucciones.
    
    ═══════════════════════════════════════════════════════════════════
    """)

if __name__ == "__main__":
    mostrar_informacion()
