from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from rest_framework_simplejwt.tokens import RefreshToken



ADMIN, CLIENT, SELLER, WAREHOUSE_WORKER =('admin', 'client', 'seller', 'warehouse_worker')


class User(AbstractUser):

    USER_ROLES1 =(
         (ADMIN,ADMIN),
         (CLIENT,CLIENT),
         (SELLER,SELLER),
         (WAREHOUSE_WORKER,WAREHOUSE_WORKER)

     )

    user_roles = models.CharField(max_length=20, choices=USER_ROLES1, default=CLIENT)
    phone = models.CharField(max_length=30, blank=True, null=True)
    photo = models.ImageField(
        upload_to="user_photos/",
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=["jpeg", "jpg", "heic", "heif", "png"])]
    )



    def token(self):
        
        refresh = RefreshToken.for_user(self)
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh)  
        }

    def __str__(self):
        return self.username