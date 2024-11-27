from components.global_clock import GlobalClock
import random
import math
from globals import DEBUG_CAR
def debug(str):
    if DEBUG_CAR:
        print(str)

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
        self.tank_level = self.get_fuel_level()
        self.current_position = spawn_location
        self.gas_stations = gas_stations
        self.gas_station_keys = list(gas_stations.keys())
        self.gas_price_memory = -100 # an arbitrary, low value that will be set to a real value later
        self.loyalty = None
        self.dealbreaker_delta = 0.05
        self.top_speed = 13.5
        self.time_active = 0
        self.at_intersection = False
        self.time_at_intersection = 0
        self.fuel_burn_rate = 0.0009 # gallons/second, derived from 20mpg driving at 13.5 m/s
        self.traversal = self.calculate_location_timing()

    def __repr__(self):
        return f'Car #{self.id}: Currently at {self.current_position}, Going to {self.destination}, Fuel level: {self.current_fuel}/{self.fuel_capacity} ({self.get_fuel_percent()})'
    
    def get_fuel_percent(self):
        return f'{round((self.current_fuel * 100 / self.fuel_capacity), 2)}%'
    
    def get_fuel_level(self):
        return self.current_fuel/self.fuel_capacity
    
    def decide_to_buy(self, price):
        if self.get_fuel_level() < 0.1:
            debug(f'(car.py): Car {self.id} is buying gas (almost out)')
            # Needs gas no matter the price
            return True
        if self.get_fuel_level() < 0.6:
            debug(f'(car.py): Car {self.id} might buy some gas')
            ran = random.randint(1,10)
            # 20% chance of the car buying even though it doesn't really need it
            if ran <= 2:
                debug(f'(car.py): Car {self.id} is buying gas (20% chance)')
                return True
            # 80% chance of the car buying only if it identifies it as a good deal compared to the last visited station
            elif price <= self.gas_price_memory - self.dealbreaker_delta:
                debug(f'(car.py): Car {self.id} is buying gas (good deal)')
                return True
                    
        self.gas_price_memory = price
        return False

    def clear_gas_price_memory(self):
        self.gas_price_memory = -100

    def calculate_location_timing(self):
        """
        Returns a dictionary of timestamps identifying
        where the car will be at that timestamp
        """
        # debug(f'Route = {self.route}')
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

        d[time] = -1 # Despawn
        # debug(d)
        return d

    def buy_gas(self, gas_station):
        self.clear_gas_price_memory()
        gallons = self.fuel_capacity - self.current_fuel
        gas_station.sell_gas(volume=gallons, car_id=self.id)
        self.fuel

    def update(self, time):
        """
        Returns position of car
        Moves car, burning gas
        Car might also buy gas 
        """
        if time in self.traversal:
            coords = self.traversal[time]
            self.current_fuel -= self.fuel_burn_rate * (time - self.spawn_time) # Time elapsed since spawn
            if self.current_fuel <= 0:
                debug(f"(car.py): Car {self.id} ran out of fuel!")
                return -1 # Despawn FIXME: If it doesn't despawn, it will definitely buy gas at next station.
            self.current_position = coords
            if coords in self.gas_station_keys:
                gas_station = self.gas_stations[coords][0]
                gas_price = gas_station.posted_gas_price
                if self.decide_to_buy(gas_price):
                    gallons = self.fuel_capacity - self.current_fuel
                    if gas_station.sell_gas(volume=gallons, car_id=self.id):
                        self.clear_gas_price_memory()
                        self.current_fuel = self.fuel_capacity

        if self.current_position == -1:
            debug(f"(car.py): Car {self.id} has reached its destination and despawned (Time: {time})")
            return -1
        return self.current_position

    # Extra: Write a function that reroutes car if they don't have enough gas to get to destination