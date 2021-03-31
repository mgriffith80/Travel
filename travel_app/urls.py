from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('logout', views.logout),
    path('main', views.main),
    path('login', views.login),
    path('addtrip', views.addtrip),
    path('processTrip', views.process_trip),
    path('trip/<int:tripId>', views.trip),
    path('delete/<int:tripId>', views.delete),
    path('updateTrip/<int:tripId>', views.update_trip),
    path('processUpdateTrip/<int:tripId>', views.process_update_trip),
    path('joinTrip/<int:tripId>', views.join_trip),
    path('unjoinTrip/<int:tripId>', views.unjoin_trip),
    

]