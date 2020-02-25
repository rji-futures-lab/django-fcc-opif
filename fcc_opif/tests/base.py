from django.test import Client

class AdminPageTestBase:

    def setUp(self):

        self.client = Client()
        self.response = self.client.post('/admin')

    def test_response_success(self):
        self.assertEqual(self.response.status_code, 200)