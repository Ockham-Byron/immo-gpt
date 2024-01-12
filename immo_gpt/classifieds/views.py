import os
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext as _
from django.utils.text import slugify
from .forms import AddHomeForm, AddFirstDescription, AddEditStyle
from .const import *
from openai import OpenAI

from .models import Home, Classified, Style

client = OpenAI(api_key=os.environ.get("API_KEY"),)

def decode_utf8(text):
    bytes_text = text.encode('latin1')  # Convert to bytes using latin1 encoding
    return bytes_text.decode('utf8')

def detect_language(formatted_prompt):
      response=client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
          {"role": "user", "content":formatted_prompt},
        ]
      )
      return response.choices[0].message.content

def correct_with_explanations(formatted_prompt):
  response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
          {"role": "user", "content":formatted_prompt},
        ]
      )
      
  return response.choices[0].message.content.strip()

def openai_correct_text(formatted_prompt):
  response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
          {"role": "user", "content":formatted_prompt},
        ]
      )
      
  return response.choices[0].message.content.strip()

def detect_style(formatted_prompt):
      response=client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
          {"role": "user", "content":formatted_prompt},
        ]
      )
      return response.choices[0].message.content

def define_style_from_reference(text):
  response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
    {
      "role": "system",
      "content": "You will be provided with a text and your task is to describe its style. Step1: You will recognize the language of the text provided. Step2: You will give a precise description of the style. The description will be in the language recognized in step1 and of maximum 150 words. This style could be reused to write another text so the description of the style has to be general, with no details of the content."
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
@login_required
def styles(request):
  user = request.user
  general_styles= Style.objects.filter(agent=None)
  member_styles= Style.objects.filter(agent=user)

  context = {
    'general_styles':general_styles,
    'member_styles':member_styles
  }
  return render(request, "classifieds/all-styles.html", context=context)

@login_required
def add_style(request):
  if request.method=='POST':
    short_description=request.POST.get('short_description')
    long_description=request.POST.get('long_description')
    style=Style(agent=request.user, short_description=short_description, long_description=long_description)
    style.save()
    return redirect('styles')

  return render(request, "classifieds/define-style.html")

@login_required
def define_style_from_text(request):

  if request.method == "POST":
    text=request.POST.get("text")
    long_description = define_style_from_reference(text)
    short_description = give_style_short_description(long_description)
    style = Style(agent=request.user, short_description = short_description, long_description=long_description)
    style.save()
    return redirect('styles')

  return render(request, "classifieds/define-style-from-text.html")

@login_required
def define_style_from_classified(request, slug):
  classified = get_object_or_404(Classified, slug=slug)
  styles = Style.objects.filter(agent = None) | Style.objects.filter(agent=request.user)
  long_description = define_style_from_reference(classified.text)
  short_description = give_style_short_description(long_description)
  if styles.filter(short_description=short_description).exists():
    style = Style.objects.get(short_description=short_description)
    classified.style = style
    classified.save()
    return redirect('home-detail', classified.home.slug)
  else:
    style = Style(agent=request.user, short_description = short_description, long_description=long_description)
    style.save()
    classified.style = style
    classified.save()
    return redirect('styles')
  
  
@login_required
def edit_style(request, id):
  style = get_object_or_404(Style, id=id)
  if style.agent == request.user:
    own_style = True
  else:
    own_style = False
  if request.method == 'POST':
    form = AddEditStyle(request.POST, instance=style)
    if form.is_valid():
      if own_style:
        style=form.save()
        
      else:
        new_style = form.save(commit=False)
        new_style.agent=request.user
        new_style.save()
      return redirect('styles')
  else:
    form = AddEditStyle(instance=style)

  context = {
    'style':style,
    'own_style':own_style,
    'form':form
  }

  return render(request, 'classifieds/style-create-edit.html',context=context)


@login_required
def delete_style(request, id):
  style=get_object_or_404(Style, id=id)
  style.delete()
  return redirect('styles')

@login_required
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

@login_required
def add_first_description(request,slug):
  home=get_object_or_404(Home, slug=slug)
  if request.method == 'POST':
    form=AddFirstDescription(request.POST)
    if form.is_valid():
      classified = form.save(commit=False)
      classified.home=home
      classified.save()
      return redirect('home-detail', slug= home.slug)
  else:
    form=AddFirstDescription()

  return render(request, 'classifieds/description-create-edit.html', {'form':form, 'home':home})


@login_required
def description_update_with_openai(request, slug):
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
    new_classified = Classified(text=text, home=classified.home, style=style, version=new_version, is_ai_generated=True)
    new_classified.save()  
    return redirect('home-detail', slug=home.slug)

  context = {'home': home,
             'classified':classified, 
             'styles':styles}

  return render(request, 'classifieds/description-update.html', context=context)

@login_required
def description_edit(request, slug):
  classified = get_object_or_404(Classified, slug=slug)
  home = classified.home

  if request.method == 'POST':
    form = AddFirstDescription(request.POST, instance=classified)
    if form.is_valid():
      form.save()
      return redirect('home-detail', slug=home.slug)
  
  else:
    form = AddFirstDescription( instance=classified)

  return render(request, 'classifieds/description-create-edit.html', {'form':form, 'home':home, 'classified':classified})


@login_required
def description_delete(request, slug):
  classified = get_object_or_404(Classified, slug=slug)
  home=classified.home
  classified.delete()
  return redirect('home-detail', slug=home.slug)

@login_required
def add_home(request):
  form = AddHomeForm()

  if request.method == 'POST':
    form = AddHomeForm(request.POST)
    if form.is_valid():
      form = AddHomeForm(request.POST)
      home = form.save(commit=False)
      home.agent = request.user
      home.save()
      return redirect('add-first-description', slug=home.slug)
  else:
      for error in list(form.errors.values()):
          print(request, error)
  
  return render(request, 'classifieds/home-create.html', {'form': form})

@login_required
def update_home(request, slug):
  home = get_object_or_404(Home, slug=slug)
  form = AddHomeForm(instance=home)

  if request.method== 'POST':
    form=AddHomeForm(request.POST, instance=home)
    if form.is_valid():
      home=form.save(commit=False)
      new_slug = slugify(home.name + '_' + str(home.id))
      home.slug = new_slug
      home.save()
      messages.success(request, _('The home has been successfully updated '))
      return redirect(to='home-detail', slug=new_slug)
    
  return render(request, 'classifieds/home-update.html', {'form': form, 'home': home})
    
@login_required
def delete_home(request, slug):
  home = get_object_or_404(Home, slug=slug)
  home.delete()
  return redirect('agent-homes', )


@login_required
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

@login_required
def correct_text(request, slug):
  classified = get_object_or_404(Classified, slug=slug)
  text=classified.text
  formatted_prompt1=LANGUAGE_PROMPT.format(text=text)
  language=detect_language(formatted_prompt1)
  # formatted_prompt2=CORRECTION_GENERATION_PROMPT.format(text=text1, language=language)
  # corrections = correct_with_explanations(formatted_prompt2)
  # classified.corrections=corrections
  formatted_prompt=CORRECT_TEXT_PROMPT.format(text=text, language=language)
  corrected_text=openai_correct_text(formatted_prompt)
  classified.text=corrected_text
  classified.save()
  context = {
    
    'classified':classified
  }

  return render(request, "classifieds/explanations.html", context=context)
  
  
  
@login_required
def explanations(request, slug):
  classified = get_object_or_404(Classified, slug=slug)
  
  return render(request, "classifieds/explanations.html", {'classified':classified})