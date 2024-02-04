import unittest
from unittest.mock import MagicMock, AsyncMock

from sqlalchemy.ext.asyncio import AsyncSession

from src.entity.models import Contact, User
from src.schemas.contact import ContactSchema
from src.repository.contacts import create_contact, get_contacts, get_contact, update_contact, delete_contact


class TestAsyncContact(unittest.IsolatedAsyncioTestCase):

    def setUp(self) -> None:
        self.user = User(
            id=1,
            username='test_user',
            password='test_password',
            confirmed=True)
        self.session = AsyncMock(spec=AsyncSession)

    async def test_get_contacts(self):
        limit = 10
        offset = 0
        contacts = [Contact(id=1, name='test_name_1', surname='test_surname_1', email='test_1@ukr.net',
                            phone='+380671111111', birthday='1985-02-01', user=self.user),
                    Contact(id=2, name='test_name_2', surname='test_surname_2', email='test_2@ukr.net',
                            phone='+380672222222', birthday='1985-02-02', user=self.user),
                    Contact(id=3, name='test_name_3', surname='test_surname_3', email='test_3@ukr.net',
                            phone='+380673333333', birthday='1985-02-03', user=self.user)]
        mocked_contacts = MagicMock()
        mocked_contacts.scalars.return_value.all.return_value = contacts
        self.session.execute.return_value = mocked_contacts
        result = await get_contacts(None, None, None, limit, offset, self.session, self.user)
        self.assertEqual(result, contacts)

        # Search by name
        result = await get_contacts('test_name_1', None, None, limit, offset, self.session, self.user)
        test_result = [contacts[0]]
        self.assertEqual([result[0]], test_result)

        # Search by surname
        result = await get_contacts(None, 'test_surname_2', None, limit, offset, self.session, self.user)
        test_result = [contacts[1]]
        self.assertEqual([result[1]], test_result)

        # Search by email
        result = await get_contacts(None, None, 'test_3@ukr.net', limit, offset, self.session, self.user)
        test_result = [contacts[2]]
        self.assertEqual([result[2]], test_result)

    async def test_get_contact(self):
        contact = Contact(id=1, name='test_name_1', surname='test_surname_1', email='test_1@ukr.net',
                          phone='+380671111111', birthday='1985-02-01', user=self.user)
        mocked_contact = MagicMock()
        mocked_contact.scalar_one_or_none.return_value = contact
        self.session.execute.return_value = mocked_contact
        result = await get_contact(1, self.session, self.user)
        self.assertEqual(result, contact)

    async def test_create_contact(self):
        body = ContactSchema(name='test_name_1', surname='test_surname_1', email='test_1@ukr.net',
                             phone='+380671111111', birthday='1985-02-01')
        result = await create_contact(body, self.session, self.user)
        self.assertIsInstance(result, Contact)
        self.assertEqual(result.name, body.name)
        self.assertEqual(result.surname, body.surname)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone, body.phone)
        self.assertEqual(result.birthday, body.birthday)

    async def test_update_contact(self):
        body = ContactSchema(name='test_update_name_1', surname='test_update_surname_1', email='test_update_1@ukr.net',
                             phone='+380671111111', birthday='1985-02-01')
        mocked_contact = MagicMock()
        mocked_contact.scalar_one_or_none.return_value = Contact(id=1, name='test_name_1', surname='test_surname_1',
                                                                 email='test_1@ukr.net', phone='+380671111111',
                                                                 birthday='1985-02-01', user=self.user)
        self.session.execute.return_value = mocked_contact
        result = await update_contact(1, body, self.session, self.user)
        self.assertIsInstance(result, Contact)
        self.assertEqual(result.name, body.name)
        self.assertEqual(result.surname, body.surname)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone, body.phone)
        self.assertEqual(result.birthday, body.birthday)

    async def test_delete_contact(self):
        mocked_contact = MagicMock()
        mocked_contact.scalar_one_or_none.return_value = Contact(id=1, name='test_name_1', surname='test_surname_1',
                                                                 email='test_1@ukr.net', phone='+380671111111',
                                                                 birthday='1985-02-01', user=self.user)
        self.session.execute.return_value = mocked_contact
        result = await delete_contact(1, self.session, self.user)
        self.session.delete.assert_called_once()
        self.session.commit.assert_called_once()
        self.assertIsInstance(result, Contact)