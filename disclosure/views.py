import os

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import F, Q, Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template import loader

from rest_framework import viewsets
from rest_framework.decorators import api_view, list_route
from rest_framework.response import Response

from ballot.models import Ballot
from finance.models import IndependentMoney
from locality.models import City
from locality.serializers import LocalitySerializer
from swagger_nickname_registry import swagger_nickname


@api_view(['GET'])
@swagger_nickname('search')
def search_view(request):
    """
    Search for a location with ballot/disclosure data.
    ---

    parameters:
      - name: q
        description: The user's search query
        type: string
        paramType: query

    response_serializer:
        LocalitySerializer
    """
    query = request.query_params.get('q', '')
    query_set = City.objects.filter(~Q(ballot=None), name__icontains=query)
    serializer = LocalitySerializer(query_set, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@swagger_nickname('disclosure_summary')
def locality_disclosure_summary_view(request, ballot_id):
    """
    Display summarized disclosure information for a ballot
    ---
    parameters:
      - name: ballot_id
        description: The ballot_id
        paramType: path
        type: integer
        required: true
    """
    # TODO: set up ElectionDay app.
    ballot = get_object_or_404(Ballot, id=ballot_id)
    locality = City.objects.get(id=ballot.locality_id)

    # Get all relevant rows of IndependentMoney
    benefits = IndependentMoney.objects.filter(
        beneficiary__ballot_item_selection__ballot_item__ballot=ballot)

    # Simple measures
    num_contributions = benefits.count()
    total_benefits = benefits.aggregate(total=Sum(F('amount')))['total']

    # Summary measures by benefactor type
    key_map = dict(IN='individual', CO='corporation',
                   PF='recipient_committee')
    benefits_groupedby_type = benefits \
        .values_list('benefactor__benefactor_type') \
        .annotate(total=Sum(F('amount')))
    benefits_by_type = dict([(key_map[vals[0]], vals[1])  # alias keys
                             for vals in benefits_groupedby_type])

    # Summarize by locality.
    results_by_locality = dict(
        unknown_location=benefits
        .filter(benefactor__benefactor_locality=None),
        inside_location=benefits
        .filter(benefactor__benefactor_locality=locality),
        inside_state=benefits
        .filter(benefactor__benefactor_locality__city__state=locality.state),
        outside_state=benefits
        .exclude(benefactor__benefactor_locality=None)
        .exclude(benefactor__benefactor_locality__city__state=locality.state))
    total_by_locality = dict(
        [(key, val.aggregate(tot=Sum(F('amount')))['tot'] or 0)  # 0 for empty
         for key, val in results_by_locality.items()])

    return Response({
        "location": {
            "name": locality.name or locality.short_name,
            "id": locality.id,
            "next_election": ballot.date if ballot else None
        },
        "contribution_total": total_benefits,
        "contribution_count": num_contributions,
        "contribution_by_type": benefits_by_type,
        "contribution_by_area": total_by_locality,
    })


class BallotItemResponseViewSet(viewsets.ViewSet):
    """
    Abstract class serving both candidates and referendums
    """

    def supporting(self, request, ballot_item_response_id):
        """
        Display summarized supporting committee information
        """
        return Response([
            {'id': 1, 'name': 'Citizens for a Better Oakland', 'contributions': 185859},  # noqa
            {'id': 2, 'name': 'Oaklanders for Ethical Government', 'contributions': 152330},  # noqa
            {'id': 3, 'name': 'Americans for Liberty', 'contributions': 83199},
            {'id': 4, 'name': 'Golden State Citizens for Positive Reform',
             'contributions': 23988}
        ], content_type='application/json')

    @list_route(['GET'])
    def opposing(self, request, ballot_item_response_id):
        """
        Display summarized opposing committee information
        """
        return Response([
            {'id': 5, 'name': 'The Public Commission for Ethical Civic Reform',
             'contributions': 15040},
            {'id': 6, 'name': 'The Committee of True Americans who Dearly '
                      'Love America and Liberty', 'contributions': 7943}
        ])


class ReferendumViewSet(BallotItemResponseViewSet):
    @list_route(['GET'])
    def supporting(self, request, referendum_id):
        """
        Groups making contributions/expenditures in support of a referendum.
        """
        # ballot_item_response_id =   # query from referendumresponse model
        return super(ReferendumViewSet, self).supporting(
            request, ballot_item_response_id=1)

    @list_route(['GET'])
    def opposing(self, request, referendum_id):
        """
        Groups making contributions/expenditures in opposition to a referendum.
        """
        # ballot_item_response_id =   # query from referendumresponse model
        return super(ReferendumViewSet, self).opposing(
            request, ballot_item_response_id=1)


class CandidateViewSet(BallotItemResponseViewSet):
    @list_route(['GET'])
    def supporting(self, request, candidate_id):
        """
        Groups making contributions/expenditures in support of a candidate.
        """
        return super(CandidateViewSet, self).supporting(
            request, ballot_item_response_id=candidate_id)

    @list_route(['GET'])
    def opposing(self, request, candidate_id):
        """
        Groups making contributions/expenditures in opposition to a referendum.
        """
        return super(CandidateViewSet, self).opposing(
            request, ballot_item_response_id=candidate_id)


def homepage_view(request):
    """Relevant links and potential issues."""
    template = loader.get_template('homepage.html')
    template_context = {}
    if settings.CRON_LOGS_DIR:
        template_context['cronjobs'] = []
        cronlogs = os.listdir(settings.CRON_LOGS_DIR)
        for cronlog in cronlogs:
            cronlog_filepath = os.path.join(settings.CRON_LOGS_DIR, cronlog)

            # On the deploy host, we archive old logs into an "archive" folder.
            # Skip that folder.
            if os.path.isdir(cronlog_filepath):
                continue

            with open(cronlog_filepath, 'r') as f:
                template_context['cronjobs'] += [f.read()]
    return HttpResponse(template.render(template_context, request))


@login_required
def missing_data_view(request):
    """Report on which ballot data are missing.

    * Ballot - dates should be set (None by default)
    * Beneficiary - what is their position (support/oppose), on which BallotItemSelection?
    *
    """
    template = loader.get_template('missing-ballot-data.html')
    template_context = {
        'bad_ballots': Ballot.objects.filter(date=None)}
    return HttpResponse(template.render(template_context, request))
