import os
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from .forms import AddHomeForm
from openai import OpenAI

from .models import Home, Classified, Style

client = OpenAI(api_key=os.environ.get("API_KEY"),)

def define_style_from_reference(text):
  response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
    {
      "role": "system",
      "content": "You will be provided with a text and your task is to describe its style. You will give an exhaustive description of the style."
    },
    {
      "role": "user",
      "content": text
    }
    ],
    temperature=0.7,
    top_p=1
    )
  
  return response.choices[0].message.content

def give_style_short_description(style):
  response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
    {
      "role": "system",
      "content": "You will be provided with a description of a style. You will give a short description of maximum two words of this style."
    },
    {
      "role": "user",
      "content": style
    }
    ],
    temperature=0.7,
    top_p=1
    )
  
  return response.choices[0].message.content


def create_description_update_classified(style, text):
   response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
    {
      "role": "system",
      "content": "You will be provided with a real estate classified and your task is to rewrite it using the following style: " + style + " in French."
    },
    {
      "role": "user",
      "content": text
    }
    ],
    temperature=0.7,
    top_p=1
    )
   
   return response.choices[0].message.content

# Create your views here.
def define_style(request, slug):
  classified = get_object_or_404(Classified, slug=slug)

  long_description = define_style_from_reference(classified.text)
  short_description = give_style_short_description(long_description)
  style = Style(agent=request.user, short_description = short_description, long_description=long_description)
  style.save()
  classified.style = style
  classified.save()
  return render(request, "classifieds/all-styles.html")

def simple_update_classified_without_home(request):

  if request.method == 'POST':
    
    agent = request.user
    style = request.POST.get('style')
    description = request.POST.get('text')
    name = "Sans nom"
    price = 0

   
    
    text = create_description_update_classified(style, description)
    print(text)

    

    home = Home(name=name, price=price, agent=agent)
    home.save()

    classified = Classified(text=text, home=home)
    classified.save()  

    
  return render(request, 'classifieds/simple-update.html')

def description_update(request, slug):
  classified = Classified.objects.get(slug=slug)
  home = classified.home
  classifieds = Classified.objects.filter(home=home)
  styles = Style.objects.filter(agent = None) | Style.objects.filter(agent=request.user)
  styles = styles.exclude(pk=classified.style.pk)
  
  
  if request.method == 'POST':
    new_version = classifieds.count() + 1
    style_input = request.POST.get('style')
    style=Style.objects.get(pk=style_input)
    description = classified.text
    text = create_description_update_classified(style.long_description, description)
    new_classified = Classified(text=text, home=classified.home, style=style, version=new_version)
    new_classified.save()  
    return redirect('home-detail', slug=home.slug)

  context = {'home': home,
             'classified':classified, 
             'styles':styles}

  return render(request, 'classifieds/description-update.html', context=context)

def add_home(request):
  form = AddHomeForm()

  if request.method == 'POST':
    form = AddHomeForm(request.POST)
    if form.is_valid():
      form = AddHomeForm(request.POST)
      home = form.save(commit=False)
      home.agent = request.user
      home.save()
      return redirect('home-detail', slug=home.slug)
  else:
      for error in list(form.errors.values()):
          print(request, error)
  
  return render(request, 'classifieds/home-create.html', {'form': form})

def agent_homes(request):
  homes = Home.objects.filter(agent=request.user)

  context = {'homes':homes,}

  return render(request, 'classifieds/agent-homes.html', context=context)

def home_detail(request, slug):
  home = get_object_or_404(Home, slug=slug)
  is_complete = False
  is_detailed = False


  if home.features.count() > 0 or home.nb_pieces != None  or home.nb_rooms != None  or home.nb_floors != None or home.city != None or home.neighborhood != None:
    is_detailed = True

  if home.features.count() > 0 and home.nb_pieces  and home.nb_rooms  and home.nb_floors and home.city and home.neighborhood:
    is_complete = True

  print(is_complete)
  
  if Classified.objects.filter(home=home).exists():
    classifieds = Classified.objects.filter(home=home)
    last_classified = classifieds.latest('created_at')
    classifieds = classifieds.order_by('-created_at')[1:]
  else:
    classifieds = None
    last_classified = None

  context = {'home':home,
             'classifieds':classifieds,
             'last_classified' :last_classified,
             'is_complete':is_complete,
             'is_detailed':is_detailed,
             }

  return render(request, 'classifieds/home-detail.html', context=context)