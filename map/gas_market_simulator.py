from components.global_clock import GlobalClock
from map.shortest_paths import get_shortest_paths
from components.car import Car
from components.competing_station import Competitor
from components.dqn_station import DQNStation
from components.intersection import Intersection
from components.roadway import Roadway
from map.wholesale_prices import get_wholesale_prices
import math
import random

class GasMarketSimulator:
    
    def __init__(self, layout_name):
        self.map_data = self.get_map(layout_name)
        self.shortest_paths = get_shortest_paths(self.map_data["roadways"], self.map_data["intersections"])
        self.wholesale_prices = get_wholesale_prices(start='2023-01-01', end='2023-12-31')
        self.clock = GlobalClock()
        self.default_speed_limit = 13.5 # (m/s)   ~30 miles per hour
        self.default_wait_time = 30 # (s)
        self.default_spawn_rate = 5 # (cars/s)
        self.intersections = {} # (x,y): reference to object,
        self.gas_stations = {} # (x,y): (reference to object, type)
        self.roadways = {} # (x,y): reference to object
        self.map = self.build_map()
        self.visualization_data = self.init_viz_data()
        self.relative_traffic_baseline = [0.11,0.13,0.15,0.19,0.2,0.3,0.5,0.83,0.81,0.72,0.66,0.63,0.63,0.64,0.72,0.87,0.95,1,0.82,0.65,0.49,0.398,0.26,0.2]
        self.today_hourly_traffic = self.init_traffic()
        self.car_count = 0
        self.cars = self.init_cars()

    def init_traffic(self):
        l = []
        max_t = self.map_data["max_traffic"]
        for i in range(len(self.relative_traffic_baseline)):
            noise = random.gauss(0, 0.025)
            hourly_cars = math.floor(max_t * (self.relative_traffic_baseline[i] + noise))
            l.append(hourly_cars)

        # print(l)
        return l

    def init_cars(self):
        """Initializes cars at time 0"""
        cars_to_spawn = self.today_hourly_traffic[0]
        car_list = []
        print(cars_to_spawn)
        for _ in range(0, cars_to_spawn):
            intersections = list(self.map_data["intersections"].keys())
            spawn = random.choice(intersections)
            dest = random.choice(intersections)
            while dest == spawn:
                dest = random.choice(intersections)
            route = self.shortest_paths[self.map_data["intersections"][spawn]][self.map_data["intersections"][dest]][1]
            new_car = Car(id=self.car_count, spawn_location=spawn, destination=dest, route=route, fuel_capacity=15, gas_stations=self.gas_stations, intersections=self.intersections)
            self.car_count += 1
            # print(new_car)
            car_list.append(new_car)
        
        return car_list


    def init_viz_data(self):
        visualization_data = {
            "static": self.map, # Things that stay the same: Map dimensions; the locations of gas stations, intersections, and roadways.
            "gas_station_order": self.map_data["gas_stations"],
            "dynamic": [], # Things that can change each second: time, locations of cars, posted gas prices, and other visible DQNStation state variables.
        }
        return visualization_data
    
    def add_viz_data(self, dqn_state_vars, car_locations):
        """
        Adds dqn_state_vars DICT and car_locations LIST to viz data
        Timestamp = index
        """
        self.visualization_data["dynamic"].append( (dqn_state_vars,car_locations) )

    def spawn_cars(self):
        """Calculates expected number of cars, spawns more if needed"""

    def get_gas_prices(self):
        """Returns a dictionary of:
          key=gas station coordinates
          value=gas station posted price
        """
        gas_prices = {}
        for coordinate, (gas_station, _) in self.gas_stations.items():
            gas_prices[coordinate] = gas_station.posted_gas_price

        return gas_prices

    def get_time(self):
        return self.clock.get_time()
    
    def get_hour_of_day(self):
        return math.floor(self.get_time() / 3600) % 24

    def get_map(self, name):
        if name == "College Station":
            College_Station = {
                "height": 6, # Grid map height (y)
                "width": 5, # Grid map width (x)
                "gas_stations": [((0,3), "dqn"), ((0,2), "match_nearest"), ((0,6), "match_nearest"), ((2,6), "match_nearest"), ((5,1), "fixed_markup")], # coordinate, pricing strategy pairs
                "roadways": [((0,6), (2,6)), ((2,6), (5,6)), ((0,6), (0,3)), ((2,6), (2,3)), ((5,6), (5,3)), ((0,3), (2,3)), ((2,3), (5,3)), ((0,3), (0,2)), ((0,2), (0,1)), ((0,1), (0,0)), ((5,3), (5,1)), ((5,1), (5,0)), ((0,0), (2,0)), ((2,0), (3,0)), ((3,0), (5,0))], # endpoint coordinate, endpoint coordinate pairs
                "intersections": {(0, 6): 0, (2, 6): 1, (5, 6): 2, (0, 3): 3, (2, 3): 4, (5, 3): 5, (0, 2): 6, (0, 1): 7, (5, 1): 8, (0, 0): 9, (2, 0): 10, (3, 0): 11, (5, 0): 12}, # dictionary of: key = coordinates, value = id
                "max_traffic": 500, # Absolute maximum number of cars on map
            }
            return College_Station
        else:
            return {"error": "Layout does not exist."}
        
    def build_map(self):
        """
        Returns a 2D array of dictionaries (each index representing a coordinate of a grid)
        This array can only have one of each at each index:
        -gas_station
        -intersection
        -roadway
        """
        height = self.map_data["height"]
        width = self.map_data["width"]

        # Initialize the 2D array of dictionaries
        smap = [[{} for _ in range(height + 1)] for _ in range(width + 1)]

        # Add gas stations to the map
        for gas_station in self.map_data["gas_stations"]:
            coordinates, type = gas_station
            x, y = coordinates
            if type == "dqn":
                new_station = DQNStation( (x,y), self.map_data["gas_stations"], self.shortest_paths, self.map_data["intersections"], self.wholesale_prices[0], None, None, None)
                smap[x][y]["gas_station"] = new_station
                smap[x][y]["dqn"] = True
                self.gas_stations[(x,y)] = (new_station, type)
            else:
                new_station = Competitor( (x,y), self.map_data["gas_stations"], self.shortest_paths, self.map_data["intersections"], self.wholesale_prices[0], type)
                smap[x][y]["gas_station"] = new_station
                self.gas_stations[(x,y)] = (new_station, type)

        # Add intersections to the map
        for intersection in self.map_data["intersections"]:
            x, y = intersection
            new_intxn = Intersection( (x,y), self.default_wait_time, self.default_spawn_rate)
            smap[x][y]["intersection"] = new_intxn
            self.intersections[(x,y)] = new_intxn

        # Add roadways to the map
        for roadway in self.map_data["roadways"]:
            start, end = roadway
            x1, y1 = start
            x2, y2 = end
            if x1 == x2: # Vertical road
                maxY = max(y1,y2)
                minY = min(y1,y2)
                while maxY >= minY:
                    new_rdwy = Roadway( ((x1),(maxY)), "horizontal", self.default_speed_limit)
                    smap[x1][maxY]["roadway"] = new_rdwy
                    self.roadways[(x1,maxY)] = new_rdwy
                    maxY -= 1
            if y1 == y2: # Horizontal road
                maxX = max(x1,x2)
                minX = min(x1,x2)
                while maxX >= minX:
                    new_rdwy = Roadway( ((maxX),(y1)), "vertical", self.default_speed_limit)
                    smap[maxX][y1]["roadway"] = new_rdwy
                    self.roadways[(maxX,y1)] = new_rdwy
                    maxX -= 1
        return smap
        
    def run_simulation(self, iterations):
        """
        Updates dynamic objects EVERY SECOND. Passes the necessary information required by the objects to update each cycle. 
        """
        print(f'Start: {len(self.cars)}')
        loops = 0
        while loops < iterations:
            time = self.clock.get_time()
            car_locations_display = []
            dqn_state_vars_display = {
                "p_w": None,
                "p_o": None,
                "p_c": {},
                "d": None,
                "i": None,
            }

            # Update wholesale price and set flag to update stations
            p_w = 0
            p_w_update = False
            if self.get_hour_of_day() == 0: # Start of new day
                if time in self.wholesale_prices:
                    p_w = self.wholesale_prices[time]
                    dqn_state_vars_display["p_w"] = p_w
                    p_w_update = True
                    
            # Spawn cars based on current time and predetermined relative traffic flow
            
            # Cars will proceed traversal or despawn, burn gas, and decide to buy gas
            updated_cars = []
            for car in self.cars:
                loc = car.update(time)
                if loc != -1:
                    updated_cars.append(car)
                    car_locations_display.append(loc)

            self.cars = updated_cars


            # Gas stations will update price based on the current state
            old_gas_prices = self.get_gas_prices()
            for coordinate, (gas_station, type) in self.gas_stations.items():  # Use .items() to get key-value pairs
                if type == "dqn":
                    dqn_state_vars_display["p_o"] = gas_station.update(old_gas_prices, p_w if p_w_update else None)
                    # Set the rest of dqn_state_vars_display
                    dqn_state_vars_display["d"] = gas_station.get_d()
                    dqn_state_vars_display["i"] = gas_station.get_i()
                else:
                    dqn_state_vars_display["p_c"][coordinate] = gas_station.update(old_gas_prices, p_w if p_w_update else None)

            ### Add a new entry into the visualization_data dictionary
            self.add_viz_data(dqn_state_vars_display, car_locations_display)

            ### Testing:

            loops += 1
            self.clock.tick()
        
        print(f'Viz data start: {self.visualization_data["dynamic"][0]}')
        print(f'Viz data final: {self.visualization_data["dynamic"][iterations-1]}')
        print(f'End: {len(self.cars)}')


