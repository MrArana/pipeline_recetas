import os
import json
import psycopg2
import logging
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s - [%(levelname)s] - %(name)s - %(message)s")
logger = logging.getLogger("DatabaseManager")

def obtener_conexion():
    try:
        return psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
    except psycopg2.OperationalError as e:
        logger.error(f"Error de conexión a PostgreSQL. ¿Está Docker activo?: {e}")
        raise e

def inicializar_tabla():
    conn = obtener_conexion()
    cursor = conn.cursor()
    # Usamos el tipo nativo JSONB para permitir indexación avanzada GIN
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recetas (
            id SERIAL PRIMARY KEY,
            id_meal VARCHAR(50) UNIQUE,
            name VARCHAR(255),
            category VARCHAR(100),
            area VARCHAR(100),
            ingredients JSONB,
            instructions TEXT,
            llm_representation TEXT
        );
    """)
    conn.commit()
    cursor.close()
    conn.close()
    logger.info("Estructura de la base de datos verificada de forma correcta.")

def guardar_receta(receta: dict):
    conn = obtener_conexion()
    cursor = conn.cursor()
    try:
        # ON CONFLICT DO NOTHING evita duplicados si el script se ejecuta varias veces
        cursor.execute("""
            INSERT INTO recetas (id_meal, name, category, area, ingredients, instructions, llm_representation)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id_meal) DO NOTHING;
        """, (
            receta["id_meal"],
            receta["name"],
            receta["category"],
            receta["area"],
            json.dumps(receta["ingredients"]),
            receta["instructions"],
            receta["llm_representation"]
        ))
        conn.commit()
        logger.info(f"Receta '{receta['name']}' persistida exitosamente.")
    except Exception as e:
        conn.rollback()
        logger.error(f"Error al insertar la receta '{receta['name']}': {e}")
    finally:
        cursor.close()
        conn.close()


def obtener_recetas_guardadas():
    conn = obtener_conexion()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT
                id_meal,
                name,
                category,
                area,
                ingredients,
                instructions,
                llm_representation
            FROM recetas
            ORDER BY name;
        """)

        recetas = cursor.fetchall()
        return recetas

    except Exception as e:
        logger.error(f"Error obteniendo recetas: {e}")
        return []

    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    print("\n--- TEST UNITARIO: PERSISTENCIA ---")
    inicializar_tabla()
    print("✅ Conexión e inicialización correctas.\n")