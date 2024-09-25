from django.db import models
from herbs.models import Tovar
from users.models import User

class OrderitemQueryset(models.QuerySet):
    def total_price(self):
        return sum(cart.products_price() for cart in self)
    
    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
        return 0

class Order(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.SET_DEFAULT, blank=True, null=True, verbose_name='User', default=None)
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Time of create')
    phone_number = models.CharField(max_length=50, default='Phone number')
    delivery_address = models.TextField(null=True, blank=True, verbose_name='Delivery data' )
    e_mail = models.EmailField(verbose_name='Email',)
    is_paid = models.BooleanField(default=False, verbose_name='Is paid')
    status = models.CharField(max_length=50, default='In process', verbose_name='Status of order')

    class Meta:
        db_table = 'order'

    def __str__(self):
        if self.user:
            return f"Order N {self.pk} | Customer {self.user.first_name} {self.user.last_name}"
        else:
            return f"Order N {self.pk} | Customer Anonymous"

class OrderItem(models.Model):
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE, verbose_name='Order')
    product = models.ForeignKey(Tovar, on_delete=models.SET_DEFAULT, null=True, verbose_name='Product', default=None)
    name = models.CharField(max_length=150, verbose_name='Name')
    size = models.CharField(max_length=100, blank=True, null=True, verbose_name='Size')
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Price')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Quantity')
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Date of sale")

    class Meta:
        db_table = 'order_item'

    objects = OrderitemQueryset.as_manager()

    def products_price(self):
        return round(self.product.price * self.quantity, 2)
    
    def __str__(self):
        return f"Product {self.name} | Order N {self.order.pk}"

class LandsUndNumbers(models.Model):
    land = models.CharField(max_length=100)
    number_code = models.CharField(max_length=10, unique=True)
    phone_number_length = models.PositiveIntegerField()

    def __str__(self):
        return self.land