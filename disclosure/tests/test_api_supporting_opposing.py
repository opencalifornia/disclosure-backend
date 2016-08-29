from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase

from ballot.tests.factory import CandidateFactory, OfficeElectionFactory, \
    ReferendumFactory, ReferendumSelectionFactory
from finance.tests.factory import BeneficiaryFactory, IndependentMoneyFactory


class SupportingOpposingCandidateTests(APITestCase):
    def setUp(self):
        self.office_election = OfficeElectionFactory()
        self.candidate = CandidateFactory(
            office_election=self.office_election
        )

    def test_candidate_opposing_list(self):
        beneficiary = BeneficiaryFactory(
            support=False,
            ballot_item_selection=self.candidate,
        )
        money = IndependentMoneyFactory(
            beneficiary=beneficiary,
            amount=30.5,
        )

        url = reverse('candidate_opposing',
                      kwargs={'candidate_id': self.candidate.id})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(len(resp.data) > 0)

        # TODO: replace dummy tests with live data tests.
        row = resp.data[0]
        self.assertIn('name', row)
        self.assertIn('contributions_received', row)
        self.assertEqual(row.get('contributions_received'), money.amount)

    def test_candidate_supporting_list(self):
        beneficiary = BeneficiaryFactory(
            support=True,
            ballot_item_selection=self.candidate,
        )
        money = IndependentMoneyFactory(
            beneficiary=beneficiary,
            amount=15.5,
        )

        url = reverse('candidate_supporting',
                      kwargs={'candidate_id': self.candidate.id})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(len(resp.data) > 0)

        # TODO: replace dummy tests with live data tests.
        row = resp.data[0]
        self.assertIn('name', row)
        self.assertIn('contributions_received', row)
        self.assertEqual(row.get('contributions_received'), money.amount)


class SupportingOpposingReferendumTests(APITestCase):
    def setUp(self):
        self.referendum = referendum = ReferendumFactory()
        self.referendum_selection = ReferendumSelectionFactory(
            in_favor=True,
            ballot_item=referendum
        )

    def test_referendum_opposing_list(self):
        beneficiary = BeneficiaryFactory(
            support=False,
            ballot_item_selection=self.referendum_selection,
        )
        IndependentMoneyFactory(
            beneficiary=beneficiary,
            amount=40.5,
        )

        url = reverse('referendum_opposing',
                      kwargs={'referendum_id': self.referendum.id})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(len(resp.data) > 0)

        row = resp.data[0]
        self.assertIn('name', row)
        self.assertIn('contributions_received', row)
        self.assertEqual(row.get('contributions_received'), 40.5)

    def test_referendum_supporting_list(self):
        beneficiary = BeneficiaryFactory(
            support=True,
            ballot_item_selection=self.referendum_selection,
        )
        IndependentMoneyFactory(
            beneficiary=beneficiary,
            amount=55.5,
        )

        url = reverse('referendum_supporting',
                      kwargs={'referendum_id': self.referendum.id})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(len(resp.data) > 0)

        row = resp.data[0]
        self.assertIn('name', row)
        self.assertIn('contributions_received', row)
        self.assertEqual(row.get('contributions_received'), 55.5)
