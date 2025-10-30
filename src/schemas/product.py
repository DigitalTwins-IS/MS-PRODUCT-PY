"""
Schemas de Producto (Product)
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ProductBase(BaseModel):
    """Schema base de Producto"""
    name: str = Field(..., min_length=3, max_length=255, description="Nombre del producto")
    description: Optional[str] = Field(None, description="Descripción del producto")
    price: float = Field(..., gt=0, description="Precio del producto (en COP)")
    category: Optional[str] = Field(None, max_length=100, description="Categoría del producto")


class ProductCreate(ProductBase):
    """Schema para crear un producto"""
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Galletas Festival",
                "description": "Galletas rellenas de vainilla 12 unidades",
                "price": 3500.00,
                "category": "Snacks"
            }
        }


class ProductUpdate(BaseModel):
    """Schema para actualizar un producto"""
    name: Optional[str] = Field(None, min_length=3, max_length=255)
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    category: Optional[str] = Field(None, max_length=100)
    is_active: Optional[bool] = Field(None, description="Estado activo o inactivo")
    
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Galletas Festival Fresa",
                "price": 3700.00,
                "category": "Snacks"
            }
        }


class ProductResponse(ProductBase):
    """Schema de respuesta de producto"""
    id: int = Field(..., description="ID del producto")
    is_active: bool = Field(..., description="Indica si el producto está activo")
    created_at: datetime = Field(..., description="Fecha de creación")
    updated_at: Optional[datetime] = Field(None, description="Última actualización")


    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Galletas Festival",
                "description": "Galletas rellenas de vainilla 12 unidades",
                "price": 3500.00,
                "category": "Snacks",
                "is_active": True,
                "created_at": "2025-10-27T12:00:00Z",
                "updated_at": "2025-10-27T12:00:00Z"
            }
        }


class HealthResponse(BaseModel):
    """Schema de respuesta del health check"""
    status: str
    service: str
    version: str
    database: str

    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "service": "MS-PRODUCT-PY",
                "version": "1.0.0",
                "database": "connected"
            }
        }