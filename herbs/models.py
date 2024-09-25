from django.db import models
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField



class Tovar(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextUploadingField(blank=True)
    product_benefits= RichTextUploadingField(blank=True)
    ingredients = RichTextUploadingField(blank=True)
    usage_instructions = RichTextUploadingField(blank=True)
    condition_of_product = models.CharField(max_length=100,blank=True, null=True)
    main_purpose = models.CharField(max_length=100,blank=True, null=True)
    active_ingredients = models.CharField(max_length=100,blank=True, null=True)
    department = models.CharField(max_length=100,blank=True, null=True)
    expiration_date = models.CharField(max_length=100,blank=True, null=True)
    region_of_manufacture = models.CharField(max_length=100,blank=True, null=True)
    photo = models.ImageField(upload_to='photo/tovar/')
    price = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    time_create = models.DateTimeField(auto_now_add= True)
    time_update = models.DateTimeField(auto_now= True)
    is_published = models.BooleanField(default=True)
    group = models.ManyToManyField('Group', related_name="tovars")
    sale_category = models.ForeignKey('Sale_category', on_delete=models.PROTECT, null=True, blank=True)
    slug = models.SlugField(max_length=100, db_index=True, unique=True, verbose_name='Url')
    quantity = models.PositiveIntegerField(default=0,)
    tovar_variations = models.ManyToManyField('TovarVariation', related_name='tovars', blank=True, default=1)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('tovar', kwargs={'tovar_slug':self.slug})
    
    def get_price(self, variation_id=None):
        if variation_id:
            try:
                variation = self.tovar_variations.get(id=variation_id)
                return variation.price_after_discount()
            except TovarVariation.DoesNotExist:
                return self.price
        return self.price
    
    def variation_info(self, variation_id=None):
        if variation_id:
            try:
                variation = self.tovar_variations.get(id=variation_id)
                return variation.size
            except TovarVariation.DoesNotExist:
                return None
        return None

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ("id",)

class TovarPhoto(models.Model):
    tovar = models.ForeignKey(Tovar, related_name='photos', on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='photo/tovar/')

    class Meta:
        verbose_name = 'Фото товара'
        verbose_name_plural = 'Фото товаров'
        ordering = ('id',)

class TovarVariation(models.Model):
    tovar = models.ForeignKey(Tovar, related_name='variations', on_delete=models.CASCADE)
    size = models.CharField(max_length=100,)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    discount = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, help_text="Discount in percentage")

    def price_after_discount(self):
        discount_amount = (self.discount / 100) * self.price
        return self.price - discount_amount

    def __str__(self):
        return f"{self.size} - {self.price} $"

    class Meta:
        verbose_name = 'Вариант товара'
        verbose_name_plural = 'Варианты товаров'

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