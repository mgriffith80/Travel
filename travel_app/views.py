from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

def index(request):
    return render(request, "login.html")

def register(request):
    errors = User.objects.basic_validator(request.POST)
    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')

    password = request.POST['password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    this_user = User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'], password = pw_hash)
    request.session['user_id'] = this_user.id
    return redirect('/')

def main(request):
    if "user_id" not in request.session:
        return redirect('/')
    context = {
        "trips_nah": Trip.objects.exclude(trips_joined=request.session['user_id']),
        "users_trips": Trip.objects.filter(trips_joined=request.session['user_id']),
        "user": User.objects.get(id=request.session['user_id']),
        "trips": Trip.objects.all()
    }
    return render(request, "main.html", context)

def addtrip(request):
    context = {
        "user": User.objects.get(id=request.session['user_id']),
        "trips": Trip.objects.all()

    }
    return render(request, "addtrip.html", context)

def process_trip(request):
    errors = Trip.objects.basic_validator(request.POST)
    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/addtrip')

    this_user = User.objects.get(id=request.session['user_id'])
    this_trip = Trip.objects.create(destination=request.POST['destination'], desc=request.POST['desc'], travel_date_from=request.POST['travel_date_from'], travel_date_to=request.POST['travel_date_to'], planned_by= this_user)
    this_trip.trips_joined.add(this_user)
    
    return redirect ('/main')

def trip(request, tripId):
    context = {
        "this_user": User.objects.get(id=request.session['user_id']),
        "this_trip": Trip.objects.get(id=tripId),
    }
    return render(request, "tripInfo.html", context)

def delete(request, tripId):
    trip_to_delete = Trip.objects.get(id=tripId)
    trip_to_delete.delete()

    return redirect('/main')

def update_trip(request, tripId):
    context = {
        "user": User.objects.get(id=request.session['user_id']),
        "trip": Trip.objects.get(id=tripId)
    }
    return render(request, "updateTrip.html", context)

def process_update_trip(request, tripId):
    errors = Trip.objects.basic_validator(request.POST)
    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/updateTrip/{tripId}')


    trip_to_update = Trip.objects.get(id=tripId)
    trip_to_update.destination = request.POST['destination']
    trip_to_update.desc = request.POST['desc']
    trip_to_update.travel_date_from = request.POST['travel_date_from']
    trip_to_update.travel_date_to = request.POST['travel_date_to']
    trip_to_update.save()

    return redirect('/main')


def join_trip(request, tripId):
    this_user = User.objects.get(id=request.session['user_id'])
    this_trip = Trip.objects.get(id=tripId)
    this_trip.trips_joined.add(this_user)

    return redirect('/main')

def unjoin_trip(request, tripId):
    this_user = User.objects.get(id=request.session['user_id'])
    this_trip = Trip.objects.get(id=tripId)
    this_trip.trips_joined.remove(this_user) 

    return redirect('/main')

def logout(request):
    del request.session['user_id']
    return redirect('/')

def login(request):   
    user = User.objects.filter(email=request.POST['email'])
    if user:
        logged_user = user[0]
    if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
        request.session['user_id'] = logged_user.id
        return redirect('/main')

    messages.error(request, "Invalid login")

    return redirect('/')
