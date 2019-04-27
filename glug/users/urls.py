from django.urls import path
from users import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'users'

urlpatterns = [
	path('',views.index,name='index'),
	path('login/',views.login,name='login'),
	path('logout/',views.logout,name="logout"),
	path('register/',views.register,name='register'),
	path('event_create/',views.event_create,name='event_create'),
	
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
