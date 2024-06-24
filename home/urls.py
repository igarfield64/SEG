from django.urls import path
from .views import *


urlpatterns = [
    path('', contract, name = 'contract'),
    path('form/', welcome, name='form'),
    path('logout/', clogout, name='logout'),
    path('import_contractors/', import_contractors, name ='import_contractors'),
    path('handle_contractors/', handle_contractors, name = 'handle_contractors'),
    path('review_contractors/', review_contractors, name = 'review_contractors')
]

