import pytest
import json
from django.urls import reverse

# from ..models import FibonacciData
from fibonacci_app.models import FibonacciData

fibonacci_ser_url = reverse("fibonacciSerializerConsult-list")
pytestmark = pytest.mark.django_db


# ---------------- Test GET Companies ----------------
def test_zero_consults_should_return_empty_list(client) -> None:
    """reverse()
    es una función que se utiliza para generar URLs dinámicamente a
    partir de los nombres de las rutas definidas en tu aplicación.
    En lugar de codificar una URL directamente como "http://127.0.0.1:8000/companies/",
    puedes usar reverse para asegurarte de que las URLs sean consistentes y reflejen
    cualquier cambio que realices en las rutas.
    El primer argumento de reverse es el nombre de la ruta (definido en tus urls.py con el atributo name).
    """
    response = client.get(fibonacci_ser_url)
    assert response.status_code, 200
    assert json.loads(response.content) == []


def test_make_consult_and_check_result_is_stored(client):
    # Creamos previamente un dato en la base de datos (esto no es con POST)
    test_company = FibonacciData.objects.create(number=0, result=0)
    response = client.get(fibonacci_ser_url)
    assert response.status_code, 200
    content_data = response.data[0]
    assert content_data["number"] == 0
    assert content_data["result"] == 0
    test_company.delete()


# ---------------- Test POST Companies -----------------
def test_create_consult_with_no_arguments_should_fail(client) -> None:
    response = client.post(path=fibonacci_ser_url)
    assert response.status_code, 400
    response = client.get(fibonacci_ser_url)
    assert response.status_code, 200
    assert response.data == []


def test_create_consult_with_arguments_should_pass(client) -> None:
    data = {"number": 1, "result": 1}
    response = client.post(path=fibonacci_ser_url, data=data)
    assert response.status_code == 201
    assert response.data["number"] == data["number"]
    assert response.data["result"] == data["result"]


def test_consult_two_times_the_same_nuber_should_fail(client):
    data = {"number": 1, "result": 1}
    response = client.post(path=fibonacci_ser_url, data=data)
    assert response.status_code == 201
    response = client.post(path=fibonacci_ser_url, data=data)
    assert response.status_code == 400


def test_with_mock_assuring_logic_was_called(client) -> None:
    pass
