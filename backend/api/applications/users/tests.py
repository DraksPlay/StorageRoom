from django.test.client import Client
from rest_framework.test import APITestCase


class UsersTestClass(APITestCase):

    def setUp(self):
        self.client = Client()
        self.user_data = {"email": "test@gmail.com",
                          "password": "test_pass"}

    def test_create_user(self):

        user_response = self.client.post("/api/users/create_user/",
                                         self.user_data)
        self.assertEqual(user_response.status_code, 201)

        new_data = dict(self.user_data)
        new_data["email"] = "invalid"
        user_invalid_response = self.client.post("/api/users/create_user/",
                                                 new_data)
        self.assertEqual(user_invalid_response.status_code, 400)

        new_data = dict(self.user_data)
        new_data["password"] = ""
        user_invalid_response = self.client.post("/api/users/create_user/",
                                                 new_data)
        self.assertEqual(user_invalid_response.status_code, 400)

    def test_read_user(self):
        user_response = self.client.post("/api/users/create_user/",
                                         self.user_data)
        user_id = user_response.data.get('id')

        user_response = self.client.get(f"/api/users/get_user/{user_id}")
        self.assertEqual(user_response.status_code, 200)
        self.assertEqual(user_response.data.get("email"), self.user_data.get("email"))
        self.assertEqual(user_response.data.get("balance"), 0)

        user_response = self.client.get(f"/api/users/get_user/999")
        self.assertEqual(user_response.status_code, 400)

    def test_read_users(self):
        self.client.post("/api/users/create_user/", self.user_data)
        new_data = dict(self.user_data)
        new_email = "admin@gmail.com"
        new_data["email"] = new_email
        self.client.post("/api/users/create_user/", new_data)

        user_response = self.client.get(f"/api/users/get_users/")
        self.assertEqual(user_response.status_code, 200)
        users = list(user_response.data)
        self.assertEqual(len(users), 2)
        emails = [new_email, self.user_data.get("email")]
        for user in users:
            self.assertIn(user.get("email"), emails)

    def test_update_users(self):
        user_response = self.client.post("/api/users/create_user/",
                                         self.user_data)
        user_id = user_response.data.get('id')

        new_balance = 50
        user_response = self.client.patch(f"/api/users/update_user/{user_id}",
                                          {"balance": new_balance},
                                          content_type="application/json")
        self.assertEqual(user_response.status_code, 200)

        user_response = self.client.get(f"/api/users/get_user/{user_id}")
        self.assertEqual(user_response.data.get("balance"), new_balance)

        user_response_invalid = self.client.patch(f"/api/users/update_user/{999}",
                                                  {"balance": new_balance},
                                                  content_type="application/json")
        self.assertEqual(user_response_invalid.status_code, 400)

    def test_delete_user(self):
        user_response = self.client.post("/api/users/create_user/",
                                         self.user_data)
        user_id = user_response.data.get('id')

        user_response = self.client.delete(f"/api/users/delete_user/{user_id}")
        self.assertEqual(user_response.status_code, 200)

        user_response = self.client.get(f"/api/users/get_user/{user_id}")
        self.assertEqual(user_response.status_code, 400)

        user_response = self.client.delete(f"/api/users/delete_user/{user_id}")
        self.assertEqual(user_response.status_code, 400)
