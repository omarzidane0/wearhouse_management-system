from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(order)
admin.site.register(orderitems)
admin.site.register(status)
admin.site.register(CanConvertTo)
