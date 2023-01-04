import uuid
from django.db import models
import os
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin,
)

fpoint = open(os.path.abspath(   os.path.join(os.path.dirname(__file__), 'default_point.txt')), 'r', encoding='UTF-8')
default_point = fpoint.read()
fpoint.close()
class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(
            username=username,
            email=self.normalize_email(email),
            password=password,
        )
        user.is_admin=True
        user.is_staff=True
        user.is_superuser=True
        user.save(using=self._db)
        return user
#ユーザーアカウントのモデルクラス
class Account(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(verbose_name='username',max_length=100, blank=True,null=True,default='',)
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, db_index=True)
    unused_point = models.FloatField(default=default_point)
    exp = models.FloatField(default=0)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.username
