from pydantic import BaseModel
from models.product import Product


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

    def __str__(self):
        return f'{self.product.product_name}, {self.product.product_accompaniment}, {self.points}, {self.price}'