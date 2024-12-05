from abc import ABC, abstractmethod

from schemas.contacts import ContactCreate, ContactUpdate


class IContactRepository(ABC):

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def get_by_id(self, contact_id: int):
        pass

    @abstractmethod
    def create(self, contact: ContactCreate):
        pass

    @abstractmethod
    def update(self, contact_id: int, contact: ContactUpdate):
        pass

    @abstractmethod
    def delete(self, contact_id: int):
        pass

    @abstractmethod
    def search(self, first_name: str = None, last_name: str = None, email: str = None):
        pass

    @abstractmethod
    def get_upcoming_birthdays(self):
        pass


class ContactService:
    def __init__(self, repository: IContactRepository):
        self.contact_repository = repository

    def get_all_contacts(self):
        return self.contact_repository.get_all()

    def get_contact(self, contact_id: int):
        return self.contact_repository.get_by_id(contact_id)

    def create_contact(self, contact: ContactCreate):
        return self.contact_repository.create(contact)

    def update_contact(self, contact_id: int, contact: ContactUpdate):
        return self.contact_repository.update(contact_id, contact)

    def delete_contact(self, contact_id: int):
        return self.contact_repository.delete(contact_id)

    def search_contacts(self, first_name: str = None, last_name: str = None, email: str = None):
        return self.contact_repository.search(first_name, last_name, email)

    def get_upcoming_birthdays(self):
        return self.contact_repository.get_upcoming_birthdays()
