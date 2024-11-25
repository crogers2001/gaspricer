from components.global_clock import GlobalClock
import random
import math

class Car:
    
    def __init__(self, id, spawn_location, destination, route, fuel_capacity, gas_stations, intersections):
        self.id = id
        self.clock = GlobalClock()
        self.spawn_location = spawn_location
        self.spawn_time = self.clock.get_time()
        self.route = route
        self.destination = destination
        self.fuel_capacity = fuel_capacity
        self.current_fuel = random.randint(1,fuel_capacity)
        self.tank_level = self.current_fuel/self.fuel_capacity
        self.current_position = spawn_location
        self.gas_stations = gas_stations
        self.gas_station_keys = list(gas_stations.keys())
        self.gas_station_memory = {}
        self.top_speed = 13.5
        self.time_active = 0
        self.at_intersection = False
        self.time_at_intersection = 0
        self.fuel_burn_rate = 0.0009 # gallons/second, derived from 20mpg driving at 13.5 m/s
        self.traversal = self.calculate_location_timing()

    def __repr__(self):
        return f'Car #{self.id}: Currently at {self.current_position}, Going to {self.destination}, Fuel level: {self.current_fuel}/{self.fuel_capacity} ({round((self.current_fuel*100/self.fuel_capacity),2)}%)'
    
    def decide_to_buy(self, price):
        print(f'Car {self.id} is at a gas station')
        if self.tank_level < 0.1:
            print(f'Car {self.id} will definitely buy some gas')
            return True
        if self.tank_level < 0.5:
            print(f'Car {self.id} might buy some gas')
            return True
        return False

 
    def calculate_location_timing(self):
        """
        Returns a dictionary of timestamps identifying
        where the car will be at that timestamp
        """
        # print(f'Route = {self.route}')
        d = {}
        d[self.spawn_time] = self.spawn_location
        time = self.spawn_time + 30
        time_for_300m = math.ceil(300 / self.top_speed)
        
        for i, coordinate in enumerate(self.route[:-1]):  # Iterate until the second-to-last coordinate
            x, y = coordinate
            xp, yp = self.route[i + 1]
            
            if coordinate == self.destination:
                break
            
            if x == xp:  # Moving vertically
                step = 1 if yp > y else -1
                for j in range(y + step, yp + step, step):  # Include the endpoint `yp`
                    time += time_for_300m
                    d[time] = (x, j)
            elif y == yp:  # Moving horizontally
                step = 1 if xp > x else -1
                for j in range(x + step, xp + step, step):  # Include the endpoint `xp`
                    time += time_for_300m
                    d[time] = (j, y)
            
            # Add time for the intersection decision or delay
            time += 30

        d[time] = (-1,-1) # Despawn time
        # print(d)
        return d

    def update(self, time):
        """
        Returns position of car
        Car might also buy gas 
        """
        if time in self.traversal:
            coords = self.traversal[time]
            self.current_position = coords
            if coords in self.gas_station_keys:
                self.decide_to_buy(self.gas_stations[coords].posted_gas_price)

        return self.current_position

    # Write a function that reroutes car if they don't have enough gas to get to destination