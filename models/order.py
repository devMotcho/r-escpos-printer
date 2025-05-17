from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from models.order_product import OrderProduct, OrderProductDto
from models.customer import Customer

class Order(BaseModel):
    """
    Represents a complete order made by a customer.

    Attributes:
        id (int): Unique order identifier.
        customer(Customer): Customer that made the order.
        delivery_time (datetime): Scheduled delivery or pickup time.
        created (datetime): Timestamp when the order was created.
        order_products (list[OrderProduct]): list of ordered products with detailed information.
        total_price (float): Total cost of the order.
        printed (bool): Flag to indicate if the order has been printed.
    """
    id: int
    customer : Customer
    delivery_time: datetime
    created: datetime
    order_products: list[OrderProduct]
    total_price: float
    printed: bool
                    
    def __str__(self):
        return f'Pedido n{self.id}, {self.order_products.__str__()}, {self.total_price}'
    
    def order_type(self) -> str:
        if self.customer.full_address.strip() == "":
            return "Recolha no Restaurante"
        return "Entrega ao Domicilio"
    
    def order_fast_info(self) -> str:
        if self.customer.full_address.strip() == "":
            return "VB - " + self.formated_time()
        return "ED - "+ self.formated_time()
    
    def formated_date(self) -> str:
        return f"{self.delivery_time.strftime('%d-%m-%Y')}"
    
    def formated_time(self) -> str:
        return f"{self.delivery_time.strftime('%H:%M:%S')}"


class OrderDto(BaseModel):
    """
    Data Transfer Object (DTO) for Order.

    This class serves as an intermediary representation of an order, containing both order details and
    customer information. It is designed to facilitate the transfer of data between different layers of an
    application (e.g., from a presentation layer to a business logic layer) without exposing the full internal
    structure of the domain models.
    """
    id: int
    customer : str
    email: str
    nif: int
    full_address: str
    locality_name : Optional[str] = None
    indication : Optional[str] = None
    phone_number: str
    delivery_time: datetime
    created: datetime
    order_products: list[OrderProductDto]
    total_price: float
    printed: bool

    def manipulate_orderDto(self) -> tuple:
        """
        Converts the OrderDto instance into corresponding Customer and Order objects.

        This method extracts the customer-related information to instantiate a Customer object and uses
        the order-related fields to instantiate an Order object. It then assigns the Customer object to the
        Order's customer attribute. The resulting tuple (customer, order) is returned for further processing
        in the application.

        Returns:
            tuple: A tuple containing:
                - Customer: The instantiated Customer object with populated attributes.
                - Order: The instantiated Order object with the associated Customer and populated attributes.
        """
        customer = Customer(
            name=self.customer,
            email=self.email,
            nif=self.nif,
            full_address=self.full_address,
            phone_number=self.phone_number,
            locality_name=self.locality_name
        )
        order_products = []
        for op in self.order_products:
            order_products.append(op.manipulate_order_product_dto())

        order = Order(
            id=self.id,
            customer=customer,
            created=self.created,
            order_products=order_products,
            total_price=self.total_price,
            printed=self.printed,
            delivery_time=self.delivery_time
        )

        return (customer, order)