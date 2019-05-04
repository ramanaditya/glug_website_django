from django.shortcuts import render
import datetime
import pyrebase
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import auth
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.oauth2 import id_token
from google.auth.transport import requests
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os
#from glug.pyrebase_settings import db, authe

from django import db
db.connections.close_all()

now = datetime.datetime.now()
time = now.strftime("%Y-%m-%d %H:%M")

BASE_DIRS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
serviceAccount = os.path.join(
    BASE_DIRS, "glugmvit-web-firebase-adminsdk-fcfa3-d4143f72cc.json")

config = {
    'apiKey': os.environ.get('APIKEY', ''),
    'authDomain': os.environ.get('AUTHDOMAIN', ''),
    'databaseURL': os.environ.get('DATA_BASE_URL', ''),
    'projectId': os.environ.get('PROJECT_ID', ''),
    'storageBucket': os.environ.get('STORAGE_BUCKET', ''),
    'messagingSenderId': os.environ.get('messagingSenderId', ''),
    'serviceAccount': "glugmvit-web-firebase-adminsdk-9bz9b-0b162e3c22.json",
}
firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
db = firebase.database()
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
    'projectId': "glugmvit-web",
})


# Create your views here
# .
def home(request):
    #print("Hello")
    time = now.strftime("%Y-%m-%d %H:%M")
    try:
        localId = request.session['localId']
        user_db = db.child('users_profile').child(localId).get()
        user_list = []
        users_profile_info = []
        #print(user_db)
        for per in user_db.each():
            user_list.append(per.val())
        #print(user_list)
        #for person in user_list:
        #    users_profile.append(person['details'])
        users_profile_info = user_list[0]
        #users_profile = request.session['users_profile']
        request.session['users_profile_info'] = users_profile_info
        #print(users_profile)
        #request.session['users_profile'] = users_profile
        #print("End")
    except:
        users_profile_info = {"username": 'username', "verified": 0,
                         'email': 'email', 'password': 'password','registered':0}
   
    if request.method == "POST":
        value = request.POST.get('sub_mit')
        try:
            #user = ""
            event_data = db.child("Created Events").get()
            #event_data.update({'ram':'boy'})
            #print(event_data)
            year_list = []
            event_detail = []
            event_reg_can = []
            event_app_list = []

            for year in event_data.each():
                year_list.append(year.val())
            #print(year_list)
            #print(users_profile['localId'])
            for year in year_list:
                #print(text)
                #print(type(text))
                for month in year.values():
                    for date in month.values():
                        for name in date.values():
                            for k, detail in name.items():
                                if k == 'details':
                                    event_detail.append(detail)
                                elif k == 'Registered':
                                    #print(k)
                                    #print(detail.values())
                                    for i, j in detail.items():
                                        #print('i','j')
                                        #print(i,j)
                                        event_app_list.append(j['email'])
                                        try:
                                            users_profile_info = request.session['users_profile_info']
                                            if i == users_profile_info['localId']:
                                                #print("Iniside lop")
                                                #print(users_profile_info['localId'])
                                                event_reg_can.append(j)
                                                
                                        except:
                                            #print('elase')
                                            pass
                                else:
                                    pass
                        #print(x)
            #print(event_detail)
            #print(event_reg_can)
            #print(event_app_list)
            event_app_list.append('example@gmail.com')
            request.session['event_app_list'] = event_app_list
            try:
                for i in event_reg_can:
                    for p, q in i.items():
                        data[p] = q
                db.child("users_profile").child(localId).child(
                    "details").child("Event Registered").child(data['event_id']).update(data)
            except:
                pass

            '''for i in event_reg_can:
                for j,k in i.items():
                    if k == users_profile['email']:
                        data[j] = k
                    else:
                        pass'''
            #print("here")

            #print(event_reg_can)
            #event_detail = [{'count': 1, 'created_by': 'adityaraman96@gmail.com', 'created_id': 'OLD7v4aC7KPeUFrXPaSDywWU2Cx2', 'event_date': 'event_date','event_details': 'event_details', 'event_name': 'event_name', 'event_price': 'event_price', 'event_time': 'event_time', 'event_venue': 'event_venue', 'tag': 'ml'}]
            event_reg_can_count = len(event_reg_can)
            event_detail_count = len(event_detail)
            #request.session['event_reg_can_count'] = event_reg_can_count
            #request.session['event_detail'] = event_detail\
            #print("End")
        except:
            #print("event_detail in except")
            event_detail = [{
                "contact_number": "9901",
                "created_at": "2019-04-28 23:19",
                "created_by": "adityaraman1996@gmail.com",
                "created_id": "L0Fosodih9gybPuHAvoPztKuRxN2",
                "date": 18,
                "event_details": "",
                "event_headline": "Nothing Much",
                "event_name": "Mozilla Firefox",
                "event_price": 500,
                "event_time": "event_time",
                "event_venue": "Computer Lab",
                "img_event_url": "",
                "month": 4,
                "month_str": "Apr",
                "tag": ["App", "Web"],
                "year": 2019
            }]
            event_detail_count = 0
            event_reg_can_count = 0
            event_reg_can = 0
        if users_profile_info['registered']:
            #user = request.session['user']
            #print(user)
            #print("index")
            #print(user['email'],user['registered'])
            #user = user

            #idtoken = request.session['uid']
            #a = authe.get_account_info(idtoken)
            if value == 'Create Event':
                value = 3
            if value == 'Open Project':
                value = 4
            #print("If try")
            user_f = {'registered': True}
            #print(user)
            return render(request, 'home.html', {'value': value, 'user': users_profile_info, 'user_f': user_f['registered'], 'event_detail': event_detail, 'time': time, 'event_detail_count': event_detail_count, 'event_reg_can': event_reg_can, 'event_reg_can_count': event_reg_can_count, 'event_app_list': event_app_list})

        else:
            if value == "Register Now":
                value = 1
            if value == "Login":
                value = 2
            user_f = {'registered': False}
            #print("If Except")
            return render(request, 'home.html', {'value': value, 'user': "", 'user_f': user_f['registered'], 'event_detail': "", 'time': time, 'event_detail_count': event_detail_count, 'event_reg_can': event_reg_can, 'event_reg_can_count': event_reg_can_count})
    else:
        try:
            #user = ""
            #event_data = db.child("Created Events").get()
            event_data = db.child("Created Events").get()
            #print(event_data)
            year_list = []
            event_detail = []
            event_reg_can = []
            event_app_list = []
            user_reg_dict = {}
            for year in event_data.each():
                year_list.append(year.val())
            #print(year_list)
            #print(users_profile['localId'])
            for year in year_list:
                #print(text)
                #print(type(text))
                for month in year.values():
                    for date in month.values():
                        for name in date.values():
                            for k, detail in name.items():
                                if k == 'details':
                                    event_detail.append(detail)
                                elif k == 'Registered':
                                    #print(k)
                                    #print(detail.values())
                                    for i, j in detail.items():
                                        #print('i','j')
                                        #print(i,j)
                                        #event_app_list.append(j['email'])
                                        try:
                                            users_profile_info = request.session['users_profile_info']
                                            if i == users_profile_info['localId']:
                                                #print(users_profile_info['localId'])
                                                user_reg_dict = j
                                                #print(user_reg_dict)
                                                event_reg_can.append(user_reg_dict)
                                                
                                        except:
                                            #print('elase')
                                            
                                            pass
                                else:
                                    pass
                        #print(x)
                #print(event_detail)
            event_reg_can.append('example@gmail.com')
            #print("list")
            #print(event_reg_can)
            #print(event_app_list)
            request.session['event_app_list'] = event_reg_can
            try:
                for i in event_reg_can:
                    for p, q in i.items():
                        data[p] = q
                localId = request.session['localId']
                db.child("users_profile").child(localId).child(
                    "details").child("Event Registered").child(data['event_id']).update(data)
            except:
                pass

            '''for i in event_reg_can:
                for j,k in i.items():
                    if k == users_profile['email']:
                        data[j] = k
                    else:
                        pass'''
            #print("here")

            #print(event_reg_can)
            #event_detail = [{'count': 1, 'created_by': 'adityaraman96@gmail.com', 'created_id': 'OLD7v4aC7KPeUFrXPaSDywWU2Cx2', 'event_date': 'event_date','event_details': 'event_details', 'event_name': 'event_name', 'event_price': 'event_price', 'event_time': 'event_time', 'event_venue': 'event_venue', 'tag': 'ml'}]
            event_reg_can_count = len(event_reg_can)
            event_detail_count = len(event_detail)
            #request.session['event_reg_can_count'] = event_reg_can_count
            #request.session['event_detail'] = event_detail
        except:
            #print("event_detail in except")
            event_detail = [{
                "contact_number": "9901",
                "created_at": "2019-04-28 23:19",
                "created_by": "adityaraman1996@gmail.com",
                "created_id": "L0Fosodih9gybPuHAvoPztKuRxN2",
                "date": 18,
                "event_details": "",
                "event_headline": "Nothing Much",
                "event_name": "Mozilla Firefox",
                "event_price": 500,
                "event_time": "event_time",
                "event_venue": "Computer Lab",
                "img_event_url": "/media/image5.png",
                "month": 4,
                "month_str": "Apr",
                "tag": ["App", "Web"],
                "year": 2019
            }]
            event_app_list = []
            event_detail_count = 0
            event_reg_can_count = 0
            event_reg_can = 0
        if users_profile_info['registered']:
            #if users_profile['registered']:
            #user = request.session['user']
            value = 0
            #user = users_profile
            #print("Else try")
            #print(users_profile['registered'])
            user_f = {'registered': True}
            return render(request, 'home.html', {'value': value, 'user': users_profile_info, 'user_f': user_f['registered'], 'event_detail': event_detail, 'time': time, 'event_detail_count': event_detail_count, 'event_reg_can': event_reg_can, 'event_reg_can_count': event_reg_can_count, 'event_app_list': event_app_list})
        else:
            #print("Else Except")
            value = 2
            user_f = {'registered': False}
            #print(user_f['registered'])
            return render(request, 'home.html', {'value': value, 'user_f': user_f['registered'], 'event_detail': event_detail, 'time': time, 'event_detail_count': event_detail_count, 'event_reg_can': event_reg_can, 'event_reg_can_count': event_reg_can_count})


