import requests
from typing import List

from models.order import OrderDto
from app.settings import ORDERS_URL

def fetch_orders(access_key : str) -> List[OrderDto]:
    """
    Retrieves orders from the remote service.

    This function makes an HTTP GET request to the orders endpoint using the provided access key.
    It builds the necessary headers for authorization and content type, then processes the response.
    If the response indicates a failure (status code other than 200), an exception is raised. Otherwise,
    the JSON response is parsed and used to create a list of OrderDto objects.

    Args:
        access_key (str): The bearer token used to authorize the request to the orders service.

    Returns:
        List[OrderDto]: A list of OrderDto objects representing the orders retrieved from the service.

    Raises:
        Exception: If the HTTP response status code is not 200, indicating a failure to fetch orders.
    """
    headers = {
        "Authorization" : f'Bearer {access_key}',
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
