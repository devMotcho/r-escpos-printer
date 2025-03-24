import requests
from typing import List
from datetime import datetime

from models.order import OrderDto, Order
from models.product import Product
from models.order_product import OrderProduct
from app.settings import ORDERS_URL, UPDATE_ORDER_URL

def fetch_orders(access_token : str) -> List[OrderDto]:
    """
    Retrieves orders from the remote service.

    This function makes an HTTP GET request to the orders endpoint using the provided access key.
    It builds the necessary headers for authorization and content type, then processes the response.
    If the response indicates a failure (status code other than 200), an exception is raised. Otherwise,
    the JSON response is parsed and used to create a list of OrderDto objects.

    Args:
        access_token (str): The bearer token used to authorize the request to the orders service.

    Returns:
        List[OrderDto]: A list of OrderDto objects representing the orders retrieved from the service.

    Raises:
        Exception: If the HTTP response status code is not 200, indicating a failure to fetch orders.
    """
    headers = {
        "Authorization" : f'Bearer {access_token}',
        "Content-Type" : "application/json"
    }

    response = requests.get(ORDERS_URL, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Falha ou reunir pedidos : {response.status_code} - {response.text}")
    
    data = response.json()
    orders = [OrderDto(**order_data) for order_data in data]

    for order in orders:
        print(order)

    return orders


def update_order_status(order : Order, access_token : str) -> bool:
    """
    Updates the status of an order to 'printed'.

    This function sends an HTTP PUT request to update the status of a specific order,
    marking it as printed in the system. The URL is constructed by appending the order's ID
    to the base update URL. The request headers include the access token for authorization
    and specify the content type as JSON. If the response status code is not 200, an exception
    is raised. Otherwise, it returns True, indicating that the update was successful.

    Args:
        order (Order): The Order object whose status is to be updated.
        access_token (str): The access token used for authorization.

    Returns:
        bool: True if the order status is updated successfully.

    Raises:
        Exception: If the HTTP response status code is not 200, indicating a failure to update.
    """
    url = UPDATE_ORDER_URL + f'{order.id}/'

    headers = {
        "Authorization" : f"Bearer {access_token}",
        "Content-Type" : "application/json"
    }

    response = requests.put(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f'Falha ao marcar pedido n {order.id} como imprimido : {response.status_code} - {response.text}')
    
    return True


def dummy_fetch_orders() -> List[OrderDto]:
    orders = []

    dummy_order_product = OrderProduct(
        product=Product(category="Testing", product_name="Test Product", product_accompaniment=""),
        purchased_with_points=False,
        quantity=1,
        points=0,
        price=10.0,
        note="Sample note"
    )

    dummy_order_dto = OrderDto(
        id=101,
        customer_name="Alice Smith",
        email="alice.smith@example.com",
        nif=987654321,
        full_address="123 Example St, Test City",
        phone_number="555-1234",
        delivery_time=datetime.now(),
        created=datetime.now(),
        order_products=[dummy_order_product],
        total_price=10.0,
        printed=False
    )

    orders.append(dummy_order_dto)

    return orders