from rest_framework import serializers
from .models import water_leakage

class WaterLeakageSerializer(serializers.ModelSerializer):
    total_flow = serializers.SerializerMethodField()
    per_hour = serializers.SerializerMethodField()
    average = serializers.SerializerMethodField()

    class Meta:
        model = water_leakage
        fields = '__all__'

    def get_total_flow(self, obj):
        return obj.flow2 + obj.flow3

    def get_per_hour(self, obj):

        one_hour_ago = now() - timedelta(hours=1)
        last_hour_data = water_leakage.objects.filter(timestamp__gte=one_hour_ago)
        total_flow1 = sum(item.flow1 for item in last_hour_data)
        flow1_avg = total_flow1 / len(last_hour_data) if last_hour_data else 0  # Calculate total flow average
        return flow1_avg

    def get_average(self, obj):
        last_10_data = water_leakage.objects.order_by('-id')[:10]
        total_flow1 = sum(item.flow1 for item in last_10_data)
        total_flow2 = sum(item.flow2 for item in last_10_data)
        total_flow3 = sum(item.flow3 for item in last_10_data)
        flow1_avg = total_flow1 / len(last_10_data) if last_10_data else 0
        flow2_avg = total_flow2 / len(last_10_data) if last_10_data else 0
        flow3_avg = total_flow3 / len(last_10_data) if last_10_data else 0
        total_flow_avg = (flow1_avg + flow2_avg + flow3_avg)  # Calculate total flow average
        return {"flow1": flow1_avg, "flow2": flow2_avg, "flow3": flow3_avg, "total_flow": total_flow_avg}

from rest_framework import serializers
from .models import Complaint

class IssueReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = '__all__'


from rest_framework import serializers
from .models import Complaint
from datetime import timedelta
from django.utils.timezone import now

class ComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = '__all__'