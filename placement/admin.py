from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import *
from django.conf import settings
from django.core.mail import send_mail
User = get_user_model()

# User Model views based on user type
class CustomUserAdmin(UserAdmin):
	fieldsets = (
		(None, {'fields': ('email', 'password')}),
		(_('Personal info'), {'fields': ('name', 'roll_number', 'department', 'course', 'contact', 'year_of_passing', 'placed_company', 'package', 'offer_type')}),
		(_('Permissions'), {'fields': ('is_staff', 'is_superuser',
									   'groups', 'user_permissions')}),
		(_('Important dates'), {'fields': ('last_login', 'date_joined')}),
	)
	staff_fieldsets = (
		(None, {'fields': ('email', 'password')}),
		(_('Personal info'), {'fields': ('name', 'roll_number', 'department', 'course')}),
		(_('Permissions'), {'fields': ('is_staff',
									   'groups')}),
		(_('Important dates'), {'fields': ('last_login', 'date_joined')}),
	)
	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('email', 'name', 'roll_number', 'department', 'course', 'password1', 'password2'),
		}),
	)
	list_display = ('email', 'name', 'roll_number', 'department', 'course', 'contact', 'is_active', 'is_staff',)
	list_filter = ('is_staff', 'is_active', 'groups', 'offer_type', 'department', 'course',)
	search_fields = ('email', 'name', 'roll_number', 'department', 'course',)
	ordering = ('date_joined',)
	staff_readonly_fields = ('last_login', 'date_joined', 'email', 'roll_number',)
	actions = ['make_active', 'make_inactive']

	def make_active(self, request, queryset):
		queryset.update(is_active=True)
		self.message_user(request, "Selected users are now active")
		for user in queryset:
			if user.is_active and not user.is_staff:
				link = settings.BASE_URL
				subject = "Welcome to the Student Portal - Account Activated"
				message = "Hello " + user.name + ",\nWelcome to the Student Portal. Your account has been activated.\n\n Click this link to continue: "+ link +"\n\nRegards,\nStudent Portal"
				email_from = settings.EMAIL_HOST_USER
				recipient_list = [user.email,]
				send_mail(subject, message, email_from, recipient_list)
	make_active.short_description = "Mark selected users as active"

	def make_inactive(self, request, queryset):
		queryset.update(is_active=False)
		self.message_user(request, "Selected users are now inactive")
	make_inactive.short_description = "Mark selected users as inactive"

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

	def save_model(self, request, obj, form, change):
		if obj.is_active and not obj.is_staff:
			link = settings.BASE_URL
			subject = "Welcome to the Student Portal - Account Activated"
			message = "Hello " + obj.name + ",\nWelcome to the Student Portal. Your account has been activated.\n\n Click this link to continue: "+ link +"\n\nRegards,\nStudent Portal"
			email_from = settings.EMAIL_HOST_USER
			recipient_list = [obj.email,]
			send_mail(subject, message, email_from, recipient_list)
		obj.save()

class DepartmentAdmin(admin.ModelAdmin):
	list_display = ('name',)
	search_fields = ('name',)
	ordering = ('name',)
	list_filter = ('name',)

class CourseAdmin(admin.ModelAdmin):
	list_display = ('name', 'department',)
	search_fields = ('name', 'department__name',)
	list_filter = ('department__name',)

admin.site.site_title = "Placement Experience Portal Admin Login"
admin.site.index_title = "Placement Experience Portal - Dashboard"
admin.site.site_header = "Placement Experience Portal - Admin"

# Register your models here.
admin.site.register(Carausel)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Survey)
admin.site.register(SurveyResponse)
