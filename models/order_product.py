from pydantic import BaseModel
from models.product import Product
from typing import List


class OrderProduct(BaseModel):
    """
    Represents the association between an Order and a Product, including order-specific details.

    Attributes:
        product (Product): The product being ordered.
        purchased_with_points (bool): Indicates if points were used for this purchase.
        quantity (int): Number of product units ordered.
        points (int): points consumed.
        price (float): Price for the specified quantity.
        note (str): Additional notes for the order (e.g., customization details).
    """
    product: Product
    purchased_with_points: bool
    quantity: int
    points: int
    price: float
    note: str

    def __str__(self) -> str:
        return f'{self.product.product_name}, {self.product.product_accompaniment}, {self.points}, {self.price}'
    
    def price_str(self) -> str:
        return f'{self.points} pontos' if self.purchased_with_points else f'{self.price} EUR'
    

class OrderProductDto(BaseModel):
    """
    Data Transfer Object (DTO) for OrderProduct.

    This class serves as an intermediary representation of the details required to create an OrderProduct.
    It combines both product-related information and order-specific details. The purpose is to facilitate
    the transfer of data between application layers (such as from a presentation layer to the business logic layer)
    without exposing the underlying domain model directly.
    """
    category : str
    product_name : str
    product_accompaniment : str
    purchased_with_points: bool
    quantity: int
    points: int
    price: float
    note: str

    def manipulate_order_product_dto(self) -> OrderProduct:
        """
        Converts the OrderProductDto instance into an OrderProduct domain model instance.

        This method performs the following steps:
            1. Creates a Product instance using the product-related attributes from the DTO.
            2. Constructs an OrderProduct instance, linking the created Product with the order-specific details
               such as quantity, price, points, and any additional notes.
            3. Returns the constructed OrderProduct instance for further processing in the application.

        Returns:
            OrderProduct: An instance of OrderProduct populated with the data from the DTO.
        """
        
        product = Product(
            category=self.category,
            product_name=self.product_name,
            product_accompaniment=self.product_accompaniment
        )

        order_product = OrderProduct(
            product=product,
            purchased_with_points=self.purchased_with_points,
            quantity=self.quantity,
            points=self.points,
            price=self.price,
            note=self.note
        )

        return order_product