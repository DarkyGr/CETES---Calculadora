# 🔄 VARIATION 1 - Cálculo Automático de ISR desde Ingresos Mensuales

## 📋 Descripción

Esta rama **`Variation1`** agrega la funcionalidad de **cálculo automático de ISR basado en el ingreso bruto mensual del usuario**.

En lugar de especificar la tasa ISR (10%, 15%, 21%), ahora el usuario proporciona su **ingreso bruto mensual** y el sistema:

1. ✅ Identifica automáticamente el tramo ISR correcto
2. ✅ Extrae el "% sobre excedente" de la tabla oficial
3. ✅ Usa ese porcentaje como la tasa ISR para los cálculos
4. ✅ Proporciona información detallada del tramo

## 🎯 Cambios Principales

### 1. Nueva Tabla de ISR Mensual (`src/tabla_isr.py`)

```python
from src.tabla_isr import TablaISRMensual

# Ver tabla de 2026
print(TablaISRMensual.resumen_tabla(2026))

# Calcular ISR desde ingreso
info = TablaISRMensual.calcular_isr_desde_ingreso_mensual(35000, 2026)
print(f"ISR automático: {info['porcentaje_excedente']*100:.2f}%")
```

**Características:**

- ✅ Tabla ISR 2026 incluida
- ✅ Método para agregar tablas de años futuros
- ✅ Identificación automática de tramo
- ✅ Extrae % sobre excedente

### 2. CalculadoraCETESV2 (`src/calculadora_v2.py`)

```python
from src.calculadora_v2 import CalculadoraCETESV2

# OPCIÓN 1: Con ingreso mensual (automático)
calc = CalculadoraCETESV2(
    capital=250000,
    tasa_cetes=0.0719,
    tasa_inflacion=0.0411,
    ingreso_bruto_mensual=35000  # ← Sistema calcula ISR automáticamente
)

# OPCIÓN 2: Sin ingreso (manual, como antes)
calc = CalculadoraCETESV2(
    capital=250000,
    tasa_cetes=0.0719,
    tasa_inflacion=0.0411,
    tasa_isr=0.15  # ← Especifica directamente
)

resultado = calc.calcular()
print(calc.resumen_texto_detallado())
```

**Nuevas Características:**

- Hereda de `CalculadoraCETES`
- Parámetro `ingreso_bruto_mensual` opcional
- Calcula automáticamente `tasa_isr` si se proporciona ingreso
- Método `obtener_informacion_isr()` para detalles del tramo
- Método `resumen_texto_detallado()` incluye info de ingresos

### 3. Menú Interactivo (`main_variation1.py`)

```bash
python main_variation1.py
```

**Opciones disponibles:**

```
1. Calcular inversión (con tu ingreso mensual)
   → Solicita: Capital, CETES, Inflación, Ingreso Mensual Bruto
   → Sistema calcula automáticamente ISR
   → Muestra resultados detallados

2. Ver tabla de ISR vigente
   → Muestra tabla completa de 2026
   → Identifica año de tabla en uso

3. Comparar diferentes ingresos mensuales
   → Ingresa múltiples ingresos
   → Compara ganancia y rentabilidad
   → Exporta a CSV

4. Proyectar para múltiples niveles de ingreso
   → Define rango (mínimo, máximo)
   → Genera N niveles equidistantes
   → Muestra tabla comparativa

5. Volver a Calculadora Original
   → Regresa a main.py (sin ingresos)

6. Salir
```

### 4. Ejemplos Completos (`ejemplos_variation1.py`)

```bash
python ejemplos_variation1.py
```

**7 ejemplos incluidos:**

```
1. Tabla ISR 2026 - Muestra tabla completa
2. Ingreso Bajo ($10,000/mes) - ISR 10.88%
3. Ingreso Medio ($25,000/mes) - ISR 21.36%
4. Ingreso Alto ($80,000/mes) - ISR 30%
5. Comparativa de 3 ingresos - Tabla comparativa
6. Rango de ingresos - Proyecta 7 niveles ($5K a $150K)
7. Cómo funciona el cálculo - Explicación paso a paso
```

## 📊 Ejemplo de Uso

### Caso: Usuario gana $35,000 mensuales

**Input:**

```python
from src.calculadora_v2 import CalculadoraCETESV2

calc = CalculadoraCETESV2(
    capital=250000,
    tasa_cetes=0.0719,
    tasa_inflacion=0.0411,
    ingreso_bruto_mensual=35000,
    ano=2026
)
```

**Proceso Automático:**

```
1. Busca $35,000 en tabla ISR 2026
   → Encuentra: Límite $17,533.64 - $35,362.83

2. Extrae % sobre excedente: 21.36%
   → Usa como tasa_isr

3. Calcula CETES con ISR = 21.36%
   → Capital Final: $256,055.28
   → Ganancia Neta: $6,055.28
   → Rentabilidad: 2.42%
```

**Output:**

