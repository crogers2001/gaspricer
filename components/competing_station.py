from components.gas_station import GasStation

class Competitor(GasStation):

    def __init__(self, coordinate, gas_station_list, shortest_paths, intersections, pricing_strategy):
        super().__init__(coordinate, gas_station_list, shortest_paths, intersections)
        self.pricing_strategy = self.get_pricing_fn(pricing_strategy)
        self.fixed_markup = 0.20

    def get_pricing_fn(self, pricing_strategy):
        if pricing_strategy == "match_nearest":
            def match_nearest():
                self.set_price(self.competitor_priority_list[0]["current_price"]) # set the price to that of the nearest gas station
            return match_nearest
        
        elif pricing_strategy == "fixed_markup":
            def fixed_markup():
                self.set_price(self.current_wholesale_price + self.fixed_markup) # set the price to a fixed markup above wholesale
            return fixed_markup
        
    def update(self):
        pass


