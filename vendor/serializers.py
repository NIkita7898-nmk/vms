from rest_framework import serializers
from .models import MyUser, Vendor, PurchaseOrder


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ("id", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = MyUser.objects.create_user(**validated_data)
        return user


class VendorSerializer(serializers.ModelSerializer):
    class Meta:

        model = Vendor
        fields = "__all__"
        extra_kwargs = {
            "name": {"required": False},
            "contact_details": {"required": False},
            "address": {"required": False},
            "vendor_code": {"required": False},
            "on_time_delivery_rate": {"required": False},
            "quality_rating_avg": {"required": False},
            "average_response_time": {"required": False},
            "fulfillment_rate": {"required": False},
        }


class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = "__all__"
        extra_kwargs = {
            "delivery_date": {"required": False},
            "po_number": {"required": False},
            "items": {"required": False},
            "quantity": {"required": False},
            "vendor": {"required": False},
        }
