import unittest
import main

class TestMain(unittest.TestCase):

    def test_conveyor_total(self):
        total = 100
        obj = main.Factory(runs=total)
        result = len(obj.conveyor)
        self.assertEqual(result, total)

    def test_conveyor_contents(self):
        obj = main.Factory()
        self.assertTrue(x in obj.conveyor for x in ["A", "B", ""])

    def test_worker_total(self):
        total = 67
        obj = main.Factory(workers=total)
        result = len(obj.workers)
        self.assertEqual(result, total)

    def test_product_output(self):
        obj = main.Factory(runs=1000, workers=10)
        obj.run()
        products_produced = sum([len(x.complete) for x in obj.workers]) 
        products_on_conveyor = obj.conveyor.count('P')
        self.assertEqual(products_produced, products_on_conveyor)

    def test_item_A_used(self):
        obj = main.Factory(runs=1000, workers=10)
        total_start_A = obj.conveyor.count('A')
        obj.run()
        total_A_used = sum([len(x.complete) for x in obj.workers]) + sum([x.inventory.count('P') for x in obj.workers])
        remaining_A = obj.conveyor.count("A") + sum([x.inventory.count('A') for x in obj.workers])
        self.assertEqual(total_start_A, total_A_used + remaining_A)

    def test_item_B_used(self):
        obj = main.Factory(runs=1000, workers=10)
        total_start_B = obj.conveyor.count('B')
        obj.run()
        total_B_used = sum([len(x.complete) for x in obj.workers]) + sum([x.inventory.count('P') for x in obj.workers])
        remaining_B = obj.conveyor.count("B") + sum([x.inventory.count('B') for x in obj.workers])
        self.assertEqual(total_start_B, total_B_used + remaining_B)


if __name__ == "__main__":
    unittest.main()
