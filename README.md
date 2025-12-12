# Sales Dashboard con MongoDB Atlas y Streamlit

Proyecto académico que integra **MongoDB Atlas** con **Python/Streamlit** para analizar datos de ventas.

---

## ⚙️ Instalación

1. Crear entorno virtual (opcional):

   ```bash
   python -m venv venv       # luego de clonar el repositorio ejecutar el entorno virtual
   .\venv\Scripts\activate   # Windows
   source venv/bin/activate  # macOS/Linux
   ```

2. Instalar dependencias:
   `pip install -r requirements.txt`

3. ▶️ Ejecución con:
   `python -m streamlit run app_streamlit.py`

---

# Acerca de:

## Descripción

Este proyecto procesa datos de una tienda global (Global Superstore) y los inserta en una base de datos MongoDB Atlas. Incluye scripts para convertir datos de CSV a JSON, generar archivos JSON separados para clientes, pedidos y productos, y realizar consultas de agregación utilizando pipelines de MongoDB.

## Características

- Procesamiento de datos desde archivo CSV a formato JSON.
- Generación de archivos JSON separados para entidades (clientes, pedidos, productos).
- Inserción masiva de datos en colecciones de MongoDB Atlas.
- Esquemas de validación JSON para asegurar la integridad de los datos en las colecciones.
- Pipelines de agregación para consultas analíticas avanzadas.
- Dashboard interactivo con Streamlit para visualización de datos y reportes.

### Dashboard con Streamlit

El proyecto incluye un dashboard interactivo desarrollado con Streamlit que permite explorar los datos de ventas de manera visual y dinámica. El dashboard consta de las siguientes vistas:

- **Home**: Página de bienvenida con una descripción general del proyecto y navegación.
- **Orders Report**: Reporte de pedidos que permite analizar ventas por categoría y mes en un rango de fechas seleccionado. Incluye gráficos de líneas para visualizar tendencias.
- **Customers Report**: Reporte de clientes que muestra los mejores clientes por número de pedidos y permite encontrar el cliente con más pedidos en un rango de fechas.
- **Products Report**: Reporte de productos que agrupa productos por subcategoría y precio, mostrando distribuciones con gráficos de barras.

Para acceder al dashboard, ejecuta `python -m streamlit run app_streamlit.py` y navega entre las vistas usando la barra lateral.

### Uso

1. _Procesar datos CSV a JSON_: Ejecuta python data/processing_csv.py para convertir el archivo CSV en JSON.
2. _Generar JSONs separados_: Ejecuta python data/json_generation.py para crear archivos JSON individuales para clientes, pedidos y productos.
3. _Insertar datos en MongoDB_: Ejecuta python database_scripts/dbInsert.py para insertar los datos procesados en las colecciones de MongoDB.
4. _Ejecutar consultas_: Usa las funciones en database_scripts/pipelines.py para realizar consultas de agregación. Ejemplo: python database_scripts/pipelines.py

### Estructura de Datos

- _Fuente de datos_: data/raw/Global_Superstore2.csv (datos de ventas de tienda global).
- _Datos procesados_:
  - data/processed/customers.json: Información de clientes únicos.
  - data/processed/orders.json: Detalles de pedidos.
  - data/processed/products.json: Información de productos.

### Configuración de Base de Datos

- _Base de datos_: proyect1database2
- _Colecciones_:
  - Customers: Datos de clientes con subdocumento de dirección.
  - Orders: Información de pedidos con referencias a clientes y productos.
  - Products: Detalles de productos categorizados.
- _Validación_: Los esquemas de validación están definidos en database_scripts/validation.py (actualmente comentados; descoméntalos para aplicar validación estricta).

### Scripts Principales

- data/processing_csv.py: Convierte el archivo CSV a JSON, limpiando tipos de datos y formateando fechas.
- data/json_generation.py: Procesa el JSON crudo para generar archivos separados y únicos para cada entidad.
- database_scripts/connection.py: Establece la conexión con MongoDB Atlas.
- database_scripts/dbInsert.py: Inserta los datos JSON en las colecciones de MongoDB.
- database_scripts/pipelines.py: Contiene funciones con pipelines de agregación para consultas como ventas por categoría, top clientes, etc.
- database_scripts/validation.py: Define esquemas JSON Schema para validar la estructura de los documentos en las colecciones.

## Dependencias

- pymongo: Para interactuar con MongoDB.
- pandas: Para procesamiento de datos CSV/JSON.
- streamlit: Para el dashboard interactivo de visualización de datos.

### Notas

- Asegúrate de tener acceso a MongoDB Atlas y las credenciales configuradas.
- Los esquemas de validación están preparados pero no aplicados por defecto; edita validation.py para activarlos.
- El proyecto está diseñado para datos de ventas; ajusta según necesidades específicas.

### Licencia

Este proyecto es de uso educativo. Consulta los términos de uso de los datos fuente.
