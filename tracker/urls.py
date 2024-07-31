from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClickViewSet, ShortURLViewSet, redirect_to_original

router = DefaultRouter()
router.register(r'clicks', ClickViewSet, basename='click')
router.register(r'shorturls', ShortURLViewSet, basename='shorturl')

urlpatterns = [
    path('', include(router.urls)),
    path('track/<int:pk>/', ClickViewSet.as_view({'get': 'redirect'}), name='click_redirect'),
    path('<str:short_code>/', redirect_to_original, name='redirect_to_original'),
]
