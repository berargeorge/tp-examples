import pprint


class Order:
    CREATED = 1
    IN_PROGRESS = 2
    SENT = 3
    COMPLETED = 4

    status_options = (
        (CREATED, 'CREATED'),
        (IN_PROGRESS, 'IN_PROGRESS'),
        (COMPLETED, 'COMPLETED')
    )

    def __init__(self):
        self.status = Order.CREATED


class OPDept:
    ''' Order Processing Department - used here as a singleton '''
    warehouses = []
    orders = []

    @staticmethod
    def create_order(customer, product):
        for warehouse in OPDept.warehouses:
            product = warehouse.remove_product(product)
            if product:
                o = Order()
                o.customer = customer
                o.product = product
                OPDept.orders.append(o)
                return o

        return False

    @staticmethod
    def process_order(order):
        ''' pretend actual stuff happens '''
        order.status = Order.IN_PROGRESS

    @staticmethod
    def report():
        warehouse_report = {
            'zero_stock': 0,
            'total_products': 0,
        }

        for warehouse in OPDept.warehouses:
            warehouse_report['total_products'] += warehouse.number_products()
            if warehouse.under_stock():
                warehouse_report['zero_stock'] += 1

        order_report = {
            'number_created': 0,
            'number_in_progress': 0,
            'number_completed': 0
        }

        for order in OPDept.orders:
            if order.status == Order.CREATED:
                order_report['number_created'] += 1
            if order.status == Order.IN_PROGRESS:
                order_report['number_in_progress'] += 1
            if order.status == Order.COMPLETED:
                order_report['number_completed'] += 1

        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(warehouse_report)
        pp.pprint(order_report)


class Customer:
    total_number = 0

    def __init__(self, name, address):
        self.number = Customer.total_number = Customer.total_number + 1
        self.name = name
        self.address = address

    def place_order(self, product):
        return OPDept.create_order(self, product)

    def receive_order(self, order):
        order.status = Order.COMPLETED
        return order


class Product:
    total_number = 0
    name = ""
    price = 0

    def __init__(self):
        self.number = Product.total_number = Product.total_number + 1


class Warehouse:
    def __init__(self):
        self.products = {}
        OPDept.warehouses.append(self)

    def add_product(self, product):
        for pid, stock in self.products.items():
            if product.number == pid:
                self.products[pid] += 1
                return True

        self.products[product.number] = 1

    def remove_product(self, product):
        for pid, stock in self.products.items():
            if product.number == pid:
                self.products[pid] -= 1
                if self.products[pid] == 0:
                    del self.products[pid]
                return product

        return False

    def under_stock(self):
        return not self.products

    def number_products(self):
        return len(self.products)
