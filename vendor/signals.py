from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PurchaseOrder

@receiver(post_save, sender=PurchaseOrder)
def update_on_time_delivery_rate(sender, instance, created, **kwargs):
    if instance.status == 'completed':
        vendor = instance.vendor
        completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
        on_time_deliveries = completed_pos.filter(delivery_date__lte=instance.delivery_date).count()
        total_completed_pos = completed_pos.count()
        if total_completed_pos > 0:
            vendor.on_time_delivery_rate = (on_time_deliveries / total_completed_pos) * 100
            vendor.save()

@receiver(post_save, sender=PurchaseOrder)
def update_quality_rating_avg(sender, instance, created, **kwargs):
    if instance.status == 'completed' and instance.quality_rating is not None:
        vendor = instance.vendor
        completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed', quality_rating__isnull=False)
        total_completed_pos = completed_pos.count()
        if total_completed_pos > 0:
            quality_ratings = completed_pos.aggregate(avg_rating=models.Avg('quality_rating'))
            vendor.quality_rating_avg = quality_ratings['avg_rating']
            vendor.save()


@receiver(post_save, sender=PurchaseOrder)
def update_average_response_time(sender, instance, created, **kwargs):
    if instance.acknowledgment_date:
        vendor = instance.vendor
        completed_pos = PurchaseOrder.objects.filter(vendor=vendor, acknowledgment_date__isnull=False)
        total_completed_pos = completed_pos.count()
        if total_completed_pos > 0:
            response_times = completed_pos.annotate(
                response_time=models.ExpressionWrapper(
                    models.F('acknowledgment_date') - models.F('issue_date'),
                    output_field=models.DurationField()
                )
            ).aggregate(avg_response_time=models.Avg('response_time'))
            vendor.average_response_time = response_times['avg_response_time'].total_seconds() / 3600  # Convert to hours
            vendor.save()

@receiver(post_save, sender=PurchaseOrder)
def update_fulfillment_rate(sender, instance, created, **kwargs):
    vendor = instance.vendor
    total_pos = PurchaseOrder.objects.filter(vendor=vendor).count()
    if total_pos > 0:
        successful_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
        successful_count = successful_pos.count()
        vendor.fulfillment_rate = (successful_count / total_pos) * 100
        vendor.save()

