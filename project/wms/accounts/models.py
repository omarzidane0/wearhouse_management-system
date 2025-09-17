from django.db import models
from datetime import datetime , timedelta
from django.utils import timezone

# Create your models here.
def default_expire():
    return timezone.now() + timedelta(minutes=2)

class accounts(models.Model):
    username = models.CharField(max_length=50 , unique=True)
    email =  models.EmailField(max_length=40,unique=True)
    password = models.CharField(max_length=25)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return f"username is {self.username} password is {self.password} email is {self.email} is_admin {self.is_admin}"

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'accounts'
        verbose_name_plural = 'accounts'

class password_token(models.Model):

    email = models.EmailField(max_length=80 ,null=False )
    token = models.CharField(max_length=80)
    expire_date = models.DateTimeField(default=default_expire)

    def __str__(self):
        pass

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'password_token'
        verbose_name_plural = 'password_tokens'

