# Generated by Django 4.1.1 on 2022-09-10 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_customer_user_alter_order_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='profile',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
