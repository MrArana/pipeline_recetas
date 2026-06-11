import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - [%(levelname)s] - %(name)s - %(message)s")
logger = logging.getLogger("Transformer")

def validar_receta(receta: dict) -> bool:
    """Valida que una receta tenga los campos requeridos."""
    requeridos = ["id_meal", "name", "ingredients", "instructions"]
    valida = all(receta.get(campo) for campo in requeridos)
    return valida

def transformar_para_ia(receta_api: dict) -> dict:
    nombre = receta_api.get("strMeal", "Sin nombre").strip()
    logger.info(f"Transformando datos para la receta: '{nombre}'")
    
    ingredientes_limpios = []
    for i in range(1, 21):
        ingrediente = receta_api.get(f"strIngredient{i}")
        if ingrediente and ingrediente.strip():
            ingredientes_limpios.append(ingrediente.strip().lower())
            
    categoria = receta_api.get("strCategory", "General")
    area = receta_api.get("strArea", "Desconocido")
    instrucciones = receta_api.get("strInstructions", "").strip()
    
    ingredientes_str = ", ".join(ingredientes_limpios)
    llm_representation = (
        f"RECETA: {nombre}\n"
        f"CATEGORÍA: {categoria}\n"
        f"ORIGEN: {area}\n"
        f"INGREDIENTES: {ingredientes_str}\n"
        f"INSTRUCCIONES: {instrucciones}"
    )
    
    return {
        "id_meal": receta_api.get("idMeal"),
        "name": nombre,
        "category": categoria,
        "area": area,
        "ingredients": ingredientes_limpios,
        "instructions": instrucciones,
        "llm_representation": llm_representation
    }

if __name__ == "__main__":
    print("\n--- TEST UNITARIO: TRANSFORMADOR ---")
    mock = {"strMeal": "Mousse", "strIngredient1": " Chocolate ", "strIngredient2": " Milk "}
    print(transformar_para_ia(mock)["llm_representation"])