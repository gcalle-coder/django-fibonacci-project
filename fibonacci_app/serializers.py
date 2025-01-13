from rest_framework import serializers
from .models import FibonacciData


class FibonacciDataSerialzer(serializers.ModelSerializer):
    class Meta:
        model = FibonacciData
        fields = ["number", "result", "time"]
