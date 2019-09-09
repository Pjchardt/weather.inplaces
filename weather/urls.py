from django.urls import path

from . import views

app_name = 'weather'
urlpatterns = [
    path('', views.index, name='index'),
    path('<slug:name>/', views.get_user, name='get_user'),
]
