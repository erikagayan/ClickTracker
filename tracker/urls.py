from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClickViewSet

router = DefaultRouter()
router.register(r"clicks", ClickViewSet, basename="click")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "track/<int:pk>/",
        ClickViewSet.as_view({"get": "redirect"}),
        name="click_redirect",
    ),
]
