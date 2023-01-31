"""loop_m URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import path

from .views import RegistrationView, LoginView, LogoutView,PostListView,PostDetailView,ChangePasswordView
from rest_framework_simplejwt import views as jwt_views

app_name = 'users'
from .import views
urlpatterns = [
    path('',views.index,name="index"),
    path('threads/',views.threads,name="threads"),
    path('exportcsv/', views.exportcsv),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/',PostListView.as_view(),name='post-list'),
    path('logout/',views.logout_view,name='logout_page'),
    path('contect_us/',views.contect,name='contect_page'),
    path('resiter/', RegistrationView.as_view(), name='register'),
    path('accounts/login', LoginView.as_view(), name='register'),
    path('accounts/logout', LogoutView.as_view(), name='register'),
    path('accounts/change-password', ChangePasswordView.as_view(), name='register'),
    path('accounts/token-refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    
]
