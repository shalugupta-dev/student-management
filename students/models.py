from django.db import models


class Student(models.Model):
    roll_number = models.CharField(
        max_length=20,
        unique=True
    )
    name = models.CharField(max_length=100)
    email = models.EmailField()
    course = models.CharField(max_length=50)
    phone = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField(
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.roll_number} - {self.name}"