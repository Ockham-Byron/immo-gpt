from uuid import uuid4
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

class Classified(models.Model):
  id = models.UUIDField(default = uuid4, editable = False, primary_key=True)
  text = models.TextField(blank=False, null=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  slug = models.SlugField(max_length=255, unique= True, default=None, null=True)

  def __str__(self):
     return self.home.name
  
  def save(self, *args, **kwargs):
        super().save()
        # create slug
        if not self.slug:
            self.slug = slugify(self.home.name + '_' + str(_("classified")))
        super(Classified, self).save(*args, **kwargs)
  

class Home(models.Model):
  id = models.UUIDField(default = uuid4, editable=False, primary_key=True)
  agent = models.ForeignKey(User, on_delete=models.CASCADE)
  classified = models.OneToOneField(Classified, on_delete=models.CASCADE, related_name="home")
  name = models.CharField(max_length=150, blank=False, null=False)
  price = models.FloatField(blank=False, null=False)
  features = models.ManyToManyField(HomeFeature)
  nb_pieces = models.IntegerField()
  nb_rooms = models.IntegerField()
  surface = models.IntegerField()
  nb_floors = models.IntegerField()
  city = models.CharField(max_length=150)
  neighborhood = models.CharField(max_length=150)
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

class PieceOfHouse(models.Model):
  id = models.UUIDField(default = uuid4, editable=False, primary_key=True)
  home = models.ForeignKey(Home, related_name="pieces", on_delete=models.PROTECT)
  piece = models.ForeignKey(Piece, on_delete=models.CASCADE)
  surface = models.FloatField()
  features = models.ManyToManyField(PieceFeature)


  