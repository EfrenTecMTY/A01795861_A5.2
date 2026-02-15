"""
computeSales.py - Sistema de Cálculo de Ventas

Procesa archivos JSON de catálogo de precios y registro de ventas para
generar reportes estadísticos de ventas.

Uso:
    python computeSales.py priceCatalogue.json salesRecord.json

Autor: Efren
Fecha: 2026-02-15
"""
import json
import os
import sys
import time

# CONSTANTE GLOBAL al inicio del archivo
ANCHO_LINEA = 80  # Cantidad de símbolos "=" para delimitar secciones
# Claves requeridas en cada producto del catálogo
CLAVES_REQUERIDAS_CAT = {
    'title', 'type', 'description', 'filename',
    'height', 'width', 'price', 'rating'
}
# Claves requeridas en cada transacción de venta
CLAVES_REQUERIDAS_VTAS = {'SALE_ID', 'SALE_Date', 'Product', 'Quantity'}

def main():
    """
    Punto de entrada principal del programa.
    
    Orquesta el flujo completo: validación de parámetros, validación de archivos,
    procesamiento de datos y generación de reportes.
    
    Procesos:
        1. Valida argumentos de línea de comandos
        2. Valida existencia de archivos de entrada
           2.1 Carga la información que es válida de los archivos 
        4. Genera las ventas
        5. Imprime reporte en pantalla
        5. Guarda resultados en archivo nombrado como SalesResults.txt
    """
    validar_num_params()
    
    tiempo_inicio = time.time()
    
    archivo_catalogo, catalogo = validar_archivo_catalogo()
    archivo_vtas, vtas = validar_archivo_vtas()
    

    # Calcular tiempo transcurrido
    tiempo_fin = time.time()
    tiempo_ejecucion = tiempo_fin - tiempo_inicio

    # Imprimir en pantalla de la consola
    # imprimir_reporte_vtas(estadisticas,tiempo_ejecucion)
    # Guardar en archivo
    # guardar_reporte_vtas(estadisticas,tiempo_ejecucion)


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
    en el sistema. Valida también el formato JSON, el esquema del catálogo y
    realiza la carga de la información.
    
    Returns:
        str: Ruta del archivo de catálogo validado.
        
    Raises:
        SystemExit: Si el archivo no existe.
    """
    archivo = sys.argv[1]
    existe_archivo(archivo)
    
    datos = cargar_catalogo(archivo)

    return archivo, datos


def validar_archivo_vtas():
    """
    Valida la existencia del archivo de registro de ventas.
    
    Verifica que el archivo especificado en el segundo argumento exista
    en el sistema. Valida también el formato JSON, el esquema del catálogo y
    realiza la carga de la información.
    
    Returns:
        str: Ruta del archivo de ventas validado.
        
    Raises:
        SystemExit: Si el archivo no existe.
    """
    archivo = sys.argv[2]
    existe_archivo(archivo)
    
    datos = cargar_ventas(archivo)

    return archivo, datos


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


def cargar_catalogo(nombre_archivo):
    """
    Carga y valida todos los productos del catálogo.
    
    Procesa el archivo JSON completo validando cada producto individual.
    Los productos con errores se reportan en consola pero el procesamiento
    continúa. Solo se incluyen productos válidos en el resultado.
    
    Args:
        nombre_archivo (str): Ruta del archivo JSON de catálogo.
    
    Returns:
        list: Lista de productos válidos cargados del catálogo.
    
    Raises:
        SystemExit: Si el archivo no puede ser leído o parseado como JSON.
    """
    print(f"\nCargando catálogo desde '{nombre_archivo}'...")
    
    # Abrir archivo
    try:
        archivo = open(nombre_archivo, 'r', encoding='utf-8')
    except Exception as e:
        print(f"Error: No se pudo abrir el archivo '{nombre_archivo}'")
        print(f"Detalle: {e}")
        sys.exit(1)
    
    # Cargar información validando la calidad de cada registro
    try:
        # Parsear JSON completo
        datos = json.load(archivo)
        
        # Validar que sea array
        if not isinstance(datos, list):
            print("Error: El catálogo debe ser un array de productos.")
            archivo.close()
            sys.exit(1)
        
        productos_validos = []
        productos_con_error = 0
        
        # Procesar cada producto
        for indice, producto in enumerate(datos, start=1):
            try:
                # Validar que sea un diccionario
                if not isinstance(producto, dict):
                    raise ValueError(
                        f"El elemento debe ser un objeto JSON, "
                        f"se encontró: {type(producto).__name__}"
                    )
                
                # Validar claves requeridas
                claves_encontradas = set(producto.keys())
                claves_faltantes = CLAVES_REQUERIDAS_CAT - claves_encontradas
                
                if claves_faltantes:
                    raise ValueError(
                        f"Faltan claves requeridas: "
                        f"{', '.join(sorted(claves_faltantes))}"
                    )
                
                # Validar tipos de datos
                _validar_tipos_producto(producto)
                
                # Producto válido - agregarlo a la lista
                productos_validos.append(producto)
                
            except ValueError as e:
                # Reportar error pero continuar procesando
                productos_con_error += 1
                print(f"  Advertencia: Error en producto #{indice}: {e}")
                print(f"    Producto ignorado: {producto}")
        
        # Resumen de carga
        print("\nResumen de carga del catálogo:")
        print(f"  Productos válidos cargados: {len(productos_validos)}")
        if productos_con_error > 0:
            print(f"  Productos con errores (ignorados): {productos_con_error}")
        
        # Validar que haya al menos un producto válido
        if len(productos_validos) == 0:
            print("\nError: No se encontraron productos válidos en el catálogo.")
            archivo.close()
            sys.exit(1)
        
    except json.JSONDecodeError as e:
        print("Error: El archivo no contiene JSON válido.")
        print(f"Detalle: {e}")
        archivo.close()
        sys.exit(1)
    except Exception as e:
        print(f"Error inesperado al procesar el catálogo: {e}")
        archivo.close()
        sys.exit(1)
    
    # Cerrar el archivo del catálogo
    archivo.close()
    
    return productos_validos


def cargar_ventas(nombre_archivo):
    """
    Carga y valida todas las transacciones de ventas.
    
    Procesa el archivo JSON completo validando cada transacción individual.
    Las transacciones con errores se reportan en consola pero el procesamiento
    continúa. Solo se incluyen transacciones válidas en el resultado.
    
    Args:
        nombre_archivo (str): Ruta del archivo JSON de ventas.
    
    Returns:
        list: Lista de transacciones válidas cargadas del registro.
    
    Raises:
        SystemExit: Si el archivo no puede ser leído o parseado como JSON.
    """
    print(f"\nCargando registro de ventas desde '{nombre_archivo}'...")
    
    # Abrir archivo
    try:
        archivo = open(nombre_archivo, 'r', encoding='utf-8')
    except Exception as e:
        print(f"Error: No se pudo abrir el archivo '{nombre_archivo}'")
        print(f"Detalle: {e}")
        sys.exit(1)
    
    # Cargar información validando la calidad de cada registro
    try:
        # Parsear JSON completo
        datos = json.load(archivo)
        
        # Validar que sea array
        if not isinstance(datos, list):
            print("Error: El registro de ventas debe ser un array de transacciones.")
            archivo.close()
            sys.exit(1)
        
        ventas_validas = []
        ventas_con_error = 0
        
        # Procesar cada transacción
        for indice, venta in enumerate(datos, start=1):
            try:
                # Validar que sea un diccionario
                if not isinstance(venta, dict):
                    raise ValueError(
                        f"El elemento debe ser un objeto JSON, "
                        f"se encontró: {type(venta).__name__}"
                    )
                
                # Validar claves requeridas
                claves_encontradas = set(venta.keys())
                claves_faltantes = CLAVES_REQUERIDAS_VTAS - claves_encontradas
                
                if claves_faltantes:
                    raise ValueError(
                        f"Faltan claves requeridas: "
                        f"{', '.join(sorted(claves_faltantes))}"
                    )
                
                # Validar tipos de datos
                _validar_tipos_venta(venta)
                
                # Transacción válida - agregarla a la lista
                ventas_validas.append(venta)
                
            except ValueError as e:
                # Reportar error pero continuar procesando
                ventas_con_error += 1
                print(f"  Advertencia: Error en transacción #{indice}: {e}")
                print(f"    Transacción ignorada: {venta}")
        
        # Resumen de carga
        print("\nResumen de carga del registro de ventas:")
        print(f"  Transacciones válidas cargadas: {len(ventas_validas)}")
        if ventas_con_error > 0:
            print(f"  Transacciones con errores (ignoradas): {ventas_con_error}")
        
        # Validar que haya al menos una transacción válida
        if len(ventas_validas) == 0:
            print("\nError: No se encontraron transacciones válidas en el archivo "
                  " de las ventas.")
            archivo.close()
            sys.exit(1)
        
    except json.JSONDecodeError as e:
        print("Error: El archivo no contiene JSON válido.")
        print(f"Detalle: {e}")
        archivo.close()
        sys.exit(1)
    except Exception as e:
        print(f"Error inesperado al procesar las ventas: {e}")
        archivo.close()
        sys.exit(1)
    
    # Cerrar el archivo del catálogo
    archivo.close()
    
    return ventas_validas


def _validar_tipos_producto(producto):
    """
    Valida que los tipos de datos del producto sean correctos.
    
    Args:
        producto (dict): Diccionario con los datos del producto.
        
    Raises:
        ValueError: Si algún campo tiene un tipo de dato incorrecto.
    """
    # Validar campos de texto
    campos_texto = ['title', 'type', 'description', 'filename']
    for campo in campos_texto:
        if not isinstance(producto[campo], str):
            raise ValueError(
                f"El campo '{campo}' debe ser texto. "
                f"Se encontró: {type(producto[campo]).__name__}"
            )
    
    # Validar dimensiones (enteros)
    if not isinstance(producto['height'], int):
        raise ValueError(
            f"El campo 'height' debe ser entero. "
            f"Se encontró: {type(producto['height']).__name__}"
        )
    
    if not isinstance(producto['width'], int):
        raise ValueError(
            f"El campo 'width' debe ser entero. "
            f"Se encontró: {type(producto['width']).__name__}"
        )
    
    # Validar precio (número: int o float)
    if not isinstance(producto['price'], (int, float)):
        raise ValueError(
            f"El campo 'price' debe ser numérico. "
            f"Se encontró: {type(producto['price']).__name__}"
        )
    
    # Validar rating (entero)
    if not isinstance(producto['rating'], int):
        raise ValueError(
            f"El campo 'rating' debe ser entero. "
            f"Se encontró: {type(producto['rating']).__name__}"
        )


def _validar_tipos_venta(venta):
    """
    Valida que los tipos de datos de la transacción sean correctos.
    
    Args:
        venta (dict): Diccionario con los datos de la transacción.
        
    Raises:
        ValueError: Si algún campo tiene un tipo de dato incorrecto.
    """
    # Validar SALE_ID (entero)
    if not isinstance(venta['SALE_ID'], int):
        raise ValueError(
            f"El campo 'SALE_ID' debe ser entero. "
            f"Se encontró: {type(venta['SALE_ID']).__name__}"
        )
    
    # Validar SALE_Date (texto en formato de fecha)
    if not isinstance(venta['SALE_Date'], str):
        raise ValueError(
            f"El campo 'SALE_Date' debe ser texto. "
            f"Se encontró: {type(venta['SALE_Date']).__name__}"
        )
    
    # Validar Product (texto)
    if not isinstance(venta['Product'], str):
        raise ValueError(
            f"El campo 'Product' debe ser texto. "
            f"Se encontró: {type(venta['Product']).__name__}"
        )
    
    # Validar Quantity (entero)
    if not isinstance(venta['Quantity'], int):
        raise ValueError(
            f"El campo 'Quantity' debe ser entero. "
            f"Se encontró: {type(venta['Quantity']).__name__}"
        )


if __name__ == "__main__":
    main()
