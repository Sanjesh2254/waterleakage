from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    WaterLeakageViewSet,
    RecentWaterLeakageViewSet,
    ComplaintReportViewSet,
    get_complaints,
    create_complaint,
    update_complaint,
    delete_complaint,
    receive_data,
    delete_all_leakage_data,
)

router = DefaultRouter()
router.register(r'water_leakage', WaterLeakageViewSet, basename='water_leakage')
router.register(r'current_water_leakage', RecentWaterLeakageViewSet, basename='current_water_leakage')
router.register(r'complaint', ComplaintReportViewSet, basename='complaint')

urlpatterns = [
    path('', include(router.urls)),
    path('issues/', get_complaints, name='get_complaints'),
    path('issues/create/', create_complaint, name='create_complaint'),
    path('issues/<int:pk>/', update_complaint, name='update_complaint'),
    path('issues/<int:pk>/delete/', delete_complaint, name='delete_complaint'),
    path('receive/',receive_data, name='receive_data'),
    path('api/delete-water-data/', delete_all_leakage_data),
]
