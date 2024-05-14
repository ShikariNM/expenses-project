from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    usefulness = models.PositiveSmallIntegerField(default=1, choices=[(i, i) for i in range(1, 11)])
    color = models.CharField(max_length=7, default='#000000')

    class Meta:
        unique_together = ('user', 'title')

    def __str__(self):
        return f'{self.title}'


class Receipt(models.Model):
    title = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    purchase_time = models.DateTimeField()

    def __str__(self):
        return f"{self.title}"


class Expense(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} - {self.cost} ({self.category})"
