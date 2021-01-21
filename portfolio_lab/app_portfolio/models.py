from django.db import models


INSTITUTION_TYPES = (
    (1, "Fundation"),
    (2, "Non-goverment organization"),
    (3, "Local collection"),
)


class Category(models.Model):
    name = models.CharField(max_length=100)


class Institution(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    type = models.IntegerField(choices=INSTITUTION_TYPES, default=1)
    categories = models.ManyToManyField(Category, related_name="institutions")