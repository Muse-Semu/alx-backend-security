from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from ip_tracking.models import RequestLog, SuspiciousIP

@shared_task
def detect_anomalies():
    # Define sensitive paths
    sensitive_paths = ['/admin', '/login']
    
    # Time window: last 1 hour
    one_hour_ago = timezone.now() - timedelta(hours=1)
    
    # Get IPs with request counts in the last hour
    ip_counts = RequestLog.objects.filter(
        timestamp__gte=one_hour_ago
    ).values('ip_address').annotate(
        request_count=models.Count('id')
    ).filter(request_count__gt=100)
    
    # Flag IPs with over 100 requests/hour
    for ip_data in ip_counts:
        ip_address = ip_data['ip_address']
        count = ip_data['request_count']
        SuspiciousIP.objects.get_or_create(
            ip_address=ip_address,
            defaults={'reason': f'Exceeded 100 requests/hour: {count} requests'}
        )
    
    # Flag IPs accessing sensitive paths
    sensitive_requests = RequestLog.objects.filter(
        timestamp__gte=one_hour_ago,
        path__in=sensitive_paths
    ).values('ip_address').distinct()
    
    for ip_data in sensitive_requests:
        ip_address = ip_data['ip_address']
        SuspiciousIP.objects.get_or_create(
            ip_address=ip_address,
            defaults={'reason': f'Accessed sensitive path(s): {", ".join(sensitive_paths)}'}
        )