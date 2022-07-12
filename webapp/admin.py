from django.contrib import admin

from webapp.models import Issue


class IssueAdmin(admin.ModelAdmin):
    list_display = ['id', 'summary', 'description', 'status', 'created_at']
    list_display_links = ['summary']
    list_filter = ['summary']
    search_fields = ['id', 'summary']
    fields = ['id', 'summary', 'description', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']


admin.site.register(Issue, IssueAdmin)
