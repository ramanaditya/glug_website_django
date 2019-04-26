from django.shortcuts import render
import pyrebase 
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import auth
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.oauth2 import id_token
from google.auth.transport import requests



config = {
    'apiKey': "AIzaSyBmZkSULfm_sKjeQW646OyEUAU_DHCLdEw",
    'authDomain': "glugmvit-web.firebaseapp.com",
    'databaseURL': "https://glugmvit-web.firebaseio.com",
    'projectId': "glugmvit-web",
    'storageBucket': "glugmvit-web.appspot.com",
    'messagingSenderId': "198252493",
    'serviceAccount': "/Users/aditya/Desktop/glug_website/glug_website_django/glug/glugmvit-web-firebase-adminsdk-fcfa3-d4143f72cc.json",
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
    event_data = db.child("Created Events").get()
    dis_data = []
    event_detail = []
    for data in event_data.each():
        dis_data.append(data.val())
    #print(dis_data)
    text = {}
    for i in dis_data:
        text = i
        #print(text)
        #print(type(text))
        for v in text.values():
            for x in v.values():
                event_detail.append(x)
                #print(x)
    #print(event_detail)
    #event_detail = [{'count': 1, 'created_by': 'adityaraman96@gmail.com', 'created_id': 'OLD7v4aC7KPeUFrXPaSDywWU2Cx2', 'event_date': 'event_date','event_details': 'event_details', 'event_name': 'event_name', 'event_price': 'event_price', 'event_time': 'event_time', 'event_venue': 'event_venue', 'tag': 'ml'}]
    if request.method == "POST":
        value = request.POST.get('sub_mit')
        try:
            user = request.session['user']
            print(user)
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
            return render(request, 'index.html',{'value':value,'user':user,'user_f':user_f['registered'],'event_detail':event_detail})
            
        except:
            if value == "Register Now":
                value = 1
            if value == "Login":
                value = 2
            user_f = {'registered':False}
            print("If Except")
            return render(request, 'index.html',{'value':value,'user':user,'user_f':user_f['registered'],'event_detail':event_detail})
    else:
        try:
            user = request.session['user']
            value = 3
            user = user
            print("Else try")
            print(user['registered'])
            user_f = {'registered':True}
            return render(request,'index.html',{'value':value,'user':user ,'user_f':user_f['registered'],'event_detail':event_detail})
        except:
            print("Else Except")
            value = 2
            user_f = {'registered':False}
            print(user_f['registered'])
            return render(request,'index.html',{'value':value,'user_f':user_f['registered'],'event_detail':event_detail})
        

def login(request):
    if request.method == "POST":
        email=request.POST.get('email')
        password = request.POST.get("password")
        try:
            user = authe.sign_in_with_email_and_password(email,password)
            authe.get_account_info(user['idToken'])
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
                user_login = authe.sign_in_with_email_and_password(email,password)
                authe.get_account_info(user_login['idToken'])
                session_id=user['idToken']
                request.session['uid']=str(session_id)
                request.session['user'] = user_login
                return HttpResponseRedirect("/users")
            except:
                print("Error")
                message="Unable to create account try again"
                return render(request,"index.html",{"messg":message})
        else:
            message = "Password Didn't Match"
            return render(request,"index.html",{"messg":message})
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
#creating        
def event_create(request):
    if request.method == "POST":
        user = request.session['user']
        tag = request.POST.get('tag')
        event_name = request.POST.get('event_name')
        event_date=request.POST.get('event_date')
        event_price = request.POST.get('event_price')
        event_time=request.POST.get('event_time')
        event_venue = request.POST.get('event_venue')
        event_details = request.POST.get('event_details')
        idtoken = request.session['uid']
        a = authe.get_account_info(idtoken)
        a = a['users'][0]
        a= a['localId']
        data = {
            'tag':tag,
            'event_name':event_name,
            'created_by':user['email'],
            'created_id':a,
            'event_date':event_date,
            'event_time':event_time,
            'event_venue':event_venue,
            'event_details':event_details,
            'event_price':int(event_price)
        }
        db.child('Created Events').child(event_name).child(tag).child('details').update(data)
        return HttpResponseRedirect('/users')

    else:
        return render(request, 'users/event_create.html')


#logout view
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/users/')
