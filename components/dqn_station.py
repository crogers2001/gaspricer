from components.gas_station import GasStation
from enum import Enum

# Using code from Dr. Sharon's DQN.py and Abstract_Solver.py as a template (we might have to notify Dr. Sharon that we did this)
# Combining DQN and Abstract Solver classes

class DQNStation(GasStation):
    def __init__(self, coordinate, gas_station_list, shortest_paths, env, eval_env, options):
        super().__init__(coordinate, gas_station_list, shortest_paths)
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

class Statistics(Enum):
    Episode = 0
    Rewards = 1
    Steps = 2