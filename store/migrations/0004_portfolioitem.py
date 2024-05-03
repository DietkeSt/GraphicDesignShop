# Generated by Django 5.0.2 on 2024-05-03 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_product_average_rating_product_ratings_count'),
    ]

    operations = [
        migrations.CreateModel(
            name='PortfolioItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to='portfolio_images/')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
