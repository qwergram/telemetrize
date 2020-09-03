from django.db import models


class TelemetryRecord(models.Model):
    telemetryid = models.CharField(max_length=255)
    runtime = models.FloatField()
    time = models.FloatField()
    args = models.CharField(max_length=255)
    kwargs = models.CharField(max_length=255)
    runid = models.UUIDField()
    pwd = models.TextField()
    path = models.TextField()
    executable = models.TextField()
    ver = models.CharField(max_length=255)
    host = models.CharField(max_length=255)
    user = models.CharField(max_length=255)


    def __str__(self):
        return f'{self.telemetryid} - {self.runid}'