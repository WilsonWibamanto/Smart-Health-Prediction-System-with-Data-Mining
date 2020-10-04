from django.conf.urls import url
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'predict'

urlpatterns = [
    path('',views.home, name='home'),
    url('liver', views.liver, name="liver"),
    url('heart', views.heart, name="heart"),
    url('profile', views.profile, name="profile"),
    url('predictLiver',views.predictLiver, name="predictLiver"),
    url('predictHeart', views.predictHeart, name="predictHeart"),
    url('viewDatabase',views.viewDatabase, name="viewDatabase"),
    url('search', views.search, name="search"),
    url('registration', views.register, name="registration"),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name="logout"),
]

