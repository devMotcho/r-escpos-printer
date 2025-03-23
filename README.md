# RPrinter
This project uses python escpos to print orders to a 80mm termal printer connected to the network.

## Functionality
- Logging to a file different types of errors (`ERROR`, `WARNING`, `INFO`)
- Printer service allows to connect to your printer via Network and checks the connection status.


## Dependencies
- python or python3
- [dotenv](https://pypi.org/project/python-dotenv/)
- [pydantic](https://docs.pydantic.dev/latest/)
- [python-escpos](https://python-escpos.readthedocs.io/en/latest/user/installation.html)
- [requests](https://pypi.org/project/requests/)



## Models
This example prints a order so there are 4 models that compose the order enabling clear separation of concerns.
- `Product`: Contains details about a product.
- `Customer`: Holds customer information who places an order.
- `OrderProduct`: Acts as the intermediate model linking Orders and Products in a many-to-many relationship, capturing details specific to each product order (such as quantity and price).
- `Order`: Represents an entire order, containing one or more OrderProduct instances along with order-specific attributes.

You should adapt the models to your own needs and API data.

## Printer Service
This project uses the python-escpos library to simplify the process of printing, there are multiple types of printer connections like `Usb`, `Network`, etc...
This code uses the `Network` option, please reference to [python-escpos](https://python-escpos.readthedocs.io/en/latest/) docs on how to connect via other types of connections.