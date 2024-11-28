from map.gas_market_simulator import GasMarketSimulator
from visualization.visualization import visualize
from datetime import datetime, timedelta
import sys
import torch

if __name__ == "__main__":
    
    print("CUDA Available: ", torch.cuda.is_available())
############################################################
## To enable debugging print statements, go to globals.py ##
## and toggle the file(s)' respective debug variable      ##
############################################################
    def convert_seconds_to_timestamp(total_seconds):
        start_date = datetime(2023, 1, 1)
        new_date = start_date + timedelta(seconds=total_seconds)
        timestamp = new_date.strftime("%b %d, %Y %H:%M:%S")
        return timestamp
    
    simulator_layout = "College Station" # Eventually prompt user which map to load

    simulator = GasMarketSimulator(simulator_layout)
    print("\n#-------------------------------------------------------------------------#\n")
    print("The College Station gas market simulator has been initialized.\n")

    # Prompt user for simulation duration
    while True:
        print("1 day = 86400 seconds")
        print("1 week = 604800 seconds")
        print("1 month (30 days) = 2592000 seconds")
        print("1 year (365 days) = 31536000 seconds\n")
        user_input = input("Enter the simulation duration in seconds or 'q' to quit: ")
        if user_input.lower() == 'q':
            print("Exiting program.")
            sys.exit()
        try:
            user_time = int(user_input)
            if user_time <= 0:
                raise ValueError("The time must be a positive integer.")
            if user_time > 31536000:
                raise ValueError("This time exceeds the allowed value.")
            break
        except ValueError as e:
            print(f"Invalid input: {e}. Please try again.")

    print(f"\nThank you. Now running simulation for {user_time} iterations (Jan 1, 2023 00:00:00 to {convert_seconds_to_timestamp(user_time - 1)}) ...")
    print(f"*Please note that it won't actually take {user_time} seconds*")
    simulator.run_simulation(user_time)
    print("\nSimulation complete. Now visualizing the data ...")

    visualize(simulator.visualization_data)

