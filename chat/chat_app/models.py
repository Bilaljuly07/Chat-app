from django.db import models
from django.contrib.auth.models import User

# Organization Model
class Organization(models.Model):
    organization_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

# User Model - Extending Django's User model
class OrganizationUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Linking to the built-in User model
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

# Message Model
class Message(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)  # Automatically stores the time when message is created
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    user = models.ForeignKey(OrganizationUser, on_delete=models.CASCADE)
    message = models.TextField()

    def __str__(self):
        return f"Message by {self.user.user.username} at {self.datetime}"
