from django.db import models

PLATFORM = (
    ("Petfinder", "Petfinder"),
    ("AKC", "AKC")
)
# Create your models here.
class Breader(models.Model):
    user = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=200, blank=True, null=True)
    pet_name = models.CharField(max_length=200)
    platform = models.CharField(max_length=9, default="Petfinder", choices=PLATFORM)
    is_email_sent = models.BooleanField(default=False)
    number_of_email_sent = models.PositiveIntegerField(default=0)
    status = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.email