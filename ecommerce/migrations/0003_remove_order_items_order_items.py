# Generated by Django 4.1.5 on 2023-03-23 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0002_remove_order_items_order_items'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='items',
        ),
        migrations.AddField(
            model_name='order',
            name='items',
            field=models.ManyToManyField(to='ecommerce.orderitem'),
        ),
    ]
