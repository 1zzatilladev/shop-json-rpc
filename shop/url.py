from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

r = DefaultRouter()

r.register(r"author", views.AuthorViewSet, basename="Authorview")



urlpatterns = [
    path('books/list/<int:pk>/', views.BookRetrieveUpdateDestroyAPIView.as_view()),
    path('books/list/', views.BookListCreateApiView.as_view()),
    path('author/', include(r.urls)),
]