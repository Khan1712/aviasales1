from django.db import models


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
    origin = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="departures")
    destination = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="arrivals")
    departure_time = models.DateTimeField(auto_now=False)
    arrival_time = models.DateTimeField(auto_now=False)
    airplane = models.ForeignKey(Airplane, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    image = models.FileField(upload_to='images/')
