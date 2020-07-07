import re

from django.conf import settings
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth import logout

EXEMPT_URLS = [re.compile(settings.LOGIN_URL.lstrip('/'))]
if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
    EXEMPT_URLS += [re.compile(url) for url in settings.LOGIN_EXEMPT_URLS]

class MyMiddleWare:
    def __init__(self, get_response):
        # One time configuration and initializtion
        self.get_response = get_response
    def __call__(self, request):
        """
        Code to be executed for each request
        before the view (and later middleware) are called
        """
        
        response = self.get_response(request)

        """
        Code to be executed for each request/response after
        the view is called
        """
        
        return response
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        called just before django calls the view.
        Return either none or HttpResponse
        """

        path = request.path_info.lstrip('/')

        url_is_exempt = any(url.match(path) for url in EXEMPT_URLS)

        if url_is_exempt:
            if request.user.is_authenticated:
                if path == reverse('ap_accounts:alogout').lstrip('/'):
                    logout(request)
                    return None
                else:
                    return redirect(settings.LOGIN_REDIRECT_URL)
            return None
        else:
            if request.user.is_authenticated:
                return None
            else:
                return redirect(settings.LOGIN_URL)


        # assert hasattr(request, 'user')
        # path = request.path_info.lstrip('/')

        # url_is_exempt = any(url.match(path) for url in EXEMPT_URLS)
        # if path == reverse('accounts:logout').lstrip('/'):
        #     logout(request)

        # if request.user.is_authenticated() and url_is_exempt:
        #     return redirect(settings.LOGIN_REDIRECT_URL)
        # elif request.user.is_authenticated() or url_is_exempt:
        #     return None
        # else:
        # return redirect(settings.LOGIN_URL)

    
    # def process_exception(self, request, exception):
    #     """
    #     Called for the response if exception is raised by view.
    #     Return either none or HttpResponse
    #     """
    #     pass

    # def process_template_response(self, request, response):
    #     """
    #     request - HttpRequest object
    #     response - TemplateResponse objects

    #     return templateresponse
    #     use this for changing templateor context if it is needed.
    #     """
    #     pass
