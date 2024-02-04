import unittest
from unittest.mock import MagicMock, AsyncMock, patch

from sqlalchemy.ext.asyncio import AsyncSession

from src.entity.models import User
from src.schemas.user import UserSchema
from src.repository.users import get_user_by_email, create_user, update_token, confirmed_email, update_avatar_url


class TestAsyncContact(unittest.IsolatedAsyncioTestCase):

    def setUp(self) -> None:
        self.user = User(
            id=1,
            username='test_user',
            password='test_password',
            confirmed=True)
        self.session = AsyncMock(spec=AsyncSession)

    async def test_create_user(self):
        user = UserSchema(username='test_username_1', password='test_password_1', email='test_email_1@ukr.net')
        self.session.commit.return_value = None
        result = await create_user(body=user, db=self.session)
        self.assertTrue(hasattr(result, "id"))
        self.assertEqual(result.username, user.username)
        self.assertEqual(result.password, user.password)
        self.assertEqual(result.email, user.email)

    async def test_get_user_by_email(self):
        mocked_user = MagicMock()
        mocked_user.scalar_one_or_none.return_value = self.user
        self.session.execute.return_value = mocked_user
        result = await get_user_by_email(email='test_email_1@ukr.net', db=self.session)
        self.assertEqual(result, self.user)

    @patch('src.repository.users.User')
    async def test_update_token(self, Mock_User):
        mock_user = Mock_User.return_value
        token = 'new token'
        await update_token(mock_user, token, self.session)
        self.assertEqual(token, mock_user.refresh_token)
        self.session.commit.assert_called_once()

    @patch('src.repository.users.get_user_by_email')
    async def test_confirmed_email(self, MockGetUserByEmail):
        mock_get = MockGetUserByEmail.return_value = User()
        await confirmed_email('test_email_1@ukr.net', self.session)
        self.assertEqual(mock_get.confirmed, True)
        self.session.commit.assert_called_once()

    @patch('src.repository.users.get_user_by_email', new_callable=AsyncMock)
    async def test_update_avatar_url(self, MockGetUserByEmail):
        mock_get = MockGetUserByEmail.return_value = User()
        result = await update_avatar_url('test_email_1@ukr.net', 'test_url', self.session)
        self.assertEqual(mock_get.avatar, 'test_url')
        self.assertEqual(result.avatar, 'test_url')
        self.session.commit.assert_called_once()
        self.assertEqual(result, mock_get)

