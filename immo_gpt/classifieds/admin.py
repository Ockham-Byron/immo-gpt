from django.contrib import admin
from .models import Classified, Home

# Register your models here.
class ClassifiedAdmin(admin.ModelAdmin):
  list_display=( 'home', 'created_at', 'updated_at')
  

admin.site.register(Classified, ClassifiedAdmin)

class HomeAdmin(admin.ModelAdmin):
  list_display=( 'agent', 'created_at', 'updated_at')
  

admin.site.register(Home, HomeAdmin)