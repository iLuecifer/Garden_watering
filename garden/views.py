import os
from garden.models import SensorValue, WaterPumpeLogs
from datetime import datetime
from django.core import serializers
import datetime
import pytz
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer, CriticaValuesSerializer, SensorValueSerializer, WaterPumpeLogsSerializer
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework.views import APIView
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
#from rest_framework.permissions import IsAuthenticated
from garden_watering.permissions import IsAuthenticatedWithToken
from .utils import call_sensors, stop_motion_detection, relaisON, relaisOFF


tz = pytz.timezone('Europe/Berlin')
now = datetime.datetime.now(tz)


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer

class SensorValueList(APIView):
    serializer_class = UserSerializer
    def get(self, request):
        sensor_values = SensorValue.objects.all()
        serializer = SensorValueSerializer(sensor_values, many=True)
        return Response(serializer.data)

class WaterPumpeLogsList(APIView):
    serializer_class = UserSerializer
    def get(self, request):
        water_pump_logs = WaterPumpeLogs.objects.all()
        serializer = WaterPumpeLogsSerializer(water_pump_logs, many=True)
        return Response(serializer.data)

class Live_measurement(APIView):
    permission_classes = [IsAuthenticatedWithToken]
    def get(self, request):
        results = call_sensors()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
        if not len(results) == 0:
            return JsonResponse({"results": results})
        else:
            return JsonResponse({"text": "kein Daten"})




class Insert_sensor_value_api(APIView):
    permission_classes = [IsAuthenticatedWithToken]
    def post(self, request):
        try:
            results = call_sensors()
            air_temp = results['air_temp']['value'] if 'air_temp' in results else None
            pressure = results['pressure']['value'] if 'pressure' in results else None
            air_hum = results['air_hum']['value'] if 'air_hum' in results else None
            soil_hum = results['soil_hum']['value'] if 'soil_hum' in results else None
            soil_temp = results['soil_temp']['value'] if 'soil_temp' in results else None
            light = results['light']['value'] if 'light' in results else None

            # handle the case where a sensor value is missing
            if None in (air_temp, pressure, air_hum, soil_hum, soil_temp, light):
                return JsonResponse({"code": 400, "message": "missing sensor value"})

            current_log = WaterPumpeLogs.objects.filter(end=None).last()
            if current_log:#if there is a row it means pump ins on
                status = 1
            # handle the case where results is not a dictionary
            sensor_value = []
            sensor_value = SensorValue.objects.create(
                air_temp=air_temp,
                pressure=pressure,
                air_hum=air_hum,
                soil_hum=soil_hum,
                soil_temp=soil_temp,
                light=light,
                timestamp=datetime.datetime.now(),
                status= status
            )
        except:
            # handle all other exceptions
            return JsonResponse({"code": 400, "message": "An error occured while reading and preparing data"})
        else:
            # execute if no exception was raised in the try block
            # return a response indicating that the record was inserted
            return JsonResponse({"code": 200, "message": "successfully added", "data": results})

class GetAllSensorData_api(APIView):
    permission_classes = [IsAuthenticatedWithToken]
    def get(self, request):
        all_sensor_values = SensorValue.objects.all()
        data = serializers.serialize('json', all_sensor_values)
        return JsonResponse(data, safe=False)


motion_detection_running = False

class Motion_detection_api(APIView):
    permission_classes = [IsAuthenticatedWithToken]
    def get(self, request):
        global motion_detection_running
        if motion_detection_running:
            response = stop_motion_detection()
            motion_detection_running = False
            return response
        else:
            command = {'command': 'start'}
            motion_detection_running = True
            stop_signal_file = 'garden/stop_signal/stop_signal.txt'
            if os.path.exists(stop_signal_file):
                os.remove(stop_signal_file)
            return JsonResponse(command)
     



    

class Enable_relais_api(APIView):
    permission_classes = [IsAuthenticatedWithToken]
    #permission_classes = [IsAuthenticated]
    def get(self, request):
        status = 1
        relaisON() 
        water_pump = WaterPumpeLogs(start=datetime.datetime.now(), user=request.user)
        water_pump.save()
        #GPIO.cleanup()
        return JsonResponse({"code":200, "message": "successfully enabled"})



class Disable_relais_api(APIView):
    permission_classes = [IsAuthenticatedWithToken]
    def get(self, request):
        status = 0
        relaisOFF()
        current_log = WaterPumpeLogs.objects.filter(user=request.user, end=None).last()
        # Update the stop time
        if not current_log == None:
            current_log.stop = datetime.datetime.now()
            current_log.save()
        #GPIO.cleanup()
        return JsonResponse({"code":200, "message": "successfully disabled"})

    
class Activate_liveStream(APIView):
    permission_classes = [IsAuthenticatedWithToken]
    def get(self, request):

        from django.http import StreamingHttpResponse
        import cv2

        class CameraStreamView():
            def get_frame(self):
                cap = cv2.VideoCapture(0, cv2.CAP_V4L)
                while True:
                    ret, frame = cap.read()
                    if not ret:
                        break
                    # Convert the frame to JPEG format
                    ret, jpeg = cv2.imencode('.jpg', frame)
                    frame = jpeg.tobytes()
                    yield (b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

            def __call__(self, request):
                return StreamingHttpResponse(self.get_frame(), content_type='multipart/x-mixed-replace; boundary=frame')

        return CameraStreamView()(request)
    

class GetAllRelaisData_api(APIView):
    permission_classes = [IsAuthenticatedWithToken]
    def get(self, request):
        all_sensor_values = WaterPumpeLogs.objects.all()
        data = serializers.serialize('json', all_sensor_values)
        return JsonResponse(data, safe=True)


@api_view(['POST'])
@permission_classes([AllowAny])
def register_api(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({'username': user.username}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@csrf_exempt
class Login_api(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        print(username, password)
        user = authenticate(request=request,
                            username=username, password=password)
        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            print(token, created)
            return JsonResponse({'token': token.token})
        else:
            return JsonResponse({'status': 'fail', 'message': 'Invalid login credentials.'})

@csrf_exempt
def logout_api(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            logout(request)
            return JsonResponse({'status': '200', 'message': 'User logged out.'})
        else:
            return JsonResponse({'status': 'fail', 'message': 'User not authenticated.'})
    else:
        return JsonResponse({'status': 'fail', 'message': 'Invalid request method.'})


class CriticalValuesAPIView(APIView):
    serializer_class = CriticaValuesSerializer
    def get(self, request):
        try:
            with open('/home/it/garden_watering/garden/critical_values.json', 'r') as file:
                data = json.load(file)
                print(data)
        except FileNotFoundError:
            data = {}

        serializer = self.serializer_class(data)  # removed many=True
        print("__________serrrrr____")
        print(serializer.data)  # print serialized data
        return Response(serializer.data)

    def post(self, request):
        serializer = CriticaValuesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        with open('/home/it/garden_watering/garden/critical_values.json', 'w') as file:
            json.dump(serializer.validated_data, file)
        
        return Response(serializer.data)

class UserAPIView(APIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = AuthTokenSerializer

class CustomAuthToken(ObtainAuthToken):
    serializer_class = AuthTokenSerializer
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
