from django.test import TestCase

from user.models import User

class UserTestCase(TestCase):
    def setUp(self):
        self.user1=User.objects.create_user('user1','user1@test.com','pass1234')

    def testGetUserById(self):
        user=User.objects.get(id=self.user1.id)
        self.assertIsNotNone(user)



