# Generated by Django 3.1.6 on 2021-02-04 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_portfolio', '0006_donation_institution'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='zip_code',
            field=models.CharField(max_length=6),
        ),
    ]