from django.shortcuts import render
import pyrebase 
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import auth
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
#from django.contrib.auth import authenticate,login,logout
from google.oauth2 import id_token
from google.auth.transport import requests



config = {
    'apiKey': "AIzaSyBd9iPWogpUFx0uDNGTL1LwiYgWIYIFMJI",
    'authDomain': "glug-mvit1.firebaseapp.com",
    'databaseURL': "https://glug-mvit1.firebaseio.com",
    'projectId': "glug-mvit1",
    'storageBucket': "glug-mvit1.appspot.com",
    'messagingSenderId': "58837097878",
    'serviceAccount':"/Users/aditya/Desktop/glug_website/glug_website_django/glug/glug-mvit1-firebase-adminsdk-e5ljh-474945bd09.json"

}
firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
db=firebase.database()
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
  'projectId': "glug-mvit1",
})


# Create your views here
# .
def index(request):
    user = ""
    if request.method == "POST":
        
        #a = user[idtoken]
        #b = a['user']
        #a= a['email']
        #print(a)

        value = request.POST.get('sub_mit')
        try:
            #user = request.session['user']
            user = request.session['user']
            print("index")
            print(user['email'],user['registered'])
            user = user
            
            idtoken = request.session['uid']
            a = authe.get_account_info(idtoken)
            if value == 'Register Your Event':
                value = 3
            if value == 'Register your Project':
                value = 4
            print("If try")
            user_f = {'registered':True}
            
        except:
            if value == "Register Now":
                value = 1
            if value == "Login":
                value = 2
            user_f = {'registered':False}
            print("If Except")
        return render(request, 'index.html',{'value':value,'user':user,'user_f':user_f['registered']})
    else:
        try:
            user = request.session['user']
            value = 3
            user = user
            print("Else try")
            print(user['registered'])
            user_f = {'registered':True}
            #authe.refresh(user['refreshToken'])
            return render(request,'index.html',{'value':value,'user':user ,'user_f':user_f['registered']})
            #return render(request,'index.html',{'value':value,'user':user})
        except:
            print("Else Except")
            value = 2
            user_f = {'registered':False}
            print(user_f['registered'])
            return render(request,'index.html',{'value':value,'user_f':user_f['registered']})
        

def login(request):
    if request.method == "POST":
        email=request.POST.get('email')
        password = request.POST.get("password")
        try:
            user = authe.sign_in_with_email_and_password(email,password)
            a = authe.get_account_info(user['idToken'])
            session_id=user['idToken']
            request.session['uid']=str(session_id)
            request.session['user'] = user
            print(user)
            print(user['email'])
            print("login")
            authe.refresh(user['refreshToken'])
            return HttpResponseRedirect("/users")
        except:
            message="invalid credentials"
            print(message)
            return HttpResponseRedirect("/users",{'msg':message})
    else:
        return HttpResponseRedirect("/users")

def register(request):
    if request.method == "POST":
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        confirm_password=request.POST.get('password')
        if password == confirm_password:
            try:
                user=authe.create_user_with_email_and_password(email,password)
                new_user = authe.send_email_verification(user['idToken'])
                print(new_user)
                print(user)
                uid = user['localId']
                
                data={"displayName":username,"verified":"0",'email':email,'password':password}
                db.child("users").child(uid).child("details").set(data)
                print("Registered")
            except:
                print("Error")
                message="Unable to create account try again"
                return render(request,"index.html",{"messg":message})
        else:
            message = "Password Didn't Match"
            return render(request,"index.html",{"messg":message})
        #return render(request,"index.html")
    else:
        return render(request,"index.html")



def data_feed(request):
    if request.method == "POST":
        name = request.POST.get('name')
        verified = request.POST.get('verified')
        last_name = request.POST.get('l_name')
        data={'name':name,'verified':verified,'last_name':last_name}
        idtoken = request.session['uid']
        a = authe.get_account_info(idtoken)
        a = a['users'][0]
        a= a['localId']
        db.child('profile').child(a).child('details').update(data)
        
    else:
        return render(request, 'users/feed.html')
        

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/users/')
