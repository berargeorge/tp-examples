import unittest
from warehouse import Order, OPDept, Customer, InconsistentOrderException, \
    Product, Warehouse


class TestOrder(unittest.TestCase):
    def test_created_with_created_status(self):
        o = Order()
        self.assertEqual(o.status, Order.CREATED)

    def test_processing_sets_status_to_in_progress(self):
        o = Order()
        OPDept.process_order(o)
        self.assertEqual(o.status, Order.IN_PROGRESS)

    def test_client_receive_order_not_yet_sent_throws_error(self):
        o = Order()
        c = Customer('test name', 'test address')
        with self.assertRaises(InconsistentOrderException):
            c.receive_order(o)

    def test_client_receive_order_sent_sets_status_to_completed(self):
        o = Order()
        o.status = Order.IN_PROGRESS
        c = Customer('test name', 'test address')
        c.receive_order(o)
        self.assertEqual(o.status, Order.COMPLETED)


class TestCustomer(unittest.TestCase):
    def test_creation_sets_name_and_address(self):
        c = Customer('test name', 'test address')
        self.assertEqual(c.name, 'test name')
        self.assertEqual(c.address, 'test address')


class TestOrders(unittest.TestCase):
    def test_customer_placing_correct_order_creates_order(self):
        p = Product()
        w = Warehouse()
        w.add_product(p)
        c = Customer('test name', 'test address')
        initial_length = len(OPDept.orders)

        self.assertIsInstance(OPDept.create_order(c, p), Order)
        self.assertEqual(initial_length + 1, len(OPDept.orders))

    def test_customer_placing_order_inexistent_product_unsuccessful(self):
        p = Product()
        c = Customer('test name', 'test address')
        initial_length = len(OPDept.orders)

        self.assertFalse(OPDept.create_order(c, p))
        self.assertEqual(initial_length, len(OPDept.orders))

    def test_warehouse_report(self):
        OPDept.warehouses = []
        Warehouse()
        w2 = Warehouse()
        p = Product()
        p2 = Product()
        p3 = Product()
        w2.products = {
            p.number: '3',
            p2.number: '1',
            p3.number: '5'
        }

        expected_warehouse_report = {
            'zero_stock': 1,
            'total_products': 9
        }

        report = OPDept.report()
        self.assertEqual(
            report['warehouse_report'],
            expected_warehouse_report
        )

    def test_order_report(self):
        pass


class TestProduct(unittest.TestCase):
    pass


class TestWarehouse(unittest.TestCase):
    pass


def main():
    unittest.main()

if __name__ == '__main__':
    unittest.main()
