#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo para exportar resultados a archivos CSV.
Permite guardar y comparar múltiples escenarios.
"""

import csv
from datetime import datetime
from pathlib import Path


class ExportadorCSV:
    """Exporta resultados de CETES a archivos CSV."""
    
    def __init__(self, directorio_salida="./output"):
        """
        Inicializa el exportador.
        
        Args:
            directorio_salida (str): Ruta donde guardar los archivos
        """
        self.directorio = Path(directorio_salida)
        self.directorio.mkdir(exist_ok=True)
    
    def exportar_resultado(self, resultados, nombre_archivo=None):
        """
        Exporta un único resultado a CSV.
        
        Args:
            resultados (dict): Diccionario con los resultados
            nombre_archivo (str): Nombre del archivo (sin extensión)
        
        Returns:
            Path: Ruta del archivo creado
        """
        if nombre_archivo is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_archivo = f"cetes_{timestamp}"
        
        ruta = self.directorio / f"{nombre_archivo}.csv"
        
        with open(ruta, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Encabezados
            writer.writerow(["INVERSIÓN EN CETES - REPORTE"])
            writer.writerow(["Fecha:", datetime.now().strftime("%d/%m/%Y %H:%M:%S")])
            writer.writerow([])
            
            # Parámetros
            writer.writerow(["PARÁMETROS DE ENTRADA"])
            writer.writerow(["Capital Inicial (MXN)", resultados['capital_inicial']])
            writer.writerow(["Tasa CETES (%)", resultados['tasa_cetes'] * 100])
            writer.writerow(["Tasa Inflación (%)", resultados['tasa_inflacion'] * 100])
            writer.writerow(["Tasa Retención (%)", resultados['tasa_retencion'] * 100])
            writer.writerow(["Tasa ISR (%)", resultados['tasa_isr'] * 100])
            writer.writerow([])
            
            # Resultados
            writer.writerow(["RESULTADOS"])
            writer.writerow(["Concepto", "Monto (MXN)"])
            
            conceptos = [
                ("Rendimiento Bruto", "rendimiento_bruto"),
                ("Efecto Inflación", "efecto_inflacion"),
                ("Interés Real Gravable", "interes_real"),
                ("Retención Provisional", "retencion_provisional"),
                ("Impuesto Definitivo", "impuesto_definitivo"),
                ("Ganancia Neta", "ganancia_neta"),
                ("Capital Final", "capital_final"),
                ("Rentabilidad Efectiva (%)", "rentabilidad_efectiva"),
            ]
            
            for concepto, clave in conceptos:
                valor = resultados[clave]
                writer.writerow([concepto, f"{valor:,.2f}"])
            
            writer.writerow([])
            writer.writerow(["DIFERENCIA FINAL"])
            if resultados['saldo_a_favor'] > 0:
                writer.writerow(["Saldo a FAVOR (MXN)", resultados['saldo_a_favor']])
            elif resultados['saldo_a_pagar'] > 0:
                writer.writerow(["Saldo a PAGAR (MXN)", resultados['saldo_a_pagar']])
            else:
                writer.writerow(["Sin diferencia", 0])
        
        return ruta
    
    def exportar_comparativa(self, lista_resultados, nombre_archivo=None):
        """
        Exporta múltiples resultados para comparación.
        
        Args:
            lista_resultados (list): Lista de diccionarios de resultados
            nombre_archivo (str): Nombre del archivo
        
        Returns:
            Path: Ruta del archivo creado
        """
        if nombre_archivo is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_archivo = f"comparativa_{timestamp}"
        
        ruta = self.directorio / f"{nombre_archivo}.csv"
        
        with open(ruta, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Encabezado
            writer.writerow(["COMPARATIVA DE INVERSIONES EN CETES"])
            writer.writerow([])
            
            # Encabezados de columnas
            encabezados = ["Escenario", "Capital", "Tasa CETES", "ISR", 
                          "Rendimiento Bruto", "Ganancia Neta", "Capital Final", 
                          "Rentabilidad %", "Saldo"]
            writer.writerow(encabezados)
            
            # Datos
            for i, resultado in enumerate(lista_resultados, 1):
                saldo = resultado['saldo_a_favor'] if resultado['saldo_a_favor'] > 0 \
                        else -resultado['saldo_a_pagar']
                
                fila = [
                    f"Escenario {i}",
                    f"{resultado['capital_inicial']:,.2f}",
                    f"{resultado['tasa_cetes'] * 100:.2f}%",
                    f"{resultado['tasa_isr'] * 100:.0f}%",
                    f"{resultado['rendimiento_bruto']:,.2f}",
                    f"{resultado['ganancia_neta']:,.2f}",
                    f"{resultado['capital_final']:,.2f}",
                    f"{resultado['rentabilidad_efectiva']:.2f}%",
                    f"{saldo:,.2f}"
                ]
                writer.writerow(fila)
        
        return ruta
    
    def obtener_ultimos_archivos(self, cantidad=5):
        """Retorna los últimos archivos generados."""
        archivos = sorted(self.directorio.glob("*.csv"), 
                         key=lambda x: x.stat().st_mtime, 
                         reverse=True)[:cantidad]
        return archivos
