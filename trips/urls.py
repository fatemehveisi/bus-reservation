from django.urls import path
from .import views

urlpatterns = [
    path('',views.trip_list,name='trip_list'),
    path('<int:pk>/',views.trip_detail,name='trip_detail'),
    path('about/',views.about_page,name='about_page'),
]
