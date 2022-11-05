# Generated by Django 3.2.7 on 2021-10-20 23:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_alter_product_options'),
        ('ordersapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=0, verbose_name='количество')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='активный'),
        ),
        migrations.DeleteModel(
            name='OrderItems',
        ),
        migrations.AddField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orderitem', to='ordersapp.order', verbose_name='заказ'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product', verbose_name='продукты'),
        ),
    ]
