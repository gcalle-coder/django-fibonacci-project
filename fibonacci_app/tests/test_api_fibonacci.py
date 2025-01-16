import pytest
from unittest.mock import patch
import json
from django.urls import reverse
from fibonacci_app.models import FibonacciData

fibonacci_ser_url = reverse("fibonacciSerializerConsult-list")
pytestmark = pytest.mark.django_db
from fibonacci_app.fibonacci_logic.fibonacci_function import fibonacci_custom

# ---------------- Test GET Companies ----------------
def test_rest_api_zero_consults_should_return_empty_list(client) -> None:
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


def test_http_request(client) -> None:
    url = reverse("fibonacci_data_list")
    response = client.get(path=url)
    assert response.status_code, 200


def test_fibonacci_request_by_path_variable(client) -> None:
    response = client.get(path=f"/fibonacci_int/{2}")
    assert response.status_code == 201
    content_data = json.loads(response.content)
    assert content_data["result"] == 1


@pytest.mark.parametrize("number", [i for i in range(15)])
@pytest.mark.parametrize("execution_number", range(2))
def test_fibonacci_request_by_query_success(execution_number, number, client) -> None:
    query_data = {"number": number}
    response = client.get(path=f"/fibonacci_query/", data=query_data)
    assert response.status_code == 200
    content_data = json.loads(response.content)
    result = fibonacci_custom(query_data["number"])
    assert content_data["number"] == query_data["number"]
    assert content_data["result"] == result


def test_fibonacci_request_by_query_bad_keys_unsuccess(client) -> None:
    query_data = {"number": "t"}
    response = client.get(path=f"/fibonacci_query/", data=query_data)
    assert response.status_code == 400


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


def test_fibonacci_request_with_formulary(client) -> None:
    url = reverse("calculate_fibonacci")
    form = {"number": 1}
    response = client.post(path=url, data=form)
    # verificamos codigo de redireccion
    assert response.status_code == 302

    response = client.get(fibonacci_ser_url)
    assert response.status_code, 200
    content_data = response.data[0]
    assert content_data["number"] == 1
    assert content_data["result"] == 1


def test_with_mock_assuring_logic_was_called(client) -> None:
    """
    Mocking the 'fibonacci_custom' function with the patch decorator
    La funcion que se va a mockear es 'fibonacci_custom'
    y la finalidad de este test es validar nuestra funcion 'calculate_fibonacci_by_rest_api'
    Recordando que esta funcion es un endpoint de la API
    Y al ejercer un POST a este endpoint se llama a esta funcion.
    Damos por hecho que la
    """
    with patch("fibonacci_app.views.fibonacci_custom") as mocked_fibonacci_custom:

        # Valor que devolverá la funcion fibonacci_custom al ser llamada por la POST request a traves de
        # la ruta /fibonacci_rest_api y paráetros number = 1
        mocked_fibonacci_custom.return_value = 0
        response = client.post(path="/fibonacci_rest_api/", data={"number": 1})
        assert response.status_code == 201

        mocked_fibonacci_custom.assert_called_once_with(1)
