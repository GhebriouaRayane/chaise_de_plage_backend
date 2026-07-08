from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from app.crud import crud
from app.schemas import schemas
from app.db.session import get_db
from app.api.v1.endpoints.auth import get_current_user
from app.services.business import send_email, send_telegram_message
from app.core.config import settings

router = APIRouter()

def notify_order(order: schemas.Order):
    # Email to Admin
    admin_body = f"""
    <h1>Nouvelle Commande: {order.order_number}</h1>
    <p><b>Client:</b> {order.nom} {order.prenom}</p>
    <p><b>Téléphone:</b> {order.telephone}</p>
    <p><b>Wilaya:</b> {order.wilaya_name} ({order.wilaya_code})</p>
    <p><b>Commune:</b> {order.commune}</p>
    <p><b>Adresse:</b> {order.adresse}</p>
    <p><b>Produit:</b> {order.product_name}</p>
    <p><b>Quantité:</b> {order.quantity}</p>
    <p><b>Total:</b> {order.total_price} DA</p>
    <p><b>Date:</b> {order.created_at}</p>
    <p><b>Remarque:</b> {order.remarque or 'Aucune'}</p>
    """
    telegram_message = (
        f"Nouvelle commande {order.order_number}\n"
        f"Client: {order.nom} {order.prenom}\n"
        f"Téléphone: {order.telephone}\n"
        f"Wilaya: {order.wilaya_name} ({order.wilaya_code})\n"
        f"Commune: {order.commune}\n"
        f"Produit: {order.product_name}\n"
        f"Quantité: {order.quantity}\n"
        f"Total: {order.total_price} DA\n"
        f"Remarque: {order.remarque or 'Aucune'}"
    )
    send_telegram_message(telegram_message)
    
    # Email to Client
    if order.email:
        client_body = f"""
        <h1>Merci pour votre commande !</h1>
        <p>Bonjour {order.prenom}, votre commande <b>{order.order_number}</b> a bien été reçue.</p>
        <p>Détails : {order.quantity}x {order.product_name}</p>
        <p>Total à payer à la livraison : <b>{order.total_price} DA</b></p>
        <p>Nous vous contacterons bientôt au {order.telephone}.</p>
        """
        send_email(order.email, f"Confirmation de commande {order.order_number}", client_body)

@router.post("/", response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    try:
        db_order = crud.create_order(db, order)
        order_schema = schemas.Order.model_validate(db_order)
        background_tasks.add_task(notify_order, order_schema)
        return db_order
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[schemas.Order])
def read_orders(
    skip: int = 0, 
    limit: int = 100, 
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    return crud.get_orders(db, skip=skip, limit=limit, search=search)

@router.patch("/{order_id}", response_model=schemas.Order)
def update_order_status(
    order_id: int, 
    update: schemas.OrderUpdate, 
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    db_order = crud.update_order_status(db, order_id, update.status)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order
