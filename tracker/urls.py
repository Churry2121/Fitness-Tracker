from django.urls import path
from . import views

urlpatterns = [ 
    path('workout_list/', views.workout_list, name='workout_list'), 
    path('', views.user_login, name='login'),
    path('add/', views.add_workout, name='add_workout'),
    path('<pk>/delete', views.del_workout, name='delete_workout'), 
    path('<pk>/update', views.update_workout, name='update_workout'),
    path('logout', views.user_logout, name='logout'),
]