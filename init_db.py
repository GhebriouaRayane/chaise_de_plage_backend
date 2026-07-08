from app.db.session import SessionLocal, engine
from app.models import models
from app.core.config import settings
from app.core import security

def init():
    db = SessionLocal()
    
    # Create tables
    models.Base.metadata.create_all(bind=engine)
    
    # Add categories
    if not db.query(models.Category).first():
        cat1 = models.Category(name="Classique")
        cat2 = models.Category(name="Premium")
        db.add_all([cat1, cat2])
        db.commit()
    
    # Add initial products if empty
    if not db.query(models.Product).first():
        products = [
            models.Product(
                name="Classique Azur",
                description="Chaise de plage élégante en bois naturel avec coussin imperméable.",
                price=4500,
                image="https://images.unsplash.com/photo-1569335468885-d7d1a41e570c",
                badge="bestseller",
                features=["Structure en bois de teck", "Coussin imperméable", "Pliable", "Résistant UV"],
                category_id=1
            ),
            models.Product(
                name="Premium Horizon",
                description="Transat de luxe à dossier réglable, idéal pour les longues journées.",
                price=7200,
                image="https://images.unsplash.com/photo-1503003378590-66f89f543bc6",
                badge="nouveau",
                features=["Aluminium anodisé", "5 positions réglables", "Repose-tête"],
                category_id=2
            )
        ]
        db.add_all(products)
        db.commit()
    
    db.close()
    print("Database initialized!")

if __name__ == "__main__":
    init()
