from components.gas_station import GasStation

from globals import DEBUG_DQN_STATION
def debug(str):
    if DEBUG_DQN_STATION:
        print(str)

class DQNStation(GasStation):
    def __init__(self, coordinate, gas_station_list, shortest_paths, intersections, starting_p_w):
        super().__init__(coordinate, gas_station_list, shortest_paths, intersections, starting_p_w)
        self.p_c = {}
    
    def get_p_w(self):
        """Returns current price of wholesale"""
        return self.current_wholesale_price
    
    def get_p_o(self):
        """Returns our price"""
        return self.posted_gas_price
    
    def get_p_c(self):
        """Returns dictionary of competitors' prices in order of their proximity to us"""
        return self.p_c

    def get_t(self):
        """Returns current number of cars in front of our gas station"""
        return self.cars_at_intersection
    
    def get_d(self):
        """Returns demand (gallons sold in the last hour)"""
        return self.gallons_last_hour
    
    def get_i(self):
        """Returns current inventory"""
        return self.current_inventory
    

    def update(self, gas_prices, traffic, current_hour, new_p_w=None):
        if self.clock.get_time() == 1: # Match nearest to start
            coord_of_nearest = self.competitor_priority_list[0]
            new_price = gas_prices[coord_of_nearest]
            self.set_and_adjust_price(new_price)
            return self.posted_gas_price
        
        if new_p_w:
            self.current_wholesale_price = new_p_w
            self.replenish_inventory()

        inventory_level = self.current_inventory / self.maximum_inventory_capacity

        if current_hour == self.refueling_time and inventory_level < 0.5:
        #FIXME: Current iventory replenishing logic isn't realistic but 
        # needs to be done this way until I can think of a good way 
        # to avoid replenishing every second of the current hour
            self.replenish_inventory()

        gas_prices_copy = gas_prices.copy()
        del gas_prices_copy[self.coordinate]
        self.p_c = gas_prices_copy

        self.cars_at_intersection = traffic

        # Update gas price using DQN algorithm:
        # Use: self.set_and_adjust_price(new_price)
        return self.posted_gas_price