from models.logger import Logger
from models.log_level import LogLevel
from services.order_services import dummy_fetch_orders

if __name__ == "__main__":
    
    orders_dto = dummy_fetch_orders()

    for dto in orders_dto:
        customer, order = dto.manipulate_orderDto()
        print(order.id, customer.name)