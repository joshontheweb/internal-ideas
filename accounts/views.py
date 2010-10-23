import django.contrib.auth as django_auth
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.contrib import messages

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
                    messages.success(request, "Login Complete")
                    return HttpResponseRedirect("/")
            else:
                messages.error(request, 'This Account is Disabled')
                return HttpResponseRedirect("/")
        else:
            messages.error(request, "Invalid Credentials")
            return HttpResponseRedirect(reverse('login'))
    else:
        try:
            template_vars['return_url'] = request.GET['next']
        except KeyError:
            pass
        return render_to_response('accounts/login.html', template_vars, context_instance=RequestContext(request))

def logout(request):
    django_auth.logout(request)
    messages.success(request, 'Logout Complete')
    return HttpResponseRedirect('/')
