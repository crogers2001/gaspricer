from components.global_clock import GlobalClock
from collections import deque
from globals import DEBUG_GAS_STATION
def debug(str):
    if DEBUG_GAS_STATION:
        print(str)

class GasStation:

    def __init__(self, coordinate, gas_station_list, shortest_paths, intersections, starting_p_w):
        self.clock = GlobalClock()
        self.coordinate = coordinate # acts as ID 
        self.competitor_priority_list = self.get_station_priority_list(gas_station_list, shortest_paths, intersections)
        self.current_inventory = 0 # gallons of gas
        self.maximum_inventory_capacity = 20000 # gallons of gas
        self.operating_costs = 0.06 # required profit per gallon
        self.current_wholesale_price = starting_p_w
        self.posted_gas_price = self.current_wholesale_price + self.operating_costs
        self.sales = {} # key = car_id
        self.sales_last_hour = deque()
        self.gallons_last_hour = 0
        self.purchases = {} # key = timestamp
        self.account_balance = 100000 # starting balance



    def get_station_priority_list(self, gas_station_list, shortest_paths, intersections):
        """Returns a list of the coordinates other gas stations sorted by proximity to this gas station"""
        unsorted_list = []
        my_index = intersections[self.coordinate]
        for gs in gas_station_list:
            # ex: gs = ((0,3), "dqn")
            gs_coord = gs[0]
            gs_index = intersections[gs_coord]
            if not gs_index == my_index:
                path_cost = shortest_paths[my_index][gs_index][0]
                unsorted_list.append( (gs_coord, path_cost) )
        sorted_list = sorted(unsorted_list, key=lambda x: x[1])
        ret_list = []
        for item in sorted_list:
            # ex: item = ((0,3), 4)
            ret_list.append(item[0])
        # debug(f'Prio list for station {self.coordinate}: {ret_list}')
        return ret_list


    def sell_gas(self, volume, car_id):
        """Returns boolean value. Adjusts inventory, balance, and makes a record of the sale if valid transaction."""
        debug(f'(gas_station.py): Station {self.coordinate} has been asked to sell {volume} gallons of gas to Car #{car_id}')
        if self.current_inventory < volume:
            debug(f'Station {self.coordinate} rejected Car #{car_id}')
            return False
        self.current_inventory -= volume
        price = self.posted_gas_price
        revenue = volume * price
        profit = revenue - (volume * self.current_wholesale_price)

        timestamp = self.clock.get_time()
        self.sales_last_hour.append((timestamp, volume, price, car_id))

        if car_id not in self.sales:
            self.sales[car_id] = {'total_volume': 0, 'total_revenue': 0, 'total_profit': 0}
        self.sales[car_id]['total_volume'] += volume
        self.sales[car_id]['total_revenue'] += revenue
        self.sales[car_id]['total_profit'] += profit

        self.gallons_last_hour += volume
        self.account_balance += revenue
        debug(f'(gas_station.py): Station {self.coordinate} sold {volume} gallons of gas to Car #{car_id}')
        self._cleanup_old_sales()
        return True

    def _cleanup_old_sales(self):
        """Removes transactions from the deque that are older than one hour."""
        current_time = self.clock.get_time()
        one_hour_ago = current_time - 3600

        while self.sales_last_hour and self.sales_last_hour[0][0] < one_hour_ago:
            timestamp, volume, _, _ = self.sales_last_hour.popleft()
            self.gallons_last_hour -= volume

    def replenish_inventory(self):
        """Returns boolean value. Adjusts inventory, balance, and makes a record of the purchase if valid transaction."""
        if self.current_inventory == self.maximum_inventory_capacity:
            return False
        volume = self.maximum_inventory_capacity - self.current_inventory
        cost = -(volume * self.current_wholesale_price)
        self.purchases[self.clock.get_time()] = (cost, volume, self.current_wholesale_price)
        self.current_inventory = self.maximum_inventory_capacity
        self.account_balance =+ cost
        debug(f'(gas_station.py): Station {self.coordinate} restocked with {volume} gallons (Time: {self.clock.get_time()}).')
        return True

    def set_price(self, new_price):
        self.posted_gas_price = new_price

