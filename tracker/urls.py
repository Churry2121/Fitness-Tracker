from django.urls import path
from . import views

urlpatterns = [ 
    path('', views.workout_list, name='workout_list'), 
    path('add/', views.add_workout, name='add_workout'),
    path('delete/<int:pk>', views.del_workout, name='delete_workout'), 
]