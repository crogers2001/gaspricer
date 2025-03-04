from components.gas_station import GasStation
from components.dqn_agent import DQNAgent
import random
from collections import deque

from globals import DEBUG_DQN_STATION
def debug(str):
    if DEBUG_DQN_STATION:
        print(str)

class DQNStation(GasStation):
    def __init__(self, coordinate, gas_station_list, shortest_paths, intersections, starting_p_w):
        super().__init__(coordinate, gas_station_list, shortest_paths, intersections, starting_p_w)
        self.p_c = {}
        # self.dqn_agent = DQNAgent(coordinate, gas_station_list, shortest_paths, intersections, starting_p_w)
        self.state_size = 6  # State includes p_w, p_o, avg(p_c), traffic, demand, inventory
        self.action_size = 7 # -0.03, -0.02, -0.01, 0, +0.01, +0.02, +0.03
        self.action_price_delta = (self.action_size - 1) / 2
        self.memory = deque(maxlen=2000)
        self.agent = DQNAgent(self.state_size, self.action_size)
        self.discount_factor = 0.95
        self.reward_history = []
            
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
        self._cleanup_old_sales()
        self.current_hour = current_hour

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
        state = self.get_state(gas_prices, traffic)
        action = self.act(state)
        price_change = (action - self.action_price_delta) / 100 
        new_price = max(self.get_p_w(), min(self.get_p_o() + price_change, self.get_p_w() + 0.5))
        
        self.set_and_adjust_price(new_price)
        next_state = self.get_state(gas_prices, traffic)
        reward = self.calculate_reward()
        done = False
        
        debug(f'(dqn_station.py): State- {state}, Action- {action}, Reward- {reward}, NextState- {next_state}, Done- {done}')
        self.reward_history.append(reward)

        self.remember(state, action, reward, next_state, done)
        if len(self.memory) > 32:
            self.replay(32)
        
        return self.posted_gas_price
    
    # def get_state(self, gas_prices, traffic):
    #     # Define how to construct the state from the environment
    #     return [self.current_wholesale_price, self.posted_gas_price, traffic, self.gallons_last_hour, self.current_inventory]
    
    def get_state(self, gas_prices, traffic):
        """Constructs the state representation for the DQN."""
        p_w = self.get_p_w()
        p_o = self.get_p_o()
        p_c = sum(gas_prices.values()) / len(gas_prices) if gas_prices else p_o  # Avg competitor price
        t = traffic
        d = self.get_d()
        i = self.get_i()
        return [p_w, p_o, p_c, t, d, i]

    def calculate_reward(self):
        # Define how to calculate the reward
        # return self.gallons_last_hour - self.operating_costs
        gallons_sold = self.get_d()  # Demand = Gallons sold in the last hour
        profit = (gallons_sold * self.get_p_o()) - (gallons_sold * self.get_p_w())
        volume = gallons_sold

        reward = self.discount_factor * (profit + volume)
        return reward

    def calculate_price_from_action(self, action):
        # Define how to map an action to a price
        return self.current_wholesale_price + 0.01 * action
    
    def act(self, state):
        """Get action from the DQN agent."""
        return self.agent.act(state)

    def remember(self, state, action, reward, next_state, done):
        """Store experience in memory."""
        self.memory.append((state, action, reward, next_state, done))

    def replay(self, batch_size):
        """Train the agent on a batch of past experiences."""
        self.agent.replay(batch_size)
