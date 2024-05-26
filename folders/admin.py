from django.contrib import admin
from .models import Folder, UploadFile, UploadZip
# Register your models here.

class UploadFileInline(admin.TabularInline):
    model = UploadFile
    extra = 0
    readonly_fields = ('image', 'date_added',)
    fields = ('image', 'date_added')

    def has_add_permission(self, request, obj):
        return False

@admin.register(Folder)
class FolderAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'token',)
    inlines = [UploadFileInline]

@admin.register(UploadFile)
class UploadImageAdmin(admin.ModelAdmin):
    list_display = ('owner', 'folder', 'image', 'date_added',)
    list_filter = ('owner', 'folder',)
    search_fields = ('owner__username', 'folder__name',)
    
    
admin.site.register(UploadZip)