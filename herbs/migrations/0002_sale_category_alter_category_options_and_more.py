# Generated by Django 4.1.7 on 2023-11-18 18:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('herbs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sale_category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100)),
                ('time_create', models.DateTimeField(auto_now_add=True)),
                ('time_update', models.DateTimeField(auto_now=True)),
                ('is_published', models.BooleanField(default=True)),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='Url')),
            ],
            options={
                'verbose_name': 'Категория карусели',
                'verbose_name_plural': 'Категории карусели',
            },
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterModelOptions(
            name='group',
            options={'verbose_name': 'Группа', 'verbose_name_plural': 'Группы'},
        ),
        migrations.AlterModelOptions(
            name='tovar',
            options={'verbose_name': 'Товар', 'verbose_name_plural': 'Товары'},
        ),
        migrations.CreateModel(
            name='Sale_tovar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('photo', models.ImageField(upload_to='photo/tovar/')),
                ('alt_price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('neu_price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('time_create', models.DateTimeField(auto_now_add=True)),
                ('time_update', models.DateTimeField(auto_now=True)),
                ('is_published', models.BooleanField(default=True)),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='Url')),
                ('sale_category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='herbs.sale_category')),
            ],
            options={
                'verbose_name': 'Товар карусели',
                'verbose_name_plural': 'Товары карусели',
            },
        ),
    ]
