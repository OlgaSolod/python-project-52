from django.db import models
from django.contrib.auth import get_user_model
from task_manager.status.models import Status

User = get_user_model()

class Task(models.Model):
    name = models.CharField(max_length=30, blank=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    creator = models.ForeignKey(User, on_delete=models.PROTECT, related_name='creator')
    status = models.ForeignKey(Status, on_delete=models.PROTECT, null=True)
    executor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='executor')

    def __str__(self):
        return self.get_name()
    
    def get_name(self):
        return self.name