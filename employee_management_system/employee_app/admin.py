from django.contrib import admin
from .models import Profile,Employee,CustomField
# Register your models here.
admin.site.register(Profile)
admin.site.register(Employee)
admin.site.register(CustomField)