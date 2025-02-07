from django.contrib import admin
from .models import Organization, OrganizationUser, Message

# Register Organization model
@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('organization_id', 'name')  # Display these fields in the list view
    search_fields = ('organization_id', 'name')  # Enable search by organization ID and name

# Register OrganizationUser model
@admin.register(OrganizationUser)
class OrganizationUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'organization')  # Display user and organization in the list view
    search_fields = ('user__username', 'organization__name')  # Enable search by username and organization name

# Register Message model
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('datetime', 'organization', 'user', 'message')  # Display relevant fields in the list view
    list_filter = ('organization', 'datetime')  # Filter messages by organization and datetime
    search_fields = ('user__user__username', 'message')  # Enable search by username and message content
