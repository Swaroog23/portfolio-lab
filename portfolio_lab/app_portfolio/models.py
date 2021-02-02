from django.db import models
from django.contrib.auth.models import User


INSTITUTION_TYPES = (
    (1, "Fundation"),
    (2, "Non-goverment organization"),
    (3, "Local collection"),
)


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Institution(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    type = models.IntegerField(choices=INSTITUTION_TYPES, default=1)
    categories = models.ManyToManyField(Category, related_name="institutions")


class Donation(models.Model):
    quantity = models.IntegerField()
    categories = models.ManyToManyField(Category, related_name="donations")
    address = models.CharField(max_length=50)
    phone_number = models.IntegerField()
    city = models.CharField(max_length=100)
    zip_code = models.IntegerField()
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)
