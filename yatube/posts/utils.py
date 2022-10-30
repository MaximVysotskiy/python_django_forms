from django.core.paginator import Paginator

from .constants import DISPLAYED_POSTS


def get_page_context(queryset, request):
    paginator = Paginator(queryset, DISPLAYED_POSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return {
        'paginator': paginator,
        'page_number': page_number,
        'page_obj': page_obj,
    }
