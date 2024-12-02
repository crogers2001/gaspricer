from map.gas_market_simulator import GasMarketSimulator
from visualization.visualization import visualize
from datetime import datetime, timedelta
import sys
import matplotlib.pyplot as plt
from scipy.stats import linregress
import numpy as np

if __name__ == "__main__":
    
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
        print("1 month = 2592000 seconds")
        print("1 year = 31536000 seconds\n")
        print("For demonstration purposes, it is recommended to run the simulation for 86400 - 604800 seconds.\n")
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
    

    for key, value in simulator.gas_stations.items():
        gas_station, type = value
        coordinate = key
        label = f'Station @ {coordinate} ({type})'
        x = []
        y = []
        if type == "dqn":
            for i, reward in enumerate(gas_station.reward_history):
                x.append(i)
                y.append(reward)
            plt.plot(x,y, label=label)
            x_array = np.array(x)
            y_array = np.array(y)
            slope, intercept, _, _, _ = linregress(x_array, y_array)
            trend_line = slope * x_array + intercept
            plt.plot(x, trend_line, linestyle='--', label='Trend')

            growth_rate_per_day = slope * 86400  # Assuming time is in seconds

            plt.text(
            0.05 * max(x), 0.95 * max(y),  # Position text near the top-left
            f"Growth Rate:\n"
            f"{growth_rate_per_day:.2f} / day",
            fontsize=10,
            bbox=dict(facecolor='white', alpha=0.7)
            )

    plt.xlabel('Time (sec)')
    plt.ylabel('Reward')
    plt.title('DQN Reward Over Time')
    plt.legend()
    plt.show()


    for key, value in simulator.gas_stations.items():
        gas_station, type = value
        coordinate = key
        label = f'Station @ {coordinate} ({type})'
        x = []
        y = []
        for timestamp, figures in gas_station.sales.items():
            instantaneous_profit = figures[0]
            profit = instantaneous_profit
            if len(y) > 0:
                profit += y[-1]
            x.append(timestamp)
            y.append(profit)
        plt.plot(x,y, label=label)

    plt.xlabel('Time (sec)')
    plt.ylabel('Profit ($)')
    plt.title('Profits Gained by Each Gas Station')
    plt.legend()
    plt.show()
    
    visualize(simulator.visualization_data)