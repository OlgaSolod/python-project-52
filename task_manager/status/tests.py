from django.test import TestCase
from task_manager.status.models import Status
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your tests here.
class StatusTestCase(TestCase):

    def test_create_status(self):
        Status.objects.create(name="First status")
        self.assertEqual(Status.objects.get(pk=1).name, "First status")

    def test_update_status(self):
        Status.objects.create(name="First status")
        status = Status.objects.get(pk=1)
        status.name = "Second status"
        status.save()
        self.assertEqual(Status.objects.get(pk=1).name, "Second status")

    def test_delete_status(self):
        Status.objects.create(name="First status")
        status = Status.objects.get(pk=1)
        status.delete()
        self.assertFalse(Status.objects.filter(pk=1))
