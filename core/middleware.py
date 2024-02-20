from django.http import HttpResponsePermanentRedirect


class NoWWWRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host()

        if host.lower().startswith('www.'):
            return HttpResponsePermanentRedirect(
                'https://' + host[4:] + request.path
            )
        else:
            return self.get_response(request)
