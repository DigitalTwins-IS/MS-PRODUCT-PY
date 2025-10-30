"""
Tests para MS-PRODUCT-PY
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.main import app
from src.models.database import Base, get_db
from src.models.product import Product

# Base de datos de pruebas en memoria
SQLALCHEMY_TEST_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_TEST_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_database():
    """Crear y limpiar base de datos antes de cada test"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


# ============================================================================
# TESTS DE SALUD Y CONECTIVIDAD
# ============================================================================

def test_health_check():
    """Test del health check"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ["healthy", "unhealthy"]
    assert data["service"] == "MS-PRODUCT-PY - User Management Service"

# ============================================================================
# TESTS CRUD DE PRODUCTOS
# ============================================================================

def test_create_product():
    """Crear un producto exitosamente"""
    product_data = {
        "name": "Galletas Festival",
        "description": "Galletas de vainilla 12 unidades",
        "price": 3500.00,
        "category": "Snacks"
    }
    
    response = client.post("/api/v1/products/products", json=product_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == product_data["name"]
    assert data["price"] == product_data["price"]
    assert data["is_active"] is True


def test_create_duplicate_product():
    """No permitir crear productos con el mismo nombre"""
    product_data = {
        "name": "Coca-Cola 500ml",
        "description": "Bebida gaseosa tamaño personal",
        "price": 2500.00,
        "category": "Bebidas"
    }


    # Crear el primero
    response1 = client.post("/api/v1/products/products", json=product_data)
    assert response1.status_code == 201

    # Intentar crear duplicado
    response2 = client.post("/api/v1/products/products", json=product_data)
    assert response2.status_code == 400
    assert "ya existe" in response2.json()["detail"]


def test_list_products_filtered_by_category():
    """Listar productos filtrando por categoría"""
    products = [
        {"name": "Pepsi 500ml", "description": "Bebida gaseosa", "price": 2500, "category": "Bebidas"},
        {"name": "Papas Margarita", "description": "Snacks de papas", "price": 2000, "category": "Snacks"},
    ]
    for product in products:
        client.post("/api/v1/products/products", json=product)

    response = client.get("/api/v1/products/products?category=Bebidas")
    assert response.status_code == 200
    data = response.json()
    assert all("Bebidas" in (p["category"] or "") for p in data)


def test_update_product():
    """Actualizar un producto existente"""
    # Crear producto
    product_data = {
        "name": "Leche Alpina 1L",
        "description": "Leche entera",
        "price": 4200.00,
        "category": "Lácteos"
    }
    create_response = client.post("/api/v1/products/products", json=product_data)
    assert create_response.status_code == 201
    product_id = create_response.json()["id"]

    # Actualizar producto
    update_data = {"price": 4500.00, "description": "Leche entera 1L Alpina"}
    update_response = client.put(f"/api/v1/products/products/{product_id}", json=update_data)
    assert update_response.status_code == 200
    data = update_response.json()
    assert data["price"] == 4500.00
    assert "Alpina" in data["description"]


def test_soft_delete_product():
    """Desactivar (soft delete) un producto"""
    product_data = {
        "name": "Agua Cristal 600ml",
        "description": "Agua mineral sin gas",
        "price": 2000.00,
        "category": "Bebidas"
    }
    create_response = client.post("/api/v1/products/products", json=product_data)
    assert create_response.status_code == 201
    product_id = create_response.json()["id"]

    # Soft delete
    delete_response = client.delete(f"/api/v1/products/products/{product_id}")
    assert delete_response.status_code == 204

    # Verificar que esté inactivo
    db = TestingSessionLocal()
    db_product = db.query(Product).filter(Product.id == product_id).first()
    assert db_product.is_active is False


# ============================================================================
# TESTS ADICIONALES (LISTADO, DETALLE)
# ============================================================================

def test_get_product_by_id():
    """Obtener producto por ID"""
    product_data = {
        "name": "Yogurt Alpina Fresa",
        "description": "Yogurt de fresa 200ml",
        "price": 1800.00,
        "category": "Lácteos"
    }
    create_response = client.post("/api/v1/products/products", json=product_data)
    assert create_response.status_code == 201
    product_id = create_response.json()["id"]

    response = client.get(f"/api/v1/products/products/{product_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == product_id
    assert data["name"] == "Yogurt Alpina Fresa"


def test_get_product_not_found():
    """Intentar obtener un producto inexistente"""
    response = client.get("/api/v1/products/products/999")
    assert response.status_code == 404
    assert "no encontrado" in response.text.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])