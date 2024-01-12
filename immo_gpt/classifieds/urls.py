from django.urls import path
from django.utils.translation import gettext as _
from .views import *

urlpatterns = [
  path(_('add-home'), add_home, name='add-home'),
  path(_('update-home/<slug>'), update_home, name='update-home'),
  path(_('agent-homes'), agent_homes, name='agent-homes'),
  path(_('home-detail/<slug>'), home_detail, name='home-detail'),
  path(_('simple-update'), simple_update_classified_without_home, name='simple-update'),
  path(_('delete-home/<slug>'), delete_home, name='delete-home'),
  path(_('description-update/<slug>'), description_update_with_openai, name='description-update'),

  #descriptions
  path(_('add-first-description/<slug>'), add_first_description, name='add-first-description'),
  path(_('edit-description/<slug>'), description_edit, name='edit-description'),
  path(_('delete-description/<slug>'), description_delete, name='delete-description'),

  #styles
  path(_('styles'), styles, name='styles'),
  path(_('add-style'), add_style, name='add-style'),
  path(_('add-style-from-scratch'), add_style_from_scratch, name='add-style-from-scratch'),
  path(_('define-style'), define_style_from_text, name='define-style-from-text'), 
  path(_('define-style/<slug>'), define_style_from_classified, name='define-style-from-classified'), 
  path(_('edit-style/<id>'), edit_style, name='edit-style'),
  path(_('delete-style/<id>'), delete_style, name='delete-style'),

  #visits
  path(_('add-visit/<slug>'), add_visit, name='add-visit'),
    
  #corrections
  path(_('correct-text/<slug>'), correct_text, name="correct-text"),
  path(_('corrections-explanations/<slug>'), explanations, name="explanations"),


] 