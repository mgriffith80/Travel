from django.db import models
from datetime import date, datetime
import re

class UserManager(models.Manager):
    def basic_validator(self, post_data):
        errors = {}
        
        if(len(post_data['first_name']) < 2):
            errors['first_name'] = "First name must be atleast 2 characters"
        if(len(post_data['last_name']) < 2):
            errors['last_name'] = "Last name must be atleast 2 characters"
        

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')  
        if not EMAIL_REGEX.match(post_data['email']):
            errors['email'] = "Invalid email address!"

        user = User.objects.filter(email=post_data['email'])
        if user:
            errors['email'] = "Email already used!"

        if(len(post_data['password']) > 64 or len(post_data['password']) < 8):
            errors['password'] = "Password must be 64 characters or less, and more than 8"
        if(post_data['confirm'] != post_data['password']):
            errors['password'] = "Passwords must match"

            
        return errors

class TripManager(models.Manager):
    def basic_validator(self, post_data):
        errors = {}    

        if(len(post_data['destination']) < 1):
            errors['destination'] = "Destination is required"   
        if(len(post_data['desc']) < 1):
            errors['desc'] = "Description is required" 
        
        if post_data['travel_date_from'] != "":
            travel_date_from = datetime.strptime(post_data['travel_date_from'], '%Y-%m-%d') 
            if travel_date_from < datetime.today():
                errors['travel_date_from'] = "Travel date from must be in the future"

            travel_date_to = datetime.strptime(post_data['travel_date_to'], '%Y-%m-%d')
            if travel_date_to < datetime.today():
                errors['travel_date_to'] = "Travel date to must be in the future"
        else: 
            errors['travel_date_to'] = "Cannot to empty"
        
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager() 


class Trip(models.Model):
    destination = models.CharField(max_length=45)
    desc = models.TextField()
    travel_date_from = models.DateField()
    travel_date_to = models.DateField()
    trips_joined = models.ManyToManyField(User, related_name="trips")
    planned_by = models.ForeignKey(User, related_name="trips_planned", on_delete = models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripManager()

