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
from django.urls import path
from garden import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('test/', views.my_view, name ='my_view'),
    path('insert/', views.insert_sensor_value, name ='insert_sensor_value'),
    path('sensors/getall/', views.getAllSensorData, name ='getAllSensorData'),
    path('sensors/capture/', views.pictureAtMotion, name ='pictureAtMotion'),
    path('api/enable_relais/', views.enable_relais),
    path('api/disable_relais/', views.disable_relais),
    path('api/run_motion_detection/', views.motion_detection_api),
    path('api/live/', views.activate_liveStream),
]
