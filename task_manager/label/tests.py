from django.test import TestCase
from task_manager.task.models import Task, TaskLabel
from task_manager.label.models import Label
from django.contrib.auth import get_user_model
from django.db.models import ProtectedError

User = get_user_model()

# Create your tests here.
class LabelTestCase(TestCase):
    fixtures = ['users.json']
    def setUp(self):
        self.user1 = User.objects.get(pk=1)
        self.label = Label.objects.create(name='test')
    
    def test_create_label(self):
        Label.objects.create(name='test')
        self.assertEqual(Label.objects.get(pk=1).name, 'test')

    def test_update_label(self):
        self.label.name = 'Updated'
        self.label.save()
        self.assertEqual(Label.objects.get(pk=self.label.pk).name, 'Updated')
        
    def test_delete_unbind_label(self):
        self.label.delete()
        self.assertFalse(Label.objects.filter(pk=self.label.pk).exists())
    
    def test_delete_bind_label(self):
        label = Label.objects.create(name="Important")
        task = Task.objects.create(name="Test Task", creator_id=1)
        TaskLabel.objects.create(task=task, label=label)
        with self.assertRaises(ProtectedError):
            label.delete()


    
