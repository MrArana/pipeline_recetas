import logging
from src.reader import leer_recetas
from src.api_client import buscar_receta_api
from src.transformer import transformar_para_ia, validar_receta
from src.database_manager import (
    inicializar_tabla,
    guardar_receta,
    obtener_recetas_guardadas
)

# Configuración limpia: SOLO por pantalla, CERO archivos pipeline.log
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(name)s - %(message)s"
)
logger = logging.getLogger("OrquestadorCentral")

def ejecutar_pipeline():
    logger.info("=== INICIANDO PIPELINE ETL DE RECETAS ===")
    try:
        inicializar_tabla()
    except Exception as e:
        logger.critical(f"Cancelando ejecución. Fallo crítico de infraestructura: {e}")
        return

    terminos = leer_recetas("recipes.txt")
    if not terminos:
        logger.warning("No hay datos para procesar en 'recipes.txt'.")
        return
        
    for termino in terminos:
        termino_limpio = termino.strip()
        logger.info(f"Procesando término de búsqueda: '{termino_limpio}'")
        
        recetas_crudas = buscar_receta_api(termino_limpio)
        if not recetas_crudas:
            logger.warning(f"No se encontraron resultados en la API para '{termino_limpio}'.")
            continue
            
        for cruda in recetas_crudas:
            transformada = transformar_para_ia(cruda)
            if validar_receta(transformada):
                guardar_receta(transformada)
            else:
                logger.warning(f"Receta rechazada (inválida): {transformada.get('name', 'Sin nombre')}")

    logger.info("=== DATOS GUARDADOS EN POSTGRESQL ===")

    # Aquí traemos las 6 columnas (incluyendo llm_representation)
    recetas = obtener_recetas_guardadas()

    if not recetas:
        logger.warning("No existen recetas almacenadas.")
    else:
        total_recetas = len(recetas)
        print(f"\n✅ {total_recetas} recetas recuperadas de la Base de Datos.\n")
        
        # Forzamos la escritura fresca del archivo de exportación
        with open("recetas_export.txt", "w", encoding="utf-8") as f:
            f.write(f"TOTAL DE RECETAS EN BASE DE DATOS: {total_recetas}\n")
            f.write("=" * 80 + "\n\n")
            
            for i, receta in enumerate(recetas, 1):
                # Desempaquetamos las 7 columnas de la tupla que viene de la BD
                id_meal, nombre, categoria, area, ingredientes, instrucciones, llm_representation = receta
                
                f.write(f"[{i}/{total_recetas}] {nombre}\n")
                f.write(f"   ID: {id_meal}\n")
                f.write(f"   Categoría: {categoria}\n")
                f.write(f"   Origen: {area}\n")
                f.write(f"   Ingredientes: {', '.join(ingredientes)}\n")
                f.write(f"   Instrucciones: {instrucciones}\n")
                f.write(f"   --- REPRESENTACIÓN EN TEXTO PARA EL LLM ---\n")
                f.write(f"   {llm_representation.replace('\n', '\n   ')}\n") # Lo sangramos para que quede bonito
                f.write("-" * 80 + "\n\n")
        
        print("✅ Archivo 'recetas_export.txt' actualizado con éxito.\n")
        
    logger.info("=== PIPELINE ETL FINALIZADO CON ÉXITO ===")

if __name__ == "__main__":
    ejecutar_pipeline()