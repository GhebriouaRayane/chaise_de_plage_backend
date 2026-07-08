from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime, JSON, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base
import enum

class OrderStatus(str, enum.Enum):
    PENDING = "En attente"
    CONFIRMED = "Confirmée"
    SHIPPED = "Expédiée"
    DELIVERED = "Livrée"
    CANCELLED = "Annulée"

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    products = relationship("Product", back_populates="category")

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    price = Column(Float)
    image = Column(String)
    badge = Column(String, nullable=True) # nouveau, bestseller
    features = Column(JSON) # List of strings
    available = Column(Boolean, default=True)
    rating = Column(Float, default=5.0)
    reviews = Column(Integer, default=0)
    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category", back_populates="products")

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String, unique=True, index=True)
    nom = Column(String)
    prenom = Column(String)
    telephone = Column(String)
    email = Column(String, nullable=True)
    wilaya_code = Column(Integer)
    wilaya_name = Column(String)
    commune = Column(String)
    adresse = Column(Text)
    remarque = Column(Text, nullable=True)
    
    product_id = Column(Integer, ForeignKey("products.id"))
    product_name = Column(String)
    quantity = Column(Integer)
    unit_price = Column(Float)
    shipping_fee = Column(Float)
    total_price = Column(Float)
    
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class ContactMessage(Base):
    __tablename__ = "contact_messages"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    subject = Column(String)
    message = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
