from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import *

User = get_user_model()

# User Model views based on user type
class CustomUserAdmin(UserAdmin):
	fieldsets = (
		(None, {'fields': ('email', 'password')}),
		(_('Personal info'), {'fields': ('name', 'roll_number', 'department', 'course')}),
		(_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
									   'groups', 'user_permissions')}),
		(_('Important dates'), {'fields': ('last_login', 'date_joined')}),
	)
	staff_fieldsets = (
		(None, {'fields': ('email', 'password')}),
		(_('Personal info'), {'fields': ('name', 'roll_number', 'department', 'course')}),
		(_('Permissions'), {'fields': ('is_active', 'is_staff',
									   'groups')}),
		(_('Important dates'), {'fields': ('last_login', 'date_joined')}),
	)
	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('email', 'name', 'roll_number', 'department', 'course', 'password1', 'password2'),
		}),
	)
	list_display = ('email', 'name', 'roll_number', 'department', 'course', 'is_staff',)
	list_filter = ('is_staff', 'is_active', 'groups',)
	search_fields = ('email', 'name', 'roll_number', 'department', 'course',)
	ordering = ('date_joined',)
	staff_readonly_fields = ('last_login', 'date_joined', 'email', 'roll_number',)

	def get_readonly_fields(self, request, obj=None):
		if not request.user.is_superuser:
			return self.staff_readonly_fields
		else:
			return super(CustomUserAdmin, self).get_readonly_fields(request, obj)

	def get_fieldsets(self, request, obj=None):
		if not request.user.is_superuser:
			return self.staff_fieldsets
		else:
			return super(CustomUserAdmin, self).get_fieldsets(request, obj)

class DepartmentAdmin(admin.ModelAdmin):
	list_display = ('name', 'course',)
	search_fields = ('name', 'course',)
	ordering = ('name',)
	list_filter = ('name',)

admin.site.site_title = "Placement Experience Portal Admin Login"
admin.site.index_title = "Placement Experience Portal - Dashboard"
admin.site.site_header = "Placement Experience Portal - Admin"

# Register your models here.
admin.site.register(Carausel)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Department, DepartmentAdmin)
