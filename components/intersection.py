from components.car import Car

class Intersection:
    
    def __init__(self, coordinate, wait_time, spawn_rate):
        self.coordinate = coordinate # acts as ID 
        self.wait_time = wait_time
        self.spawn_rate = spawn_rate
