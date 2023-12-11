from django.urls import path
from django.utils.translation import gettext as _
from .views import *

urlpatterns = [
  path(_('add-home'), add_home, name='add-home'),
  path(_('agent-homes'), agent_homes, name='agent-homes'),
  path(_('home-detail/<slug>'), home_detail, name='home-detail'),
    path(_('simple-update'), simple_update_classified, name='simple-update')
    
] 