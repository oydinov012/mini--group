from django.db import models


class User(models.Model):
    role_choices = [
        ('admin', 'Admin'),
        ('user', 'User'),
        ('warehouse_worker', 'Warehouse Worker'),
        ('seller', 'Seller'),
    ]

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    role = models.CharField(max_length=50, choices=role_choices)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    # Required for custom user models
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'
    
    # Auth properties
    is_anonymous = False
    is_authenticated = True

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

