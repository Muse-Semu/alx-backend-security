from django.utils import timezone
from django.http import HttpResponseForbidden
from django.core.cache import cache
from django_ipgeolocation.utils import get_ip_geolocation
from ip_tracking.models import RequestLog, BlockedIP

class IPLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get IP address from request
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        ip_address = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')
        
        # Check if IP is blocked
        if BlockedIP.objects.filter(ip_address=ip_address).exists():
            return HttpResponseForbidden("Access denied: Your IP is blocked.")
        
        # Get path and timestamp
        path = request.path
        timestamp = timezone.now()

        # Check cache for geolocation data
        cache_key = f"geolocation_{ip_address}"
        geo_data = cache.get(cache_key)
        
        if not geo_data:
            # Fetch geolocation data if not cached
            try:
                response = get_ip_geolocation(ip_address)
                geo_data = {
                    'country': response.get('country_name', ''),
                    'city': response.get('city', '')
                }
                # Cache for 24 hours (24 * 60 * 60 seconds)
                cache.set(cache_key, geo_data, timeout=24 * 60 * 60)
            except Exception as e:
                # In case of API failure, set empty values
                geo_data = {'country': '', 'city': ''}
        
        # Create and save log entry
        RequestLog.objects.create(
            ip_address=ip_address,
            path=path,
            timestamp=timestamp,
            country=geo_data['country'],
            city=geo_data['city']
        )

        # Continue processing the request
        response = self.get_response(request)
        return response