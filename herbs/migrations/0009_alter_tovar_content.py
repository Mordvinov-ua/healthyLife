# Generated by Django 4.1.7 on 2024-08-16 11:34

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('herbs', '0008_alter_tovar_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tovar',
            name='content',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True),
        ),
    ]
