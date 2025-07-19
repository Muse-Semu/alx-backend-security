from django.utils import timezone
from ip_tracking.models import RequestLog

class IPLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get IP address from request
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        ip_address = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')
        
        # Get path and timestamp
        path = request.path
        timestamp = timezone.now()

        # Create and save log entry
        RequestLog.objects.create(
            ip_address=ip_address,
            path=path,
            timestamp=timestamp
        )

        # Continue processing the request
        response = self.get_response(request)
        return response