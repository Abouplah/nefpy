#-*- encoding: utf-8 -*
from django import template

register = template.Library()

@register.inclusion_tag('sort_link.html', takes_context=True)
def sort_link(context, field, label):
    request = context['request']
    params = request.GET.copy()
    current_sort = params.get('tri')
    if current_sort == field:
        sort = field + '_desc'
        indicator = u' (croissant)'
    else:
        sort = field
        if current_sort == field + '_desc':
            indicator = u' (décroissant)'
        else:
            indicator = ''

    params['tri'] = sort
    url = request.path + '?' + params.urlencode()
    return dict(label=label, url=url, indicator=indicator)

