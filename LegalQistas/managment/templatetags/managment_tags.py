from django import template
from account.models import GROUP_CLIENT, GROUP_LAWYER, GROUP_MANAGER

register = template.Library()


@register.filter
def is_lawyer(user):
    return user.groups.filter(name=GROUP_LAWYER).exists()


@register.filter
def is_manager(user):
    return user.groups.filter(name=GROUP_MANAGER).exists()


@register.filter
def user_role(user):
    if user.is_superuser or user.groups.filter(name=GROUP_MANAGER).exists():
        return 'Manager'
    if user.groups.filter(name=GROUP_LAWYER).exists():
        return 'Lawyer'
    return 'Client'
