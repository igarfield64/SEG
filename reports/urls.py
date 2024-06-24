from django.urls import path
from .views import *


urlpatterns = [
    path('main-report/', main_report, name='main_report')
]