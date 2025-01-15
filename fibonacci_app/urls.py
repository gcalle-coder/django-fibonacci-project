from rest_framework import routers
from fibonacci_app.views import (
    SerializerFibonacciCreateViews,
    calculate_fibonacci,
    list_all_fibonacci_data,
)
from django.urls import path

# Los routers se encargan de generar automáticamente las rutas necesarias para
# las operaciones CRUD (Create, Read, Update, Delete) basadas en las vistas (ViewSet)
fibonacci_router = routers.DefaultRouter()
fibonacci_router.register(
    "fibonacciSerializerConsult",
    viewset=SerializerFibonacciCreateViews,
    basename="fibonacciSerializerConsult",
)
