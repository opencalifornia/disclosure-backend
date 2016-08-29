from django.core.urlresolvers import reverse

from rest_framework.test import APITestCase

from . import factory


class ReferendumAPITest(APITestCase):
    def setUp(self):
        self.referendum = factory.ReferendumFactory()

    def test_referendum_with_id(self):
        referendum = self.referendum

        resp = self.client.get(
            reverse('referendum_get',
                    kwargs={'referendum_id': referendum.id}))

        self.assertEqual(resp.status_code, 200)
        self.assertIsNotNone(referendum.title)
        self.assertEqual(resp.data.get('id'), referendum.id)
        self.assertEqual(resp.data.get('title'), referendum.title)
        self.assertEqual(resp.data.get('number'), referendum.number)
        self.assertEqual(resp.data.get('ballot_id'), referendum.ballot.id)
        self.assertNotIn('ballot', resp.data)

    def test_referendum_bad_id_404(self):
        """ Unknown referendum ID"""
        resp = self.client.get(
            reverse('referendum_get', kwargs={'referendum_id': 0}))

        self.assertEqual(resp.status_code, 404)
