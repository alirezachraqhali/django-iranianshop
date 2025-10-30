from django.urls import path
from .views import ProductDetailView
urlpatterns = [
    path('detail/<pk>', ProductDetailView.as_view())
]