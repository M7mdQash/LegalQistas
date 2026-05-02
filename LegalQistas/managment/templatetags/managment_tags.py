from django import template

register = template.Library()


@register.filter
def is_lawyer(user):
    return user.groups.filter(name='lawyer').exists()


@register.filter
def is_manager(user):
    return user.groups.filter(name='manager').exists()


@register.filter
def user_role(user):
    if user.groups.filter(name='manager').exists():
        return 'Manager'
    if user.groups.filter(name='lawyer').exists():
        return 'Lawyer'
    return 'Customer'
