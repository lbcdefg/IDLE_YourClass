from django.contrib import admin
from .models import *
 
# Register your models here.
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Member)
admin.site.register(ClassNames)
admin.site.register(Categories)
admin.site.register(Like)