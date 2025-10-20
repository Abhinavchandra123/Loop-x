from django.conf import settings
from django.http import JsonResponse
from .models import AllowedApp




class APIKeyMiddleware:
    """Simple middleware to check X-APP-KEY header for API requests starting with /api/"""


    def __init__(self, get_response):
        self.get_response = get_response


    def __call__(self, request):
        if request.path.startswith('/api/'):
            api_key = request.META.get('HTTP_X_APP_KEY') or request.GET.get('api_key')
            if not api_key:
                return JsonResponse({'detail': 'API key missing'}, status=401)
            try:
                app = AllowedApp.objects.get(api_key=api_key, is_active=True)
            except AllowedApp.DoesNotExist:
                return JsonResponse({'detail': 'Invalid API key'}, status=403)
            response = self.get_response(request)
        return response