from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from app.crud import crud
from app.schemas import schemas
from app.db.session import get_db
from app.services.business import send_email
from app.core.config import settings

router = APIRouter()

def notify_contact(contact: schemas.ContactMessage):
    body = f"""
    <h1>Nouveau Message de Contact</h1>
    <p><b>De:</b> {contact.name} ({contact.email})</p>
    <p><b>Sujet:</b> {contact.subject}</p>
    <p><b>Message:</b></p>
    <p>{contact.message}</p>
    """
    send_email(settings.EMAILS_FROM_EMAIL, f"Contact: {contact.subject}", body)

@router.post("/", response_model=schemas.ContactMessage)
def create_contact_message(
    contact: schemas.ContactCreate, 
    background_tasks: BackgroundTasks, 
    db: Session = Depends(get_db)
):
    db_message = crud.create_contact_message(db, contact)
    message_schema = schemas.ContactMessage.model_validate(db_message)
    background_tasks.add_task(notify_contact, message_schema)
    return db_message
