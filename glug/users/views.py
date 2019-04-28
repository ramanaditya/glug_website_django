from django.shortcuts import render
import datetime
import pyrebase 
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import auth
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.oauth2 import id_token
from google.auth.transport import requests
from django.conf import settings
from django.core.files.storage import FileSystemStorage

now = datetime.datetime.now()
time = now.strftime("%Y-%m-%d %H:%M")

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
def home(request):
    time = now.strftime("%Y-%m-%d %H:%M")
    user = ""
    event_data = db.child("Created Events").get()
    #print(event_data)
    year_list = []
    event_detail = []
    event_reg_can = []
    for year in event_data.each():
        year_list.append(year.val())
    #print(year_list)
    
    for year in year_list:
        #print(text)
        #print(type(text))
        for month in year.values():
            for date in month.values():
                for name in date.values():
                    for k,detail in name.items():
                        if k == 'details':
                            event_detail.append(detail)
                        elif k == 'Registered':
                            print(k)
                            print(detail) 
                            for i in detail.values():                      
                                event_reg_can.append(i)
                        else:
                            pass
                #print(x)
    print(event_detail)
    print(event_reg_can)
    #event_detail = [{'count': 1, 'created_by': 'adityaraman96@gmail.com', 'created_id': 'OLD7v4aC7KPeUFrXPaSDywWU2Cx2', 'event_date': 'event_date','event_details': 'event_details', 'event_name': 'event_name', 'event_price': 'event_price', 'event_time': 'event_time', 'event_venue': 'event_venue', 'tag': 'ml'}]
    event_reg_can_count = len(event_reg_can)
    event_detail_count = len(event_detail)
    request.session['event_reg_can_count'] = event_reg_can_count
    request.session['event_detail'] = event_detail
    if request.method == "POST":
        value = request.POST.get('sub_mit')
        try:
            user = request.session['user']
            #print(user)
            #print("index")
            #print(user['email'],user['registered'])
            user = user
            
            
            idtoken = request.session['uid']
            a = authe.get_account_info(idtoken)
            if value == 'Create Event':
                value = 3
            if value == 'Open Project':
                value = 4
            print("If try")
            user_f = {'registered':True}
            #print(user)
            return render(request, 'home.html', {'value': value, 'user': user, 'user_f': user_f['registered'], 'event_detail': event_detail, 'time': time, 'event_detail_count': event_detail_count,'event_reg_can':event_reg_can,'event_reg_can_count':event_reg_can_count})
            
        except:
            if value == "Register Now":
                value = 1
            if value == "Login":
                value = 2
            user_f = {'registered':False}
            print("If Except")
            return render(request, 'home.html', {'value': value, 'user': user, 'user_f': user_f['registered'], 'event_detail': event_detail, 'time': time, 'event_detail_count': event_detail_count,'event_reg_can':event_reg_can,'event_reg_can_count':event_reg_can_count})
    else:
        try:
            user = request.session['user']
            value = 0
            user = user
            print("Else try")
            print(user['registered'])
            user_f = {'registered':True}
            return render(request,'home.html',{'value':value,'user':user ,'user_f':user_f['registered'],'event_detail':event_detail,'time':time,'event_detail_count': event_detail_count,'event_reg_can':event_reg_can,'event_reg_can_count':event_reg_can_count})
        except:
            print("Else Except")
            value = 2
            user_f = {'registered':False}
            print(user_f['registered'])
            return render(request, 'home.html', {'value': value, 'user_f': user_f['registered'], 'event_detail': event_detail, 'time': time, 'event_detail_count': event_detail_count,'event_reg_can':event_reg_can,'event_reg_can_count':event_reg_can_count})
        

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
                db.child("users_profle").child(uid).child("details").set(data)
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
                return render(request,"home.html",{"messg":message})
        else:
            message = "Password Didn't Match"
            return render(request,"home.html",{"messg":message})
    else:
        return render(request,"home.html")


