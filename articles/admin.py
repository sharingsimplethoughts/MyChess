from django.contrib import admin
from .models import *
# Register your models here..
admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(VideoCategory)
admin.site.register(Video)
admin.site.register(VideoWatchHistory)
admin.site.register(VideoComment)