from app.models import DataTupel, Column
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None,
                    is_admin=False, is_data_analyst=False, is_simulation_engineer=False, is_data_owner=False, **kwargs):
        if username is None:
            raise TypeError('Users must have a username.')
        if email is None:
            raise TypeError('Users must have an email.')

        user = self.model(username=username, email=self.normalize_email(email),
                          is_admin=is_admin, is_data_analyst=is_data_analyst, is_simulation_engineer=is_simulation_engineer, is_data_owner=is_data_owner)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, email, password):
        if password is None:
            raise TypeError('Superusers must have a password.')
        if email is None:
            raise TypeError('Superusers must have an email.')
        if username is None:
            raise TypeError('Superusers must have an username.')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_data_analyst = models.BooleanField(default=False)
    is_simulation_engineer = models.BooleanField(default=False)
    is_data_owner = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def __str__(self):
        return f"{self.email}"

    def getMetaData(self, id):
        meta_data = self.metadata_set.get(pk=id).first()
        if (meta_data):
            columns = meta_data.column_set.values_list('id', flat=True)
            return DataTupel.objects.filter(pk__in=columns)

    def getColumnData(self, id=None, name=None):
        if (not name == None):
            column = Column.objects.filter(name=name).first()
            if (column):
                return column.datatupel_set.all()

        if (not id == None):
            return DataTupel.objects.filter(column_id=id)

        return []
