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
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/measure/', views.Live_measurement.as_view() ),
    path('api/insert/', views.Insert_sensor_value_api.as_view()),
    path('api/getall/', views.SensorValueList.as_view()),
    path('api/enable_relais/', views.Enable_relais_api.as_view()),
    path('api/disable_relais/', views.Disable_relais_api.as_view()),
    path('api/run_motion_detection/', views.Motion_detection_api.as_view()),
    path('api/live/', views.Activate_liveStream.as_view()),
    path('api/relais_data/', views.WaterPumpeLogsList.as_view()),
    path('api/critical_values/', views.CriticalValuesAPIView.as_view()),
    path('api/register/', views.CreateUserView.as_view()),
    path('api/login/', views.CustomAuthToken.as_view()),
    path('api/logout/', views.logout_api),
    path('list/', views.UserList.as_view()),
    path('api/images/', views.image_list),
    path('api/getuser/', views.GetUserView.as_view()),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
