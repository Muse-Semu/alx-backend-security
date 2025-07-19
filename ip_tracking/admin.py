from django.contrib import admin
   from .models import RequestLog, BlockedIP

   @admin.register(RequestLog)
   class RequestLogAdmin(admin.ModelAdmin):
       list_display = ('ip_address', 'path', 'timestamp')
       list_filter = ('timestamp',)
       search_fields = ('ip_address', 'path')

   @admin.register(BlockedIP)
   class BlockedIPAdmin(admin.ModelAdmin):
       list_display = ('ip_address',)
       search_fields = ('ip_address',)