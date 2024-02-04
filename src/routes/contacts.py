from fastapi import APIRouter, HTTPException, Depends, status, Path, Query
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.entity.models import User
from src.repository import contacts as repositories_contacts
from src.schemas.contact import ContactSchema, ContactResponse
from src.services.auth import auth_service

router = APIRouter(prefix='/contacts', tags=['Contacts'])


@router.get("/", response_model=list[ContactResponse],
            dependencies=[Depends(RateLimiter(times=1, seconds=20))])
async def get_contacts(name: str = Query(None, min_length=1, max_length=50),
                        surname: str = Query(None, min_length=1, max_length=50),
                        email: str = Query(None, min_length=1, max_length=50),
                        limit: int = Query(10, ge=10, le=500),
                        offset: int = Query(0, ge=0),
                        db: AsyncSession = Depends(get_db),
                        user: User = Depends(auth_service.get_current_user)):
    """
    The get_contacts function returns a list of contacts.

    :param name: str: Filter the contacts by name
    :param min_length: Set the minimum length of the query parameter
    :param max_length: Limit the length of the name, surname and email parameters
    :param surname: str: Filter contacts by surname
    :param min_length: Specify the minimum length of a string
    :param max_length: Limit the length of the input string
    :param email: str: Filter the contacts by email
    :param min_length: Specify the minimum length of the query parameter
    :param max_length: Limit the length of a string
    :param limit: int: Limit the number of contacts returned
    :param ge: Specify the minimum value of a parameter
    :param le: Limit the number of contacts that can be returned
    :param offset: int: Specify the number of records to skip
    :param ge: Specify the minimum value for a parameter, and le is used to specify the maximum value
    :param db: AsyncSession: Get the database connection
    :param user: User: Get the current user from the database
    :return: A list of contacts
    :doc-author: Trelent
    """
    contacts = await repositories_contacts.get_contacts(name, surname, email, limit, offset, db, user)
    return contacts


@router.get("/birthdays", response_model=list[ContactResponse],
            dependencies=[Depends(RateLimiter(times=1, seconds=20))])
async def get_upcoming_birthdays(days_range: int = 7, db: AsyncSession = Depends(get_db),
                                 user: User = Depends(auth_service.get_current_user)):
    """
    The get_upcoming_birthdays function returns a list of contacts with upcoming birthdays.
    The days_range parameter specifies the number of days in the future to look for birthdays.
    The default value is 7, which means that it will return all contacts with birthdays within
    the next week.

    :param days_range: int: Specify how many days in the future to look for birthdays
    :param db: AsyncSession: Get the database session
    :param user: User: Get the current user, and the db: asyncsession parameter is used to get a database session
    :return: A list of contacts with upcoming birthdays
    :doc-author: Trelent
    """
    contacts = await repositories_contacts.get_upcoming_birthdays(days_range, db, user)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse,
            dependencies=[Depends(RateLimiter(times=1, seconds=20))])
async def get_contact(contact_id: int = Path(ge=1), db: AsyncSession = Depends(get_db),
                      user: User = Depends(auth_service.get_current_user)):
    """
    The get_contact function is a GET request that returns the contact with the given ID.
    If no such contact exists, it will return a 404 NOT FOUND error.

    :param contact_id: int: Specify the id of the contact to be retrieved
    :param db: AsyncSession: Pass the database session to the repository
    :param user: User: Get the current user
    :return: A contact object
    :doc-author: Trelent
    """
    contact = await repositories_contacts.get_contact(contact_id, db, user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return contact


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(RateLimiter(times=1, seconds=20))])
async def create_contact(body: ContactSchema, db: AsyncSession = Depends(get_db),
                         user: User = Depends(auth_service.get_current_user)):
    """
    The create_contact function creates a new contact in the database.

    :param body: ContactSchema: Validate the request body
    :param db: AsyncSession: Pass the database connection to the repository
    :param user: User: Get the current user from the auth_service
    :return: A contactschema object
    :doc-author: Trelent
    """
    contact = await repositories_contacts.create_contact(body, db, user)
    return contact


@router.put("/{contact_id}", response_model=ContactResponse,
            dependencies=[Depends(RateLimiter(times=1, seconds=20))])
async def update_contact(body: ContactSchema, contact_id: int = Path(ge=1), db: AsyncSession = Depends(get_db),
                         user: User = Depends(auth_service.get_current_user)):
    """
    The update_contact function updates a contact in the database.
        It takes an id, body and db as parameters. The id is used to find the contact in the database,
        while body contains all of the information that will be updated for that specific contact.
        The db parameter is used to connect with our PostgreSQL database.

    :param body: ContactSchema: Validate the request body
    :param contact_id: int: Get the contact id from the path
    :param db: AsyncSession: Get the database session from the dependency injection
    :param user: User: Get the current user from the auth_service
    :return: A contactschema object
    :doc-author: Trelent
    """
    contact = await repositories_contacts.update_contact(contact_id, body, db, user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(RateLimiter(times=1, seconds=20))])
async def delete_contact(contact_id: int = Path(ge=1), db: AsyncSession = Depends(get_db),
                         user: User = Depends(auth_service.get_current_user)):
    """
    The delete_contact function deletes a contact from the database.

    :param contact_id: int: Specify the id of the contact to be deleted
    :param db: AsyncSession: Get the database session
    :param user: User: Get the current user from the auth_service
    :return: A contact object
    :doc-author: Trelent
    """
    contact = await repositories_contacts.delete_contact(contact_id, db, user)
    return contact