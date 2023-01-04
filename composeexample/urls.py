from django.conf.urls.static import static
from django.conf.urls import include, url
from django.contrib.gis import admin
from django.urls import path
from django.conf import settings
import upload.views as upload
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('web/', include(('web.urls', 'web'),)),
    path('upload/', include(('upload.urls', 'upload'),)),
    path('', include(('account.urls', 'account'),)),
    path('sociallogin/', auth_views.LoginView.as_view(), name='sociallogin'),
    path('sociallogout/', auth_views.LogoutView.as_view(), name='logout'),
    path('auth/', include('social_django.urls', namespace='social')), 
]
