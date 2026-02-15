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
        3. Procesa datos (pendiente implementación)
        4. Genera las ventas
        5. Guarda resultados
    """
    validar_num_params()
    
    tiempo_inicio = time.time()
    
    archivo_catalogo, catalogo = validar_archivo_catalogo()
    archivo_vtas, vtas = validar_archivo_vtas()
    

    #datos=obtener_datos_archivo(archivo)
    # estadisticas=generar_estadisticas(datos)

    # # Calcular tiempo transcurrido
    tiempo_fin = time.time()
    tiempo_ejecucion = tiempo_fin - tiempo_inicio

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
    archivo = sys.argv[1]
    existe_archivo(archivo)
    
    datos = validar_estructura_catalogo(archivo)

    return archivo, datos


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
    archivo = sys.argv[2]
    existe_archivo(archivo)
    
    datos = validar_estructura_ventas(archivo)

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



def validar_estructura_catalogo(nombre_archivo):
    """
    Valida que el archivo JSON de catálogo cumpla con la estructura esperada.
    
    Verifica la estructura del catálogo sin necesidad de procesar todos los
    productos. Usa validación por muestreo del primer elemento como
    representativo del esquema completo.
    
    Estructura esperada del catálogo:
        - Archivo JSON válido
        - Array de productos
        - Cada producto con claves: title, type, description, filename,
          height, width, price, rating
    
    Args:
        nombre_archivo (str): Ruta del archivo JSON de catálogo a validar.
    
    Returns:
        dict: Datos del catálogo si la validación es exitosa.
    
    Raises:
        SystemExit: Si el archivo no cumple con la estructura esperada.
        
    Note:
        La validación del primer producto es suficiente como muestra
        representativa, siguiendo el principio de eficiencia sin comprometer
        integridad de datos (práctica recomendada en validación de schemas).
    """
    
    try:
        # 1. Validar que sea JSON válido
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            datos = json.load(archivo)
            
    except json.JSONDecodeError as e:
        print(f"Error: El archivo '{nombre_archivo}' no contiene JSON válido.")
        print(f"Detalle: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error al leer el archivo '{nombre_archivo}': {e}")
        sys.exit(1)
    
    # 2. Validar que sea un array
    if not isinstance(datos, list):
        print("Error: El catálogo debe ser un array de productos.")
        print(f"Se encontró: {type(datos).__name__}")
        sys.exit(1)
    
    # 3. Validar que no esté vacío
    if len(datos) == 0:
        print("Error: El catálogo está vacío. Debe contener al menos un producto.")
        sys.exit(1)
    
    # 4. Validar estructura del PRIMER producto (muestra representativa)
    primer_producto = datos[0]
    
    if not isinstance(primer_producto, dict):
        print("Error: Los productos deben ser objetos JSON.")
        print(f"Se encontró: {type(primer_producto).__name__}")
        sys.exit(1)
    
    # Verificar que tenga todas las claves requeridas
    claves_encontradas = set(primer_producto.keys())
    claves_faltantes = CLAVES_REQUERIDAS_CAT - claves_encontradas
    
    if claves_faltantes:
        print("Error: El producto no tiene la estructura completa.")
        print(f"Claves faltantes: {', '.join(sorted(claves_faltantes))}")
        sys.exit(1)
    
    # 5. Validar tipos de datos del primer producto
    try:
        _validar_tipos_producto(primer_producto)
    except ValueError as e:
        print("Error: Tipo de dato inválido en el catálogo.")
        print(f"Detalle: {e}")
        sys.exit(1)
    
    # Validación exitosa
    print(f"Catálogo validado: {len(datos)} productos encontrados.")
    return datos


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
        


def validar_estructura_ventas(nombre_archivo):
    """
    Valida que el archivo JSON de ventas cumpla con la estructura esperada.
    
    Verifica la estructura del registro de ventas sin necesidad de procesar
    todas las transacciones. Usa validación por muestreo del primer elemento
    como representativo del esquema completo.
    
    Estructura esperada del registro de ventas:
        - Archivo JSON válido
        - Array de transacciones
        - Cada transacción con claves: SALE_ID, SALE_Date, Product, Quantity
    
    Args:
        nombre_archivo (str): Ruta del archivo JSON de ventas a validar.
    
    Returns:
        dict: Datos del registro de ventas si la validación es exitosa.
    
    Raises:
        SystemExit: Si el archivo no cumple con la estructura esperada.
        
    Note:
        La validación de la primera transacción es suficiente como muestra
        representativa, siguiendo el principio de eficiencia sin comprometer
        integridad de datos.
    """
    
    try:
        # 1. Validar que sea JSON válido
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            datos = json.load(archivo)
            
    except json.JSONDecodeError as e:
        print(f"Error: El archivo '{nombre_archivo}' no contiene JSON válido.")
        print(f"Detalle: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error al leer el archivo '{nombre_archivo}': {e}")
        sys.exit(1)
    
    # 2. Validar que sea un array
    if not isinstance(datos, list):
        print("Error: El registro de ventas debe ser un array de transacciones.")
        print(f"Se encontró: {type(datos).__name__}")
        sys.exit(1)
    
    # 3. Validar que no esté vacío
    if len(datos) == 0:
        print("Error: El registro de ventas está vacío.")
        print("Debe contener al menos una transacción.")
        sys.exit(1)
    
    # 4. Validar estructura de la PRIMERA transacción (muestra representativa)
    primera_venta = datos[0]
    
    if not isinstance(primera_venta, dict):
        print("Error: Las transacciones deben ser objetos JSON.")
        print(f"Se encontró: {type(primera_venta).__name__}")
        sys.exit(1)
    
    # Verificar que tenga todas las claves requeridas
    claves_encontradas = set(primera_venta.keys())
    claves_faltantes = CLAVES_REQUERIDAS_VTAS - claves_encontradas
    
    if claves_faltantes:
        print("Error: La transacción no tiene la estructura completa.")
        print(f"Claves faltantes: {', '.join(sorted(claves_faltantes))}")
        sys.exit(1)
    
    # 5. Validar tipos de datos de la primera transacción
    try:
        _validar_tipos_venta(primera_venta)
    except ValueError as e:
        print("Error: Tipo de dato inválido en el registro de ventas.")
        print(f"Detalle: {e}")
        sys.exit(1)
    
    # Validación exitosa
    print(f"Registro de ventas validado: {len(datos)} transacciones encontradas.")
    return datos


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
