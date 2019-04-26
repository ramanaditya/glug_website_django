from django.urls import path
from users import views

app_name = 'users'

urlpatterns = [
	path('',views.index,name='index'),
	path('login/',views.login,name='login'),
	path('logout/',views.logout,name="logout"),
	path('register/',views.register,name='register'),
	path('data_feed/',views.data_feed,name='data_feed'),
	path('event_create/',views.event_create,name='event_create'),
	
]
