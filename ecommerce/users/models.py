from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, username, name, email, password=None):
        if not username:
            raise TypeError("user manager should has username.")
        if not email:
            raise TypeError("user manager should has email.")
        if not name:
            raise TypeError("user manager should has name.")
        if not password:
            raise TypeError("you should add password.")

        user = self.model(
            email=self.normalize_email(email), name=name, username=username
        )

        user.set_password(password)
        user.save()
        return user

   

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_("Username"), max_length=100, unique=True)
    name = models.CharField(_("Full Name"), max_length=255, db_index=True)
    email = models.EmailField(_("Email"), max_length=255, unique=True)
    is_verified = models.BooleanField(_("Is user verified by email"), default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=now)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "name"]

    objects = UserManager()

    def __str__(self):
        return self.username