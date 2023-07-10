from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Book)
@admin.register(IssuedBook)
class IssuedBookAdmin(admin.ModelAdmin):
    list_display = ('user','book','status','requested_date','issued_date','expiry_date')