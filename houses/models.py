from django.db import models

# Create your models here.
class House(models.Model):
    name = models.CharField(max_length=140)
    # Defining type of the value
    # charField : text having limit of the length