from typing import Optional, Self
from django.contrib.auth.models import AbstractBaseUser as DjangoAbstractBaseUser
from django.core.exceptions import ValidationError
from core.utilities import clear_Nones, uuid
from core.utilities.test import AbstractModelTestCase
from users.abstract_models import UserEmailMixin, UserUsernameMixin
from users.managers import UserManager
from users.tests import VALID_PASSWORD, generate_valid_email


class TestAbstractUserWithEmail(AbstractModelTestCase):
    """Test using the UserEmailMixin."""

    class UserWithEmail(UserEmailMixin, DjangoAbstractBaseUser):  # type: ignore # _meta issue
        USERNAME_FIELD = "email"
        objects = UserManager[Self]()

    MODELS = [UserWithEmail]

    def sample_user(
        self,
        *,
        id: Optional[str] = None,
        email: Optional[str] = None,
        password: str = VALID_PASSWORD,
        is_staff: Optional[bool] = None,
        is_superuser: Optional[bool] = None,
        is_active: Optional[bool] = None,
    ) -> UserWithEmail:
        """
        Create a sample user with the following default values:
        - `id`: auto-generated
        - `email`: unique valid email
        - `password`: pre-defined valid password
        - `is_staff`: default value
        - `is_superuser`: default value
        """
        if email is None:
            email = generate_valid_email()
        return self.UserWithEmail.objects.create_user(
            **clear_Nones(
                id=id,
                email=email,
                password=password,
                is_staff=is_staff,
                is_superuser=is_superuser,
                is_active=is_active,
            )
        )

    def test_create_user(self) -> None:
        """Test creating a UserWithEmail."""
        email = generate_valid_email()
        password = VALID_PASSWORD
        user = self.UserWithEmail.objects.create_user(email=email, password=password)
        self.assertEqual(email, user.get_username())
        self.assertEqual(email, user.email)
        self.assertNotEqual(password, user.password)
        self.assertTrue(user.check_password(password))

    def test_email_required(self) -> None:
        """Test creating a UserWithEmail without an email fails."""
        with self.assertRaises(ValidationError) as ctx:
            self.UserWithEmail.objects.create_user(password=VALID_PASSWORD)
        self.assertIn(ValidationError("Email cannot be empty."), ctx.exception.error_list)

    def test_email_invalid_fails(self) -> None:
        """Test creating a UserWithEmail with an invalid email fails."""
        with self.assertRaises(ValidationError) as ctx:
            self.UserWithEmail.objects.create_user(email="_invalid_email", password=VALID_PASSWORD)
        self.assertIn(ValidationError("Email is invalid."), ctx.exception.error_list)

    def test_email_normalized(self) -> None:
        """Test that emails are normalized for UserWithEmail."""
        sample_emails = [
            ("test1@EXAMPLE.com", "test1@example.com"),
            ("TEST2@example.com", "TEST2@example.com"),
            ("TEST3@EXAMPLE.com", "TEST3@example.com"),
            ("test4@example.COM", "test4@example.com"),
        ]
        for email, expected in sample_emails:
            with self.subTest(msg="Checking if email is normalized.", email=email, expected=expected):
                user = self.sample_user(email=email)
                self.assertEqual(expected, user.email)

    def test_email_changes_normalized(self) -> None:
        """Test that emails are normalized when updating a user."""
        user = self.sample_user()
        email, expected = ("test1@EXAMPLE.com", "test1@example.com")
        user.email = email
        user.save()
        self.assertEqual(expected, user.email)


class TestAbstractUserWithUsername(AbstractModelTestCase):
    """Test using the UserUsernameMixin."""

    class UserWithUsername(UserUsernameMixin, DjangoAbstractBaseUser):  # type: ignore # _meta issue
        USERNAME_FIELD = "username"
        objects = UserManager[Self]()

    MODELS = [UserWithUsername]

    def test_create_user(self) -> None:
        """Test creating a UserWithUsername."""
        username = uuid()
        password = VALID_PASSWORD
        user = self.UserWithUsername.objects.create_user(username=username, password=password)
        self.assertEqual(username, user.get_username())
        self.assertEqual(username, user.username)
        self.assertNotEqual(password, user.password)
        self.assertTrue(user.check_password(password))

    def test_username_required(self) -> None:
        """Test creating a UserWithUsername without a username fails."""
        with self.assertRaises(ValidationError) as ctx:
            self.UserWithUsername.objects.create(password=VALID_PASSWORD)
        self.assertIn(ValidationError("Username cannot be empty."), ctx.exception.error_list)


class TestCombinedUserEmail(AbstractModelTestCase):
    """Test using both UserEmailMixin and UserUsernameMixin, while having "email" as the primary field."""

    class CombinedUserEmail(UserEmailMixin, UserUsernameMixin, DjangoAbstractBaseUser):  # type: ignore # _meta issue
        USERNAME_FIELD = "email"
        objects = UserManager[Self]()

    MODELS = [CombinedUserEmail]

    def test_REQUIRED_FIELDS(self) -> None:
        """Test the `REQUIRED_FIELDS` class property."""
        fields = self.CombinedUserEmail.REQUIRED_FIELDS
        self.assertNotIn("email", fields)  # USERNAME_FIELD
        self.assertNotIn("username", fields)

    def test_create_user(self) -> None:
        """Test creating a CombinedUseremail."""
        email = generate_valid_email()
        username = uuid()
        password = VALID_PASSWORD
        user = self.CombinedUserEmail.objects.create_user(email=email, username=username, password=VALID_PASSWORD)
        self.assertEqual(email, user.get_username())
        self.assertEqual(email, user.email)
        self.assertEqual(username, user.username)
        self.assertNotEqual(password, user.password)
        self.assertTrue(user.check_password(password))

    def test_create_user_no_username(self) -> None:
        """Test that username is not a required field."""
        email = generate_valid_email()
        password = VALID_PASSWORD
        user = self.CombinedUserEmail.objects.create_user(email=email, password=VALID_PASSWORD)
        self.assertEqual(email, user.email)
        self.assertEqual("", user.username)
        self.assertTrue(user.check_password(password))


