# Generated by Django 3.2.7 on 2021-10-04 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20210918_1933'),
    ]

    operations = [
        migrations.AddField(
            model_name='productcategory',
            name='available',
            field=models.BooleanField(default=True),
        ),
    ]