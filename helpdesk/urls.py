from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

from tickets.forms import LoginForm

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/login/', auth_views.LoginView.as_view(authentication_form=LoginForm, template_name='registration/login.html'), name='login'),
    path('auth/', include('django.contrib.auth.urls')),
    path('', include('tickets.urls')),
]
