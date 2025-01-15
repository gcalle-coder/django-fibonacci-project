from django.shortcuts import render, redirect
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from .serializers import FibonacciDataSerialzer
from .models import FibonacciData
from .fibonacci_logic.fibonacci_function import fibonacci_custom
from .forms import CreateNewCalculation
from django.http import JsonResponse


# Create your views here.
def list_all_fibonacci_data(request):
    fibonacci_data = FibonacciData.objects.all()
    return render(request, "consults_list.html", {"fibonacci_data": fibonacci_data})


def calculate_fibonacci_int(request, number):
    result = fibonacci_custom(number)
    print(result)
    if not FibonacciData.objects.filter(number=number).exists():
        FibonacciData.objects.create(number=number, result=result)

    return render(request, "fibonacci_result.html", {"result": result})


def calculate_fibonacci(request):
    if request.method == "POST":
        form = CreateNewCalculation(request.POST)
        if form.is_valid():
            number = form.cleaned_data["number"]
            result = fibonacci_custom(number)
            print(result)
            if FibonacciData.objects.filter(number=number).exists():
                return JsonResponse(
                    {"error": "Este número ya existe en la base de datos."}, status=400
                )
            else:
                FibonacciData.objects.create(number=number, result=result)

            return redirect("fibonacci_data_list")
    else:
        form = CreateNewCalculation()

    return render(request, "fibonacci_result.html", {"form": form})


# Este decorador trata esta funcion como un POST endpoint de la API
@api_view(http_method_names=["POST"])
def calculate_fibonacci_by_rest_api(request=Request) -> Response:
    """
    Calculate fibonacci number and save in database.

    Example of content of POST request set in POSTMAN:
    {
        "number": 5,
    }

    """
    number_data = request.data.get("number")
    result = fibonacci_custom(number_data)
    if FibonacciData.objects.filter(number=number_data).exists():
        return JsonResponse(
            {"error": "Este número ya existe en la base de datos."}, status=400
        )
    else:
        FibonacciData.objects.create(number=number_data, result=result)
        return JsonResponse(
            {"result": result, "details": "La operacion ha sido exitosa"}, status=201
        )


class SerializerFibonacciCreateViews(ModelViewSet):
    queryset = FibonacciData.objects.all()
    serializer_class = FibonacciDataSerialzer
