from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=64)
    surname = models.CharField(max_length=64)
    description = models.TextField(null=True)
    address = models.ForeignKey('Address', on_delete=models.SET_NULL, null=True)
    group = models.ManyToManyField('Group')
    # photo = models.ImageField(upload_to='photos')


class Phone(models.Model):
    phone_number = models.CharField(max_length=16, unique=True)
    type = models.CharField(max_length=32)
    person = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True)


class Address(models.Model):
    city = models.CharField(max_length=64)
    street = models.CharField(max_length=64)
    house = models.PositiveSmallIntegerField()
    flat = models.PositiveSmallIntegerField(null=True, default=None)

    class Meta:
        unique_together = ('city', 'street', 'house', 'flat')


class Email(models.Model):
    email = models.CharField(max_length=64, unique=True)
    type = models.CharField(max_length=32)
    person = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True)


class Group(models.Model):
    name = models.CharField(max_length=64)
