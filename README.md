# Sistema Inteligente de Almacenamiento de Recetas (ETL)

## 1. Stack Tecnológico Elegido
* **Lenguaje:** Python 3.11+ por su robustez en flujos de datos y manipulación de estructuras nativas.
* **Base de Datos:** PostgreSQL 15 (vía Docker) debido a su excelente rendimiento relacional y su soporte nativo para tipos de datos complejos (`JSONB`).
* **Librerías principales:** `requests` para el consumo de la API REST, `psycopg2-binary` como driver de conexión a base de datos y `python-dotenv` para el desacoplamiento de secretos de configuración.

## 2. Arquitectura y Estructura de Archivos
El proyecto sigue principios de diseño modular y separación de responsabilidades (ETL):

mi_proyecto_recetas/
│
├── src/
│   ├── __init__.py
│   ├── reader.py            # [E] Extracción: Lector del archivo de entrada
│   ├── api_client.py        # [E] Extracción: Cliente HTTP de TheMealDB
│   ├── transformer.py       # [T] Transformación: Adaptación semántica para IA
│   └── database_manager.py  # [L] Carga: Gestión y persistencia en PostgreSQL
│
├── docker-compose.yml       # Orquestación local de la base de datos
├── main.py                  # Orquestador central del flujo integrado
├── recipes.txt              # Entrada de datos (Nombres a buscar)
├── recetas_export.txt       #El archivo para comprobar que todo se ha guardado bien.
├── .env.example             # Plantilla pública de configuración del entorno
└── .env                     # Variables de entorno locales (Ignorado en Git)

## 3. Diccionario de Datos del Proyecto

* id (SERIAL, PK): Identificador único interno para control de la base de datos.

* id_meal (VARCHAR, UNIQUE): El ID original de la API. Se usa como clave única para aplicar la lógica ON CONFLICT DO NOTHING, evitando que se dupliquen recetas si el script se corre varias veces.

* name (VARCHAR): Nombre del plato (ej: "Baked Salmon").

* category (VARCHAR): Categoría de la receta (ej: "Seafood").

* area (VARCHAR): País u origen de la receta (ej: "British", "Indian", "Italian", "Japanese"). Permite filtrar recetas por su procedencia geográfica/cultural.

* ingredients (JSONB): Lista estructurada de ingredientes en formato JSON (["salmon", "lemon"]). Se usa el tipo nativo JSONB de PostgreSQL porque está indexado de forma binaria. Esto permite hacer cruces lógicos a nivel de base de datos con los ingredientes del carrito del usuario de forma ultra rápida.

* instructions (TEXT): Instrucciones completas de preparación.

* llm_representation (TEXT): Bloque de texto plano pre-formateado que condensa la receta sin formatos raros de código. Está diseñado específicamente para inyectarse directamente en prompts de LLMs, optimizando el contexto y ahorrando costes de tokens.

## 4. Futuras Mejoras (Para el Sistema del Carrito de la Compra)
Para pasar este sistema a producción e implementar la funcionalidad final de recomendación basada en el carrito, añadiría con más tiempo:

* Desarrollar una API pque reciba la lista de los productos que el cliente tiene en su carrito y devuelva las recetas que coincidan, junto con los ingredientes que le falten por comprar.

* Crear una Interfaz Web Basica para que el usuario pueda ver las recetas visualmente, en lugar de leerlas desde un archivo de texto plano como hacemos ahora.

* Si el archivo recipes.txt tuviera miles de platos, el script tardaría demasiado. Añadiría un sistema para procesar y mostrar las recetas en bloques de 10 en 10 para no saturar la API ni la base de datos.

* Añadir una comprobación para que, si el usuario deja una línea en blanco en el archivo de texto o escribe caracteres raros (como números o símbolos), el programa lo detecte, lo limpie y no intente buscarlo en la API para evitar errores.

## 5. Instrucciones de Ejecución
Para levantar el entorno y ejecutar el pipeline, siga estos pasos:

* Cree su archivo de configuración local a partir de la plantilla: cp .env.example .env

* Levante el contenedor de la base de datos PostgreSQL: docker-compose up -d

* Instale las dependencias del proyecto: pip install -r requirements.txt

* Ejecute el pipeline de datos: python main.py

Nota: Al finalizar la ejecución, los logs se mostrarán por consola y se generará el archivo recetas_export.txt con el volcado del resultado.