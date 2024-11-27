from map.gas_market_simulator import GasMarketSimulator
from visualization.visualization import visualize

if __name__ == "__main__":
############################################################
## To enable debugging print statements, go to globals.py ##
## and toggle the file(s)' respective debug variable      ##
############################################################

    simulator_layout = "College Station" # Eventually prompt user which map to load

    simulator = GasMarketSimulator(simulator_layout)

    # Run simulator for desired number of 'seconds':
    # 1 day = 86400,   1 month (30 days) = 2592000,   1 year (365 days)= 31,536,000
    simulator.run_simulation(10000)

    # Open visualization to allow user to navigate through time:
    visualize(simulator.visualization_data)

