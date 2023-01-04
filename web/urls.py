from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_show, ),
    path('correct', views.correct_show, ),
    path('all', views.all_show, ),
    path('mydata', views.mydata_show, ),
    path('correct/<str:lat>/<str:lon>', views.correctdata_show, ),    
    path('purchase', views.purchase_show, ),  
    path('purchase/<str:latitude>/<str:longitude>', views.purchase_select, ),
]
