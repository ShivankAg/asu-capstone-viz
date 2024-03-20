from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('scatterplot-data/', views.send_data, name='scatterplot_data'),
    path('fetch_initial_data/', views.fetch_initial_data, name='fetch_initial_data'),
    # path('predict_next_point/', views.predict_next_point, name='predict_next_point'),
    path('time_to_ground/', views.predict_time_to_ground, name='time_to_ground'),
]