from django.contrib import admin

# Register your models here.
from submission.models import *

admin.site.site_header = 'Mocha IDE'
admin.site.site_title = 'Mocha IDE'



admin.site.register(Submission)

class GeneralAdmin(admin.ModelAdmin):
    list_display = ('time', 'level', 'message')   

class ErrorAdmin(admin.ModelAdmin):
    list_display = ('time', 'level', 'message')  

class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'language', 'status', 'exctime', 'mem')  
    search_fields = ('id',)
    list_filter = ('language','status',)


admin.site.register(WorkerErrorLog, ErrorAdmin)
admin.site.register(WorkerGeneralLog, GeneralAdmin)
