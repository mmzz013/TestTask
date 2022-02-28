from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    GENDER_SELECTION = (
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    first_name = models.CharField(max_length=55)
    last_name = models.CharField(max_length=55)
    gender = models.CharField(max_length=20, choices=GENDER_SELECTION)
    email = models.EmailField(unique=True)

    avatar = models.ImageField(upload_to='media/', blank=True)
    username = None

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.email}'
