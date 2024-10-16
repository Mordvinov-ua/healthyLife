from django.urls import path
from users.views import *

urlpatterns = [
    path('login/', login, name = 'login'),
    path('registration/', registration, name = 'registration'),
    path('profile/', profile, name = 'profile'),
    path('logout/', logout, name = 'logout'),
    path('send-tracking-email/', send_tracking_email, name='send_tracking_email'),

]