from django.db import models


# Model for submission


class Submission(models.Model):
    code = models.TextField(null=False)
    input = models.TextField(null=False)
    langs = (('c', 'c'), ('c++', 'c++'), ('py', 'py'))  # Choices for language
    language = models.CharField(max_length=9, choices=langs, default='c')
    statuses = (('queue', 'queue'), ('OK', 'OK'), ('CTE', 'CTE'), ('RTE', 'RTE'))  # Choices for status
    status = models.CharField(max_length=5, choices=statuses, default='queue')
    output = models.TextField()
    error = models.TextField()
    box = models.SmallIntegerField(null=True)  # Box No. of isolate
    exctime = models.TextField(null=True)  # Execution time of the program
    mem = models.TextField(null=True)  # memory consumption by the program


class WorkerGeneralLog(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    level = models.CharField(max_length=10)
    message = models.TextField()


class WorkerErrorLog(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    level = models.CharField(max_length=10)
    message = models.TextField()


