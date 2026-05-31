#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo principal de cálculos para inversión en CETES.
Contiene la lógica de cálculo de impuestos y rendimientos.
"""


class CalculadoraCETES:
    """Clase para calcular impuestos y rendimientos de inversiones en CETES."""
    
    # Constantes por defecto
    TASA_RETENCION_DEFECTO = 0.0090  # 0.90% oficial de Cetesdirecto
    TASAS_ISR_VALIDAS = {
        'bajo': 0.10,      # 10%
        'medio': 0.15,     # 15%
        'alto': 0.21       # 21%
    }
    
    def __init__(self, capital, tasa_cetes, tasa_inflacion, 
                 tasa_retencion=None, tasa_isr=None):
        """
        Inicializa la calculadora con los parámetros de inversión.
        
        Args:
            capital (float): Capital invertido en MXN
            tasa_cetes (float): Tasa CETES anual (ej: 0.0719 para 7.19%)
            tasa_inflacion (float): Tasa inflación anual (ej: 0.0411 para 4.11%)
            tasa_retencion (float, optional): Tasa retención (default 0.90%)
            tasa_isr (float, optional): Tasa ISR (default 15%)
        
        Raises:
            ValueError: Si los parámetros no son válidos
        """
        self._validar_parametros(capital, tasa_cetes, tasa_inflacion, tasa_isr)
        
        self.capital = capital
        self.tasa_cetes = tasa_cetes
        self.tasa_inflacion = tasa_inflacion
        self.tasa_retencion = tasa_retencion or self.TASA_RETENCION_DEFECTO
        self.tasa_isr = tasa_isr or self.TASAS_ISR_VALIDAS['medio']
        
        self.resultados = None
    
    @staticmethod
    def _validar_parametros(capital, tasa_cetes, tasa_inflacion, tasa_isr):
        """Valida que los parámetros sean válidos."""
        if capital <= 0:
            raise ValueError("El capital debe ser mayor a 0")
        if tasa_cetes < 0:
            raise ValueError("La tasa CETES no puede ser negativa")
        if tasa_inflacion < 0:
            raise ValueError("La tasa de inflación no puede ser negativa")
        if tasa_isr and (tasa_isr < 0 or tasa_isr > 1):
            raise ValueError("La tasa ISR debe estar entre 0 y 1")
    
    def calcular(self):
        """
        Realiza todos los cálculos de la inversión.
        
        Returns:
            dict: Diccionario con todos los resultados
        """
        # Cálculos básicos
        rendimiento_bruto = self.capital * self.tasa_cetes
        retencion_provisional = self.capital * self.tasa_retencion
        efecto_inflacion = self.capital * self.tasa_inflacion
        interes_real = rendimiento_bruto - efecto_inflacion
        impuesto_definitivo = interes_real * self.tasa_isr
        diferencia = impuesto_definitivo - retencion_provisional
        
        # Ganancia neta y capital final
        ganancia_neta = interes_real - impuesto_definitivo
        capital_final = self.capital + ganancia_neta
        
        # Rentabilidad efectiva
        rentabilidad_efectiva = (ganancia_neta / self.capital) * 100
        
        self.resultados = {
            'capital_inicial': self.capital,
            'rendimiento_bruto': rendimiento_bruto,
            'retencion_provisional': retencion_provisional,
            'efecto_inflacion': efecto_inflacion,
            'interes_real': interes_real,
            'impuesto_definitivo': impuesto_definitivo,
            'diferencia': diferencia,
            'ganancia_neta': ganancia_neta,
            'capital_final': capital_final,
            'rentabilidad_efectiva': rentabilidad_efectiva,
            'tasa_cetes': self.tasa_cetes,
            'tasa_inflacion': self.tasa_inflacion,
            'tasa_isr': self.tasa_isr,
            'tasa_retencion': self.tasa_retencion,
            'saldo_a_favor': max(0, -diferencia),
            'saldo_a_pagar': max(0, diferencia)
        }
        
        return self.resultados
    
    def obtener_resultado(self, clave):
        """Obtiene un resultado específico."""
        if self.resultados is None:
            self.calcular()
        return self.resultados.get(clave, None)
    
    def resumen_texto(self):
        """Retorna un resumen en texto legible."""
        if self.resultados is None:
            self.calcular()
        
        r = self.resultados
        lineas = [
            "RESUMEN DE INVERSIÓN EN CETES",
            "=" * 50,
            f"Capital Inicial:        ${r['capital_inicial']:,.2f} MXN",
            f"Rendimiento Bruto:      ${r['rendimiento_bruto']:,.2f} MXN",
            f"Efecto Inflación:       -${r['efecto_inflacion']:,.2f} MXN",
            f"Interés Real:           ${r['interes_real']:,.2f} MXN",
            f"Retención Provisional:  ${r['retencion_provisional']:,.2f} MXN",
            f"Impuesto Definitivo:    ${r['impuesto_definitivo']:,.2f} MXN",
            f"Ganancia Neta:          ${r['ganancia_neta']:,.2f} MXN",
            f"Capital Final:          ${r['capital_final']:,.2f} MXN",
            f"Rentabilidad Efectiva:  {r['rentabilidad_efectiva']:.2f}%",
            ""
        ]
        
        if r['saldo_a_favor'] > 0:
            lineas.append(f"✅ SALDO A FAVOR:  ${r['saldo_a_favor']:,.2f} MXN")
        elif r['saldo_a_pagar'] > 0:
            lineas.append(f"⚠️  SALDO A PAGAR: ${r['saldo_a_pagar']:,.2f} MXN")
        else:
            lineas.append("➖ SIN DIFERENCIA: $0.00 MXN")
        
        return "\n".join(lineas)


def crear_calculadora(capital, tasa_cetes, tasa_inflacion, 
                      tasa_retencion=None, tasa_isr=None):
    """
    Función de conveniencia para crear y calcular en una línea.
    
    Returns:
        dict: Resultados del cálculo
    """
    calc = CalculadoraCETES(capital, tasa_cetes, tasa_inflacion, 
                           tasa_retencion, tasa_isr)
    return calc.calcular()
