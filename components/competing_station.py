from gas_station import GasStation

class Competitor(GasStation):

    def __init__(self, pricing_strategy, gas_station_list, shortest_paths):
        self.pricing_strategy = self.get_policy_fn(pricing_strategy)
        self.fixed_markup = 0.20

    def get_pricing_fn(self, pricing_strategy):
        if pricing_strategy == "match nearest":
            def match_nearest():
                self.set_price(self.competitor_priority_list[0]["current_price"]) # set the price to that of the nearest gas station
            return match_nearest
        
        elif pricing_strategy == "fixed markup":
            def fixed_markup():
                self.set_price(self.current_wholesale_price + self.fixed_markup) # set the price to a fixed markup above wholesale
            return fixed_markup


