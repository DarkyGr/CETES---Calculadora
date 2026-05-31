# Calculadora de CETES - Instrucciones de Copilot

## Descripción del Proyecto

Herramienta completa en Python para calcular impuestos, rendimientos y proyecciones de inversiones en CETES (Certificados de la Tesorería) de México.

## Características Principales

- ✅ Cálculo de retención provisional y impuesto definitivo
- ✅ Análisis comparativo de diferentes escenarios
- ✅ Proyecciones multi-año
- ✅ Análisis de sensibilidad
- ✅ Exportación a CSV

## Stack Tecnológico

- **Lenguaje**: Python 3.6+
- **Dependencias**: None (solo librerías estándar)
- **Módulos**: calculadora, exportador, comparador

## Estructura del Código

```
src/
├── calculadora.py      # CalculadoraCETES (clase principal)
├── exportador.py       # ExportadorCSV (exportación)
├── comparador.py       # ComparadorEscenarios, AnalizadorSensibilidad
└── __init__.py         # Inicializador del paquete

main.py                 # Interfaz interactiva
tests/
└── test_calculadora.py # Tests unitarios
```

## Reglas de Desarrollo

1. **Nomenclatura**: Usar español para comentarios y documentación, inglés en código
2. **Documentación**: Todas las funciones deben tener docstrings
3. **Tests**: Agregar tests para nuevas funcionalidades
4. **Formato**: Seguir PEP 8 (máximo 100 caracteres por línea)
5. **Validación**: Validar parámetros al inicializar calculadoras

## Cómo Ejecutar

### Modo Interactivo
```bash
python main.py
```

### Tests
```bash
python tests/test_calculadora.py
```

### Uso Programático
```python
from src.calculadora import CalculadoraCETES

calc = CalculadoraCETES(250000, 0.0719, 0.0411, tasa_isr=0.15)
resultado = calc.calcular()
print(calc.resumen_texto())
```

## Clases Principales

### CalculadoraCETES
- Métodos: `calcular()`, `obtener_resultado()`, `resumen_texto()`
- Parámetros: capital, tasa_cetes, tasa_inflacion, tasa_isr

### ExportadorCSV
- Métodos: `exportar_resultado()`, `exportar_comparativa()`

### ComparadorEscenarios
- Métodos: `comparar_por_tasa_isr()`, `proyectar_multiples_anos()`

### AnalizadorSensibilidad
- Métodos: `variar_tasa_cetes()`, `variar_inflacion()`

## Convenciones de Código

- Constantes en MAYÚSCULAS (ej: TASA_RETENCION_DEFECTO)
- Métodos privados comienzan con `_`
- Resultados se retornan como diccionarios
- Excepciones: ValueError para parámetros inválidos

## Nuevas Funcionalidades Sugeridas

1. Exportar a Excel con gráficos
2. API REST para consultas remotas
3. Interfaz gráfica (Tkinter o PyQt)
4. Integración con bases de datos
5. Soporte para otras inversiones financieras

## Pruebas

Ejecutar tests regularmente:
```bash
python tests/test_calculadora.py -v
```

Coverage esperado: >90% del código principal

## Notas Importantes

- La retención provisional es 0.90% del capital
- El cálculo del interés real resta inflación al rendimiento bruto
- Las tasas ISR válidas son: 10%, 15%, 21%
- El SAT devolverá la diferencia si la retención excede el impuesto
