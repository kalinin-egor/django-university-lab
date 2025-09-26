from django.urls import path

from . import views

app_name = 'rentals'

urlpatterns = [
    path('ekexam/', views.ekexam_page, name='ekexam'),
]
