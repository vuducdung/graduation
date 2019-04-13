from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.contrib.auth.models import UserManager


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        # role = Roles.objects.get(id="2").first()
        user = self.model(
            email=self.normalize_email(email),

        )
        # user.role = role

        user.set_password(password)
        user.save(using=self._db)
        return user
    #
    # def create_superuser(self, email, date_of_birth, password):
    #     """
    #     Creates and saves a superuser with the given email, date of
    #     birth and password.
    #     """
    #     user = self.create_user(
    #         email,
    #         password=password,
    #         date_of_birth=date_of_birth,
    #     )
    #     user.is_admin = True
    #     user.save(using=self._db)
    #     return user


class Roles(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Accounts(AbstractBaseUser):
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # date_of_birth = models.DateField()
    is_active = models.BooleanField(default=False)
    # status = models.CharField(max_length=20)
    # nickName = models.CharField(max_length=255)
    role = models.ForeignKey(Roles, on_delete=models.CASCADE, default=2)
    avatar=models.CharField(max_length=255, default="#")


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = MyUserManager()
