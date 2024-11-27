from components.gas_station import GasStation
from enum import Enum
from globals import DEBUG_DQN_STATION
def debug(str):
    if DEBUG_DQN_STATION:
        print(str)

# Using code from Dr. Sharon's DQN.py and Abstract_Solver.py as a template (we might have to notify Dr. Sharon that we did this)
# Combining DQN and Abstract Solver classes

class DQNStation(GasStation):
    def __init__(self, coordinate, gas_station_list, shortest_paths, intersections, starting_p_w, env, eval_env, options):
        super().__init__(coordinate, gas_station_list, shortest_paths, intersections, starting_p_w)
        self.p_c = {}
        self.statistics = [0] * len(Statistics)
        self.env = env
        self.eval_env = eval_env
        self.options = options
        self.total_steps = 0
    


    def init_stats(self):
        pass

    def step(self, action):
        """
        Take one step in the environment while keeping track of statistical information
        Param:
            action:
        Return:
            next_state: The next state
            reward: Immediate reward
            done: Is next_state terminal
            info: Gym transition information
        """
        pass

    def calc_reward(self, state):
        pass

    def run_greedy(self):
        """
        Run the greedy policy.
        """
        pass
    
    # def close(self):
    #     pass

    def train_episode(self):
        pass

    def __str__(self):
        pass

    def create_greedy_policy(self):
        pass

    # def get_out_header():
    #     ans = "Domain,Solver"
    #     for s in Statistics:
    #         ans += "," + s.name
    #     return ans

    # def plot(self, stats, smoothing_window=20, final=False):
    #     pass

    # def get_stat(self):
    #     try:
    #         domain = self.env.unwrapped.spec.id
    #     except:
    #         domain = self.env.name
    #     ans = "{},{}".format(domain, str(self))
    #     for s in Statistics:
    #         ans += "," + str(self.statistics[s.value])
    #     return ans
    def get_p_w(self):
        """Returns current price of wholesale"""
        return self.current_wholesale_price
    
    def get_p_o(self):
        """Returns our price"""
        return self.posted_gas_price
    
    def get_p_c(self):
        """Returns dictionary of competitors' prices"""
        return self.p_c

    def get_d(self):
        """Returns demand (gallons sold in the last hour)"""
        return self.gallons_last_hour
    
    def get_i(self):
        """Returns current inventory"""
        return self.current_inventory
    
    def update(self, gas_prices, new_p_w=None):
        if new_p_w:
            self.current_wholesale_price = new_p_w
            self.replenish_inventory()

        gas_prices_copy = gas_prices.copy()
        del gas_prices_copy[self.coordinate] # Remove self from gas_prices_copy
        self.p_c = gas_prices_copy

        #Update gas price using DQN algorithm:

        return self.posted_gas_price

class Statistics(Enum):
    Episode = 0
    Rewards = 1
    Steps = 2