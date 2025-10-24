from django.db import models
from django.conf import settings
from accounts.models import accounts
from inventory.models import ProductStock


class Cart(models.Model):
    user = models.ForeignKey(accounts, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart ({self.id}) - User: {self.user}"

    def total_items(self):
        return sum(item.quantity for item in self.items.all())

    def total_price(self):
        return sum(item.quantity * item.product.price for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(ProductStock, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('cart', 'product')  # منع تكرار نفس المنتج في نفس السلة

    def __str__(self):
        return f"{self.product.product.name} ({self.quantity})"

    def subtotal(self):
        return self.quantity * self.product.price