"""
computeSales.py - Sistema de Cálculo de Ventas

Procesa archivos JSON de catálogo de precios y registro de ventas para
generar reportes estadísticos de ventas.

Uso:
    python computeSales.py priceCatalogue.json salesRecord.json

Autor: Efren
Fecha: 2026-02-15
"""
import os
import sys
import time

# CONSTANTE GLOBAL al inicio del archivo
ANCHO_LINEA = 80  # Cantidad de símbolos "=" para delimitar secciones

def main():
    """
    Punto de entrada principal del programa.
    
    Orquesta el flujo completo: validación de parámetros, validación de archivos,
    procesamiento de datos y generación de reportes.
    
    Procesos:
        1. Valida argumentos de línea de comandos
        2. Valida existencia de archivos de entrada
        3. Procesa datos (pendiente implementación)
        4. Genera las ventas
        5. Guarda resultados
    """
    validar_num_params()
    
    tiempo_inicio = time.time()
    
    archivo_catalogo = validar_archivo_catalogo()
    archivo_vtas = validar_archivo_vtas()
    

    #datos=obtener_datos_archivo(archivo)
    # estadisticas=generar_estadisticas(datos)

    # # Calcular tiempo transcurrido
    # tiempo_fin = time.time()
    # tiempo_ejecucion = tiempo_fin - tiempo_inicio

    # # Imprimir en pantalla de la consola
    # imprimir_estadisticas(estadisticas,tiempo_ejecucion)
    # # Guardar en archivo
    # guardar_estadisticas(estadisticas,tiempo_ejecucion)


def validar_num_params():
    """
    Valida que se hayan proporcionado los parámetros requeridos.
    
    El programa requiere dos argumentos: archivo de catálogo y archivo de ventas.
    Si faltan parámetros, muestra el uso correcto y termina la ejecución.
    
    Raises:
        SystemExit: Si no se proporcionan exactamente 2 parámetros.
    """
    if len(sys.argv) < 3:
        print("Error: Faltan parámetros para la correcta ejecución del programa.")
        print("Uso: python computeSales.py priceCatalogue.json salesRecord.json")
        sys.exit(1)


def validar_archivo_catalogo():
    """
    Valida la existencia del archivo de catálogo de precios.
    
    Verifica que el archivo especificado en el primer argumento exista
    en el sistema. En futuras versiones validará también el formato JSON
    y el esquema del catálogo.
    
    Returns:
        str: Ruta del archivo de catálogo validado.
        
    Raises:
        SystemExit: Si el archivo no existe.
    """
    filename = sys.argv[1]
    existe_archivo(filename)

    return filename


def validar_archivo_vtas():
    """
    Valida la existencia del archivo de registro de ventas.
    
    Verifica que el archivo especificado en el segundo argumento exista
    en el sistema. En futuras versiones validará también el formato JSON
    y consistencia de datos de ventas.
    
    Returns:
        str: Ruta del archivo de ventas validado.
        
    Raises:
        SystemExit: Si el archivo no existe.
    """
    filename = sys.argv[2]
    existe_archivo(filename)

    return filename


def existe_archivo(archivo):
    """
    Verifica la existencia de un archivo en el sistema.
    
    Si el archivo no existe, muestra un mensaje de error descriptivo
    y termina la ejecución del programa.
    
    Args:
        archivo (str): Ruta del archivo a validar.
        
    Raises:
        SystemExit: Si el archivo especificado no existe en la ruta proporcionada.
    """
    if not os.path.exists(archivo):
        print(f"Error: El archivo '{archivo}' especificado no existe.")
        print("Verifique la ruta y vuelva a intentar.")
        sys.exit(1)


if __name__ == "__main__":
    main()
