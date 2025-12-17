from django import template

register = template.Library()

@register.filter(name='eh_admin')
def eh_admin(user):
    return user.is_superuser or user.groups.filter(name='Administrador').exists()   