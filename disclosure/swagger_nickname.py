"""
Provides the swagger "nickname" field, a friendly name for
the swagger client methods.
"""
from rest_framework.views import get_view_name


def view_name(cls, suffix=None):
    """ Lowercases the view name.
    Front-end will see search.search_view_get() vs. search.Search_View_GET()"""
    if not suffix:
        # Lowercase the default nickname. Default from:
        # http://www.django-rest-framework.org/api-guide/settings/#view_name_function
        return get_view_name(cls, suffix).lower()

    return suffix.lower()
