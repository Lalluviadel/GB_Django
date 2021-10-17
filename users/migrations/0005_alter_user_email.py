# Generated by Django 3.2.7 on 2021-10-17 00:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(error_messages={'unique': 'An email is already used.'}, max_length=254, unique=True),
        ),
    ]