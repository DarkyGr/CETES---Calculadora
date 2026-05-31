# 🚀 GUÍA DE USO RÁPIDA - CALCULADORA DE CETES

¡Bienvenido! Esta guía te ayudará a empezar en 5 minutos.

## 📱 Forma Más Rápida (Recomendada)

### Opción A: Menú Interactivo (Más Fácil)

```bash
python main.py
```

Se abrirá un menú donde puedes:

- ✅ Calcular tu inversión
- ✅ Comparar tasas ISR
- ✅ Proyectar años futuros
- ✅ Analizar sensibilidad
- ✅ Exportar a CSV

### Opción B: Ejemplos Ejecutables

```bash
python ejemplos.py
```

Muestra 7 ejemplos completos con datos reales.

### Opción C: Inicio Rápido

```bash
python INICIO_RAPIDO.py
```

6 formas diferentes de usarla con una línea de código.

## 💻 Uso en Python

### Ejemplo 1: Cálculo Rápido (3 líneas)

```python
from src.calculadora import CalculadoraCETES

calc = CalculadoraCETES(250000, 0.0719, 0.0411, tasa_isr=0.15)
print(calc.calcular())  # Retorna diccionario con todos los datos
```

### Ejemplo 2: Con Formato Bonito

```python
from src.calculadora import CalculadoraCETES

calc = CalculadoraCETES(250000, 0.0719, 0.0411, tasa_isr=0.15)
calc.calcular()
print(calc.resumen_texto())  # Imprime tabla formateada
```

### Ejemplo 3: Comparar 3 Tasas ISR

```python
from src.comparador import ComparadorEscenarios

comp = ComparadorEscenarios()
resultados = comp.comparar_por_tasa_isr(250000, 0.0719, 0.0411)
# Retorna {'10%': {...}, '15%': {...}, '21%': {...}}
```

### Ejemplo 4: Proyectar 5 Años

```python
proyecciones = comp.proyectar_multiples_anos(250000, 0.0719, 0.0411, 0.15, anos=5)
# Retorna lista con resultados por cada año
```

### Ejemplo 5: Exportar a CSV

```python
from src.exportador import ExportadorCSV

exportador = ExportadorCSV("./output")
exportador.exportar_resultado(resultado, "mi_inversion")
```

## 🧪 Tests y Validación

```bash
# Ejecutar tests (debe pasar todos)
python tests/test_calculadora.py

# Resultado esperado: OK (16 tests)
```

## 📊 Interpretación de Resultados

| Campo                 | Significado                        |
| --------------------- | ---------------------------------- |
| **Rendimiento Bruto** | Lo que ganas sin restar nada       |
| **Efecto Inflación**  | Pérdida de poder adquisitivo       |
| **Interés Real**      | Ganancia real después de inflación |
| **Saldo a Favor**     | Lo que te devuelven en declaración |
| **Ganancia Neta**     | Lo que realmente conservas         |

## 🎯 Casos de Uso Típicos

### Caso 1: Solo quiero saber mi ganancia neta

```python
from src.calculadora import CalculadoraCETES
calc = CalculadoraCETES(250000, 0.0719, 0.0411, tasa_isr=0.15)
print(f"Ganancia: ${calc.calcular()['ganancia_neta']:,.2f}")
```

### Caso 2: Quiero ver si me devuelven dinero en impuestos

```python
resultado = calc.calcular()
saldo = resultado['saldo_a_favor'] - resultado['saldo_a_pagar']
if saldo > 0:
    print(f"✅ Te devolverán: ${saldo:,.2f}")
else:
    print(f"⚠️ Deberás pagar: ${abs(saldo):,.2f}")
```

### Caso 3: Quiero comparar diferentes tasas ISR

```python
from src.comparador import ComparadorEscenarios
comp = ComparadorEscenarios()
resultados = comp.comparar_por_tasa_isr(250000, 0.0719, 0.0411)
for tasa, res in resultados.items():
    print(f"ISR {tasa}: Ganancias ${res['ganancia_neta']:,.2f}")
```

### Caso 4: Quiero ver cómo crecerá mi dinero en 5 años

```python
proyecciones = comp.proyectar_multiples_anos(250000, 0.0719, 0.0411, 0.15, anos=5)
print(f"Inicio: $250,000")
print(f"Después de 5 años: ${proyecciones[-1]['capital_final']:,.2f}")
```

## 📂 Estructura de Archivos

```
├── main.py                    ← Ejecuta esto para menú interactivo
├── ejemplos.py                ← Ejemplos completos (ejecutar)
├── INICIO_RAPIDO.py           ← Ejemplos básicos
├── README.md                  ← Documentación completa
├── requirements.txt           ← Dependencias (ninguna)
├── src/
│   ├── calculadora.py         ← Lógica principal
│   ├── exportador.py          ← Exportar a CSV
│   └── comparador.py          ← Comparativas y proyecciones
├── tests/
│   └── test_calculadora.py    ← Tests unitarios
└── output/                    ← Archivos CSV generados aquí
```

## ⚡ Atajos en VS Code

1. **F5** → Ejecuta el archivo actual
2. **Ctrl+Shift+D** → Panel de Debug
3. Selecciona "Python: Main (Interactivo)" en la lista
4. **F5** → Comienza menú interactivo

## ❓ Preguntas Frecuentes

### P: ¿Necesito instalar algo?

R: No, solo Python 3.6+. Sin dependencias externas.

### P: ¿Cómo sé si me devuelven dinero?

R: Busca "Saldo a Favor" en los resultados. Si es positivo, ¡te devuelven!

### P: ¿Qué es el "Interés Real"?

R: Tu ganancia después de restar la inflación. Es lo que realmente ganas en poder adquisitivo.

### P: ¿Puedo proyectar más de 5 años?

R: Sí, cambia el parámetro `anos=10` (o el número que quieras).

### P: ¿Dónde se guardan los CSV?

R: En la carpeta `./output/` del proyecto.

## 🆘 Si Algo Falla

1. Verifica que estés en la carpeta correcta: `cd "/Code/Python/CETES - Calculadora"`
2. Ejecuta los tests: `python tests/test_calculadora.py`
3. Si pasan, el programa funciona bien
4. Revisa el README.md para información más detallada

## 📖 Siguiente Paso

- Lee **README.md** para documentación completa
- Ejecuta **main.py** para el menú interactivo
- Ejecuta **ejemplos.py** para ver casos reales

---

¡Listo! Ya puedes empezar a usar la calculadora. 🎉
