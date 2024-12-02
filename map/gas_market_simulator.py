from components.global_clock import GlobalClock
from map.shortest_paths import get_shortest_paths
from components.car import Car
from components.basic_station import BasicStation
from components.dqn_station import DQNStation
from components.intersection import Intersection
from components.roadway import Roadway
from map.wholesale_prices import get_wholesale_prices
import math
import random
from globals import DEBUG_GAS_MARKET_SIMULATOR
def debug(str):
    if DEBUG_GAS_MARKET_SIMULATOR:
        print(str)

class GasMarketSimulator:
    
    def __init__(self, layout_name, viz=True):
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
        self.today_hourly_traffic_cts = []
        self.today_hourly_traffic_slopes = []
        self.tomorrow_first_traffic_ct = 0
        self.update_today_hourly_traffic(noise_sd=0.025, init=True)
        self.car_count = 0
        self.cars = self.init_cars()
        self.viz = viz


    def update_today_hourly_traffic(self, noise_sd, init=False):
        """
        Updates:
            -self.today_hourly_traffic_cts :: expected # of cars on map at each hour of today
            -self.today_hourly_traffic_slopes :: difference in # of cars per second between expected # of cars on map at each hour of today
            -self.tomorrow_first_traffic_ct :: the expected # of cars on map at hour 0 of next day (needed for slopes)
        """
        relative_traffic_baseline = [0.11,0.13,0.15,0.19,0.2,0.3,0.5,0.83,0.81,0.72,0.66,0.63,0.63,0.64,0.72,0.87,0.95,1,0.82,0.65,0.49,0.398,0.26,0.2]
        time_intervals = len(relative_traffic_baseline)
        counts = []
        slopes = []
        max_t = self.map_data["max_traffic"]
        if init:
            tomorrow_ct = math.floor(max_t * (relative_traffic_baseline[0] + random.gauss(0, noise_sd)))
        else:
            tomorrow_ct = self.tomorrow_first_traffic_ct
        counts.append(tomorrow_ct)

        for i in range(1, time_intervals):
            noise = random.gauss(0, noise_sd)
            hourly_cars = math.floor(max_t * (relative_traffic_baseline[i] + noise))
            counts.append(hourly_cars)

        transition = time_intervals - 1
        for i in range(time_intervals):
            if i == transition:
                slope = round((tomorrow_ct - counts[i]) / 3600, 10)
            else:
                slope = round((counts[i+1] - counts[i]) / 3600, 10)
            slopes.append(slope)

        self.today_hourly_traffic_cts = counts
        self.today_hourly_traffic_slopes = slopes
        self.tomorrow_first_traffic_ct = tomorrow_ct
        # debug(f'(gms.py): Expected traffic SLOPES at hour interval: {slopes} (length: {len(slopes)})')
        # debug(f'(gms.py): Expected traffic at hour interval: {counts} (length: {len(counts)})')

    def init_cars(self):
        """Initializes cars at time 0"""
        #FIXME: Adjust starting car positions to not only be at intersections for time 0
        cars_to_spawn = self.today_hourly_traffic_cts[0]
        car_list = []
        debug(f'(gms.py): Initializing with {cars_to_spawn} cars.')
        for _ in range(0, cars_to_spawn):
            intersections = list(self.map_data["intersections"].keys())
            spawn = random.choice(intersections)
            dest = random.choice(intersections)
            while dest == spawn:
                dest = random.choice(intersections)
            route = self.shortest_paths[self.map_data["intersections"][spawn]][self.map_data["intersections"][dest]][1]
            new_car = Car(id=self.car_count, spawn_location=spawn, destination=dest, route=route, fuel_capacity=15, gas_stations=self.gas_stations, intersections=self.intersections)
            self.car_count += 1
            # debug(f'(gms.py): Added: {new_car}')
            car_list.append(new_car)
        
        return car_list

    def spawn_cars(self, count):
        """
        Updates self.cars by adding 'count' number of new cars
        """
        for _ in range(0, count):
            intersections = list(self.map_data["intersections"].keys())
            spawn = random.choice(intersections)
            dest = random.choice(intersections)
            while dest == spawn:
                dest = random.choice(intersections)
            route = self.shortest_paths[self.map_data["intersections"][spawn]][self.map_data["intersections"][dest]][1]
            new_car = Car(id=self.car_count, spawn_location=spawn, destination=dest, route=route, fuel_capacity=15, gas_stations=self.gas_stations, intersections=self.intersections)
            self.car_count += 1
            self.cars.append(new_car)

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
                "gas_stations": [((0,3), "dqn"), ((0,2), "fixed_markup"), ((0,6), "fixed_markup"), ((2,6), "match_nearest"), ((5,1), "fixed_markup")], # coordinate, pricing strategy pairs
                "roadways": [((0,6), (2,6)), ((2,6), (5,6)), ((0,6), (0,3)), ((2,6), (2,3)), ((5,6), (5,3)), ((0,3), (2,3)), ((2,3), (5,3)), ((0,3), (0,2)), ((0,2), (0,1)), ((0,1), (0,0)), ((5,3), (5,1)), ((5,1), (5,0)), ((0,0), (2,0)), ((2,0), (3,0)), ((3,0), (5,0))], # endpoint coordinate, endpoint coordinate pairs
                "intersections": {(0, 6): 0, (2, 6): 1, (5, 6): 2, (0, 3): 3, (2, 3): 4, (5, 3): 5, (0, 2): 6, (0, 1): 7, (5, 1): 8, (0, 0): 9, (2, 0): 10, (3, 0): 11, (5, 0): 12}, # dictionary of: key = coordinates, value = id
                "max_traffic": 500, # Absolute maximum number of cars on map
            }
            return College_Station
        elif name == "College Station Baseline":
            baseline = {
                "height": 6, # Grid map height (y)
                "width": 5, # Grid map width (x)
                "gas_stations": [((0,3), "match_nearest"), ((0,2), "fixed_markup"), ((0,6), "fixed_markup"), ((2,6), "match_nearest"), ((5,1), "fixed_markup")], # coordinate, pricing strategy pairs
                "roadways": [((0,6), (2,6)), ((2,6), (5,6)), ((0,6), (0,3)), ((2,6), (2,3)), ((5,6), (5,3)), ((0,3), (2,3)), ((2,3), (5,3)), ((0,3), (0,2)), ((0,2), (0,1)), ((0,1), (0,0)), ((5,3), (5,1)), ((5,1), (5,0)), ((0,0), (2,0)), ((2,0), (3,0)), ((3,0), (5,0))], # endpoint coordinate, endpoint coordinate pairs
                "intersections": {(0, 6): 0, (2, 6): 1, (5, 6): 2, (0, 3): 3, (2, 3): 4, (5, 3): 5, (0, 2): 6, (0, 1): 7, (5, 1): 8, (0, 0): 9, (2, 0): 10, (3, 0): 11, (5, 0): 12}, # dictionary of: key = coordinates, value = id
                "max_traffic": 500, # Absolute maximum number of cars on map
            }
            return baseline
        else:
            raise ValueError("Map doesn't exist.")
        
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
                new_station = DQNStation( (x,y), self.map_data["gas_stations"], self.shortest_paths, self.map_data["intersections"], self.wholesale_prices[0])
                smap[x][y]["gas_station"] = new_station
                smap[x][y]["dqn"] = True
                self.gas_stations[(x,y)] = (new_station, type)
            else:
                new_station = BasicStation( (x,y), self.map_data["gas_stations"], self.shortest_paths, self.map_data["intersections"], self.wholesale_prices[0], type)
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
        EVERY SECOND:
            -Updates dynamic objects (gas stations and cars) by passing them necessary dynamic data.
            -Maintains expected quantity of active cars on map
            -Adds new entry into self.visualization_data["dynamic"] containing data that may change each second.
        """
        day_ct = 1
        loops = 0
        p_w = 0
        while loops < iterations:
            time = self.clock.get_time()
            current_hour = self.get_hour_of_day()
            seconds_in_current_hour = time % 3600
            current_car_ct = len(self.cars)
            #FIXME: If we can get traffic data specific to days of the week, holiday season, etc-- add more trackers to affect current traffic level

            car_locations_display = {} # Change to list if you want to render each individual car
            dqn_state_vars_display = {
                "p_w": None,
                "p_o": None,
                "p_c": {},
                "t": None,
                "d": None,
                "i": None,
            }


            ### Things that only change at the start of a new day
            p_w_update = False
            if current_hour == 0:
                if time in self.wholesale_prices:
                    p_w = self.wholesale_prices[time]
                    p_w_update = True
                if time >= 3600 and seconds_in_current_hour == 0: 
                    day_ct += 1
                    debug(f'Day {day_ct}-- Recalculating hourly traffic.')
                    self.update_today_hourly_traffic(noise_sd=0.025)
            dqn_state_vars_display["p_w"] = p_w

            ### Cars will proceed traversal or despawn, burn gas, and decide to buy gas
            updated_cars = []
            for car in self.cars:
                loc = car.update(time)
                if loc != -1:
                    updated_cars.append(car)
                    if loc in car_locations_display:
                        car_locations_display[loc] += 1
                    else:
                        car_locations_display[loc] = 1

            self.cars = updated_cars

            ### Gas stations will update price based on the current state
            old_gas_prices = self.get_gas_prices()
            for coordinate, (gas_station, type) in self.gas_stations.items():  # Use .items() to get key-value pairs
                traffic = car_locations_display.get(coordinate, 0)
                if type == "dqn":
                    dqn_state_vars_display["p_o"] = gas_station.update(old_gas_prices, traffic, current_hour, p_w if p_w_update else None)
                    # Set the rest of dqn_state_vars_display
                    dqn_state_vars_display["t"] = gas_station.get_t()
                    dqn_state_vars_display["d"] = gas_station.get_d()
                    dqn_state_vars_display["i"] = gas_station.get_i()
                else:
                    dqn_state_vars_display["p_c"][coordinate] = gas_station.update(old_gas_prices, current_hour, p_w if p_w_update else None)


            ### Spawning Cars to maintain expected traffic volume to compensate for despawning Cars:
            expected_car_ct = math.floor(self.today_hourly_traffic_cts[current_hour] + (self.today_hourly_traffic_slopes[current_hour] * (seconds_in_current_hour)))
            cars_to_spawn = expected_car_ct - current_car_ct
            if cars_to_spawn > 0:
                # debug(f'(gms.py): Seconds: {time}, Hour: {current_hour}, SiCH: {seconds_in_current_hour}, RCount: {current_car_ct}, ECount: {expected_car_ct}, HTC: {self.today_hourly_traffic_cts[current_hour]}, Slope: {self.today_hourly_traffic_slopes[current_hour]}')
                self.spawn_cars(cars_to_spawn)


            ### Add a new entry into the visualization_data dictionary
            if self.viz == True:
                self.add_viz_data(dqn_state_vars_display, car_locations_display)

            loops += 1
            self.clock.tick()
        
        # debug(f'DQNStation state variables at end:')
        # dqn, _ = self.gas_stations[(0,3)]
        # debug(f'p_w = {dqn.get_p_w()}')
        # debug(f'p_o = {dqn.get_p_o()}')
        # debug(f'p_c = {dqn.get_p_c()}')
        # debug(f't = {dqn.get_t()}')
        # debug(f'd = {dqn.get_d()}')
        # debug(f'i = {dqn.get_i()}')


