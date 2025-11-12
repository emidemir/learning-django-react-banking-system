# yourapp/middleware.py
from django.shortcuts import redirect
from django.urls import reverse
from rest_framework.response import Response
from rest_framework import status

class VerificationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.user.is_authenticated and not request.user.is_verified:
            # Paths that don't require verification (e.g., the verification endpoint itself)
            allowed_paths = [
                reverse('verify-account'),
            ]

            # If the current request path is not an allowed path
            if request.path not in allowed_paths and not request.path.startswith('/admin/'):
                is_api_request = (
                    request.META.get('HTTP_ACCEPT') == 'application/json' or
                    'api' in request.path # Simple check, adjust as needed for your URL structure
                    # You could also check if view_func is an instance of APIView, but that's more complex
                )

                if is_api_request:
                    return Response(
                        {'detail': 'Account not verified. Please verify your email.'},
                        status=status.HTTP_403_FORBIDDEN
                    )
                else:
                    return redirect(reverse('verify-account'))
        return None