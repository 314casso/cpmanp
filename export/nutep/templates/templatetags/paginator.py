# -*- coding: utf-8 -*-
from django import template

register = template.Library()

LEADING_PAGE_RANGE_DISPLAYED = TRAILING_PAGE_RANGE_DISPLAYED = 10
LEADING_PAGE_RANGE = TRAILING_PAGE_RANGE = 8
NUM_PAGES_OUTSIDE_RANGE = 2 
ADJACENT_PAGES = 4

def base_paginator(context):
    paginator = context['paginator']
    page_obj = context['page_obj']
    pages = paginator.num_pages
    page = page_obj.number
    in_leading_range = in_trailing_range = False
    pages_outside_leading_range = pages_outside_trailing_range = range(0)
    if pages <= LEADING_PAGE_RANGE_DISPLAYED + NUM_PAGES_OUTSIDE_RANGE + 1:
        in_leading_range = in_trailing_range = True
        page_range = [n for n in range(1, pages + 1)]
    elif page <= LEADING_PAGE_RANGE:
        in_leading_range = True
        page_range = [n for n in range(1, LEADING_PAGE_RANGE_DISPLAYED + 1)]
        pages_outside_leading_range = [n + pages for n in range(0, -NUM_PAGES_OUTSIDE_RANGE, -1)]
    elif page > pages - TRAILING_PAGE_RANGE:
        in_trailing_range = True
        page_range = [n for n in range(pages - TRAILING_PAGE_RANGE_DISPLAYED + 1, pages + 1) if n > 0 and n <= pages]
        pages_outside_trailing_range = [n + 1 for n in range(0, NUM_PAGES_OUTSIDE_RANGE)]
    else: 
        page_range = [n for n in range(page - ADJACENT_PAGES, page + ADJACENT_PAGES + 1) if n > 0 and n <= pages]
        pages_outside_leading_range = [n + pages for n in range(0, -NUM_PAGES_OUTSIDE_RANGE, -1)]
        pages_outside_trailing_range = [n + 1 for n in range(0, NUM_PAGES_OUTSIDE_RANGE)]

    # Now try to retain GET params, except for 'page'
    # Add 'django.core.context_processors.request' to settings.TEMPLATE_CONTEXT_PROCESSORS beforehand
    request = context['request']
    params = request.GET.copy()        
    if 'page' in params:
        del(params['page'])
    get_params = params.urlencode()

    return {
        'pages': pages,
        'page': page,
        'previous': page_obj.previous_page_number() if page_obj.has_previous() else None,
        'next': page_obj.next_page_number() if page_obj.has_next() else None,
        'has_previous': page_obj.has_previous(),
        'has_next': page_obj.has_next(),
        'page_range': page_range,
        'in_leading_range': in_leading_range,
        'in_trailing_range': in_trailing_range,
        'pages_outside_leading_range': pages_outside_leading_range,
        'pages_outside_trailing_range': pages_outside_trailing_range,
        'get_params': get_params,
    }

def digg_paginator(context):
    base_result = base_paginator(context)
    base_result['ul_class'] = 'ui-widget-content no-border'    
    return base_result
    

def bootstrap_paginator(context):
    base_result = base_paginator(context)
    base_result['ul_class'] = 'pagination'    
    return base_result

 
register.inclusion_tag("paginator.html", takes_context=True)(digg_paginator)
register.inclusion_tag("paginator.html", takes_context=True)(bootstrap_paginator)