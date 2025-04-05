from typing import Optional
from pydantic import BaseModel

class Customer(BaseModel):
    """
    Represents the customer placing an order.

    Attributes:
        name (str): The customer's name.
        email (str): The customer's email address.
        nif (int): The tax identification number (PT).
        full_address (str): The customer's address (if empty, implies pickup).
        phone_number (str): The customer's contact number.
    """
    name: str
    email: str
    nif: int
    full_address: str
    phone_number: str
    locality_name : Optional[str] = None
    indication : Optional[str] = None

    def __str__(self):
        return f"{self.name}, {self.email}"