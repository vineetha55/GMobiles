# Generated by Django 5.1.4 on 2025-01-22 10:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Global_App', '0009_contact_productattribute'),
    ]

    operations = [
        migrations.CreateModel(
            name='Multi_Bookings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_price', models.FloatField(null=True)),
                ('delivery', models.FloatField(null=True)),
                ('sub_total', models.FloatField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(max_length=100, null=True)),
                ('ship_add', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Global_App.user_ship_address')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Global_App.registration')),
            ],
        ),
        migrations.CreateModel(
            name='Order_Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('book', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Global_App.multi_bookings')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Global_App.product')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Global_App.registration')),
            ],
        ),
    ]
