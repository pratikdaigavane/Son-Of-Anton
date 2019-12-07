from django.contrib import admin
from logger.models import *

# Register your models here.



class GeneralLogAdmin(admin.ModelAdmin):
    list_display = ('time', 'level', 'message')  

class SpecialLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'level', 'method', 'status_code') 

admin.site.register(GeneralLog, GeneralLogAdmin)
admin.site.register(SpecialLog, SpecialLogAdmin)

