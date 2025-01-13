from django.shortcuts import render, redirect
from rest_framework import generics
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


class SerializerFibonacciCreateViews(generics.ListCreateAPIView):
    queryset = FibonacciData.objects.all()
    serializer_class = FibonacciDataSerialzer
