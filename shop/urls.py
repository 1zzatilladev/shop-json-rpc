from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .json_rpc import rpc_server

r = DefaultRouter()
r.register(r"categories", views.CategoryViewSet, basename="CategoryView")

urlpatterns = [
    path("", rpc_server.view, name="json_rpc"),
    path('products/', views.ProductApiView.as_view()),
    path('products/<int:pk>/', views.ProductApiView.as_view()),
    path('products/list/', views.ProductListCreateApiView.as_view()),
    path('categories/', include(r.urls)),
]
