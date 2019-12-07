from django.db import models




class DBLogEntry(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    level = models.CharField(max_length=10)
    path = models.TextField()
    hostname = models.TextField()
    remote_address = models.TextField()
    method = models.TextField()
    request_data = models.TextField(null=True)
    status_code = models.IntegerField(default=500)
    response = models.TextField(null=True)
    response_time = models.FloatField(default=0)

    def save(self, *args, **kwargs):
        if self.response is None:
            self.response = ""
        if self.request_data is None:
            self.request_data = ""
        if 400 <= self.status_code < 500:
            self.level = 'WARNING'
        if 500 <= self.status_code:
            self.level = 'ERROR'
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class GeneralLogAbs(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    level = models.CharField(max_length=10)
    message = models.TextField()

    class Meta:
        abstract = True


class GeneralLog(GeneralLogAbs):
    pass


class SpecialLog(DBLogEntry):
    pass

# worker log models
