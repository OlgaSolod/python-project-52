from django.test import TestCase
from task_manager.task.models import Task
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


# Create your tests here.
class TaskTestCase(TestCase):
    fixtures = ["users.json"]

    def setUp(self):
        self.user1 = User.objects.get(pk=1)
        self.user2 = User.objects.get(pk=2)
        self.task = Task.objects.create(
            name="Task by user2", creator_id=self.user2.pk
        )

    def test_create_task(self):
        Task.objects.create(name="Created Task", creator=self.user1)
        self.assertEqual(Task.objects.get(pk=2).name, "Created Task")

    def test_update_task(self):
        self.task.name = "Updated Task"
        self.task.save()
        self.assertEqual(
            Task.objects.get(pk=self.task.pk).name, "Updated Task"
            )

    def test_delete_task(self):
        task = Task.objects.create(name="Temporary Task", creator=self.user2)
        task.delete()
        self.assertFalse(Task.objects.filter(pk=task.pk).exists())

    def test_impossible_delete_not_user_task(self):
        self.client.login(username=self.user1.username, password="123")
        response = self.client.post(
            reverse("delete_task", kwargs={"pk": self.task.pk})
        )
        # Проверяем, что задача все еще существует
        self.assertTrue(Task.objects.filter(pk=self.task.pk).exists())

        # Проверяем, что получили редирект
        self.assertEqual(response.status_code, 302)
