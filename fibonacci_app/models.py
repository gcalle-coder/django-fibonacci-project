from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.
class FibonacciData(models.Model):
    number = models.IntegerField(
        unique=True, default=0, validators=[MaxValueValidator(50), MinValueValidator(0)]
    )
    result = models.IntegerField()
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.number} - {self.result}"
