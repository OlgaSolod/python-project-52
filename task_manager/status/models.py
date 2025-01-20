from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.
class Status(models.Model):
    name = models.CharField(max_length=30, blank=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.get_name()

    def get_name(self):
        return f"{self.name}"
