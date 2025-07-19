from django.db import models

class RequestLog(models.Model):
    ip_address = models.CharField(max_length=45)  # Supports both IPv4 and IPv6
    timestamp = models.DateTimeField()
    path = models.CharField(max_length=200)
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.ip_address} - {self.path} at {self.timestamp}"

    class Meta:
        ordering = ['-timestamp']

class BlockedIP(models.Model):
    ip_address = models.CharField(max_length=45, unique=True)  # Unique to prevent duplicate IPs

    def __str__(self):
        return self.ip_address