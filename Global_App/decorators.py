from . models import *
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect

def logged_inn2(function):
    def _function(request,*args,**kwargs):
        m = Registrations.objects.get(user = request.user)
        if m.User_role != 'admin':
            try:
                del request.session['logg']
                messages.success(request, 'Please login as admin')
                return HttpResponseRedirect('home')
            except:
                messages.success(request, 'Please login as admin')
                return HttpResponseRedirect('home')
        else:
            return function(request, *args, **kwargs)
    return _function
