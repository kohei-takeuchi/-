from django.conf.urls import url
from django.urls import path

from . import views


app_name="account"
urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),  
    path("login/", views.MyLoginView.as_view(), name="login"),
    path("logout/", views.MyLogoutView.as_view(), name="logout"),
    path('signup/', views.RegistrationView.as_view(), name='signup'),
    path('user/', views.UserProfileView.as_view(), name="user"),
    path('account/change/', views.UserChangeView.as_view(), name="change"),
    path('account/sentpass/', views.sent_pass, name="sentpass"),
    path('account/changepass/<str:user>/<str:senttime>', views.password_change, name="changepass"),
    path('password_change_post/', views.password_change_post, name="sentpass"),
]
