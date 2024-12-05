from datetime import datetime, timedelta

from sqlalchemy import create_engine, Column, Integer, String, Date, or_, and_, extract
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from schemas.contacts import ContactCreate, ContactUpdate
from services.contact_service import IContactRepository

DATABASE_URL = "postgresql://postgres:qwerty@localhost:5432/hw10"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
Base.metadata.create_all(bind=engine)


class Contact(Base):
    __tablename__ = 'contacts'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone_number = Column(String, unique=True, index=True)
    birthday = Column(Date)
    additional_data = Column(String, nullable=True)


class ContactRepository(IContactRepository):
    def __init__(self):
        self.db = SessionLocal()

    def get_all(self):
        return self.db.query(Contact).all()

    def get_by_id(self, contact_id: int):
        return self.db.query(Contact).filter(Contact.id == contact_id).first()

    def create(self, contact: ContactCreate):
        db_contact = Contact(**contact.model_dump())
        self.db.add(db_contact)
        self.db.commit()
        self.db.refresh(db_contact)
        return db_contact

    def update(self, contact_id: int, contact: ContactUpdate):
        db_contact = self.get_by_id(contact_id)
        if db_contact:
            for key, value in contact.model_dump(exclude_unset=True).items():
                setattr(db_contact, key, value)
            self.db.commit()
            self.db.refresh(db_contact)
        return db_contact

    def delete(self, contact_id: int):
        db_contact = self.get_by_id(contact_id)
        if db_contact:
            self.db.delete(db_contact)
            self.db.commit()
        return db_contact

    def search(self, first_name: str = None, last_name: str = None, email: str = None):
        query = self.db.query(Contact)
        if first_name:
            query = query.filter(Contact.first_name.ilike(f"%{first_name}%"))
        if last_name:
            query = query.filter(Contact.last_name.ilike(f"%{last_name}%"))
        if email:
            query = query.filter(Contact.email.ilike(f"%{email}%"))
        return query.all()

    def get_upcoming_birthdays(self):
        today = datetime.today()
        upcoming_days = [(today + timedelta(days=i)).date() for i in range(7)]

        upcoming_month_days = [(d.month, d.day) for d in upcoming_days]

        conditions = [
            and_(
                extract('month', Contact.birthday) == month,
                extract('day', Contact.birthday) == day
            )
            for month, day in upcoming_month_days
        ]

        return self.db.query(Contact).filter(or_(*conditions)).all()
