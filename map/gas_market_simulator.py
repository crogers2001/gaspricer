from components.global_clock import GlobalClock
from shortest_paths import get_adjacency_matrix
from components.car import Car
from components.competing_station import Competitor
from components.dqn_station import DQNStation
from components.intersection import Intersection
from components.roadway import Roadway


class GasMarketSimulator: # Needs to output a big dataset for visualization.py to display
    
    def __init__(self, layout_name):
        self.map_data = self.get_map(layout_name)
        self.map = self.build_map()
        self.clock = GlobalClock()
        self.shortest_paths = get_adjacency_matrix(self.map.roadways, self.map.intersections)
        self.default_speed_limit = 0.45 # (m/s)   ~30 miles per hour
        self.default_wait_time = 60 # (s)
        self.default_spawn_rate = 5 # (cars/s)
        self.default_pricing_strategy = "match nearest"

    def get_time(self):
        return self.time.get_time()
    
    def get_map(self, name):
        if name == "College Station":
            College_Station = {
                "height": 6, # Grid map height
                "width": 5, # Grid map width
                "competing_stations": [(6,0), (6,2), (2,0), (1,5)], # Coordinates of gas stations
                "roadways": [((0,6), (2,6)), ((2,6), (5,6)), ((0,6), (0,3)), ((2,6), (2,3)), ((5,6), (5,3)), ((0,3), (2,3)), ((2,3), (5,3)), ((0,3), (0,2)), ((0,2), (0,1)), ((0,1), (0,0)), ((5,3), (5,1)), ((5,1), (5,0)), ((0,0), (2,0)), ((2,0), (3,0)), ((3,0), (5,0))], # Coordinates of endpoints of each roadway between intersections
                "intersections": [(6,0), (6,2), (6,5), (3,0), (3,2), (3,5), (2,0), (1,0), (1,5), (0,0), (0,2), (0,3), (0,5)], # Coordinates of intersections
                "dqn_stations": [(3,0)], # Coordinates of gas stations controlled by DQN
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
        for competing_station in self.map_data["competing_stations"]:
            x, y = competing_station
            smap[x][y]["gas_station"] = Competitor( (x,y), self.default_pricing_strategy, )

        # Add DQN stations to the map (just to change the color in visualization)
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


