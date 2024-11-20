from gas_station import GasStation

class Competitor(GasStation):

    def __init__(self, coordinate, pricing_strategy, gas_station_list, shortest_paths):
        self.coordinate = coordinate
        self.pricing_strategy = self.get_policy_fn(pricing_strategy)
        self.station_priority_list = self.get_station_priority_list(gas_station_list, shortest_paths)

    def get_station_priority_list(gas_station_list, shortest_paths):
        pass
        
    def match_nearest(self):
        pass

    def get_policy_fn(self, pricing_strategy):
        if pricing_strategy == "match nearest":
            return self.match_nearest()

