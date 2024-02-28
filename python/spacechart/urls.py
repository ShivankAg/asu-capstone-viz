from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('scatterplot-data/', views.send_data, name='scatterplot_data'),
    path('fetch_initial_data/', views.fetch_initial_data, name='fetch_initial_data'),
]