# Calculadora de CETES - Inversiones en México

Una herramienta completa en Python para calcular impuestos, rendimientos y proyecciones de inversiones en **CETES** (Certificados de la Tesorería) de México.

## 🎯 Características

✅ **Cálculo Preciso de Impuestos**

- Cálculo de rendimiento bruto
- Retención provisional automática (0.90%)
- Impuesto definitivo sobre interés real (ajustado por inflación)
- Saldo a favor o a pagar

✅ **Análisis Comparativo**

- Comparación de diferentes tasas ISR (10%, 15%, 21%)
- Comparación de múltiples escenarios
- Mejor y peor escenario automático

✅ **Proyecciones Multi-Año**

- Proyectar inversión a lo largo de varios años
- Seguimiento de capital acumulado y ganancia acumulada
- Reinversión automática del capital final

✅ **Análisis de Sensibilidad**

- Variación de tasa CETES y su impacto
- Variación de inflación y su impacto
- Identificar riesgos y oportunidades

✅ **Exportación a CSV**

- Guardar resultados en archivos CSV
- Generar comparativas de múltiples escenarios
- Historial de cálculos realizados

## 📋 Requisitos

- **Python 3.6+**
- Sin dependencias externas (solo librerías estándar)

## 🚀 Instalación

### Opción 1: Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd CETES\ -\ Calculadora
```

### Opción 2: Descargar archivos

Descarga todos los archivos y colócalos en una carpeta.

## 💻 Uso

### 1. Modo Interactivo

Ejecuta el script principal con:

```bash
python main.py
```

Se te presentará un menú interactivo con opciones:

```
1. Calcular inversión única
2. Comparar diferentes tasas ISR
3. Proyectar múltiples años
4. Analizar sensibilidad de tasas
5. Salir
```

### 2. Uso Programático

```python
from src.calculadora import CalculadoraCETES

# Crear calculadora
calc = CalculadoraCETES(
    capital=250000,           # MXN
    tasa_cetes=0.0719,        # 7.19%
    tasa_inflacion=0.0411,    # 4.11%
    tasa_isr=0.15             # 15%
)

# Calcular
resultado = calc.calcular()

# Mostrar resumen
print(calc.resumen_texto())
```

### 3. Comparación de Escenarios

```python
from src.comparador import ComparadorEscenarios

comparador = ComparadorEscenarios()

# Comparar diferentes tasas ISR
resultados = comparador.comparar_por_tasa_isr(
    capital=250000,
    tasa_cetes=0.0719,
    tasa_inflacion=0.0411
)

print(comparador.generar_resumen_comparativa())
```

### 4. Proyección Multi-Año

```python
# Proyectar 5 años
proyecciones = comparador.proyectar_multiples_anos(
    capital_inicial=250000,
    tasa_cetes_anual=0.0719,
    tasa_inflacion_anual=0.0411,
    tasa_isr=0.15,
    anos=5
)

for p in proyecciones:
    print(f"Año {p['ano']}: Capital Final = ${p['capital_final']:,.2f}")
```

### 5. Análisis de Sensibilidad

```python
from src.comparador import AnalizadorSensibilidad

# Analizar cómo cambia la ganancia con variación de tasa CETES
variaciones = AnalizadorSensibilidad.variar_tasa_cetes(
    capital=250000,
    tasa_base=0.0719,
    tasa_inflacion=0.0411,
    tasa_isr=0.15,
    rango_variacion=0.02,  # ±2%
    pasos=5
)

for var in variaciones:
    print(f"Tasa: {var['tasa_variada']*100:.2f}% → Ganancia: ${var['ganancia_neta']:,.2f}")
```

### 6. Exportar a CSV

```python
from src.exportador import ExportadorCSV

exportador = ExportadorCSV("./output")

# Exportar un resultado individual
exportador.exportar_resultado(resultado, "mi_inversion")

# Exportar comparativa
exportador.exportar_comparativa(lista_de_resultados, "comparativa")
```

## 📊 Ejemplo Completo

```python
from src.calculadora import CalculadoraCETES
from src.exportador import ExportadorCSV

# Crear calculadora
calc = CalculadoraCETES(
    capital=250000,
    tasa_cetes=0.0719,
    tasa_inflacion=0.0411,
    tasa_isr=0.15
)

# Calcular
resultado = calc.calcular()

# Mostrar en pantalla
print(calc.resumen_texto())

