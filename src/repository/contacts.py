from datetime import datetime, timedelta

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.entity.models import Contact, User
from src.schemas.contact import ContactSchema


async def get_contacts(name: str | None, surname: str | None, email: str | None, limit: int, offset: int,
                       db: AsyncSession, user: User):
    """
    The get_contacts function returns a list of contacts that match the given parameters.

    :param name: str | None: Filter the contacts by name
    :param surname: str | None: Filter the contacts by surname
    :param email: str | None: Filter the contacts by email
    :param limit: int: Limit the number of results returned
    :param offset: int: Specify the number of records to skip
    :param db: AsyncSession: Pass the database session to the function
    :param user: User: Filter the contacts by user
    :return: A list of contacts
    :doc-author: Trelent
    """
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
    """
    The get_upcoming_birthdays function returns a list of contacts whose birthdays are within the specified range.
    The function takes two arguments: days_range and db. The days_range argument is an integer that specifies how many
    days in advance to look for upcoming birthdays, while the db argument is an AsyncSession object that represents a
    connection to the database.

    :param days_range: int: Specify the range of days to search for birthdays
    :param db: AsyncSession: Pass a database session to the function
    :param user: User: Filter the contacts by user
    :return: A list of contacts whose birthday is in the next days_range days
    :doc-author: Trelent
    """
    today = datetime.today().date()
    start_period = today.strftime('%m-%d')
    end_period = (today + timedelta(days_range)).strftime('%m-%d')
    statement = select(Contact).filter_by(user=user).filter(func.to_char(Contact.birthday, 'MM-DD').between(start_period, end_period))
    contacts = await db.execute(statement)
    return contacts.scalars().all()


async def get_contact(contact_id: int, db: AsyncSession, user: User):
    """
    The get_contact function returns a contact from the database.

    :param contact_id: int: Specify the contact's id
    :param db: AsyncSession: Pass the database session to the function
    :param user: User: Get the user from the database
    :return: A contact object
    :doc-author: Trelent
    """
    statement = select(Contact).filter_by(id=contact_id, user=user)
    contact = await db.execute(statement)
    return contact.scalar_one_or_none()


async def create_contact(body: ContactSchema, db: AsyncSession, user: User):
    """
    The create_contact function creates a new contact in the database.

    :param body: ContactSchema: Validate the request body
    :param db: AsyncSession: Pass the database session to the function
    :param user: User: Get the user id from the token
    :return: A contact object
    :doc-author: Trelent
    """
    contact = Contact(**body.model_dump(exclude_unset=True), user=user)
    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactSchema, db: AsyncSession, user: User):
    """
    The update_contact function updates a contact in the database.
        Args:
            contact_id (int): The id of the contact to update.
            body (ContactSchema): A ContactSchema object containing all fields for a new Contact object.
            db (AsyncSession): An async session with an open transaction to use for querying and updating
            data in the database.  This is provided by FastAPI via Dependency Injection, so you don't need
            to worry about it!  Just make sure you include it as an argument in your function definition,
            and FastAPI will handle passing this parameter when calling your function!

    :param contact_id: int: Identify the contact that will be deleted
    :param body: ContactSchema: Create a new contact object
    :param db: AsyncSession: Get the database session
    :param user: User: Get the user from the request
    :return: The updated contact
    :doc-author: Trelent
    """
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
    """
    The delete_contact function deletes a contact from the database.

    :param contact_id: int: Specify the contact to delete
    :param db: AsyncSession: Pass in the database session
    :param user: User: Ensure that the user is only deleting their own contacts
    :return: The contact that was deleted
    :doc-author: Trelent
    """
    statement = select(Contact).filter_by(id=contact_id, user=user)
    result = await db.execute(statement)
    contact = result.scalar_one_or_none()
    if contact:
        await db.delete(contact)
        await db.commit()
    return contact