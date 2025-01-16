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


def calculate_fibonacci_by_int_path(request, number):
    result = fibonacci_custom(number)
    print(result)
    if not FibonacciData.objects.filter(number=number).exists():
        FibonacciData.objects.create(number=number, result=result)
    return JsonResponse(
        {"result": result, "details": "La operacion ha sido exitosa"}, status=201
    )


def calculate_fibonacci_by_query(request):
    """
    Calcula el número de Fibonacci basado en un parámetro pasado por query string.
    Ejemplo de URL: /mi_vista?number=5
    """
    # Obtener el valor de la query string 'number'
    number = request.GET.get("number")

    if number is None:
        return JsonResponse(
            {"error": "El parámetro 'number' es requerido."}, status=400
        )

    try:
        number = int(number)  # Convertir a entero
    except ValueError:
        return JsonResponse(
            {"error": "El parámetro 'number' debe ser un entero válido."}, status=400
        )

    # Lógica del cálculo de Fibonacci
    result = fibonacci_custom(number)

    return JsonResponse({"number": number, "result": result}, status=200)


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
    number_data = int(request.data.get("number"))
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
