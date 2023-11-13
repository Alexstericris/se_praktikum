from django.contrib import admin
from user.models import User
from .models import *
# Register your models here.

admin.site.register(User)
admin.site.register(Log)
admin.site.register(MetaData)
admin.site.register(Column)
admin.site.register(DataTupel)