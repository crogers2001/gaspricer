from components.global_clock import GlobalClock
import random

class Car:
    
    def __init__(self, id, fuel_capacity, gas_station_set, roadway_list, intersection_list, shortest_paths):
        self.id = id
        self.time = GlobalClock()
        self.fuel_capacity = fuel_capacity
        self.current_fuel_level = fuel_capacity
        self.shortest_paths = shortest_paths
        self.spawn_location = self.generate_spawn(intersection_list)
        self.destination = self.generate_destination(intersection_list)
        self.route = self.choose_route(roadway_list)
        self.current_position = self.spawn_location
        self.gas_station_memory = {}
        self.speed = 0

    def __repr__(self):
        return f'Car #{self.id}: Currently at {self.current_position}, Fuel level: {self.current_fuel_level}/{self.fuel_capacity}'

    def generate_spawn(self, intersection_list):
        """Returns a random intersection"""
        return random.choice(intersection_list)
    
    def generate_destination(self, intersection_list):
        """Returns a random intersection that isn't the spawn"""
        possible_locations = [location for location in intersection_list if location != self.spawn_location]
        return random.choice(possible_locations)

    def choose_route(self, intersection_list):
        """Returns list of roadways and intersections it will pass through"""
        spawn_idx = intersection_list.index(self.spawn_location)
        destination_idx = intersection_list.index(self.destination)


    def decide_to_buy(self):
        if self.current_fuel_level < 0.1:
            return True
        if self.current_fuel_level < 0.5:
            return True
        return False
    
    def observe_speed_limit(self):
        """Updates current speed to the speed limit of the Roadway this Car is currently on"""
        pass

    def update(self):
        pass