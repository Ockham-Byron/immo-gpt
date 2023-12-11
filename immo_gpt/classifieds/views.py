import os
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from openai import OpenAI

from .models import Home, Classified

client = OpenAI(api_key=os.environ.get("API_KEY"),)

def create_simple_update_classified(style, text):
   response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
    {
      "role": "system",
      "content": "You will be provided with a real estate classified, and your task is to rewrite it using the following style: " + style
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
def simple_update_classified(request):

  if request.method == 'POST':
    
    agent = request.user
    style = request.POST.get('style')
    description = request.POST.get('text')
    name = "Sans nom"
    price = 0

   
    
    text = create_simple_update_classified(style, description)
    print(text)

    

    home = Home(name=name, price=price, agent=agent)
    home.save()

    classified = Classified(text=text, home=home)
    classified.save()  

    
  return render(request, 'classifieds/simple-update.html')

def add_home(request):
  return render(request, 'classifieds/home-create.html')

def agent_homes(request):
  homes = Home.objects.filter(agent=request.user)

  context = {'homes':homes,}

  return render(request, 'classifieds/agent-homes.html', context=context)

def home_detail(request, slug):
  home = get_object_or_404(Home, slug=slug)
  classified = get_object_or_404(Classified, home=home)

  context = {'home':home,
             'classified':classified}

  return render(request, 'classifieds/home-detail.html', context=context)