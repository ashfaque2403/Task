from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return self.user.username

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    position = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class CustomField(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='custom_fields')
    field_name = models.CharField(max_length=50)
    field_value = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.field_name} for {self.employee.name}"

    