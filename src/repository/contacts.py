from datetime import datetime, timedelta

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.entity.models import Contact, User
from src.schemas.contact import ContactSchema


async def get_contacts(name: str | None, surname: str | None, email: str | None, limit: int, offset: int,
                       db: AsyncSession, user: User):
    statement = select(Contact).filter_by(user=user).offset(offset).limit(limit)
    if name:
        statement = statement.filter(Contact.name.like(f'%{name}%'))
    if surname:
        statement = statement.filter(Contact.surname.like(f'%{surname}%'))
    if email:
        statement = statement.filter(Contact.email.like(f'%{email}%'))
    contacts = await db.execute(statement)
    return contacts.scalars().all()


async def get_upcoming_birthdays(days_range: int, db: AsyncSession, user: User):
    today = datetime.today().date()
    start_period = today.strftime('%m-%d')
    end_period = (today + timedelta(days_range)).strftime('%m-%d')
    statement = select(Contact).filter_by(user=user).filter(func.to_char(Contact.birthday, 'MM-DD').between(start_period, end_period))
    contacts = await db.execute(statement)
    return contacts.scalars().all()


async def get_contact(contact_id: int, db: AsyncSession, user: User):
    statement = select(Contact).filter_by(id=contact_id, user=user)
    contact = await db.execute(statement)
    return contact.scalar_one_or_none()


async def create_contact(body: ContactSchema, db: AsyncSession, user: User):
    contact = Contact(**body.model_dump(exclude_unset=True), user=user)
    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactSchema, db: AsyncSession, user: User):
    statement = select(Contact).filter_by(id=contact_id, user=user)
    result = await db.execute(statement)
    contact = result.scalar_one_or_none()
    if contact:
        contact.name = body.name
        contact.surname = body.surname
        contact.email = body.email
        contact.phone = body.phone
        contact.birthday = body.birthday
        await db.commit()
        await db.refresh(contact)
    return contact


async def delete_contact(contact_id: int, db: AsyncSession, user: User):
    statement = select(Contact).filter_by(id=contact_id, user=user)
    result = await db.execute(statement)
    contact = result.scalar_one_or_none()
    if contact:
        await db.delete(contact)
        await db.commit()
    return contact