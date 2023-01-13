from random import choice

class Factory():
    def __init__(self, runs=100, workers=1):
        self.conveyor = [choice(["A", "B", ""]) for x in range(0, runs)]
        self.workers = [Worker() for x in range(workers)]

        print(f'''
    Total Runs: {len(self.conveyor)}
    Total A: {self.conveyor.count('A')}
    Total B: {self.conveyor.count('B')}
    Empty spaces: {self.conveyor.count('')}
        ''')

    def run(self):
        for i,x in enumerate(self.conveyor):
            for worker in self.workers:
                if x == "" and "P" in worker.inventory and i >= worker.mem:
                    worker.inventory.remove("P")
                    worker.complete.append("P")
                    self.conveyor.pop(i)
                    self.conveyor.insert(i, "P")
                    break

                elif len(worker.inventory) < worker.max_items:
                    if x not in worker.inventory and x != "":
                        worker.inventory.append(x)
                        self.conveyor.pop(i)
                        self.conveyor.insert(i, "")
                        if all(value in worker.inventory for value in ["A", "B"]):
                            worker.inventory.remove("A")
                            worker.inventory.remove("B")
                            worker.inventory.append("P")
                            worker.mem = i+4
                        break

class Worker():
    def __init__(self):
        self.inventory = []
        self.max_items = 2
        self.complete = []
        self.mem = 0


def launch(runs, workers):
        app = Factory(runs, workers)
        app.run()
        for i,x in enumerate(app.workers):
            print(f"Worker {i+1} completed {len(x.complete)} products - Inventory: {x.inventory}")
        print(f'''
    Total Products: {sum([len(x.complete) for x in app.workers]) + sum([x.inventory.count("P") for x in app.workers])}
    Unused A: {sum([x.inventory.count('A') for x in app.workers]) + app.conveyor.count("A")}
    Unused B: {sum([x.inventory.count('B') for x in app.workers]) + app.conveyor.count("B")}    
        ''')    

if __name__ == '__main__':
    launch(runs=100, workers=6)