def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get("password")
        try:
            user = authe.sign_in_with_email_and_password(email, password)
            a = authe.get_account_info(user['idToken'])
            session_id = user['idToken']
            request.session['uid'] = str(session_id)
            #request.session['user'] = user
            localId = user['localId']
            request.session['localId'] = localId
            #print(localId)
            #print(a)
            #print(user['email'])
            #print(user)
            '''data = {}
            for i,j in user.items():
                data[i] = j
            db.child('users_profile').child(localId).child('details').update(data)'''
            #print("login")
            data = {'emailVerified':a['users'][0]['emailVerified']}
            
            #print(data)
            db.child('users_profile').child(localId).child('details').update(data)
            authe.refresh(user['refreshToken'])

            #request.session['users_profile'] = users_profile
            return HttpResponseRedirect("/")
        except:
            message = "invalid credentials"
            #print(message)
            return HttpResponseRedirect("/", {'msg': message})
    else:
        #print("Not login")
        return HttpResponseRedirect("/")


def register(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        contact_number = request.POST.get('contact_number')
        password = request.POST.get('password')
        confirm_password = request.POST.get('password')
        name = first_name + str(' ') + last_name
        if password == confirm_password:
            try:
                new_user = authe.create_user_with_email_and_password(
                    email, password)
                user_email = authe.send_email_verification(new_user['idToken'])

                uid = new_user['localId']
                data1 = {"first_name": first_name,'last_name':last_name,'name':name,'password':password,'contact_number':contact_number, "verified": 0,'email': new_user['email'],'admin':0,'member':1,'superuser':0}
                '''db.child("users_profile").child(uid).child("details").update(data)'''
                #print("Registered")
                user = authe.sign_in_with_email_and_password(email, password)
                a = authe.get_account_info(user['idToken'])
                session_id = user['idToken']
                request.session['uid'] = str(session_id)
                #request.session['user'] = user
                localId = user['localId']
                request.session['localId'] = localId
                #print(localId)
                #print(a)
                #print(user['email'])
                #print(user)
                data2 = {}
                for i, j in user.items():
                    data2[i] = j
                '''z = db.child('users_profile').child(
                    localId).child('details').update(data_1)'''
                #print("login")
                data = {}
                for i, j in a.items():
                    #print(i, j)
                    if i == 'users':
                        for m, n in j[0].items():
                            #print(m, n)
                            if m == "providerUserInfo":
                                for p, q in n[0].items():
                                    #print(p, q)
                                    data[p] = q
                            else:
                                data[m] = n
                    else:
                        data[i] = j
                #print("DAta 1")
                #print(data1)
                #print("Data 2")
                #print(data2)
                data.update(data1)
                data.update(data2)
                #print(data)
                authe.refresh(user['refreshToken'])
                localId = request.session['localId']
                y = db.child('users_profile').child(localId).child('details').update(data)
                authe.refresh(user['refreshToken'])


                '''print(new_user)
                print(user)
               
                authe.get_account_info(user_login['idToken'])
                session_id = user['idToken']
                request.session['uid'] = str(session_id)
                request.session['user'] = user_login'''
                #print("last register")
                return HttpResponseRedirect("/")
            except:
                #print("Error")
                message = "Unable to create account try again"
                return render(request, "register.html", {"msg": message})
        else:
            message = "Password Didn't Match"
            return render(request, "register.html", {"msg": message})
    else:
        return render(request, "register.html")
#creating
def event_create(request):
    if request.method == "POST":
        users_profile_info = request.session['users_profile_info']
        tag = request.POST.get('tag')
        
        try:
            img_event = request.FILES['img_event']
            fs = FileSystemStorage()
            filename = fs.save(img_event.name, img_event)
            img_event_url = fs.url(filename)
        except:
            img_event_url = ""
        #print(img_event)
        tag = tag.split(",")
        event_name = request.POST.get('event_name')
        event_date = request.POST.get('event_date')
        year = int(event_date[-4:])
        month = int(event_date[0:2])
        month_list = ['NULL', 'Jan', 'Feb', 'Mar', 'Apr', 'May',
                      'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        month_str = month_list[month]
        date = int(event_date[3:5])
        event_price = request.POST.get('event_price')
        event_time = request.POST.get('event_time')
        event_venue = request.POST.get('event_venue')
        event_headline = request.POST.get('event_headline')
        event_details = request.POST.get('event_details')
        contact_number = request.POST.get('contact_number')
        alt_name = request.POST.get('alt_name')
        alt_email = request.POST.get('alt_email')
        alt_contact = request.POST.get('alt_contact')

        #idtoken = request.session['uid']
        #a = authe.get_account_info(idtoken)
        #a = a['users'][0]
        #a = a['localId']
        created_at = time
        try:
            data = {
                'event_name': event_name,
                'date': date,
                'month': month,
                'month_str': month_str,
                'year': year,
                'tag': tag,
                'img_event_url': img_event_url,
                'event_time': event_time,
                'event_venue': event_venue,
                'event_price': int(event_price),
                'event_headline': event_headline,
                'event_details': event_details,
                'created_by_name': users_profile_info['name'],
                'created_by_email': users_profile_info['email'],
                'contact_number': users_profile_info['contact_number'],
                'created_id': users_profile_info['localId'],
                'created_at': created_at,
                'alt_name':alt_name,
                'alt_email':alt_email,
                'alt_contact':alt_contact,
            }
        except:
            data = {
                'event_name': event_name,
                'date': date,
                'month': month,
                'month_str': month_str,
                'year': year,
                'tag': tag,
                'img_event_url': img_event_url,
                'event_time': event_time,
                'event_venue': event_venue,
                'event_price': int(event_price),
                'event_headline': event_headline,
                'event_details': event_details,
                'created_by_name': users_profile_info['name'],
                'created_by_email': users_profile_info['email'],
                'contact_number': contact_number,
                'created_id': users_profile_info['localId'],
                'created_at': created_at,
            }
        
        event_data = db.child("Created Events").get()
        db.child('Created Events').child(year).child(month).child(
            date).child(event_name).child('details').update(data)
        return HttpResponseRedirect('/')

    else:
        users_profile_info = request.session['users_profile_info']
        #event_app_list = request.session['event_app_list']
        #event_detail = request.session['event_detail']
        return render(request, 'event_create.html', {'user': users_profile_info})


#logout view
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')


def cancel(request):
    return HttpResponseRedirect('/')


def event_apply(request):
    if request.method == "POST":
        year = request.POST.get('year')
        month = request.POST.get('month')
        date = request.POST.get('date')
        event_name = request.POST.get('event_name')

        
        #ev_submit = request.POST.get('ev_submit')
        #event_reg_can_count = request.session['event_reg_can_count']
        #event_reg_can_count = str(int(event_reg_can_count + 1))
        #my_dict = {}
        #event_dict = request.POST.get('event_dict')

        #print("Dict")
        #print(event_dict)
    
        #users_profile = request.session['users_profile']
        #email = users_profile['email']
        '''event_detail = request.session['event_detail']
        user_db = db.child('users_profile').get()
        user_list = []
        users_profiel = []
        for per in user_db.each():
            user_list.append(per.val())
        print(user_list)
        for person in user_list:
            users_profile.append(person)
        #print(users_profile)'''
        users_profile_info = request.session['users_profile_info']
        event_id = str(year)+'-'+str(month)+'-'+str(date)
        name = users_profile_info['first_name'] + str(' ') + users_profile_info['last_name']
        data = {
            'event_id': event_id,
            'event_name': event_name,
            'email': users_profile_info['email'],
            'name': name,
            'contact_number': users_profile_info['contact_number'],
            #'last_name': users_profile['last_name'],
            #'contact_number': users_profile['contact_number'],
            #'username': users_profile['username'],
        }
        #uid = user['localId']
        event_app_list = request.session['event_app_list']
        #print("USERS PROFILE")
        #print(users_profile_info)
        localId = request.session['localId']
        event_data = db.child("Created Events").get()
        db.child('Created Events').child(year).child(month).child(date).child(
            event_name).child('Registered').child(localId).update(data)
        users_db = db.child("users_profile").get()
        db.child("users_profile").child(localId).child('details').child('registered_events').child(event_id).child(event_name).update(data)
        return HttpResponseRedirect('/')

    else:
        year = request.session['year']
        month = request.session['month']
        date = request.session['date']
        event_name = request.session['event_name']
        event_id = str(year)+'-'+str(month)+'-'+str(date)
        found = request.session['found']
        return render(request, 'events/info.html', {
            'event_ids' : event_id,
            'event_names': event_name,
            'found':found,
        })


def info(request):
    if request.method == "POST":
        year = request.POST.get('year')
        month = request.POST.get('month')
        date = request.POST.get('date')
        event_name = request.POST.get('event_name')
        ev_submit = request.POST.get('ev_submit')

        request.session['year'] = year
        request.session['month'] = month
        request.session['date'] = date
        request.session['event_name'] = event_name

        #if(ev_submit == "info"):
        event_venue = request.POST.get('event_venue')
        contact_number = request.POST.get('contact_number')
        created_at = request.POST.get('created_at')
        created_by_name = request.POST.get('created_by_name')
        created_by_email = request.POST.get('created_by_email')
        event_details = request.POST.get('event_details')
        event_headline = request.POST.get('event_headline')
        event_price = request.POST.get('event_price')
        event_time = request.POST.get('event_time')
        img_event_url = request.POST.get('img_event_url')
        month_str = request.POST.get('month_str')
        tag = request.POST.get('tag')
        alt_name = request.POST.get('alt_name')
        alt_email = request.POST.get('alt_email')
        alt_contact = request.POST.get('alt_contact')
        event_app_list = request.session['event_app_list']
        
        event_det_list = event_details.split('.')
        
        #print(event_det_list)
        found = 0
        event_id = str(str(year)+'-'+str(month)+'-'+str(date))
        #print("info")
        #print(event_app_list)
        #print(event_id)
        for i in event_app_list:
            if i == "example@gmail.com":
                pass
            elif i['event_id'] == str(event_id):
                found = 1
                break
            else:
                found = 0
        request.session['found'] = found
        try:
            users_profile_info = request.session['users_profile_info']
            return render(request, 'events/info.html', {'contact_number': contact_number,
                                                        'created_at': created_at,
                                                        'created_by_email': created_by_email,
                                                        'created_by_name':created_by_name,
                                                        'date': date,
                                                        'alt_name':alt_name,
                                                        'alt_email':alt_email,
                                                        'alt_contact':alt_contact,
                                                        'event_details': event_det_list,
                                                        'event_headline': event_headline,
                                                        'event_name': event_name,
                                                        'event_price': int(event_price),
                                                        'event_time': event_time,
                                                        'event_venue': event_venue,
                                                        'img_event_url': img_event_url,
                                                        'month': month, 'month_str': month_str, 'tag': tag, 'year': year, 'event_app_list': event_app_list, 'user': users_profile_info,'found':found})
        except:
                return render(request, 'events/info.html', {'contact_number': contact_number,
                                                        'created_at': created_at,
                                                        'created_by_name':created_by_name,
                                                        'created_by_email': created_by_email,
                                                        'date': date,
                                                        'alt_name':alt_name,
                                                        'alt_email':alt_email,
                                                        'alt_contact':alt_contact,
                                                        'event_details': event_det_list,
                                                        'event_headline': event_headline,
                                                        'event_name': event_name,
                                                        'event_price': int(event_price),
                                                        'event_time': event_time,
                                                        'event_venue': event_venue,
                                                        'img_event_url': img_event_url,
                                                        'month': month, 'month_str': month_str, 'tag': tag, 'year': year, 'event_app_list': event_app_list,'found':found})

    else:
        return HttpResponseRedirect('/')




def dashboard_edit(request):
    if request.method == "POST":
        users_profile_info = request.session['users_profile_info']
        email = users_profile_info['email']
        uid = users_profile_info['localId']
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        try:
            dp = request.FILES.get['dp']
            fs = FileSystemStorage()
            filename = fs.save(dp.name, dp)
            dp_url = fs.url(filename)
        except:
            dp_url =""
            
        dob = request.POST.get('dob')
        usn = request.POST.get('usn')
        sem = request.POST.get('sem')
        desc = request.POST.get('desc')
        email = request.POST.get('email')
        contact_number = request.POST.get('contact_number')
        data = {
            'first_name': first_name,
            'last_name': last_name,
            'dp_url': dp_url,
            'dob':dob,
            'usn':usn,
            'sem':sem,
            'desc':desc,
            #'email':email,
            'contact_number':contact_number,
        }
        localId = request.session['localId']
        db.child("users_profile").child(localId).child("details").update(data)
        localId = request.session['localId']
        user_db = db.child('users_profile').child(localId).get()
        user_list = []
        users_profile_info = []
        #print(user_db)
        for per in user_db.each():
            user_list.append(per.val())
        #print(user_list)
        #for person in user_list:
        #    users_profile.append(person['details'])
        users_profile_info = user_list[0]
        #users_profile = request.session['users_profile']
        #request.session['users_profile'] = users_profile
        #print(users_profile)
        return render(request, 'users/dashboard.html',{'user':users_profile_info})
    else:
        users_profile_info = request.session['users_profile_info']
        return render(request, 'users/dashboard_edit.html',{'user':users_profile_info})


def dashboard(request):
    users_profile_info = request.session['users_profile_info']
    count_db = db.child('users_profile').get()
    total_user_count = 0
    for person in count_db.each():
        total_user_count += 1
    #print("Count")
    #print(total_user_count)
    #print(users_profile_info)
    if request.method == "POST":
        return HttpResponseRedirect( '/')
    else:
        return render(request, 'users/dashboard.html',{'user':users_profile_info,'total_user_count':total_user_count})

def resetpassword(request):
    users_profile_info = request.session['users_profile_info']
    authe.send_password_reset_email(users_profile_info['email'])
    auth.logout(request)
    return HttpResponseRedirect('/')
