from django.urls import path
from users import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'users'

urlpatterns = [
	path('',views.home,name='home'),
	path('login/',views.login,name='login'),
	path('logout/',views.logout,name="logout"),
	path('register/',views.register,name='register'),
	path('event_create/',views.event_create,name='event_create'),
	path('cancel/',views.cancel,name='cancel'),
	path('event_apply/',views.event_apply,name='event_apply'),
	path('dashboard_edit/', views.dashboard_edit, name="dashboard_edit"),
	path('dashboard/', views.dashboard, name="dashboard"),
	path('info/',views.info, name="info"),
	path('resetpassword/',views.resetpassword,name="resetpassword"),
	
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
