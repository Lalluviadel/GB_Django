# Generated by Django 3.2.7 on 2021-09-28 22:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('baskets', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='basket',
            old_name='products',
            new_name='product',
        ),
        migrations.AlterField(
            model_name='basket',
            name='quantity',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
