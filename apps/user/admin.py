from django.contrib import admin
from .models import User

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser', 'last_login', 'date_joined']
    list_display_links = ['id', 'username']
    list_filter = ['is_active', 'is_staff', 'is_superuser']
    search_fields = ['id', 'username', 'email', 'first_name', 'last_name']
    readonly_fields = ['id', 'last_login', 'date_joined']
    ordering = ['id']
    filter_horizontal = ()
    actions_on_top = True
    actions_on_bottom = False
    actions_selection_counter = True
    date_hierarchy = 'date_joined'
    save_on_top = True
    save_on_bottom = False
    save_as = True
    list_per_page = 10
    list_max_show_all = 200
    list_editable = ['is_active', 'is_staff', 'is_superuser']
    show_full_result_count = True
    show_admin_actions = True
    show_change_link = True
    show_delete_link = True
    show_history_link = True
    show_full_documentation_link = True
    preserve_filters = True
