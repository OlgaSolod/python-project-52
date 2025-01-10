from django.test import TestCase
from django.contrib.auth import get_user_model

# Create your tests here.


User = get_user_model()


class UserTestCase( TestCase):
    fixtures = ["users.json"]

    def test_create_user(self):
        User.objects.create(
            username="dracomalfoy",
            email="",
            password="123",
            first_name="draco",
            last_name="malfoy",
            last_login=None,
            is_superuser=0,
            is_staff=False,
            is_active=True,
            date_joined="2025-01-10 15:37:08.988618"
        )
        created_user = User.objects.get(username="dracomalfoy")
        self.assertEqual(created_user.username, "dracomalfoy")

    def test_update_user(self):
        user = User.objects.get(pk=1)
        user.first_name = "test!!"
        self.assertEqual(user.first_name, 'test!!')

    def test_delete_user(self):
        user = User.objects.get(pk=2)
        user.delete()
        self.assertFalse(User.objects.filter(pk=2))