from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from account.models import User


class Airplane(models.Model):
    airplane = models.CharField(max_length=20)

    def __str__(self):
        return self.airplane


class Country(models.Model):
    country = models.CharField(max_length=20)

    def __str__(self):
        return self.country


GENDER_CHOICES = (
    ('man', 'мужской'),
    ('woman', 'женский'),
)


class Person(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10)
    nationality = models.CharField(max_length=30)
    passport_number = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name} {self.surname}"


class Ticket(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    origin = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="departures")
    destination = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="arrivals")
    departure_time = models.DateTimeField(auto_now=False)
    arrival_time = models.DateTimeField(auto_now=False)
    ticket_price = models.IntegerField(default=20, blank=True)
    airplane = models.ForeignKey(Airplane, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    image = models.FileField(upload_to='images/')


class Comment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return f'{self.author}:{self.body}'


class Likes(models.Model):
    likes = models.BooleanField(default=False)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='likes')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')

    def __str__(self):
        return str(self.likes)


class Rating(models.Model):
    rating = models.IntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(5)])
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='rating')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rating')

    def __str__(self):
        return str(self.rating)


class Favorite(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='favorite')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite')
    favorite = models.BooleanField(default=True)