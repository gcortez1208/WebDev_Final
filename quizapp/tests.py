from django.test import TestCase


class QuizAppTests(TestCase):
    def test_homepage_renders(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_submit_redirects_on_get(self):
        response = self.client.get("/submit/")
        self.assertEqual(response.status_code, 302)
