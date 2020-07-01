from django.contrib import admin
from category.models import *
# Register your models here.
admin.site.register(Category)
admin.site.register(Video)
admin.site.register(Comment)