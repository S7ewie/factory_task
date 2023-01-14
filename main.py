from random import choice

class Factory():
    '''
    Generates a ransomised conveyor list up to the number of runs specified.
    Instanciates a number of Worker objects based on the number of workers specified.
    '''
    def __init__(self, runs=100, workers=1):
        self.conveyor = [choice(["A", "B", ""]) for x in range(0, runs)]
        self.workers = [Worker() for x in range(workers)]

    def begin_workday(self):
        for i,x in enumerate(self.conveyor):
            for worker in self.workers:
                # Workers will be looped through in sequential order (position 1 Top > position 1 Bottom > position 2 Top, position 2 Bottom etc.)
                # Consider having a worker attribute for conveyor position x and y.
                # Instead of looping through workers in turn, could loop through x position in turn and assign priority at random to either position y.
                if x == "" and "P" in worker.inventory and i >= worker.mem:
                    # Priority will be given to placing down a completed product but only if the current conveyor slot is empty and only if the worker has held onto it for at least 4 turns
                    worker.inventory.remove("P")
                    worker.complete.append("P")
                    self.conveyor.pop(i)
                    self.conveyor.insert(i, "P")
                    break

                elif len(worker.inventory) < worker.max_items:
                    # This will execute if the above doesn't satisfy and the worker doesn't have a full inventory.
                    if x not in worker.inventory and x != "":
                        # Worker will only pick up an item he doesn't already have.
                        worker.inventory.append(x)
                        self.conveyor.pop(i)
                        self.conveyor.insert(i, "")
                        if all(value in worker.inventory for value in ["A", "B"]):
                            # If a worker holds both items, he will proceed to build a product.
                            worker.build_item(i)
                        break

class Worker():
    '''
    Generate worker object for factory.
    '''
    def __init__(self):
        self.inventory = []
        self.max_items = 2 # Change to adjust the maximum number of items a worker can hold in their inventory. WARNING: Raising this may break self.mem
        self.complete = []
        self.mem = 0 # Used to mark the earlier index at which a worker can place down a product depending on there being an empty space.

    def build_item(self, i):
        self.inventory.remove("A")
        self.inventory.remove("B")
        self.inventory.append("P")
        self.mem = i+4 # Worker will hold onto the product for at least 4 turns.


def launch(runs, workers):
        app = Factory(runs, workers)

        print(f'''
    Total Runs: {len(app.conveyor)}
    Total A: {app.conveyor.count('A')}
    Total B: {app.conveyor.count('B')}
    Empty spaces: {app.conveyor.count('')}
        ''')

        app.begin_workday()

        for i,x in enumerate(app.workers):
            print(f"Worker {i+1} completed {len(x.complete)} products - Inventory: {x.inventory}")
        print(f'''
    Total Products: {sum([len(x.complete) for x in app.workers]) + sum([x.inventory.count("P") for x in app.workers])}
    Unused A: {sum([x.inventory.count('A') for x in app.workers]) + app.conveyor.count("A")}
    Unused B: {sum([x.inventory.count('B') for x in app.workers]) + app.conveyor.count("B")}    
        ''')    

if __name__ == '__main__':
    launch(runs=100, workers=6) # Change number of runs or workers here.
