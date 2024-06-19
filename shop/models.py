from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    USER_ROLE_CHOICES = (
        ("client","client"),
        ("seller","seller"),
        ("admin","admin")
    )

    image = models.ImageField(upload_to='profile_pics/',blank=True,null=True,default='profile_pics/default.jpg')
    phone_number = models.CharField(max_length=13,blank=True,null=True)
    address = models.CharField(max_length=200,blank=True,null=True)
    user_role = models.CharField(max_length=10,choices=USER_ROLE_CHOICES,default="client")

class Category(models.Model):
    name = models.CharField(max_length=50,unique=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(max_length=200)
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    image = models.ImageField(upload_to='books/',blank=True,null=True)
    description = models.TextField()
    in_stock = models.BooleanField(default=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    @property
    def total_price(self):
        return self.price * self.quantity


class Cart(models.Model):
    book = models.OneToOneField(Book,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.book.name