from components.global_clock import GlobalClock

class GasStation:

    def __init__(self, coordinate, gas_station_list, shortest_paths, intersections):
        self.clock = GlobalClock()
        self.coordinate = coordinate # acts as ID 
        self.competitor_priority_list = self.get_station_priority_list(gas_station_list, shortest_paths, intersections)
        self.current_inventory = 0 # gallons of gas
        self.maximum_inventory_capacity = 20000 # gallons of gas
        self.posted_gas_price = 0 
        self.current_wholesale_price = 0
        self.sales = {} 
        self.purchases = {}
        self.account_balance = 100000 # starting balance

    def get_station_priority_list(self, gas_station_list, shortest_paths, intersections):
        """Returns a list of the other gas stations sorted by proximity to this gas station"""
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
        # print(f'Prio list for station {self.coordinate}: {ret_list}')
        return ret_list


    def sell_gas(self, volume, car_id):
        """Returns boolean value. Adjusts inventory, balance, and makes a record of the sale if valid transaction."""
        if self.current_inventory < volume:
            return False
        self.current_inventory -= volume
        price = self.posted_gas_price
        revenue = volume * price
        profit = revenue - (volume * self.current_wholesale_price)
        self.sales[self.clock.get_time()] = (profit, volume, price, car_id) # profit, volume, price, car_id
        self.account_balance += revenue
        return True

    def replenish_inventory(self, wholesale_price):
        """Returns boolean value. Adjusts inventory, balance, and makes a record of the purchase if valid transaction."""
        if self.current_inventory == self.maximum_inventory_capacity:
            return False
        self.current_wholesale_price = wholesale_price
        volume = self.maximum_inventory_capacity - self.current_inventory
        cost = -(volume * wholesale_price)
        self.purchases[self.clock.get_time()] = (cost, volume, wholesale_price)
        self.account_balance =+ cost
        return True

    def set_price(self, new_price):
        self.posted_gas_price = new_price

