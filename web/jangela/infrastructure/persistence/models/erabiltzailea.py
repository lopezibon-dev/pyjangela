from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

from jangela.domain.enums.rola import Rola
from jangela.infrastructure.persistence.models.choices import enum_choices, enum_max_length


class ErabiltzaileaManager(BaseUserManager):
    """Erabiltzaileak email bidez sortzeko managerra (username gabe)."""

    use_in_migrations = True

    def _sortu(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Emaila derrigorrezkoa da.")
        email = self.normalize_email(email)
        erabiltzailea = self.model(email=email, **extra_fields)
        # Pasahitza hash moduan gordetzen da (1. araua)
        erabiltzailea.set_password(password)
        erabiltzailea.save(using=self._db)
        return erabiltzailea

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._sortu(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser-ak is_staff=True izan behar du.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser-ak is_superuser=True izan behar du.")
        return self._sortu(email, password, **extra_fields)


class ErabiltzaileaModel(AbstractUser):
    """Erabiltzailea: saioa emailarekin hasten da (username gabe)."""

    username = None
    # Email bakarra (1. araua)
    email = models.EmailField(unique=True)
    # Rol bakarra (2. araua)
    rola = models.CharField(max_length=enum_max_length(Rola), choices=enum_choices(Rola))
    # Menu beganoaren hobespena (16. araua)
    beganoa = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "rola"]

    objects = ErabiltzaileaManager()

    class Meta:
        db_table = "erabiltzailea"

    def __str__(self):
        return self.email
