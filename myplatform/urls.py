"""
URL configuration for myplatform project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from fibonacci_app.views import (
    calculate_fibonacci,
    calculate_fibonacci_by_int_path,
    calculate_fibonacci_by_query,
    list_all_fibonacci_data,
    calculate_fibonacci_by_rest_api,
)
from fibonacci_app.urls import fibonacci_router

# superuser admin
# user: gorka
# password: fast

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(fibonacci_router.urls)),
    path("fibonacci/", calculate_fibonacci, name="calculate_fibonacci"),
    path("fibonacci_int/<int:number>", calculate_fibonacci_by_int_path, name="fibonacci_int_path"),
    path("fibonacci_query/", calculate_fibonacci_by_query, name="fibonacci_query"),
    path("fibonacci_list/", list_all_fibonacci_data, name="fibonacci_data_list"),
    path(
        "fibonacci_rest_api/",
        calculate_fibonacci_by_rest_api,
        name="rest_api_calculate_fibonacci",
    ),
]
