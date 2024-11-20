from components.global_clock import GlobalClock
from shortest_paths import get_adjacency_matrix

class GasMarketSimulator: # Needs to output a big dataset for visualization.py to display
    
    def __init__(self, layout_name):
        self.map = self.get_map(layout_name)
        self.time = GlobalClock()
        self.shortest_paths = get_adjacency_matrix(self.map.roadways, self.map.intersections)

    def get_time(self):
        return self.time.get_time()
    
    def get_map(self, name):
        if name == "College Station":
            College_Station = {
                "height": 6, # Grid map height
                "width": 5, # Grid map width
                "gas_stations": [(6,0), (6,2), (3,0), (2,0), (1,5)], # Coordinates of gas stations
                "roadways": [((0,6), (2,6)), ((2,6), (5,6)), ((0,6), (0,3)), ((2,6), (2,3)), ((5,6), (5,3)), ((0,3), (2,3)), ((2,3), (5,3)), ((0,3), (0,2)), ((0,2), (0,1)), ((0,1), (0,0)), ((5,3), (5,1)), ((5,1), (5,0)), ((0,0), (2,0)), ((2,0), (3,0)), ((3,0), (5,0))], # Coordinates of start and end of each roadway between intersections
                "intersections": [(6,0), (6,2), (6,5), (3,0), (3,2), (3,5), (2,0), (1,0), (1,5), (0,0), (0,2), (0,3), (0,5)], # Coordinates of intersections
                "dqn_stations": [(3,0)], # Coordinates of gas stations controlled by DQN
                "max_traffic": 250, # Absolute maximum number of cars on map
            }
            return College_Station
        else:
            return {"error": "Layout does not exist."}
        


    
    def add_3_seconds(self):
        self.time.tick()
        self.time.tick()
        self.time.tick()

