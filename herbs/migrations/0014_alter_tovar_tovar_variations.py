# Generated by Django 4.1.7 on 2024-10-10 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('herbs', '0013_tovar_active_ingredients_tovar_condition_of_product_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tovar',
            name='tovar_variations',
            field=models.ManyToManyField(blank=True, related_name='tovars', to='herbs.tovarvariation'),
        ),
    ]
