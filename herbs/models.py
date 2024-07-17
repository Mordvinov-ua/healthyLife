from django.db import models
from django.urls import reverse

class Tovar(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    photo = models.ImageField(upload_to='photo/tovar/')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    time_create = models.DateTimeField(auto_now_add= True)
    discount = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, help_text="Discount in percentage")
    time_update = models.DateTimeField(auto_now= True)
    is_published = models.BooleanField(default=True)
    group = models.ForeignKey('Group', on_delete=models.PROTECT)
    sale_category = models.ForeignKey('Sale_category', on_delete=models.PROTECT, null=True, blank=True)
    slug = models.SlugField(max_length=100, db_index=True, unique=True, verbose_name='Url')
    quantity = models.PositiveIntegerField(default=0,)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('tovar', kwargs={'tovar_slug':self.slug})

    def price_after_discount(self):
        discount_amount = (self.discount / 100) * self.price
        return self.price - discount_amount

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ("id",)

class Group(models.Model):
    photo = models.ImageField(upload_to='photo/group/')
    name = models.CharField(max_length=100, db_index=True)
    category = models.ForeignKey('Category', on_delete=models.PROTECT)
    time_create = models.DateTimeField(auto_now_add= True)
    time_update = models.DateTimeField(auto_now= True)
    is_published = models.BooleanField(default=True)
    slug = models.SlugField(max_length=100, db_index=True, unique=True, verbose_name='Url')

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('group', kwargs={'group_slug':self.slug})

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
    
class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    time_create = models.DateTimeField(auto_now_add= True)
    time_update = models.DateTimeField(auto_now= True)
    is_published = models.BooleanField(default=True)
    slug = models.SlugField(max_length=100, db_index=True, unique=True, verbose_name='Url')

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('cat', kwargs={'cat_slug':self.slug})
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Sale_category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    time_create = models.DateTimeField(auto_now_add= True)
    time_update = models.DateTimeField(auto_now= True)
    is_published = models.BooleanField(default=True)
    slug = models.SlugField(max_length=100, db_index=True, unique=True, verbose_name='Url')

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('sale_cat', kwargs={'sale_cat_id':self.id})
    
    class Meta:
        verbose_name = 'Категория карусели'
        verbose_name_plural = 'Категории карусели'
    
'''class Sale_tovar(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    photo = models.ImageField(upload_to='photo/tovar/')
    time_create = models.DateTimeField(auto_now_add= True)
    time_update = models.DateTimeField(auto_now= True)
    is_published = models.BooleanField(default=True)
    slug = models.SlugField(max_length=100, db_index=True, unique=True, verbose_name='Url')

    alt_price = models.DecimalField(max_digits=6, decimal_places=2)
    neu_price = models.DecimalField(max_digits=6, decimal_places=2)
    

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('sale_cat', kwargs={'sale_slug':self.slug})
    
    class Meta:
        verbose_name = 'Товар карусели'
        verbose_name_plural = 'Товары карусели'''