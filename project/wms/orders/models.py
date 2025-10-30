from django.db import models
from accounts.models import accounts , Roles
from inventory.models import ProductStock
# Create your models here.
class status(models.Model):
    name = models.CharField(max_length=20 , unique=True)
    def __str__(self):
        return self.name
class CanConvertTo(models.Model):
    fromstatus = models.ForeignKey(
        status,
        on_delete=models.CASCADE,
        related_name='can_convert_from'
    )
    tostatus = models.ForeignKey(
        status,
        on_delete=models.CASCADE,
        related_name='can_convert_to'
    )
    allowed_rolls = models.ManyToManyField(Roles , blank=True)
    
    def __str__(self):
        return f"from {self.fromstatus} To {self.tostatus}"
class order(models.Model):
    owner = models.ForeignKey(accounts , on_delete=models.CASCADE , related_name='owner')
    driver = models.ForeignKey(accounts , on_delete=models.CASCADE , related_name='driver' , null=True , blank=True)
    status = models.ForeignKey(status , on_delete=models.CASCADE , default=1)
    created_at = models.DateTimeField(auto_now_add=True , null=True)
    def __str__(self):
        if not self.driver:
            return f"Owner {self.owner.username} , driver Not Assigned ,  status {self.status.name}"
        return f"Owner {self.owner.username} , driver {self.driver.username} ,  status {self.status.name}"
class orderitems(models.Model):
    order_f = models.ForeignKey(order , on_delete=models.CASCADE)
    product = models.ForeignKey(ProductStock  , on_delete=models.CASCADE)
    qty = models.IntegerField(default=1)
    def __str__(self):
        return f"{self.product.product.name}"