from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.gis.db import models

class UserProfileManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, username, password, **extra_fields)

class UserProfile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    location = models.PointField(geography=True, null=True, blank=True)
    phone_number = models.CharField(max_length=15)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

class Customer(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)  
    location = models.PointField(geography=True, null=True, blank=True)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(max_length=255)

    def __str__(self):
        return self.user.username

class Item(models.Model):
    ENGINE_PARTS = 'Engine Parts'
    ELECTRICAL_PARTS = 'Electrical Parts'
    SUSPENSION_AND_STEERING = 'Suspension and Steering'
    TRANSMISSION_AND_DRIVETRAIN = 'Transmission and Drivetrain'
    BODY_AND_FRAME = 'Body and Frame'
    ACCESSORIES = 'Accessories'
    PERFORMANCE_UPGRADES = 'Performance Upgrades'
    MAINTENANCE_AND_CARE = 'Maintenance and Care'
    OILS_AND_LUBRICANTS = 'Oils and Lubricants'

    CATEGORY_CHOICES = [
        (ENGINE_PARTS, 'Engine Parts'),
        (ELECTRICAL_PARTS, 'Electrical Parts'),
        (SUSPENSION_AND_STEERING, 'Suspension and Steering'),
        (TRANSMISSION_AND_DRIVETRAIN, 'Transmission and Drivetrain'),
        (BODY_AND_FRAME, 'Body and Frame'),
        (ACCESSORIES, 'Accessories'),
        (PERFORMANCE_UPGRADES, 'Performance Upgrades'),
        (MAINTENANCE_AND_CARE, 'Maintenance and Care'),
        (OILS_AND_LUBRICANTS ,'Oils and Lubricants'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='jsh/product_images/')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default=ENGINE_PARTS)
    brand = models.CharField(max_length=255, default='JSH')

    def __str__(self):
        return self.name
    


class Review(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.customer.user.username} for {self.item.name}"

class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item, through='CartItem')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order by {self.customer.user.username} on {self.date}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.quantity}x {self.item.name}"
    
class Wishlist(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item)

    def __str__(self):
        return f"Wishlist for {self.user.username}"
    
class Administrator(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)  

    def __str__(self):
        return self.user.username