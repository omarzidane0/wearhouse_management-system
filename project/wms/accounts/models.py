from django.db import models
from datetime import datetime , timedelta
from django.utils import timezone

# Create your models here.
def default_expire():
    return timezone.now() + timedelta(minutes=2)

class Roles(models.Model):
    role = models.CharField(max_length=15 , unique=True)
    can_add_users = models.BooleanField(default=False)
    can_create_orders = models.BooleanField(default=False)
    can_deliver_orders = models.BooleanField(default=False)
    can_add_products = models.BooleanField(default=False)
    can_manage_orders = models.BooleanField(default=False)
    home_href = models.CharField(max_length=20 , default="home")
    def __str__(self):
        return f"Role is {self.role}"
    

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Roles'
        verbose_name_plural = 'Roles'

class accounts(models.Model):
    username = models.CharField(max_length=50 , unique=True)
    email =  models.EmailField(max_length=40,unique=True)
    password = models.CharField(max_length=25)
    role = models.ForeignKey("Roles", on_delete=models.CASCADE , null=False , default=0)
    phone_num = models.IntegerField(default=000)

    def __str__(self):
        return f"username is {self.username} password is {self.password} email is {self.email} "

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'accounts'
        verbose_name_plural = 'accounts'

class password_token(models.Model):

    email = models.EmailField(max_length=80 ,null=False )
    token = models.CharField(max_length=80)
    expire_date = models.DateTimeField(default=default_expire)



    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'password_token'
        verbose_name_plural = 'password_tokens'

