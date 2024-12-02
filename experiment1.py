from map.gas_market_simulator import GasMarketSimulator

print("Running simulator for 30 days, 40 times...")

simulator_baseline_layout = "College Station Baseline"
simulator_experimental_layout = "College Station"


with open("results.txt", "a") as file:
    file.write(f"-------start---------\n")

for i in range(1, 21):
    simulator = GasMarketSimulator(simulator_baseline_layout, viz=False)
    simulator.run_simulation(2592000)  # Run simulation for 30 days
    subject, _ = simulator.gas_stations[(0, 3)]
    profit = 0
    volume = 0
    for timestamp, figures in subject.sales.items():
        profit += figures[0]
        volume += figures[1]
    profit = round(profit, 3)
    volume = round(volume, 4)

    # Write results for baseline to file
    with open("results.txt", "a") as file:
        file.write(f"Baseline Simulation #{i} - {profit} , {volume}\n")

    print(f"Completed simulation #{i} for baseline")
    del simulator

for i in range(1, 21):
    simulator = GasMarketSimulator(simulator_experimental_layout, viz=False)
    simulator.run_simulation(2592000)  # Run simulation for 30 days
    subject, _ = simulator.gas_stations[(0, 3)]
    profit = 0
    volume = 0
    for timestamp, figures in subject.sales.items():
        profit += figures[0]
        volume += figures[1]
    profit = round(profit, 3)
    volume = round(volume, 4)

    # Write results for experimental to file
    with open("results.txt", "a") as file:
        file.write(f"Experimental Simulation #{i} - {profit} , {volume}\n")

    print(f"Completed simulation #{i} for experimental")
    del simulator

with open("results.txt", "a") as file:
    file.write(f"--------end--------\n")

print("Results written to results.txt.")
