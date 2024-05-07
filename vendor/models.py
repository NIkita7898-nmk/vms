from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

from constant import STATUS_CHOICE


# Create your models here.
class CustomUserManager(BaseUserManager):
    """
    Base user manager
    """

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class MyUser(AbstractBaseUser, PermissionsMixin):
    """
    Model to store data of registered User"""

    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Vendor(models.Model):
    """
    Model to store details of vendor
    """

    name = models.CharField(max_length=50, blank=False, null=False)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(unique=True, max_length=50)
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self):
        return self.name


class PurchaseOrder(models.Model):
    """
    Model to store detail about purchase order
    """

    po_number = models.CharField(unique=True, max_length=50)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField(null=True)
    items = models.JSONField()
    quantity = models.PositiveIntegerField()
    status = models.CharField(choices=STATUS_CHOICE, default="pending", max_length=20)
    quality_rating = models.FloatField(null=True)
    issue_date = models.DateTimeField(auto_now_add=True)
    acknowledgment_date = models.DateTimeField(null=True)

    def __str__(self):
        return self.po_number


class Performance(models.Model):
    """
    Model to store performance details of any vendor
    """

    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def on_time_delivery_rate(self):
        completed_pos = PurchaseOrder.objects.filter(status="completed")
        total_completed_pos = completed_pos.count()
        on_time_delivered_pos = completed_pos.filter(
            delivery_date__lte=timezone.now()
        ).count()
        if total_completed_pos == 0:
            return 0
        return (on_time_delivered_pos / total_completed_pos) * 100

    def quality_rating_avg(self):
        completed_pos_with_rating = PurchaseOrder.objects.filter(
            status="completed", quality_rating__isnull=False
        )
        if completed_pos_with_rating.exists():
            return completed_pos_with_rating.aggregate(
                avg_rating=avg("quality_rating")
            )["avg_rating"]
        return 0

    def average_response_time(self):
        acknowledged_pos = PurchaseOrder.objects.filter(status="acknowledged")
        if acknowledged_pos.exists():
            response_times = acknowledged_pos.values_list(
                "acknowledgment_date", flat=True
            ) - acknowledged_pos.values_list("issue_date", flat=True)
            return sum(response_times, timezone.timedelta()) / len(response_times)
        return timezone.timedelta()

    def fulfillment_rate(self):
        total_pos = self.purchase_orders.count()
        if total_pos == 0:
            return 0
        fulfilled_pos = PurchaseOrder.objects.filter(
            status="completed", issues__isnull=True
        ).count()
        return (fulfilled_pos / total_pos) * 100
