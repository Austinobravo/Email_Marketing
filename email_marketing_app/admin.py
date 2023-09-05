from django.contrib import admin
from .models import Email
# Register your models here.

class EmailAdmin(admin.ModelAdmin):
    list_filter = ['email_address']
    search_fields = ['email_address']

admin.site.register(Email, EmailAdmin)
