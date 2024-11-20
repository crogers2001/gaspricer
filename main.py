from map.gas_market_simulator import GasMarketSimulator

if __name__ == "__main__":

    simulator_layout = "College Station" # Eventually prompt user which map to load

    # Load up the simulator with chosen map:
    simulator = GasMarketSimulator(simulator_layout)
    print(f'Loaded {simulator_layout} map.')

    # Prompt user how long they want the simulation to run for:

    # Run simulator for desired amount of time (usually days):

    # Open visualization to allow user to navigate through time to see the price changes and traffic movement:


    


    #### Testing clock
    print(f'Start global clock: {simulator.get_time()}')
    simulator.add_3_seconds()
    print(f'Middle global clock: {simulator.get_time()}')
    simulator.move_car()
    print(f'End global clock: {simulator.get_time()}')
