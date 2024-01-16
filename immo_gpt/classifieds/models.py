from uuid import uuid4
from tinymce.models import HTMLField
from django.utils.timezone import now
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.db import models
User = get_user_model()

# Create your models here.

class Piece(models.Model):
  id = models.UUIDField(default = uuid4, editable=False, primary_key=True)
  agent = models.ForeignKey(User, blank = True, null=True, on_delete=models.CASCADE)
  name = models.CharField(max_length=100, unique=True)

  def __str__(self):
     return self.name

class PieceFeature(models.Model):
  id = models.UUIDField(default=uuid4, editable=False, primary_key=True)
  agent = models.ForeignKey(User, on_delete=models.CASCADE)
  short_description = models.CharField(max_length=200)
  long_description = models.TextField

  def __str__(self):
     return self.short_description



class HomeFeature(models.Model):
  id = models.UUIDField(default=uuid4, editable=False, primary_key=True)
  agent = models.ForeignKey(User, on_delete=models.CASCADE)
  short_description = models.CharField(max_length=200)
  long_description = models.TextField()

  def __str__(self):
     return self.short_description


  

class Home(models.Model):
  id = models.UUIDField(default = uuid4, editable=False, primary_key=True)
  agent = models.ForeignKey(User, on_delete=models.CASCADE)
  
  name = models.CharField(max_length=150, blank=False, null=False)
  price = models.FloatField(blank=False, null=False)
  features = models.ManyToManyField(HomeFeature, blank=True)
  nb_pieces = models.IntegerField(null=True, blank=True)
  nb_rooms = models.IntegerField(null=True, blank=True)
  surface = models.IntegerField(null=True, blank=True)
  nb_floors = models.IntegerField(null=True, blank=True)
  city = models.CharField(max_length=150, null=True, blank=True)
  neighborhood = models.CharField(max_length=150, null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  slug = models.SlugField(max_length=255, unique= True, default=None, null=True)

  def __str__(self):
    return self.name
  
  def save(self, *args, **kwargs):
        super().save()
        # create slug
        if not self.slug:
            self.slug = slugify(self.name + '_' + str(self.id))
        super(Home, self).save(*args, **kwargs)

class Style(models.Model):
   id = models.UUIDField(default=uuid4, editable=False, primary_key=True)
   agent = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
   is_agent_style = models.BooleanField(default=False)
   short_description = models.CharField(max_length=200, blank=False, null=False)
   long_description = models.TextField(blank=False, null=False)

   def __str__(self):
      return self.short_description

  

class Classified(models.Model):
  id = models.UUIDField(default = uuid4, editable = False, primary_key=True)
  home = models.ForeignKey(Home, on_delete=models.CASCADE, related_name="classified", null=True, blank=True)
  style = models.ForeignKey(Style, on_delete=models.SET_NULL, null=True, blank=True )
  text = models.TextField(blank=False, null=False)
  corrections = models.TextField(blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  version = models.IntegerField(default=1)
  is_ai_generated = models.BooleanField(default=False)
  slug = models.SlugField(max_length=255, unique= True, default=None, null=True)

  def __str__(self):
     return self.home.name
  
  def save(self, *args, **kwargs):
        super().save()
        # create slug
        if not self.slug:
            self.slug = slugify(self.home.name + '_' + str(_("classified") + '_' + str(self.id))) 
        super(Classified, self).save(*args, **kwargs)

class PieceOfHouse(models.Model):
  id = models.UUIDField(default = uuid4, editable=False, primary_key=True)
  home = models.ForeignKey(Home, related_name="pieces", on_delete=models.PROTECT)
  piece = models.ForeignKey(Piece, on_delete=models.CASCADE)
  surface = models.FloatField()
  features = models.ManyToManyField(PieceFeature)

class Visit(models.Model):
  id = models.UUIDField(default = uuid4, editable = False, primary_key=True)
  home = models.ForeignKey(Home, on_delete=models.CASCADE, related_name="visits", null=True, blank=True)
  style = models.ForeignKey(Style, on_delete=models.SET_NULL, null=True, blank=True )
  text = models.TextField(blank=False, null=False)
  corrections = models.TextField(blank=True, null=True)
  visit_date = models.DateField(blank=True, null=True, default=now)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  version = models.IntegerField(default=1)
  is_ai_generated = models.BooleanField(default=False)
  slug = models.SlugField(max_length=255, unique= True, default=None, null=True)

  @property
  def copy_id(self):
     return self.version + 1000

  def __str__(self):
     return self.home.name + '-visit' + self.visit_date 
  
  def save(self, *args, **kwargs):
        super().save()
        # create slug
        if not self.slug:
            self.slug = slugify(self.home.name + '_' + str(_("visit") + '_' + str(self.id))) 
        super(Visit, self).save(*args, **kwargs)



  