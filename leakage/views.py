from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import water_leakage
from .serializers import WaterLeakageSerializer

class WaterLeakageViewSet(viewsets.ModelViewSet):
    queryset = water_leakage.objects.all().order_by('-id')[:50]  # Fetch the last 10 records
    serializer_class = WaterLeakageSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'

    
class RecentWaterLeakageViewSet(viewsets.ModelViewSet):
    serializer_class = WaterLeakageSerializer
    
    def get_queryset(self):
        # Get the most recent timestamp
        latest_timestamp = water_leakage.objects.all().order_by('-timestamp').first().timestamp
        data= water_leakage.objects.filter(timestamp=latest_timestamp).order_by('-timestamp')
        print(data)
        # Filter to only include records with the most recent timestamp
        return water_leakage.objects.filter(timestamp=latest_timestamp).order_by('-timestamp')
    
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Complaint
from .serializers import ComplaintSerializer

@api_view(['GET'])
def get_complaints(request):
    username = request.query_params.get('user')
    if username == 'admin':
        complaints = Complaint.objects.all()
    else:
        complaints = Complaint.objects.filter(user=username)
    serializer = ComplaintSerializer(complaints, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_complaint(request):
    serializer = ComplaintSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_complaint(request, pk):
    username = request.query_params.get('user')
    try:
        complaint = Complaint.objects.get(id=pk, user=username)
    except Complaint.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ComplaintSerializer(complaint, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_complaint(request, pk):
    username = request.query_params.get('user')
    try:
        complaint = Complaint.objects.get(id=pk, user=username)
    except Complaint.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    complaint.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


from rest_framework import viewsets
from .models import Complaint
from .serializers import IssueReportSerializer

class ComplaintReportViewSet(viewsets.ModelViewSet):
    queryset =Complaint.objects.all()
    serializer_class = IssueReportSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user']  # Filter by user















# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import water_leakage

@csrf_exempt  # Disable CSRF for simplicity (for testing)
def receive_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Parse JSON data
            flow1 = data.get('flow1')
            flow2 = data.get('flow2')
            flow3 = data.get('flow3')
            pressure = data.get('pressure')

            # Save data to database
            water_leakage.objects.create(flow1=flow1, flow2=flow2, flow3=flow3, pressure=pressure)

            return JsonResponse({"message": "Data saved successfully"}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def get_recent_data(request, count):
    try:
        count = int(count)  # Convert the parameter to an integer
        recent_data = water_leakage.objects.order_by('-id')[:count]  # Get latest N records
        
        # Convert queryset to JSON format
        data_list = [
            {
                "id": obj.id,
                "flow1": obj.flow1,
                "flow2": obj.flow2,
                "flow3": obj.flow3,
                "pressure": obj.pressure,
                "timestamp": obj.timestamp.strftime("%Y-%m-%d %H:%M:%S")
            } 
            for obj in recent_data
        ]

        return JsonResponse({"recent_data": data_list}, safe=False)
    
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
    





from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import water_leakage

@api_view(['DELETE'])
def delete_all_leakage_data(request):
    water_leakage.objects.all().delete()
    return Response({"message": "All water leakage data deleted."}, status=status.HTTP_204_NO_CONTENT)
