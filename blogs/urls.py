from django.urls import path
from blogs import views

app_name = 'blogs'

urlpatterns = [
	path('',views.index,name='index'),
]
