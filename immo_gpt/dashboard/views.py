from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model

# Create your views here.
def dashboard_view(request):
  if request.user.is_authenticated:
    user=request.user
    stripe_public_key = settings.STRIPE_LIVE_SECRET_KEY
    pricing_table_id = settings.STRIPE_PRICING_TABLE_ID

    context = {'user': user,
               'stripe_public_key': stripe_public_key,
                'pricing_table_id': pricing_table_id,
               }

    return render(request, 'dashboard/dashboard.html', context=context)
  
  else:
    return redirect('login')