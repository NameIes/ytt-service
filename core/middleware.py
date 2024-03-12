"""NoWWWRedirectMiddleware redirects all HTTP requests from www.domain.com to domain.com."""

from django.http import HttpResponsePermanentRedirect


class NoWWWRedirectMiddleware:
    """Redirects all HTTP requests from www.domain.com to domain.com."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host()

        if host.lower().startswith('www.'):
            return HttpResponsePermanentRedirect(
                'https://' + host[4:] + request.path
            )

        return self.get_response(request)
