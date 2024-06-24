from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import connection
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.urls import reverse
from django.views.decorators.cache import never_cache, cache_control
from django.db.models import Q
from .forms import *
from .models import Contractor
import csv, json
from io import TextIOWrapper
# Create your views here.


#@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/login/')
@never_cache

def contract(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, first_name, last_name, phone, email, badge, created_by, created_on FROM Contractors")
        contractors = cursor.fetchall()
        #if contractors:
            #print(contractors)

    contractors_data = []
    for contractor in contractors:
        contractor_data = {
            'id': contractor[0],
            'first_name': contractor[1],
            'last_name': contractor[2],
            'phone': contractor[3],
            'email': contractor[4],
            'badge': contractor[5],
            'created_by': contractor[6],
            'created_on': contractor[7],
        }
        contractors_data.append(contractor_data)
    return render(request, 'contractor.html', {'contractors': contractors_data})
    


@login_required(login_url='/login/')
@never_cache

def welcome(request):

    if request.method == 'POST':
        form = CommunicatonsForm(request.POST)
        if form.is_valid():
            """The issue was with the condition and 'submit' in request.POST in your welcome view. This condition was checking if the string 'submit' was present in the request.POST dictionary, which is not necessary for checking form validity and saving data.
            When a form is submitted, Django automatically populates request.POST with the form data. The is_valid() method of the form checks if the submitted data is valid based on the form's fields and validation rules.
            By removing and 'submit' in request.POST, the form is saved whenever it is valid, regardless of the submit button being clicked. This change allows the form to be saved correctly when submitted."""
            form.save()
            print(form.cleaned_data)
            request.session['comm-form-submitted'] = True
            return redirect('import_contractors')
        else:
            print("Form Invalid")
        
    else:
        form = CommunicatonsForm()
    return render(request, 'home_view.html', {'form': form})


 
@login_required(login_url='/login/')
@never_cache

def import_contractors(request):
    exists, mismatch = [], []
    if request.method == 'POST':
        csv_file = request.FILES.get('csv_file')

        if not csv_file or not csv_file.name.lower().endswith('.csv'):
            messages.error(request, 'Please upload a valid CSV file.')
            return render(request, 'import_contractors.html')

        with connection.cursor() as cursor:
            try:
                csv_data = TextIOWrapper(csv_file.file, encoding='utf-8')
                csv_reader = csv.reader(csv_data)
                next(csv_reader)  # Skip header row

                for row in csv_reader:
                    # Extract fields from CSV
                    first_name, last_name, phone, email, badge, created_by = row[:6]

                    # Check for existing contrasouctor in the database
                    cursor.execute(
                        "SELECT first_name, last_name, phone, email, badge, created_by FROM Contractors WHERE first_name = %s AND last_name = %s AND phone = %s AND email = %s AND badge = %s AND created_by = %s",
                        [first_name, last_name, phone, email, badge, created_by]
                    )
                    existing_contractor = cursor.fetchone()
                    print("Checking contractor:", first_name, last_name, phone, email, badge, created_by)
                    if existing_contractor:
                        # Append existing contractor to the list
                        exists.append(existing_contractor)
                        #print("Found:",existing_contractor)
                    else:
                        # Append mismatched contractor to the list
                        mismatch.append([first_name, last_name, phone, email, badge, created_by])

                messages.success(request, 'Contractors checked successfully.')
            except Exception as e:
                messages.error(request, f'An error occurred: {e}')
            
            request.session['exists'] = exists
            request.session['mismatch'] = mismatch
            return redirect('handle_contractors')
    
    return render(request, 'import_contractors.html')


@login_required(login_url='/login/')
@never_cache

def handle_contractors(request):

    #if request.session.get('comm-form-submitted'):
    exists_list = request.session.get('exists')
    mismatch_list = request.session.get('mismatch')
    
     
    return render(request, 'handle_contractors.html', {'existing_contractors': exists_list, 'mismatched_contractors': mismatch_list})


@login_required(login_url='/login/')
@never_cache

def review_contractors(request):
    review_set = set(tuple(item) for item in request.session.get('exists', []))
    filtered_contractors = None

    if request.method == 'POST':
        selected_contractors = request.POST.getlist('selected_contractors')
        if selected_contractors:
            for item in selected_contractors:
                contractor_data = tuple(item.split(','))
                review_set.add(contractor_data)
            
            # Convert the set back to a list for the session storage
            review_list = [list(contractor) for contractor in review_set]
            request.session['exists'] = review_list
        else:
            first_name = request.POST.get('first_name', '')
            last_name = request.POST.get('last_name', '')
            badge = request.POST.get('badge', '')
            phone = request.POST.get('phone', '')

            filters = Q()
            if first_name:
                filters &= Q(first_name__icontains=first_name)
            if last_name:
                filters &= Q(last_name__icontains=last_name)
            if badge:
                filters &= Q(badge__icontains=badge)
            if phone:
                filters &= Q(phone__icontains=phone)

            # Apply filters to existing contractors list
            if filters:
                filtered_contractors = Contractor.objects.filter(filters)

    review_list = [list(contractor) for contractor in review_set]
    return render(request, 'review_contractors.html', {
        'review_list': review_list,
        'filtered_contractors': filtered_contractors,
    })

def todo_list(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('<script>window.close();</script>')  # Redirect to success page after saving
    else:
        form = TodoForm() 
    return render(request, 'todo.html', {'form': form})

def clogout(request):
    logout(request)
    response = redirect(reverse('login'))
    return response


"""exists, mismatch = [], []
    if request.method == 'POST':
        csv_file = request.FILES.get('csv_file')

        if not csv_file or not csv_file.name.lower().endswith('.csv'):
            messages.error(request, 'Please upload a valid CSV file.')
            return render(request, 'import_contractors.html')

        with connection.cursor() as cursor:
            try:
                csv_data = TextIOWrapper(csv_file.file, encoding='utf-8')
                csv_reader = csv.reader(csv_data)
                next(csv_reader)  # Skip header row
                for row in csv_reader:
                    #id = int(row[0])
                    first_name = row[0]
                    last_name = row[1]
                    phone = row[2]
                    email = row[3]
                    badge = row[4]
                    created_by = row[5]
                    #created_on = row[7]
                    #print(row)  # Print the row that is being checked
                    cursor.execute("SELECT * FROM Contractors WHERE first_name = %s AND last_name = %s AND phone = %s AND email = %s AND badge = %s AND created_by = %s",
                                   [first_name, last_name, phone, email, badge, created_by])
                    existing_contractor = cursor.fetchone()
                    if existing_contractor:
                        print("Contractor Found in DB:", existing_contractor)
                        existing_contractor = existing_contractor[0:6]
                        print(existing_contractor)
                        exists.append(existing_contractor)
                    else:
                        #print("Contractor not found in database:", row)
                        row = row[0:6]
                
                        mismatch.append(row)
                messages.success(request, 'Contractors checked successfully.')
            except Exception as e:
                messages.error(request, f'An error occurred: {e}')
        
        # Redirect to handle_contractors with exists and mismatch as arguments
        request.session['exists'] = exists
        request.session['mismatch'] = mismatch
        return redirect('handle_contractors')
    
    return render(request, 'import_contractors.html')
"""
