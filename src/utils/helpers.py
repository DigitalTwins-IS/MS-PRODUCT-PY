"""
Funciones de utilidad para productos
"""
import re
from fastapi import HTTPException


def format_price(price: float) -> float:
    """
    Redondea el precio a dos decimales positivos
    """
    if price < 0:
        raise HTTPException(status_code=400, detail="El precio no puede ser negativo")
    return round(price, 2)


def validate_category(category: str) -> str:
    """
    Valida que la categoría tenga solo letras, espacios o guiones
    """
    if category and not re.match(r"^[A-Za-zÁÉÍÓÚáéíóúñÑ\s-]+$", category):
        raise HTTPException(status_code=400, detail="La categoría contiene caracteres inválidos")
    return category.strip() if category else category