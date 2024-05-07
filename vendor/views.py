from django.utils import timezone

from rest_framework.views import APIView
from rest_framework import status, generics
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from django_filters.rest_framework import DjangoFilterBackend

from .serializers import UserSerializer

from .models import Vendor, PurchaseOrder
from .serializers import (
    UserSerializer,
    VendorSerializer,
    PurchaseOrderSerializer,
)
from .filters import PurchaseOrderFilter

from rest_framework.decorators import action
from rest_framework import status


# Create your views here.
class UserCreateAPIView(APIView):
    """
    Api view to create user
    """

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VendorViewSet(generics.ListCreateAPIView):
    """
    A Viewset to create and get vendors
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer


class VendorUpdateDeleteViewSet(generics.RetrieveUpdateDestroyAPIView):
    """
    A Viewset to update and delete vendor
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer


class PurchaseOrderViewSet(generics.ListCreateAPIView):
    """
    A Viewset to create and get purchase orders
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PurchaseOrderFilter


class PurchaseOrderUpdateDeleteViewSet(generics.RetrieveUpdateDestroyAPIView):
    """
    A ViewSet to update and delete purchase orders
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer


class VendorPerformanceAPIView(generics.RetrieveAPIView):
    """
    A Viewset to get performance of vendor
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        performance_data = {
            "on_time_delivery_rate": instance.on_time_delivery_rate,
            "quality_rating_avg": instance.quality_rating_avg,
            "average_response_time": instance.average_response_time,
            "fulfillment_rate": instance.fulfillment_rate,
        }
        return Response(performance_data)


class PurchaseOrderAcknowledgeView(generics.CreateAPIView):
    """
    A ViewSet to acknowledge purchase orders
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        if "vendor" not in data.keys():
            return Response({"message": "vendor id is required"})
        if "items" not in data.keys():
            return Response({"message": "Items are required"})
        if "quantity" not in data.keys():
            return Response({"message": "Item quantity is required"})
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save(acknowledgment_date=timezone.now())
        return Response(
            {"message": "Purchase order acknowledged successfully"},
            status=status.HTTP_201_CREATED,
        )
