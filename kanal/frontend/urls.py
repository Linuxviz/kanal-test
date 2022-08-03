from django.urls import path

from frontend import views

urlpatterns = [
    path('', views.main_view, name='main_page'),
]
