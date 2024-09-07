from django.db import models
from herbs.models import Tovar, TovarVariation
from users.models import User

class  CartQueryset(models.QuerySet):
    
    def total_price(self):
        return sum(cart.products_price() for cart in self)
    
    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
        return 0


class Cart(models.Model):

    user = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True, verbose_name="User")
    product = models.ForeignKey(to=Tovar, on_delete=models.CASCADE, verbose_name="Product")
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name="Quantity")
    session_key = models.CharField(max_length=32, blank=True, null=True)
    variation = models.ForeignKey(TovarVariation, on_delete=models.SET_NULL, null=True, blank=True)
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name="timestamp")

    class Meta:
        db_table = "cart"
        verbose_name = "Basket"
        verbose_name_plural = "Basket"

    objects = CartQueryset().as_manager()


    def products_price(self):
        '''if self.product.discount:
            self.product.price_after_discount = self.product.price * (1 - self.product.discount / 100)
            return round(self.product.price_after_discount * self.quantity, 2)
        else:
        return round(self.product.price * self.quantity, 2)'''
        if self.variation:
            price = self.variation.price
        else:
            price = self.product.price
        return round(price * self.quantity, 2)
        

    def __str__(self):
        if self.user:
            return f"Basket {self.user.username} | Product {self.product.title} | Count {self.quantity}"
        return f"Anonim carts | Product {self.product.title} | Count {self.quantity}"


