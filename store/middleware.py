from store.models import User

class AnonymousQuickMartUser:
    id = None
    name = ''
    email = ''
    role = ''
    is_authenticated = False
    is_anonymous = True

    def __str__(self):
        return 'AnonymousUser'

class QuickMartAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_id = request.session.get('user_id')
        if user_id:
            try:
                user = User.objects.filter(id=user_id).first()
                if user:
                    request.user = user
                else:
                    request.user = AnonymousQuickMartUser()
            except Exception:
                request.user = AnonymousQuickMartUser()
        else:
            request.user = AnonymousQuickMartUser()

        response = self.get_response(request)
        return response

def quickmart_context_processor(request):
    user = getattr(request, 'user', None)
    if not user:
        user = AnonymousQuickMartUser()

    endpoint = ''
    endpoint_dot = ''
    if hasattr(request, 'resolver_match') and request.resolver_match:
        endpoint = request.resolver_match.view_name or ''
        endpoint_dot = endpoint.replace(':', '.')

    return {
        'current_user': user,
        'user': user,
        'request_endpoint': endpoint,
        'endpoint_dot': endpoint_dot,
    }
