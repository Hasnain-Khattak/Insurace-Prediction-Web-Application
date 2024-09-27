from django.urls import path
from .views import home_view, about_us, contact_us, prediction, login_view, RegisterView

urlpatterns = [
    path('', home_view, name='home'),
    path('about-us/', about_us, name='about'),
    path('contact-us/', contact_us, name='contact'),
    path('prediction/', prediction, name='prediction'),
    path('login/', login_view, name='login'),
    path('registration/', RegisterView.as_view(), name='registration'),
    path('predict/', prediction, name='predict'),  # Add this line
]