import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - [%(levelname)s] - %(name)s - %(message)s")
logger = logging.getLogger("Reader")

def leer_recetas(ruta_archivo: str) -> list:
    logger.info(f"Leyendo archivo de entrada: '{ruta_archivo}'")
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            lineas = [linea.strip() for linea in f if linea.strip()]
        logger.info(f"Se encontraron {len(lineas)} términos válidos para procesar.")
        return lineas
    except FileNotFoundError:
        logger.error(f"Archivo no encontrado en la ruta: {ruta_archivo}")
        return []

if __name__ == "__main__":
    print("\n--- TEST UNITARIO: LECTOR ---")
    print(f"Resultado: {leer_recetas('recipes.txt')}\n")