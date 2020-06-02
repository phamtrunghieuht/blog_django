from django.urls import path
from .views import views
urlpatterns = [
    path('hello/', views.hello, name = 'hello'),
]