import logging
from django.shortcuts import get_object_or_404, redirect, render
from carts.models import Cart
from orders.models import Order, OrderItem
from users.forms import ProfileForm, UserLoginForm, UserRegistrationForm
from django.contrib import auth, messages
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch

from users.models import User

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail


def login(request):
    if request.method == "POST":
        form = UserLoginForm(data = request.POST)
        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            user = auth.authenticate(username=username, password=password)
            session_key = request.session.session_key

            if user:
                auth.login(request, user)
                messages.success(request, f"{username} welkome")
                if session_key:
                    Cart.objects.filter(session_key=session_key).update(user=user)

                redirect_page = request.POST.get("next", None)
                if redirect_page and redirect_page != reverse("logout"):
                    return HttpResponseRedirect(request.POST.get("next"))

                return HttpResponseRedirect(reverse("profile"))
    else:
        form = UserLoginForm()
    
    context={
        "title":"Home-login",
        "form":form
    }
    return render(request, 'users/login.html', context)

def registration(request):
    if request.method == "POST":
        form = UserRegistrationForm(data = request.POST)
        if form.is_valid():
            form.save()

            session_key = request.session.session_key

            user=form.instance
            auth.login(request,user)

            if session_key:
                Cart.objects.filter(session_key=session_key).update(user=user)

            return HttpResponseRedirect(reverse("profile"))
    else:
        form = UserRegistrationForm()
    
    context={
        "title":"Home-registration",
        "form":form
    }
    return render(request, 'users/registration.html', context)

@login_required
def profile(request):
    if request.method == "POST":
        form = ProfileForm(data = request.POST, instance=request.user, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully")
            return HttpResponseRedirect(reverse_lazy("profile"))
        else:
            messages.error(request, "Error updating profile: " + str(form.errors))
    else:
        form = ProfileForm(instance=request.user)
    
    orders =(Order.objects.filter(user=request.user)
              .prefetch_related(
                  Prefetch(
                      "orderitem_set",
                      queryset=OrderItem.objects.select_related("product"),
                  )
              )
              .order_by("-id")
            )

    context={
        "title":"Home-profile",
        "form":form,
        "orders":orders,
    }
    return render(request, 'users/profile.html', context)

@login_required
def logout(request):
    auth.logout(request)
    return redirect(reverse("home"))


# Настройка логирования
logger = logging.getLogger(__name__)

def send_tracking_email(request):
    tracking_number = request.POST.get('tracking_number')
    user_id = request.POST.get('user_id')

    if not tracking_number or not user_id:
        return JsonResponse({'success': False, 'error': 'Не переданы необходимые данные'})

    try:
        user = get_object_or_404(User, id=user_id)  # Получаем пользователя по ID
        if user.email:
            send_mail(
                'Your tracking number',
                f'Your tracking number: {tracking_number}',
                'ukrainehealthy.life@gmail.com',  
                [user.email],
                fail_silently=False,
            )
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'У пользователя нет email'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})