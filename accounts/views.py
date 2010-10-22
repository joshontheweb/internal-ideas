import django.contrib.auth as django_auth
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response

def login(request):
    ''' logs in a user '''
    template_vars = {}
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        try:
            return_url = request.POST['return_url']
        except KeyError:
            return_url = None
        user = django_auth.authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                django_auth.login(request, user)
                if return_url:
                    return HttpResponseRedirect(return_url)
                else:
                    return HttpResponse('Alright! You\'re Logged In')
            else:
                return HttpResponse('This Account is Disabled')
        else:
            return HttpResponse('Invalid Login')
    else:
        try:
            template_vars['return_url'] = request.GET['next']
        except KeyError:
            pass
        return render_to_response('accounts/login.html', template_vars)

def logout(request):
    django_auth.logout(request)
    return HttpResponseRedirect('/')
