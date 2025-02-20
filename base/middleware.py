from django.conf import settings
from django.http import HttpResponse

class MaintenanceModeMiddleware:
    """
    MIDDLEWARE THAT CHEKCKS IF THE APPLICATION IS IN MAINTENANCE MODE
    IF THE MAINTENANCE_MODE IS SET TO TRUE, IT RENDER AN ERROR MESSAGE
    """
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        if getattr(settings, 'MAINTENANCE_MODE', False):
            return HttpResponse('Sorry, the application is currently in maintenance mode. Please try again later.', status=503)
        return self.get_response(request)