# Exportar
exportador = ExportadorCSV()
exportador.exportar_resultado(resultado, "mi_inversion")
```

## 🔍 Interpretación de Resultados

### Campos Principales

| Campo                     | Descripción                                                    |
| ------------------------- | -------------------------------------------------------------- |
| **Rendimiento Bruto**     | Lo que ganas sin restar nada: `Capital × Tasa CETES`           |
| **Efecto Inflación**      | Pérdida de poder adquisitivo: `Capital × Tasa Inflación`       |
| **Interés Real Gravable** | Lo que realmente ganas: `Rendimiento - Inflación`              |
| **Retención Provisional** | Lo que retiene Cetesdirecto: `Capital × 0.90%`                 |
| **Impuesto Definitivo**   | Impuesto sobre interés real: `Interés Real × ISR`              |
| **Ganancia Neta**         | Lo que realmente te quedas: `Interés Real - Impuesto`          |
| **Rentabilidad Efectiva** | Porcentaje real de ganancia: `(Ganancia Neta / Capital) × 100` |
| **Saldo a Favor**         | Lo que te devuelven: `Max(0, Retención - Impuesto)`            |

### Interpretación del Saldo

- ✅ **Saldo a FAVOR**: Recibirás devolución al presentar declaración
- ⚠️ **Saldo a PAGAR**: Deberás pagar en tu declaración anual
- ➖ **Sin diferencia**: La retención fue exacta

## 🧪 Ejecutar Tests

Para validar que todo funciona correctamente:

```bash
python tests/test_calculadora.py
```

Tests incluidos:

- ✓ Cálculos correctos
- ✓ Validación de parámetros
- ✓ Casos límite
- ✓ Comparativas
- ✓ Análisis de sensibilidad

## 📁 Estructura del Proyecto

```
CETES - Calculadora/
├── main.py                          # Script principal interactivo
├── requirements.txt                 # Dependencias (none requeridas)
├── README.md                        # Este archivo
├── src/
│   ├── __init__.py                  # Inicializador del paquete
│   ├── calculadora.py               # Lógica principal de cálculos
│   ├── exportador.py                # Exportación a CSV
│   └── comparador.py                # Análisis comparativo y multi-año
├── tests/
│   └── test_calculadora.py          # Tests unitarios
├── output/                          # Archivos CSV generados
└── .github/
    └── copilot-instructions.md      # Instrucciones para Copilot
```

## 🔧 Funciones Principales

### `CalculadoraCETES`

Clase principal para realizar cálculos.

```python
calc = CalculadoraCETES(capital, tasa_cetes, tasa_inflacion, tasa_isr)
resultado = calc.calcular()
print(calc.resumen_texto())
```

### `ExportadorCSV`

Exporta resultados a archivos CSV.

```python
exportador = ExportadorCSV("./output")
exportador.exportar_resultado(resultado, "nombre")
exportador.exportar_comparativa(lista_resultados, "comparativa")
```

### `ComparadorEscenarios`

Compara múltiples escenarios y proyecta años.

```python
comparador = ComparadorEscenarios()
resultados = comparador.comparar_por_tasa_isr(...)
proyecciones = comparador.proyectar_multiples_anos(...)
```

### `AnalizadorSensibilidad`

Analiza impacto de cambios en parámetros.

```python
variaciones = AnalizadorSensibilidad.variar_tasa_cetes(...)
variaciones = AnalizadorSensibilidad.variar_inflacion(...)
```

## 📚 Referencias

Esta calculadora se basa en:

1. Tasa de retención provisional oficial de Cetesdirecto: 0.90%
2. Cálculo de interés real (rendimiento - inflación) según SAT
3. ISR aplicable según declaración anual (10%, 15%, 21%)
4. Sistema de devoluciones del SAT para retenciones excesivas

## 💡 Casos de Uso

1. **Persona Inversora Individual**: Calcula tu devolución antes de presentar declaración
2. **Asesor Financiero**: Compara escenarios para recomendaciones
3. **Investigador**: Analiza sensibilidad de variables económicas
4. **Empresa**: Proyecta inversiones tesorería a múltiples años

## 📝 Ejemplos de Resultados

```
RESUMEN DE INVERSIÓN EN CETES
==================================================
Capital Inicial:        $250,000.00 MXN
Rendimiento Bruto:      $17,975.00 MXN
Efecto Inflación:       -$10,275.00 MXN
Interés Real:           $7,700.00 MXN
Retención Provisional:  $2,250.00 MXN
Impuesto Definitivo:    $1,155.00 MXN
Ganancia Neta:          $6,545.00 MXN
Capital Final:          $256,545.00 MXN
Rentabilidad Efectiva:  2.62%

✅ SALDO A FAVOR:  $1,095.00 MXN
```

## 🤝 Contribuciones

¿Encontraste un bug o tienes sugerencias?

1. Abre un issue describiendo el problema
2. Proporciona un ejemplo reproducible
3. Sugiere una solución si tienes una

## 📄 Licencia

Este proyecto está disponible bajo licencia MIT.

## ⚠️ Disclaimer

Esta calculadora proporciona estimaciones basadas en los parámetros ingresados.
Los valores reales pueden variar según:

- Cambios en tasas oficiales de Cetesdirecto
- Cambios en las tasas ISR según ingresos totales
- Ajustes de política fiscal del SAT
- Cambios en tasas de inflación real

**Consulta siempre con un asesor fiscal antes de tomar decisiones financieras.**

## 📞 Soporte

Para preguntas o problemas:

1. Revisa la documentación en README.md
2. Ejecuta los tests: `python tests/test_calculadora.py`
3. Abre un issue en el repositorio

---

**Última actualización:** May 2026
**Versión:** 1.0.0
