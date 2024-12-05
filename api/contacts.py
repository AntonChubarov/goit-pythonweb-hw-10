from typing import List

from fastapi import APIRouter, HTTPException, status

from repositories.contact_repository import ContactRepository
from schemas.contacts import ContactCreate, ContactUpdate, ContactOut
from services.contact_service import ContactService

router = APIRouter(prefix="/contacts", tags=["contacts"])

service = ContactService(ContactRepository())


@router.get("/", response_model=List[ContactOut])
def read_contacts(
        first_name: str = None,
        last_name: str = None,
        email: str = None,
):
    if first_name or last_name or email:
        contacts = service.search_contacts(first_name, last_name, email)
    else:
        contacts = service.get_all_contacts()
    return contacts


@router.get("/upcoming_birthdays", response_model=List[ContactOut])
def read_upcoming_birthdays():
    return service.get_upcoming_birthdays()


@router.post("/", response_model=ContactOut, status_code=status.HTTP_201_CREATED)
def create_contact(contact: ContactCreate):
    return service.create_contact(contact)


@router.get("/{contact_id}", response_model=ContactOut)
def read_contact(contact_id: int):
    contact = service.get_contact(contact_id)
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


@router.put("/{contact_id}", response_model=ContactOut)
def update_contact(contact_id: int, contact: ContactUpdate):
    updated_contact = service.update_contact(contact_id, contact)
    if updated_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return updated_contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contact(contact_id: int):
    deleted_contact = service.delete_contact(contact_id)
    if deleted_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return
