from components.global_clock import GlobalClock
from shortest_paths import get_shortest_paths
from components.car import Car
from components.competing_station import Competitor
from components.dqn_station import DQNStation
from components.intersection import Intersection
from components.roadway import Roadway


class GasMarketSimulator: # Need to make functions to output stuff for visualization.py to display
    
    def __init__(self, layout_name):
        self.map_data = self.get_map(layout_name)
        self.map = self.build_map()
        self.clock = GlobalClock()
        self.shortest_paths = get_shortest_paths(self.map_data["roadways"], self.map_data["intersections"])
        self.default_speed_limit = 0.45 # (m/s)   ~30 miles per hour
        self.default_wait_time = 60 # (s)
        self.default_spawn_rate = 5 # (cars/s)

    def get_time(self):
        return self.clock.get_time()
    
    def get_map(self, name):
        if name == "College Station":
            College_Station = {
                "height": 6, # Grid map height (y)
                "width": 5, # Grid map width (x)
                "gas_stations": [((0,3), "dqn"), ((0,2), "match_nearest"), ((0,6), "match_nearest"), ((2,6), "match_nearest"), ((5,1), "fixed_markup")], # coordinate, pricing strategy pairs
                "roadways": [((0,6), (2,6)), ((2,6), (5,6)), ((0,6), (0,3)), ((2,6), (2,3)), ((5,6), (5,3)), ((0,3), (2,3)), ((2,3), (5,3)), ((0,3), (0,2)), ((0,2), (0,1)), ((0,1), (0,0)), ((5,3), (5,1)), ((5,1), (5,0)), ((0,0), (2,0)), ((2,0), (3,0)), ((3,0), (5,0))], # endpoint coordinate, endpoint coordinate pairs
                "intersections": {(0, 6): 0, (2, 6): 1, (5, 6): 2, (0, 3): 3, (2, 3): 4, (5, 3): 5, (0, 2): 6, (0, 1): 7, (5, 1): 8, (0, 0): 9, (2, 0): 10, (3, 0): 11, (5, 0): 12}, # dictionary of: key = coordinates, value = id
                "max_traffic": 250, # Absolute maximum number of cars on map
            }
            return College_Station
        else:
            return {"error": "Layout does not exist."}
        
    def build_map(self):
        """
        Returns a 2D array of dictionaries (each index representing a coordinate of a grid)
        """
        height = self.map_data["height"]
        width = self.map_data["width"]

        # Initialize the 2D array of dictionaries
        smap = [[{} for _ in range(width + 1)] for _ in range(height + 1)]

        # Add gas stations to the map
        for gas_station in self.map_data["gas_stations"]:
            coordinates, type = gas_station
            x, y = coordinates
            if type == "dqn":
                smap[x][y]["gas_station"] = DQNStation( (x,y), )
            else:
                smap[x][y]["gas_station"] = Competitor( (x,y), self.map_data["gas_stations"], self.shortest_paths, type)

        # Add DQN stations to the map
        for dqn_station in self.map_data["dqn_stations"]:
            x, y = dqn_station
            smap[x][y]["dqn_station"] = True

        # Add intersections to the map
        for intersection in self.map_data["intersections"]:
            x, y = intersection
            smap[x][y]["intersection"] = Intersection( (x,y), self.default_wait_time, self.default_spawn_rate)

        # Add roadways to the map
        for roadway in self.map_data["roadways"]:
            start, end = roadway
            x1, y1 = start
            x2, y2 = end
            if x1 == x2: # Vertical road
                maxY = max(y1,y2)
                minY = min(y1,y2)
                while maxY >= minY:
                    smap[x1][maxY]["roadway"] = Roadway( ((x1),(maxY)), self.default_speed_limit)
                    maxY -= 1
            if y1 == y2: # Horizontal road
                maxX = max(x1,x2)
                minX = min(x1,x2)
                while maxX >= minX:
                    smap[maxX][y1]["roadway"] = Roadway( ((maxX),(y1)), self.default_speed_limit)
                    maxX -= 1
        return smap
        


    
    def add_3_seconds(self): # testing
        self.time.tick()
        self.time.tick()
        self.time.tick()

