from django.db import models

# Create your models here.

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