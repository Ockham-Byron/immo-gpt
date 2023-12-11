from django.urls import path
from django.utils.translation import gettext as _
from .views import *

urlpatterns = [
    path(_('simple-update'), simple_update_classified, name='simple-update')
    
] 