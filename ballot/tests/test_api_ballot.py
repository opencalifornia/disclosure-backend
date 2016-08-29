from django.core.urlresolvers import reverse

from rest_framework.test import APITestCase

from . import factory


class BallotAPITest(APITestCase):
    def setUp(self):
        self.ballot = factory.BallotFactory()
        self.office_election = factory.OfficeElectionFactory(ballot=self.ballot)
        self.referendum = factory.ReferendumFactory(ballot=self.ballot)

    def test_ballot(self):
        ballot_url = reverse(
            'ballot_get', kwargs={'ballot_id': self.ballot.id})
        resp = self.client.get(ballot_url)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data.get('id'), self.ballot.id)
        self.assertEqual(resp.data.get('date'), self.ballot.date)
        self.assertEqual(resp.data.get('locality_id'), self.ballot.locality.id)
        self.assertIn('ballot_items', resp.data)

        # Find the first office_election
        office_election = next(b for b in resp.data.get('ballot_items')
                               if b['contest_type'] == 'Office')
        # Find the first referendum
        referendum = next(b for b in resp.data.get('ballot_items')
                          if b['contest_type'] == 'Referendum')

        self.assertIn('id', office_election)
        self.assertIn('name', office_election)
        self.assertIn('candidates', office_election)

        self.assertIn('id', referendum)
        self.assertIn('number', referendum)
        self.assertIn('title', referendum)

    def test_ballot_bad_id_404(self):
        """ Unknown ballot ID"""
        ballot_url = reverse(
            'ballot_get', kwargs={'ballot_id': 0})
        resp = self.client.get(ballot_url)

        self.assertEqual(resp.status_code, 404, ballot_url)

    def test_current_ballot(self):
        ballot_url = reverse(
            'current_ballot', kwargs={'locality_id': self.ballot.locality_id})
        resp = self.client.get(ballot_url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data.get('id'), self.ballot.id)
        self.assertEqual(resp.data.get('date'), self.ballot.date)
        self.assertEqual(resp.data.get('locality_id'), self.ballot.locality.id)
        self.assertIn('ballot_items', resp.data)

        # Find the first office_election
        office_election = next(b for b in resp.data.get('ballot_items')
                               if b['contest_type'] == 'Office')
        # Find the first referendum
        referendum = next(b for b in resp.data.get('ballot_items')
                          if b['contest_type'] == 'Referendum')

        self.assertIn('id', office_election)
        self.assertIn('name', office_election)
        self.assertIn('candidates', office_election)

        self.assertIn('id', referendum)
        self.assertIn('number', referendum)
        self.assertIn('title', referendum)
