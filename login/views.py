import logging
from duo_web import sign_request, verify_response
from django.conf import settings
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

logger = logging.getLogger('app')
config = settings.CONFIG


@require_http_methods(['GET'])
def login_view(request):
    """
    View  /login/
    """
    if request.user.is_authenticated:
        return redirect('home_view')
    request.session['login_next_url'] = get_next_url(request)
    return render(request, 'login.html')


@require_http_methods(['POST'])
def do_logout(request):
    """
    View  /logout/
    """
    next_url = get_next_url(request)
    logout(request)
    request.session['login_next_url'] = next_url
    return redirect(next_url)


@require_http_methods(['POST'])
def do_login(request):
    """
    View  /auth/
    """
    try:
        _username = request.POST.get('username')
        _password = request.POST.get('password')
        user = authenticate(username=_username, password=_password)
        if user:
            # 2factor
            sign = sign_request(
                config['duo']['ikey'],
                config['duo']['skey'],
                config['duo']['akey'],
                _username,
            )

            data = {
                'sign': sign,
                'host': config['duo']['host'],
            }
            request.session['login_next_url'] = get_next_url(request)
            return render(request, 'duo.html', {'data': data})
        else:
            messages.add_message(
                request, messages.WARNING,
                'Invalid Login. Please Try Again.',
                extra_tags='danger',
            )
            return redirect('login_view')
    except Exception as error:
        logger.exception(error)
        messages.add_message(
            request, messages.WARNING,
            'Error: {}'.format(error),
            extra_tags='danger',
        )
        return redirect('login_view')


@csrf_exempt
@require_http_methods(['POST'])
def do_duo(request):
    """
    View  /duo/
    """
    try:
        sig_response = request.POST.get('sig_response')
        authenticated_username = verify_response(
            config['duo']['ikey'],
            config['duo']['skey'],
            config['duo']['akey'],
            sig_response,
        )
        user = User.objects.get(username=authenticated_username)
        if not user:
            messages.add_message(
                request, messages.WARNING,
                'Two Factor Authentication Failed.',
                extra_tags='danger',
            )
            return redirect('login_view')
        login(request, user)
        return HttpResponseRedirect(get_next_url(request))
    except Exception as error:
        logger.exception(error)
        messages.add_message(
            request, messages.WARNING,
            'Error: {}'.format(error),
            extra_tags='danger',
        )
        return redirect('login_view')


def get_next_url(request):
    """
    Determine 'next' Parameter
    """
    try:
        next_url = request.GET['next']
    except:
        try:
            next_url = request.POST['next']
        except:
            try:
                next_url = request.session['login_next_url']
            except:
                next_url = '/'
    if not next_url:
        next_url = '/'
    if '?next=' in next_url:
        next_url = next_url.split('?next=')[1]
    return next_url
