from django.core.urlresolvers import reverse

from rest_framework.test import APITestCase

from . import factory


class OfficeElectionAPITest(APITestCase):
    def setUp(self):
        self.office_election = factory.OfficeElectionFactory()

        # Create two candidates
        factory.CandidateFactory(office_election=self.office_election)
        factory.CandidateFactory(office_election=self.office_election)

    def test_office_election_with_id(self):
        office_election = self.office_election
        resp = self.client.get(
            reverse('office_election_get',
                    kwargs={'office_election_id': office_election.id}))

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data.get('id'), office_election.id)
        self.assertEqual(resp.data.get('locality_id'), office_election.office.locality.id)
        self.assertEqual(len(resp.data.get('candidates')), 2)
        self.assertNotIn('contest_type', resp.data)
        self.assertNotIn('office', resp.data)
        self.assertNotIn('ballot', resp.data)

    def test_office_election_bad_id_404(self):
        """ Unknown office election ID"""
        resp = self.client.get(
            reverse('office_election_get', kwargs={'office_election_id': 0}))

        self.assertEqual(resp.status_code, 404)


class CandidateAPITest(APITestCase):
    def setUp(self):
        self.candidate = factory.CandidateFactory()

    def test_candidate_with_id(self):
        candidate = self.candidate
        resp = self.client.get(
            reverse('candidate_get',
                    kwargs={'candidate_id': candidate.id}))

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data.get('id'), candidate.id)
        self.assertEqual(resp.data.get('first_name'), candidate.first_name)
        self.assertEqual(resp.data.get('last_name'), candidate.last_name)
        self.assertEqual(resp.data.get('photo_url'), candidate.photo_url)
        self.assertEqual(resp.data.get('ballot_item_id'), candidate.office_election.id)
        self.assertEqual(resp.data.get('office_election_id'), candidate.office_election.id)
        self.assertIsNotNone(candidate.party.name)
        self.assertEqual(resp.data.get('party'), candidate.party.name)

    def test_candidate_bad_id_404(self):
        """ Unknown candidate ID"""
        resp = self.client.get(
            reverse('candidate_get', kwargs={'candidate_id': 0}))

        self.assertEqual(resp.status_code, 404)
