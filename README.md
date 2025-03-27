# REscposPrinter
This repo is a Python project that leverages the python-escpos library to print orders on an 80mm thermal printer connected to a network.

## Functionality
- **Error Logging:** Logs different types of errors (ERROR, WARNING, INFO) to a file to help debug and resolve issues.
- **Printer Service:** Connects to your printer via network and verifies its connection status using the python-escpos library.
- **Document Formatting:** Formats ESC/POS documents based on clearly defined models.
- **API Authentication:** Authenticates with a provided API to obtain necessary tokens.
- **Fetching & Updating Orders:** Get and update orders from the backend server.
- **A script Controller:** It coordinates printer operations, server communication, and order fulfillment with robust error handling and retry mechanisms.
- **Tray Icon Menu:** Allows users to controle the script in a simple way using the pystray library.



## Dependencies
- python (or python3)
- [dotenv](https://pypi.org/project/python-dotenv/)
- [pydantic](https://docs.pydantic.dev/latest/)
- [python-escpos](https://python-escpos.readthedocs.io/en/latest/user/installation.html)
- [requests](https://pypi.org/project/requests/)
- [pystray](https://pypi.org/project/pystray/)


## Models
The order printed by this project is composed of four main models, each promoting a clear separation of concerns:

- `Product`: Contains details about a product.
- `Customer`: Holds customer information for the order.
- `OrderProduct`: Acts as an intermediate model linking Orders and Products in a many-to-many relationship. It captures details specific to each product order (e.g., quantity, price, notes).
- `Order`: Represents an entire order, containing one or more OrderProduct instances along with order-specific attributes (such as order ID, delivery details, total price, etc.).

- `OrderDto` and `OrderProductDto` are the models that store the data from the response of the API, both have a method called `manipulate_<model_name>_dto` that provides a simple way to create the normal models that will be used.

*Note: You should adapt these models to suit your own API data and specific requirements.*

## Printer Service
This project uses the python-escpos library to simplify printing operations. It supports various types of printer connections, including USB and Network. This code sample specifically uses the Network connection option.

For details on connecting via other methods, please refer to the [python-escpos documentation](https://python-escpos.readthedocs.io/en/latest/).

## Auth Service
The function `get_auth_tokens` demonstrates how the project handles API authentication, including error handling, retries, and token extraction.

*Note: I pretend to add more Authentication functionality.*

## Order Service
The order service handles the API requests that need to be made to the server in order to:
- Get the orders weren't printed
- Update the status of a order to `printed`
- Dummy order, to test without making the orders fetch called `dummy_fetch_orders`

## Script Controller
`ScriptController` is the core class managing an automated order processing system. It coordinates printer operations, server communication, and order fulfillment with robust error handling and retry mechanisms.
- Start/stop control via `start_script()`/`stop_script()`
- Real-time status through status_message property
- Requires proper error handling in dependent services
- Thread-safe design using locks
- Resource cleanup on shutdown

## Tray Icon Menu
Is a system tray icon controller for print automation script present on the `main.py` file.
Provides visual status monitoring and basic controls through system tray interface.
