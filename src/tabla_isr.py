#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tablas de ISR Mensual por año en México.
Proporciona tasas de ISR basadas en ingresos brutos mensuales.
"""

from datetime import datetime


class TablaISRMensual:
    """Gestiona las tablas de ISR mensual por año."""
    
    # Tabla ISR Mensual 2026 (Provisional)
    # Formato: (limite_inferior, limite_superior, cuota_fija, porcentaje_excedente)
    TABLA_ISR_2026 = [
        (0.01, 844.59, 0.00, 0.0192),
        (844.60, 7168.51, 16.22, 0.0640),
        (7168.52, 12598.02, 420.95, 0.1088),
        (12598.03, 14644.64, 1011.68, 0.1600),
        (14644.65, 17533.63, 1339.14, 0.1792),
        (17533.64, 35362.83, 1856.84, 0.2136),
        (35362.84, 55736.68, 5665.16, 0.2352),
        (55736.69, 106410.50, 10457.09, 0.3000),
        (106410.51, 141880.66, 25659.23, 0.3200),
        (141880.67, 425641.99, 37009.69, 0.3400),
        (425642.00, float('inf'), 133488.54, 0.3500),
    ]
    
    # Tablas para otros años (estructura para agregar fácilmente)
    TABLAS_ISR = {
        2026: TABLA_ISR_2026,
        # 2025: [...],  # Se agregaría cuando esté disponible
        # 2024: [...],  # Se agregaría cuando esté disponible
    }
    
    @staticmethod
    def obtener_tabla(ano=None):
        """
        Obtiene la tabla de ISR para un año específico.
        
        Args:
            ano (int, optional): Año de la tabla. Por default, año actual.
        
        Returns:
            list: Tabla de ISR para el año especificado
        
        Raises:
            ValueError: Si el año no tiene tabla disponible
        """
        if ano is None:
            ano = datetime.now().year
        
        if ano not in TablaISRMensual.TABLAS_ISR:
            anos_disponibles = ", ".join(map(str, sorted(TablaISRMensual.TABLAS_ISR.keys())))
            raise ValueError(
                f"Tabla de ISR para {ano} no disponible. "
                f"Años disponibles: {anos_disponibles}"
            )
        
        return TablaISRMensual.TABLAS_ISR[ano]
    
    @staticmethod
    def calcular_isr_desde_ingreso_mensual(ingreso_bruto_mensual, ano=None):
        """
        Calcula la tasa ISR basada en el ingreso mensual bruto.
        
        Args:
            ingreso_bruto_mensual (float): Ingreso bruto mensual en MXN
            ano (int, optional): Año de cálculo (default año actual)
        
        Returns:
            dict: Contiene:
                - 'ingreso': Ingreso bruto mencionado
                - 'limite_inferior': Límite inferior del tramo
                - 'limite_superior': Límite superior del tramo
                - 'cuota_fija': Cuota fija del tramo
                - 'porcentaje_excedente': Porcentaje a aplicar al excedente
                - 'tasa_isr': Tasa ISR a usar para cálculos
        
        Raises:
            ValueError: Si ingreso es inválido
        """
        if ingreso_bruto_mensual <= 0:
            raise ValueError("El ingreso bruto mensual debe ser mayor a 0")
        
        tabla = TablaISRMensual.obtener_tabla(ano)
        
        # Buscar el tramo correcto
        for limite_inf, limite_sup, cuota_fija, porcentaje_excedente in tabla:
            if limite_inf <= ingreso_bruto_mensual <= limite_sup:
                return {
                    'ingreso': ingreso_bruto_mensual,
                    'ano': ano or datetime.now().year,
                    'limite_inferior': limite_inf,
                    'limite_superior': limite_sup,
                    'cuota_fija': cuota_fija,
                    'porcentaje_excedente': porcentaje_excedente,
                    'tasa_isr': porcentaje_excedente,  # Para compatibilidad con CalculadoraCETES
                }
        
        # No debe llegar aquí si la tabla está bien formada
        raise ValueError(f"Ingreso ${ingreso_bruto_mensual:,.2f} fuera de rango")
    
    @staticmethod
    def obtener_ano_tabla_actual():
        """Retorna el año actual disponible en las tablas."""
        ano_actual = datetime.now().year
        anos_disponibles = sorted(TablaISRMensual.TABLAS_ISR.keys())
        
        if ano_actual in TablaISRMensual.TABLAS_ISR:
            return ano_actual
        
        # Retorna el año más reciente disponible
        return anos_disponibles[-1] if anos_disponibles else None
    
    @staticmethod
    def listar_anos_disponibles():
        """Retorna lista de años con tablas disponibles."""
        return sorted(TablaISRMensual.TABLAS_ISR.keys())
    
    @staticmethod
    def agregar_tabla(ano, tabla_isr):
        """
        Agrega una nueva tabla de ISR para un año.
        
        Args:
            ano (int): Año de la tabla
            tabla_isr (list): Lista de tuplas (limite_inf, limite_sup, cuota_fija, porcentaje)
        """
        TablaISRMensual.TABLAS_ISR[ano] = tabla_isr
    
    @staticmethod
    def resumen_tabla(ano=None):
        """Retorna un resumen en texto de la tabla ISR."""
        tabla = TablaISRMensual.obtener_tabla(ano)
        ano = ano or datetime.now().year
        
        lineas = [
            f"\n📊 TABLA DE ISR MENSUAL {ano}",
            "="*90,
            f"{'Límite Inferior':<18} {'Límite Superior':<18} {'Cuota Fija':<15} {'% Excedente':<15}",
            "-"*90
        ]
        
        for limite_inf, limite_sup, cuota_fija, porcentaje in tabla:
            if limite_sup == float('inf'):
                limite_sup_str = "En adelante"
            else:
                limite_sup_str = f"${limite_sup:>12,.2f}"
            
            lineas.append(
                f"${limite_inf:>14,.2f}  {limite_sup_str:<17}  ${cuota_fija:>11,.2f}  {porcentaje*100:>12.2f}%"
            )
        
        return "\n".join(lineas)
