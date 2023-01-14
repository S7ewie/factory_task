import unittest
import main

class TestMain(unittest.TestCase):

    def test_conveyor_total(self):
        '''
        Test number of items in generated list match total number of runs.
        '''
        total = 100
        obj = main.Factory(runs=total)
        result = len(obj.conveyor)
        self.assertEqual(result, total)

    def test_conveyor_final(self):
        '''
        Test start and end conveyors differ but remain the same length.
        '''
        obj = main.Factory(runs=1000, workers=10)
        before_workday = [x for x in obj.conveyor]
        obj.begin_workday()
        after_workday = obj.conveyor
        self.assertEqual(len(before_workday), len(after_workday))
        self.assertTrue(before_workday != after_workday)
        
    def test_conveyor_contents(self):
        '''
        Test conveyor only contains valid items.
        '''
        obj = main.Factory()
        self.assertTrue(x in obj.conveyor for x in ["A", "B", ""])

    def test_worker_total(self):
        '''
        Test correct number of workers are created.
        '''
        total = 67
        obj = main.Factory(workers=total)
        result = len(obj.workers)
        self.assertEqual(result, total)

    def test_product_output(self):
        '''
        Test the total number of products produced, match the number of products on the conveyor
        (This doesn't include products still sitting in worker inventories.)
        '''
        obj = main.Factory(runs=1000, workers=10)
        obj.begin_workday()
        products_produced = sum([len(x.complete) for x in obj.workers])
        products_on_conveyor = obj.conveyor.count('P')
        self.assertEqual(products_produced, products_on_conveyor)

    def test_item_A_used(self):
        '''
        The the total number of item A on the conveyor at the start, matches the total remaining plus total used in products.
        '''
        obj = main.Factory(runs=1000, workers=10)
        total_start_A = obj.conveyor.count('A')
        obj.begin_workday()
        total_A_used = sum([len(x.complete) for x in obj.workers]) + sum([x.inventory.count('P') for x in obj.workers])
        remaining_A = obj.conveyor.count("A") + sum([x.inventory.count('A') for x in obj.workers])
        self.assertEqual(total_start_A, total_A_used + remaining_A)

    def test_item_B_used(self):
        '''
        The the total number of item B on the conveyor at the start, matches the total remaining plus total used in products.
        '''
        obj = main.Factory(runs=1000, workers=10)
        total_start_B = obj.conveyor.count('B')
        obj.begin_workday()
        total_B_used = sum([len(x.complete) for x in obj.workers]) + sum([x.inventory.count('P') for x in obj.workers])
        remaining_B = obj.conveyor.count("B") + sum([x.inventory.count('B') for x in obj.workers])
        self.assertEqual(total_start_B, total_B_used + remaining_B)


if __name__ == "__main__":
    unittest.main()
