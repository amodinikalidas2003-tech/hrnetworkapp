from django.contrib import admin
from .models import Department, OrganizationalPost, Person, PersonPostHistory

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'manager', 'created_at')

@admin.register(OrganizationalPost)
class OrganizationalPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'department', 'parent_post', 'created_at')

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'national_id', 'user')

@admin.register(PersonPostHistory)
class PersonPostHistoryAdmin(admin.ModelAdmin):
    list_display = ('person', 'post', 'start_date', 'end_date', 'is_active')
    search_fields = ('person__user__username', 'person__user__email', 'post__title')
    list_filter = ('post__department',)
