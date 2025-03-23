from typing import List
from datetime import datetime
from pydantic import BaseModel
from models.order_product import OrderProduct
from models.customer import Customer

class Order(BaseModel):
    """
    Represents a complete order made by a customer.

    Attributes:
        id (int): Unique order identifier.
        customer(Customer): Customer that made the order.
        delivery_time (datetime): Scheduled delivery or pickup time.
        created (datetime): Timestamp when the order was created.
        order_products (List[OrderProduct]): List of ordered products with detailed information.
        total_price (float): Total cost of the order.
        printed (bool): Flag to indicate if the order has been printed.
    """
    id: int
    customer : Customer
    delivery_time: datetime
    created: datetime
    order_products: List[OrderProduct]
    total_price: float
    printed: bool
                    
    def __str__(self):
        return f'Pedido n{self.id}, {self.order_products.__str__()}, {self.total_price}'
    
    def order_type(self) -> str:
        """
        Determines the type of order based on address information.
        If the full_address is not provided or is empty, it is considered a pickup.
        
        Returns:
            str: "Recolha no Restaurante" for pickup or "Entrega ao Domicilio" for delivery.
        """
        if not getattr(self, 'full_address', '').strip():
            return "Recolha no Restaurante"
        return "Entrega ao Domicilio"
