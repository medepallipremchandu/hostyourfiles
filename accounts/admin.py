# blog/admin.py

from django.contrib import admin
from accounts.models import Blog, UploadedPDF

class BlogAdmin(admin.ModelAdmin):
    pass

class UploadedPDFAdmin(admin.ModelAdmin):
    pass


admin.site.register(Blog, BlogAdmin)
admin.site.register(UploadedPDF, UploadedPDFAdmin)