# REscposPrinter
This repo is a Python project that leverages the python-escpos library to print orders on an 80mm thermal printer connected to a network.

## Functionality
- **Error Logging:** Logs different types of errors (ERROR, WARNING, INFO) to a file to help debug and resolve issues.
- **Printer Service:** Connects to your printer via network and verifies its connection status using the python-escpos library.
- **Document Formatting:** Formats ESC/POS documents based on clearly defined models.
- **API Authentication:** Authenticates with a provided API to obtain necessary tokens.


## Dependencies
- python (or python3)
- [dotenv](https://pypi.org/project/python-dotenv/)
- [pydantic](https://docs.pydantic.dev/latest/)
- [python-escpos](https://python-escpos.readthedocs.io/en/latest/user/installation.html)
- [requests](https://pypi.org/project/requests/)



## Models
The order printed by this project is composed of four main models, each promoting a clear separation of concerns:

- `Product`: Contains details about a product.
- `Customer`: Holds customer information for the order.
- `OrderProduct`: Acts as an intermediate model linking Orders and Products in a many-to-many relationship. It captures details specific to each product order (e.g., quantity, price, notes).
- `Order`: Represents an entire order, containing one or more OrderProduct instances along with order-specific attributes (such as order ID, delivery details, total price, etc.).

*Note: You should adapt these models to suit your own API data and specific requirements.*

## Printer Service
This project uses the python-escpos library to simplify printing operations. It supports various types of printer connections, including USB and Network. This code sample specifically uses the Network connection option.

For details on connecting via other methods, please refer to the [python-escpos documentation](https://python-escpos.readthedocs.io/en/latest/).

## Auth Service
The function `get_auth_tokens` demonstrates how the project handles API authentication, including error handling, retries, and token extraction.

*Note: In the future I pretend to add more Authentication functionality, but for now is all that the project needs.*