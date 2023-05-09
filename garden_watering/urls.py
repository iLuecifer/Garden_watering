"""
URL configuration for garden_watering project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from garden import views 
from django.urls import path, re_path
from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/measure/', views.live_measurement ),
    path('api/insert/', views.Insert_sensor_value_api.as_view()),
    path('api/getall/', views.GetAllSensorData_api.as_view()),
    path('api/capture/', views.PictureAtMotion_api.as_view()),
    path('api/enable_relais/', views.Enable_relais_api.as_view()),
    path('api/disable_relais/', views.Disable_relais_api.as_view()),
    path('api/run_motion_detection/', views.Motion_detection_api.as_view()),
    path('api/live/', views.Activate_liveStream.as_view()),
    path('api/register/', views.CreateUserView.as_view(), name='register'),
    path('api/login/', views.CustomAuthToken.as_view(), name='login'),
    path('api/logout/', views.logout_api, name='logout'),
    path('list/', views.UserList.as_view(), name='logout'),
    #re_path(r'^.*', TemplateView.as_view(template_name='index.html')),

]
