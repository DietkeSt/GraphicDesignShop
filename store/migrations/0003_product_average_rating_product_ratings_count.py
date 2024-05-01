# Generated by Django 5.0.2 on 2024-05-01 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_product_users_wishlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='average_rating',
            field=models.FloatField(default=0.0, help_text='Average Rating of the Product'),
        ),
        migrations.AddField(
            model_name='product',
            name='ratings_count',
            field=models.IntegerField(default=0, help_text='Total Number of Ratings'),
        ),
    ]
