import requests
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - [%(levelname)s] - %(name)s - %(message)s")
logger = logging.getLogger("APIClient")

def buscar_receta_api(nombre_receta: str) -> list:
    url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={nombre_receta}"
    logger.info(f"Consultando TheMealDB para: '{nombre_receta}'")
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            datos = response.json()
            resultados = datos.get("meals") or []
            logger.info(f"Petición exitosa. Recetas obtenidas: {len(resultados)}")
            return resultados
        logger.warning(f"Error de API. Código de estado: {response.status_code}")
        return []
    except requests.RequestException as e:
        logger.error(f"Error de red al consultar la API para '{nombre_receta}': {e}")
        return []

if __name__ == "__main__":
    print("\n--- TEST UNITARIO: API CLIENT ---")
    res = buscar_receta_api("chicken")
    print(f"✅ Recetas obtenidas en el test: {len(res)}\n")