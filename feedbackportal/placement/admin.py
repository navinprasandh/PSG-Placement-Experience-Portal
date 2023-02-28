from django.contrib import admin
from .models import Carausel
#from django.contrib.auth.admin import UserAdmin
from placement.models import Student


# Register your models here.
admin.site.register(Carausel)

#class StudentAdmin(UserAdmin):
 #   fieldsets = (
  #      (None, {'fields': ('roll_number', 'password')}),
   #     ('Personal info', {'fields': ('email',)}),
    #    ('Permissions', {
     #       'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
      #  }),
       # ('Important dates', {'fields': ('last_login', 'date_joined')}),
 #   )

admin.site.register(Student)#, StudentAdmin)