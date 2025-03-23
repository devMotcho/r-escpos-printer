from pydantic import BaseModel

class Product(BaseModel):
    """
    Represents a product available in the restaurant or store.

    Attributes:
        category (str): The category of the product (e.g., Beverage, Main Course).
        product_name (str): The name of the product.
        product_accompaniment (str): Optional accompaniment details for the product.
    """
    category: str
    product_name: str
    product_accompaniment: str

    def __str__(self):
        return f"{self.category}, {self.product_name}, {self.product_accompaniment}"