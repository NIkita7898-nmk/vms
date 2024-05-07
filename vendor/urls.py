from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from vendor import views as view

urlpatterns = [
    path("create_user/", view.UserCreateAPIView.as_view(), name="create_user"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("vendors/", view.VendorViewSet.as_view(), name="vendor"),
    path(
        "vendors/<int:pk>/",
        view.VendorUpdateDeleteViewSet.as_view(),
        name="update-delete-vendor",
    ),
    path(
        "purchase_orders/",
        view.PurchaseOrderViewSet.as_view(),
        name="create-purchase-order",
    ),
    path(
        "purchase_orders/<int:pk>/",
        view.PurchaseOrderUpdateDeleteViewSet.as_view(),
        name="update-delete-purchase-order",
    ),
    path(
        "vendors/<int:pk>/performance/",
        view.VendorPerformanceAPIView.as_view(),
        name="vendor-performance",
    ),
    path(
        "purchase_orders/<int:pk>/acknowledge/",
        view.PurchaseOrderAcknowledgeView.as_view(),
        name="acknowledgement",
    ),
]
