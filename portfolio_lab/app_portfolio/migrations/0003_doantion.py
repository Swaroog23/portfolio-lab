# Generated by Django 3.1.5 on 2021-01-21 12:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app_portfolio', '0002_auto_20210121_1210'),
    ]

    operations = [
        migrations.CreateModel(
            name='Doantion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('address', models.CharField(max_length=20)),
                ('phone_number', models.IntegerField()),
                ('city', models.CharField(max_length=100)),
                ('zip_code', models.IntegerField()),
                ('pick_up_date', models.DateField()),
                ('pick_up_time', models.TimeField()),
                ('pick_up_comment', models.CharField(max_length=200)),
                ('categories', models.ManyToManyField(related_name='donations', to='app_portfolio.Category')),
                ('user', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
