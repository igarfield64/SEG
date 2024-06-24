from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.cache import never_cache, cache_control
from .forms import *
from home.models import Communications

def main_report(request):

    COMM_CLASS = {0: 'Batch', 1: 'One to One'}
    SERVICE_TYPE = {0: 'Chat', 1: 'Call'}
    COMM_TYPE = {0: 'Inbound', 1: 'Outbound'}

    comms = Communications.objects.all()
    for communication in comms:
        communication.comm_class = COMM_CLASS.get(communication.comm_class, 'Unknown')
        communication.service_type = SERVICE_TYPE.get(communication.service_type, 'Unknown')
        communication.comm_type = COMM_TYPE.get(communication.comm_type, 'Unknown')
    
    context = {'communications':comms}
    print(context)
    return render(request, 'comm_report.html', context)

# Create your views here.
