from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from django.contrib.postgres.fields import ArrayField

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, username, password):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")
        if not password:
            raise ValueError("Users must have a password")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username
        )

        user.is_staff, user.is_superuser = True, True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=32, unique=True, primary_key=True)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["email"]

    objects = UserManager()

    def __str__(self):
        return self.username

    def make_admin(self):
        is_staff, is_superuser = True, True

    def make_staff(self):
        is_staff, is_superuser = True, False

    def make_normal(self):
        is_staff, is_superuser = False, False

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser


class Character(models.Model):
    owner = models.ForeignKey(User, on_delete=models.PROTECT)
    name = models.CharField(max_length=32, unique=True, primary_key=True)

    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=32, unique=False)
    type = models.CharField(
        max_length=10,
        blank=True,
    )

    enhancements = ArrayField(
        models.CharField(max_length=10, blank=False),
        size=4,
    )
    owner = models.ForeignKey(Character, on_delete=models.PROTECT)

    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.name
