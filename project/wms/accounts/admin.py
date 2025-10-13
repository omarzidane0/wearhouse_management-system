from django.contrib import admin
from .models import accounts , Roles , password_token 
# Register your models here.

admin.site.register(Roles)
admin.site.register(accounts)
admin.site.register(password_token)

