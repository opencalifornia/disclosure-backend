from __future__ import absolute_import
import factory
from faker import Faker

faker = Faker()


class PartyFactory(factory.django.DjangoModelFactory):
    name = factory.Faker('company')

    class Meta:
        model = 'ballot.Party'


class StateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'locality.State'

    name = 'California'
    short_name = 'CA'


class CountyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'locality.County'

    state = factory.SubFactory(StateFactory)


class CityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'locality.City'

    county = factory.SubFactory(CountyFactory)
    state = factory.SubFactory(StateFactory)


class BallotFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'ballot.Ballot'

    locality = factory.SubFactory(CityFactory)


class ReferendumFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'ballot.Referendum'

    number = factory.Faker('random_letter')
    title = factory.Faker('text', max_nb_chars=100)
    ballot = factory.SubFactory(BallotFactory)
    contest_type = 'R'


class ReferendumSelectionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'ballot.ReferendumSelection'

    ballot_item = factory.SubFactory(ReferendumFactory)


class OfficeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'ballot.Office'

    name = factory.Faker('random_element', elements=['Mayor', 'Secretary', 'Councilmember'])
    description = 'An office'
    locality = factory.SubFactory(CityFactory)


class OfficeElectionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'ballot.OfficeElection'

    ballot = factory.SubFactory(BallotFactory)
    contest_type = 'O'
    office = factory.SubFactory(OfficeFactory)


class CandidateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'ballot.Candidate'

    first_name = factory.Faker('first_name')
    middle_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    office_election = factory.SubFactory(OfficeElectionFactory)
    party = factory.SubFactory(PartyFactory)
