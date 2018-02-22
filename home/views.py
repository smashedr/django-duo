import logging
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

logger = logging.getLogger('app')


@login_required
@require_http_methods(["GET"])
def home_view(request):
    """
    View  /
    """
    try:
        return render(request, 'home.html')
    except Exception as error:
        logger.exception(error)
        messages.add_message(
            request, messages.WARNING,
            'Error: {}'.format(error),
            extra_tags='danger',
        )
        return render(request, 'home.html')
