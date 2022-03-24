from django import template

from mainweb.models import UserRegistration

register = template.Library()


@register.filter
def get_all_universities(arg=None):
    """ Render all-universities name on search-page"""
    return UserRegistration.objects.all().values('university')
