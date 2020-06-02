from . import views
from django.urls import path

app_name = 'blog'
urlpatterns = [
    path('', views.index, name = 'index'),
    path('blog/', views.blog, name = 'blogpage'),
    path('post/<slug:post>', views.post, name = 'post'),
    path('search/', views.search, name ='search'),
    path('category/<title>', views.categoryView, name ='category'),
]
