from django.core.urlresolvers import reverse

from rest_framework.test import APITestCase

from .test_models import LocalityTest


class LocalityAPITests(LocalityTest, APITestCase):
    @classmethod
    def setUpClass(cls):
        LocalityTest.setUpClass()
        APITestCase.setUpClass()

    @classmethod
    def tearDownClass(cls):
        LocalityTest.tearDownClass()
        APITestCase.tearDownClass()

    def test_docs(self):
        locality_url = reverse('locality_get', kwargs={'locality_id': self.city.id})
        resp = self.client.get(locality_url)

        self.assertIn('name', resp.data)
        self.assertIn('id', resp.data)
