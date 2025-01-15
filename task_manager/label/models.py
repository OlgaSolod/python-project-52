from django.db import models


# Create your models here.
class Label(models.Model):
    name = models.CharField(max_length=30, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.get_name()

    def get_name(self):
        return self.name