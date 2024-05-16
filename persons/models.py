from django.db import models
from django.conf import settings

# Create your models here.

class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    age = models.IntegerField()
    email = models.EmailField()
    
    GENRE_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    ]

    genre = models.CharField(
        max_length=1,
        choices=GENRE_CHOICES,
        default='M',
    )

    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)

class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    person = models.ForeignKey('persons.Person', related_name='votes', on_delete=models.CASCADE)
