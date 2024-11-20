from components.global_clock import GlobalClock
import random

class Car:
    
    def __init__(self, fuel_capacity, gas_station_set, roadway_list, intersection_list, shortest_paths):
        self.time = GlobalClock()
        self.fuel_capacity = fuel_capacity
        self.current_fuel_level = fuel_capacity
        self.shortest_paths = shortest_paths
        self.spawn_location = self.generate_spawn(intersection_list)
        self.destination = self.generate_destination(intersection_list)
        self.route = self.choose_route(roadway_list)
        self.current_location = self.spawn_location

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
        path_cost = self.shortest_paths[spawn_idx][destination_idx]

    def decide_to_buy(self):
        if self.current_fuel_level < 0.1:
            return True
        # if price is lower than 

    def drive(self):
        self.time.tick()
        