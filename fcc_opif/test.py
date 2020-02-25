from django.test import TestCase, Client

class AdminPageTest(TestCase):

    def setUp(self):

        self.client = Client()
        self.response = self.client.get('/admin/login/?next=/admin/', {})
        #print(self.response['location'])

    def test_response_success(self):
        self.assertEqual(self.response.status_code, 200)