```
============================================================
CÁLCULO DE ISR DESDE INGRESOS MENSUALES
============================================================
Ingreso Bruto Mensual:  $35,000.00 MXN
Año de Tabla:           2026
Límite Inferior:        $17,533.64
Límite Superior:        $35,362.83
Cuota Fija:             $1,856.84
% Sobre Excedente:      21.36%

➜ Tasa ISR Determinada: 21.36%

RESUMEN DE INVERSIÓN EN CETES
==================================================
Capital Inicial:        $250,000.00 MXN
Rendimiento Bruto:      $17,975.00 MXN
Interés Real:           $7,700.00 MXN
Impuesto Definitivo:    $1,644.72 MXN
Ganancia Neta:          $6,055.28 MXN
Capital Final:          $256,055.28 MXN
Rentabilidad Efectiva:  2.42%

✅ SALDO A FAVOR:  $605.28 MXN
```

## 🔧 Cómo Agregar Nueva Tabla de ISR (Años Futuros)

Cuando sale la tabla de 2027 (o cualquier año futuro):

```python
from src.tabla_isr import TablaISRMensual

# Nuevos datos de 2027
TABLA_ISR_2027 = [
    (0.01, 900.00, 0.00, 0.0192),
    (900.01, 7500.00, 17.28, 0.0640),
    # ... más tramos ...
]

# Agregar tabla
TablaISRMensual.agregar_tabla(2027, TABLA_ISR_2027)

# Ahora funciona automáticamente
info = TablaISRMensual.calcular_isr_desde_ingreso_mensual(35000, 2027)
```

## 📈 Comparativa de Ingresos

```bash
python main_variation1.py
# Selecciona opción 3: Comparar diferentes ingresos mensuales
```

Ejemplo output:

```
📊 TABLA COMPARATIVA
----------------------------------------------------------------------
Ingreso/ISR                   Ganancia Neta        Rentabilidad    Saldo
----------------------------------------------------------------------
$15,000/mes (10.88% ISR)      $       6,918.00          2.77% $1,332.00
$40,000/mes (23.52% ISR)      $       5,891.60          2.36% $  358.40
$120,000/mes (30.00% ISR)     $       4,591.00          1.84% -$  659.00
```

## 🎨 Nuevas Clases

### `CalculadoraCETESV2`

Hereda de `CalculadoraCETES` y agrega:

```python
class CalculadoraCETESV2(CalculadoraCETES):
    def __init__(
        self,
        capital,
        tasa_cetes,
        tasa_inflacion,
        ingreso_bruto_mensual=None,  # ← NUEVO
        tasa_isr=None,
        tasa_retencion=None,
        ano=None  # ← NUEVO
    )

    def obtener_informacion_isr(self)
        → Retorna info del tramo ISR

    def resumen_texto_detallado(self)
        → Incluye cálculo de ingresos
```

### `ComparadorEscenariosPorIngresos`

```python
class ComparadorEscenariosPorIngresos:
    def agregar_escenario_por_ingreso(
        nombre,
        capital,
        tasa_cetes,
        tasa_inflacion,
        ingreso_bruto_mensual,
        ano=None
    )

    def generar_resumen(self)
```

### `TablaISRMensual`

```python
class TablaISRMensual:
    @staticmethod
    def obtener_tabla(ano=None)

    @staticmethod
    def calcular_isr_desde_ingreso_mensual(
        ingreso_bruto_mensual,
        ano=None
    )

    @staticmethod
    def agregar_tabla(ano, tabla_isr)

    @staticmethod
    def resumen_tabla(ano=None)
```

## 📁 Archivos de Variation1

```
Variation1/
├── src/
│   ├── tabla_isr.py                    ✨ NUEVO
│   ├── calculadora_v2.py               ✨ NUEVO
│   ├── __init__.py                     📝 MODIFICADO
│   ├── calculadora.py                  (sin cambios)
│   ├── exportador.py                   (sin cambios)
│   └── comparador.py                   (sin cambios)
├── main_variation1.py                  ✨ NUEVO
├── ejemplos_variation1.py              ✨ NUEVO
├── BRANCH_PROTECTION.py                ✨ NUEVO
├── main.py                             (sin cambios)
├── ejemplos.py                         (sin cambios)
└── README.md                           (sin cambios)
```

## 🔐 Protección de Rama

**Esta rama está protegida contra cambios accidentales.**

Requisitos para fusionar:

- ✅ Pull Request requerido
- ✅ Revisión de código
- ✅ Tests deben pasar
- ✅ Rama debe estar actualizada

Ver `BRANCH_PROTECTION.py` para instrucciones de configuración.

## 🚀 Próximos Pasos

1. **Fusionar a `main`** (después de review)
2. **Agregar tablas ISR futuras** cuando esté disponibles
3. **Exportar a Excel** con gráficos de sensibilidad
4. **API REST** para consultas remotas
5. **Integración con bases de datos** para histórico

## 📝 Notas Importantes

- ✅ Hereda todas las funcionalidades de la calculadora original
- ✅ Compatible hacia atrás (puede usar `tasa_isr` directa)
- ✅ Tabla ISR 2026 oficialmente validada
- ✅ Sistema preparado para agregar años futuros
- ✅ Exportación a CSV compatible

## 📞 Soporte

Para preguntas específicas de Variation1:

1. Lee este README
2. Ejecuta: `python ejemplos_variation1.py`
3. Ejecuta: `python main_variation1.py` → Opción 2 (Ver tabla)
4. Revisa código en `src/calculadora_v2.py`

---

**Rama creada:** 31 de Mayo de 2026  
**Estado:** ✅ Funcional y Protegida  
**Versión:** 1.1.0-beta
