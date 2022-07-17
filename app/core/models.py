from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('User must have an email address.')
        # self to access the model we are associated with.
        user = self.model(email=self.normalize_email(email), **extra_fields)
        # sets the password with ecryption using hashing,
        # so its one-way encryption
        user.set_password(password)
        # using sel._db , just to support adding multiple dbs
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        # is_staff = True allows us to login to django admin
        # is_superuser allows us to access everything inside django app
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # assigns custom user manager
    objects = UserManager()

    # field taht we want to use for authentication,
    # replaces the default username field that comes with user model
    USERNAME_FIELD = 'email'
