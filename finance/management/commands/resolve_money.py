from django.core.management.base import BaseCommand

from ...models import IndependentMoney


class Command(BaseCommand):
    help = 'Set up the test server'
    # option_list = custom_options

    def handle(self, *args, **options):

        related_money = []

        for im in IndependentMoney.objects.all().order_by('-amount'):
            related_money = IndependentMoney.objects.filter(
                amount=im.amount,
                benefactor=im.benefactor, beneficiary=im.beneficiary)
            if related_money.count() <= 1:
                continue
            related_money = list(related_money)
            if related_money.index(im) not in [-1, 0]:
                continue

            print str(im)
            for rm in related_money:
                print "\t%s %10s %s %s" % (
                    rm.report_date, str(rm.reporting_period)[:10], rm.filing_id, rm.source_xact_id)
