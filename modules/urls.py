from django.urls import path
from . import views

urlpatterns = [
    path('module/<int:module_id>/comment/', views.add_module_comment, name='add_module_comment'),
    path('module/<int:module_id>/rating/', views.add_module_rating, name='add_module_rating'),
]