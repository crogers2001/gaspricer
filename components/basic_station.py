from components.gas_station import GasStation
import random

from globals import DEBUG_BASIC_STATION
def debug(str):
    if DEBUG_BASIC_STATION:
        print(str)

class BasicStation(GasStation):

    def __init__(self, coordinate, gas_station_list, shortest_paths, intersections, starting_p_w, pricing_strategy):
        super().__init__(coordinate, gas_station_list, shortest_paths, intersections, starting_p_w)
        self.pricing_strategy = self.get_pricing_fn(pricing_strategy)
        self.fixed_markup = round(random.uniform(0.10, 0.20), 2)

    def get_pricing_fn(self, pricing_strategy):
        if pricing_strategy == "match_nearest":
            def match_nearest(gas_prices):
                # Get the first element from the gas station priority list
                coord_of_nearest = self.competitor_priority_list[0]
                return gas_prices[coord_of_nearest] # set the price to that of the nearest gas station
            return match_nearest
        
        elif pricing_strategy == "fixed_markup":
            def fixed_markup(gas_prices):
                return self.current_wholesale_price + self.fixed_markup # set the price to a fixed markup above wholesale
            return fixed_markup
        
    def update(self, gas_prices, current_hour, new_wholesale_price=None):
        """
        Returns new gas price
        Updates wholesale_price
        Updates gas price based on pricing strategy of competing station
        """
        self._cleanup_old_sales()

        if new_wholesale_price:
            self.current_wholesale_price = new_wholesale_price
            self.replenish_inventory()
            
        inventory_level = self.current_inventory / self.maximum_inventory_capacity
        if current_hour == self.refueling_time and inventory_level < 0.5:
        #FIXME: Current iventory replenishing logic isn't realistic but 
        # needs to be done this way until I can think of a good way 
        # to avoid replenishing every second of the current hour
            self.replenish_inventory()
        self.set_and_adjust_price(self.pricing_strategy(gas_prices))
        return self.posted_gas_price



