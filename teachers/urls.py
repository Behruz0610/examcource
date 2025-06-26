from django.urls import path
from . import views

urlpatterns = [
    path('', views.teachers_list, name='teachers_list'),
]