from django.test import TestCase

# Create your tests here.
class HomeTest(TestCase):
    def setUp(self):
        self.response = self.client.get('/')

    def test_get(self):
        """GET / must return status code 200"""
        self.assertTrue(200, self.response.status_code)

    def test_template(self):
        """Must return template index.html"""
        self.assertTemplateUsed(self.response, 'index.html')