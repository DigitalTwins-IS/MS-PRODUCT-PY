🧩 **MS-PRODUCT-PY**
Microservicio de Gestión de Productos del ecosistema Digital Twins.


📘 **Descripción General**
MS-PRODUCT-PY es un microservicio desarrollado con FastAPI y SQLAlchemy encargado de la gestión de productos dentro del sistema Digital Twins. Permite registrar, consultar, actualizar y desactivar productos de manera eficiente, siguiendo los principios de arquitectura modular y microservicios.


⚙️ **Funcionalidades Principales**
• Crear productos con validación de nombre único y precio válido.
• Listar productos con opción de filtrar por categoría.
• Actualizar productos modificando campos específicos.
• Desactivar productos (soft delete) sin eliminarlos físicamente.
• Health check para monitorear el estado del servicio.


🧰 **Tecnologías Utilizadas**
Componente	Descripción
Python 3.11+	Lenguaje base
FastAPI	Framework backend
SQLAlchemy	ORM para PostgreSQL
Pydantic	Validación de datos
Uvicorn	Servidor ASGI
Docker	Contenedorización
pytest	Framework de pruebas


⚡ **Configuración del Entorno**
1. Clonar el repositorio: git clone https://github.com/digital-twins/MS-PRODUCT-PY.git
2. Crear entorno virtual: python -m venv venv && source venv/bin/activate
3. Instalar dependencias: pip install -r requirements.txt
4. Configurar variables de entorno copiando env.example a .env


🐳 **Ejecución con Docker**
• Construir imagen: docker build -t digitaltwins/ms-product-py .
• Ejecutar contenedor: docker run -d -p 8000:8000 digitaltwins/ms-product-py
• Endpoints: http://localhost:8000/docs y http://localhost:8000/health


🧪 **Pruebas Automáticas**
Ejecutar pytest con el comando: pytest -v


🧠 **Endpoints Principales**
Método	Endpoint	Descripción
POST	/api/v1/products/products	Crear producto
GET	/api/v1/products/products	Listar productos (filtro por categoría)
GET	/api/v1/products/products/{id}	Obtener producto por ID
PUT	/api/v1/products/products/{id}	Actualizar producto
DELETE	/api/v1/products/products/{id}	Desactivar producto (soft delete)
GET	/health	Verificar estado del servicio


🔐 **Variables de Entorno**
Variable	Descripción	Valor por defecto
DATABASE_URL	URL de conexión a PostgreSQL	postgresql://dgt_user:dgt_pass@postgres-db:5432/digital_twins_db
SERVICE_HOST	Host del servicio	0.0.0.0
SERVICE_PORT	Puerto del servicio	8000
DEBUG	Modo depuración	True


🧭 **Integración con Digital Twins**
Este microservicio se comunica a través del API Gateway (NGINX) y comparte la base de datos PostgreSQL con los demás servicios del ecosistema: MS-USER-PY, MS-GEO-PY, MS-AUTH-PY y MS-REPORT-PY.