#creating        
def event_create(request):
    if request.method == "POST":
        user = request.session['user']
        tag = request.POST.get('tag')
        img_event=request.FILES.get('img_event')
        fs = FileSystemStorage()
        filename = fs.save(img_event.name, img_event)
        img_event_url = fs.url(filename)
        print(img_event)
        tag=tag.split(",")
        event_name = request.POST.get('event_name')
        event_date=request.POST.get('event_date')
        year = int(event_date[-4:])
        month=int(event_date[0:2])
        month_list=['NULL','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
        month_str = month_list[month]
        date = int(event_date[3:5])
        event_price = request.POST.get('event_price')
        event_time=request.POST.get('event_time')
        event_venue = request.POST.get('event_venue')
        event_headline = request.POST.get('event_headline')
        event_details = request.POST.get('event_details')
        contact_number=request.POST.get('contact_number')
        idtoken = request.session['uid']
        a = authe.get_account_info(idtoken)
        a = a['users'][0]
        a= a['localId']
        created_at = time
        data = {
            'event_name': event_name,
            'date': date,
            'month': month,
            'month_str': month_str,
            'year': year,
            'tag':tag,
            'img_event_url':img_event_url,
            'event_time': event_time,
            'event_venue': event_venue,
            'event_price': int(event_price),
            'event_headline': event_headline,
            'event_details': event_details,        
            'created_by':user['email'],
            'contact_number':contact_number,
            'created_id':a,
            'created_at':created_at,
        }
        db.child('Created Events').child(year).child(month).child(date).child(event_name).child('details').update(data)
        return HttpResponseRedirect('/users')

    else:
        user = request.session['user']
        event_detail = request.session['event_detail']
        return render(request, 'event_create.html', {'user': user, 'event_detail': event_detail})


#logout view
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/users/')

def cancel(request):
    return HttpResponseRedirect('/users/')

def event_apply(request):
    if request.method == "POST":
        year = request.POST.get('year')
        month = request.POST.get('month')
        date = request.POST.get('date')
        event_name = request.POST.get('event_name')
        ev_submit = request.POST.get('ev_submit')
        event_reg_can_count = request.session['event_reg_can_count']
        event_reg_can_count = str(int(event_reg_can_count + 1))
        my_dict ={}
        event_dict = request.POST.get('event_dict')
        
        
        print("Dict")
        print(event_dict)
        if(ev_submit == "Apply"):
            user = request.session['user']
            email = user['email']
            event_detail = request.session['event_detail']
            data={
                'email':user['email'],
                'diplayName':user['displayName'],
            }
            uid=user['localId']
            db.child('Created Events').child(year).child(month).child(date).child(event_name).child('Registered').child(uid).update(data)
            return HttpResponseRedirect('/users')
        if(ev_submit == "info"):
            #Dict
            #{'contact_number': '9901561092', 
            #'created_at': '2019-04-28 03:44', 
            #'created_by': 'adityaraman1996@gmail.com', 
            #'created_id': 'XNYX8OnnwUghHZ5q0z3PmNV6bdD3', 
            #'date': 11, 
            #'event_details': 'Nothing Much now', 
            #'event_headline': 'This is a Build-a-thon where you bring your best ideas and prototype.', 
            #'event_name': 'Build-a-thon', 
            #'event_price': 0, 
            #'event_time': '9:00 AM', 
            #'event_venue': 'CS Seminar Hall', 
            #'img_event_url': '/media/Screenshot%202019-04-23%20at%2012.52.59%20PM.png', 
            #'month': 5, 'month_str': 'May', 'tag': ['App', 'Web', 'ML', 'DS'], 'year': 2019}
            event_venue = request.POST.get('event_venue')
            contact_number = request.POST.get('contact_number')
            created_at = request.POST.get('created_at')
            created_by = request.POST.get('created_by')
            event_details = request.POST.get('event_details')
            event_headline = request.POST.get('event_headline')
            event_price = request.POST.get('event_price')
            event_time = request.POST.get('event_time')
            img_event_url = request.POST.get('img_event_url')
            month_str = request.POST.get('month_str')
            tag = request.POST.get('tag')
            return render(request,'events/info.html',{'contact_number': contact_number, 
                                                        'created_at': created_at, 
                                                        'created_by': created_by,  
                                                        'date': date, 
                                                        'event_details': event_details, 
                                                        'event_headline': event_headline, 
                                                        'event_name': event_name, 
                                                        'event_price': int(event_price), 
                                                        'event_time': event_time, 
                                                        'event_venue': event_venue, 
                                                        'img_event_url': img_event_url, 
                                                        'month': month, 'month_str': month_str, 'tag': tag, 'year': year,})

    else:
        return HttpResponseRedirect('/users')


def dashboard_edit(request):
    request.session['user_profile'] = db.child("users_profle").child(uid).child("details").get()
    if request.method == "POST":
        uid = user['uid']
        data ={
            'first name':'first_name',
            'last_name':'last_name',
            
        }
        db.child("users_profle").child(uid).child("details").set(data)
        return render(request,'users/dashboard_edit.html')
    else:
        return render(request,'users/dashboard_edit.html')


def dashboard(request):
    if request.method == "POST":
        return render(request, 'users/dashboard.html')
    else:
        return render(request, 'users/dashboard.html')
