from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime
from app.models.models import OrderStatus

# Category
class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    class Config:
        from_attributes = True

# Product
class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    image: str
    badge: Optional[str] = None
    features: List[str]
    available: bool = True
    rating: float = 5.0
    reviews: int = 0
    category_id: Optional[int] = None

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    class Config:
        from_attributes = True

# Order
class OrderBase(BaseModel):
    nom: str
    prenom: str
    telephone: str
    email: Optional[EmailStr] = None
    wilaya_code: int
    commune: str
    adresse: str
    remarque: Optional[str] = None
    product_id: int
    quantity: int

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    status: OrderStatus

class Order(OrderBase):
    id: int
    order_number: str
    wilaya_name: str
    product_name: str
    unit_price: float
    shipping_fee: float
    total_price: float
    status: OrderStatus
    created_at: datetime
    
    class Config:
        from_attributes = True

# Contact
class ContactCreate(BaseModel):
    name: str
    email: EmailStr
    subject: str
    message: str

class ContactMessage(ContactCreate):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

# Auth
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class AdminLogin(BaseModel):
    username: str
    password: str
