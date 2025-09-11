from django.urls import path
from main import views

app_name="main"

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:citation_pk>/', views.choice, name='choice'),
    path('<int:opinion>/<int:citation_pk>/', views.index, name='rank'),
    path('add/', views.add, name='add'),
    path('popular/', views.popular, name='popular'),
]