from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import City,Speciality,Doctor,User,Slots,Appointment,Patient
# Register your models here.

#admin.site.register(User,UserAdmin)
admin.site.register(City)
admin.site.register(Speciality)
admin.site.register(Doctor)
admin.site.register(Slots)
admin.site.register(Appointment)
admin.site.register(Patient)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields =  ('first_name','last_name','username','email','password','is_doctor','is_patient')
    list_display = ('first_name','username')
