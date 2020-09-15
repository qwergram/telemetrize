from django.contrib import admin
from base.models import TelemetryRecord

# Register your models here.

class TelemetryRecordAdmin(admin.ModelAdmin):
    
    list_display = (
        'telemetryid', 'runid', 'args', 'kwargs', 'user', 'host'
    )

admin.site.register(TelemetryRecord, TelemetryRecordAdmin)