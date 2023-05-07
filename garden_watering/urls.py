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
    path('test/', views.live_measurement ),
    path('insert/', views.insert_sensor_value_api),
    path('sensors/getall/', views.getAllSensorData_api),
    path('sensors/capture/', views.pictureAtMotion_api),
    path('api/enable_relais/', views.enable_relais_api),
    path('api/disable_relais/', views.disable_relais_api),
    path('api/run_motion_detection/', views.motion_detection_api),
    path('api/live/', views.activate_liveStream),
    path('api/register/', views.CreateUserView.as_view(), name='register'),
    path('api/login/', views.login_api, name='login'),
    path('api/logout/', views.logout_api, name='logout'),
    #re_path(r'^.*', TemplateView.as_view(template_name='index.html')),

]