class TestCombinedUserEmailRequireUsername(AbstractModelTestCase):
    """Extension of the above class `TestCombinedUserEmail, to certifications with `REQUIRE_USERNAME = True`."""

    # 'type: ignore'd because of _meta issue
    class CombinedUserEmailRequireUsername(UserEmailMixin, UserUsernameMixin, DjangoAbstractBaseUser):  # type: ignore
        USERNAME_FIELD = "email"
        REQUIRE_USERNAME = True
        objects = UserManager[Self]()

    MODELS = [CombinedUserEmailRequireUsername]

    def test_REQUIRED_FIELDS(self) -> None:
        """Test the `REQUIRED_FIELDS` class property."""
        fields = self.CombinedUserEmailRequireUsername.REQUIRED_FIELDS
        self.assertNotIn("email", fields)  # USERNAME_FIELD
        self.assertIn("username", fields)

    def test_create_user_no_username_fails(self) -> None:
        """Test that username is a required field."""
        email = generate_valid_email()
        with self.assertRaises(ValidationError) as ctx:
            self.CombinedUserEmailRequireUsername.objects.create_user(email=email, password=VALID_PASSWORD)
        self.assertIn(ValidationError("Username cannot be empty."), ctx.exception.error_list)

    def test_create_user_empty_username_fails(self) -> None:
        """Test that username is a required field."""
        email = generate_valid_email()
        username = ""
        with self.assertRaises(ValidationError) as ctx:
            self.CombinedUserEmailRequireUsername.objects.create_user(
                email=email, username=username, password=VALID_PASSWORD
            )
        self.assertIn(ValidationError("Username cannot be empty."), ctx.exception.error_list)


class TestCombinedUserUsername(AbstractModelTestCase):
    """Test using both UserEmailMixin and UserUsernameMixin, while having "username" as the primary field."""

    # 'type: ignore'd because of _meta issue
    class CombinedUserUsername(UserEmailMixin, UserUsernameMixin, DjangoAbstractBaseUser):  # type: ignore
        USERNAME_FIELD = "username"
        objects = UserManager[Self]()

    MODELS = [CombinedUserUsername]

    def test_REQUIRED_FIELDS(self) -> None:
        """Test the `REQUIRED_FIELDS` class property."""
        fields = self.CombinedUserUsername.REQUIRED_FIELDS
        self.assertNotIn("username", fields)  # USERNAME_FIELD
        self.assertNotIn("email", fields)

    def test_create_user(self) -> None:
        """Test creating a CombinedUserUsername."""
        username = uuid()
        email = generate_valid_email()
        password = VALID_PASSWORD
        user = self.CombinedUserUsername.objects.create_user(username=username, email=email, password=VALID_PASSWORD)
        self.assertEqual(username, user.get_username())
        self.assertEqual(username, user.username)
        self.assertEqual(email, user.email)
        self.assertNotEqual(password, user.password)
        self.assertTrue(user.check_password(password))

    def test_create_user_no_email(self) -> None:
        """Test that username is not a required field."""
        username = uuid()
        password = VALID_PASSWORD
        user = self.CombinedUserUsername.objects.create_user(username=username, password=VALID_PASSWORD)
        self.assertEqual(username, user.username)
        self.assertEqual("", user.email)
        self.assertTrue(user.check_password(password))


class TestCombinedUserUsernameRequireEmail(AbstractModelTestCase):
    """Extension of the above class `TestCombinedUserUsername, to certifications with `REQUIRE_EMAIL = True`."""

    # 'type: ignore'd because of _meta issue
    class CombinedUserUsernameRequireEmail(UserEmailMixin, UserUsernameMixin, DjangoAbstractBaseUser):  # type: ignore
        USERNAME_FIELD = "username"
        REQUIRE_EMAIL = True
        objects = UserManager[Self]()

    MODELS = [CombinedUserUsernameRequireEmail]

    def test_REQUIRED_FIELDS(self) -> None:
        """Test the `REQUIRED_FIELDS` class property."""
        fields = self.CombinedUserUsernameRequireEmail.REQUIRED_FIELDS
        self.assertNotIn("username", fields)  # USERNAME_FIELD
        self.assertIn("email", fields)

    def test_create_user_no_email_fails(self) -> None:
        """Test that username is a required field."""
        username = uuid()
        with self.assertRaises(ValidationError) as ctx:
            self.CombinedUserUsernameRequireEmail.objects.create_user(username=username, password=VALID_PASSWORD)
        self.assertIn(ValidationError("Email cannot be empty."), ctx.exception.error_list)

    def test_create_user_empty_email_fails(self) -> None:
        """Test that username is a required field."""
        username = uuid()
        email = ""
        with self.assertRaises(ValidationError) as ctx:
            self.CombinedUserUsernameRequireEmail.objects.create_user(
                username=username, email=email, password=VALID_PASSWORD
            )
        self.assertIn(ValidationError("Email cannot be empty."), ctx.exception.error_list)
