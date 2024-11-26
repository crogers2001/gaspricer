from map.gas_market_simulator import GasMarketSimulator
from visualization.visualization import visualize

if __name__ == "__main__":

    simulator_layout = "College Station" # Eventually prompt user which map to load

    # Load up the simulator with chosen map:
    simulator = GasMarketSimulator(simulator_layout)
    print(f'Loaded {simulator_layout} map.')

    # Prompt user how long they want the simulation to run for:

    # Run simulator for desired number of 'seconds':
    # 1 month = 2592000
    simulator.run_simulation(2592000)
            
    # Open visualization to allow user to navigate through time to see the price changes and traffic movement:
    visualize(simulator.visualization_data)

