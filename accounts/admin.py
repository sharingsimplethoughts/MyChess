from django.contrib import admin
from .models import *
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    fields = [] #for ordering the fields. even can hide field.
    search_fields = [] #mention search fields
    list_filter = [] #mention filter fields
    list_display = ['username','id','email','first_name','last_name','is_staff'] #display fields
    list_editable = []#edit displayed fields directly. editable fields must present in list_display.
    readonly_fields = ['created_on',]

class CountryCodeAdmin(admin.ModelAdmin):
    search_fields = ['country','count_code','code']

admin.site.register(CountryCode,CountryCodeAdmin)
admin.site.register(User,UserAdmin)
admin.site.register(OTPStorage)
admin.site.register(SkillLevels)
admin.site.register(UserSkillLevels)
admin.site.register(BlackListedToken)
admin.site.register(UserNotification)
admin.site.register(NotificationGroup)
admin.site.register(PlayerPoint)