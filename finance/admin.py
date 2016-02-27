from django.contrib import admin

from . import models
from _django_utils import validate_and_register_admin


class CommitteeBenefactorAdmin(admin.ModelAdmin):
    # We don't want to display unnecessary or calculated fields.
    # In particular locality choices take a while to populate.
    # Also put the fields in a logical order for filling the form.
    fields = ('name', 'type', 'filer_id', 'street', 'city', 'zip_code',
              'photo_url', 'website_url', 'facebook_url', 'twitter_url')


class OtherBenefactorAdmin(admin.ModelAdmin):
    fields = ('name', 'benefactor_type', 'street', 'city', 'zip_code',
              'photo_url', 'website_url', 'facebook_url', 'twitter_url')


class PersonBenefactorAdmin(admin.ModelAdmin):
    fields = ('first_name', 'middle_name', 'last_name', 'occupation',
              'benefactor_type', 'street', 'city', 'zip_code', 'employer',
              'photo_url', 'website_url', 'facebook_url', 'twitter_url')


class BeneficiaryAdmin(admin.ModelAdmin):
    fields = ('name', 'type', 'filer_id', 'support', 'ballot_item_selection',
              'street', 'city', 'zip_code',
              'photo_url', 'website_url', 'facebook_url', 'twitter_url')


class IndependentMoneyAdmin(admin.ModelAdmin):
    readonly_fields = ('benefactor', 'benefactor_zip', 'beneficiary',
                       'amount', 'cumulative_amount', 'report_date',
                       'reporting_period', 'source', 'source_xact_id')

admin.site.register(models.Committee)
admin.site.register(models.Employer)
validate_and_register_admin(
    models.Beneficiary, BeneficiaryAdmin, num_hidden_fields=5)
validate_and_register_admin(
    models.PersonBenefactor, PersonBenefactorAdmin, num_hidden_fields=5)
validate_and_register_admin(
    models.OtherBenefactor, OtherBenefactorAdmin, num_hidden_fields=6)
validate_and_register_admin(
    models.CommitteeBenefactor, CommitteeBenefactorAdmin, num_hidden_fields=9)
validate_and_register_admin(
    models.IndependentMoney, IndependentMoneyAdmin, num_hidden_fields=2)
