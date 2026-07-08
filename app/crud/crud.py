from sqlalchemy.orm import Session
from app.models import models
from app.schemas import schemas
from app.services.business import get_shipping_fee, get_wilaya_name
import uuid

# Category
def get_categories(db: Session):
    return db.query(models.Category).all()

def create_category(db: Session, category: schemas.CategoryCreate):
    db_category = models.Category(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

# Product
def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Product).offset(skip).limit(limit).all()

def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product_id: int, product: schemas.ProductCreate):
    db_product = get_product(db, product_id)
    if db_product:
        for key, value in product.model_dump().items():
            setattr(db_product, key, value)
        db.commit()
        db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int):
    db_product = get_product(db, product_id)
    if db_product:
        db.delete(db_product)
        db.commit()
        return True
    return False

# Order
def create_order(db: Session, order: schemas.OrderCreate):
    product = get_product(db, order.product_id)
    if not product:
        raise ValueError("Produit non trouvé")
    
    shipping_fee = get_shipping_fee(order.wilaya_code, order.quantity)
    total_price = (product.price * order.quantity) + shipping_fee
    wilaya_name = get_wilaya_name(order.wilaya_code)
    order_number = f"CMD-{uuid.uuid4().hex[:8].upper()}"
    
    db_order = models.Order(
        **order.model_dump(),
        order_number=order_number,
        wilaya_name=wilaya_name,
        product_name=product.name,
        unit_price=product.price,
        shipping_fee=shipping_fee,
        total_price=total_price,
        status=models.OrderStatus.PENDING
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def get_orders(db: Session, skip: int = 0, limit: int = 100, search: str = None):
    query = db.query(models.Order)
    if search:
        query = query.filter(
            (models.Order.nom.ilike(f"%{search}%")) | 
            (models.Order.prenom.ilike(f"%{search}%")) |
            (models.Order.order_number.ilike(f"%{search}%")) |
            (models.Order.telephone.ilike(f"%{search}%"))
        )
    return query.order_by(models.Order.created_at.desc()).offset(skip).limit(limit).all()

def update_order_status(db: Session, order_id: int, status: models.OrderStatus):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if db_order:
        db_order.status = status
        db.commit()
        db.refresh(db_order)
    return db_order

# Contact
def create_contact_message(db: Session, contact: schemas.ContactCreate):
    db_message = models.ContactMessage(**contact.model_dump())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message
