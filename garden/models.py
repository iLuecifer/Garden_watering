from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, username, email, password):
        user = self.create_user(
            username=username,
            email=email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    username = models.CharField(max_length=255, unique=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class SensorValue(models.Model):
    id = models.AutoField(primary_key=True)
    air_temp = models.FloatField()
    pressure = models.FloatField()
    air_hum = models.FloatField()
    soil_hum = models.FloatField()
    soil_temp = models.FloatField()
    light = models.FloatField()
    timestamp = models.DateTimeField()
    status = models.BooleanField(default=False)
    class Meta:
        app_label = 'garden'

class BustedPictures(models.Model):
    id = models.AutoField(primary_key = True)
    picture = models.ImageField(upload_to='busted_pictures/')
    timestamp = models.DateTimeField(auto_now=True)
    class Meta:
        app_label = 'garden'

class WaterPumpeLogs(models.Model):
    id = models.AutoField(primary_key = True)
    start = models.DateTimeField(auto_now=True)
    end = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    class Meta:
        app_label = 'garden'

