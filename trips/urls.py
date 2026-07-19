from django.urls import path
from .import views

app_name="trips"

urlpatterns = [
    path('',views.trip_list,name='trip_list'),
    path('detail/<int:pk>/',views.trip_detail,name='trip_detail'),
    path('about/',views.about_page,name='about_page'),
    path('results/',views.trip_results,name='trip_results'),
]
