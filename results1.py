import numpy as np
import matplotlib.pyplot as plt

def parse_data(file_path):
    baseline_profits = []
    baseline_volumes = []
    exp_profits = []
    exp_volumes = []

    with open(file_path, 'r') as file:
        for line in file:
            if "Baseline Simulation" in line:                
                try:
                    data = line.split('-')[1].strip()
                    profit, volume = map(float, data.split(','))
                    baseline_profits.append(profit)
                    baseline_volumes.append(volume)
                except (ValueError, IndexError):
                    print(f"Skipping invalid line: {line.strip()}")
            if "Experimental Simulation" in line:
                try:
                    data = line.split('-')[1].strip()
                    profit, volume = map(float, data.split(','))
                    exp_profits.append(profit)
                    exp_volumes.append(volume)
                except (ValueError, IndexError):
                    print(f"Skipping invalid line: {line.strip()}")
            
    
    return baseline_profits, baseline_volumes, exp_profits, exp_volumes

file_path = 'results.txt'  # Replace with your file path
b_profits, b_volumes, e_profits, e_volumes = parse_data(file_path)
# print("B Profits:", b_profits)
# print("B Volumes:", b_volumes)
# print("E Profits:", e_profits)
# print("E Volumes:", e_volumes)

data = [b_profits, b_volumes, e_profits, e_volumes]

means = [np.mean(lst) for lst in data]
std_devs = [np.std(lst) for lst in data]

x_positions = np.arange(len(data))
labels = ['Total Profit', 'Total Volume', 'Total Profit', 'Total Volume']

for label, mean, std in zip(labels, means, std_devs):
    print(f"{label}: Mean = {mean:.2f}, Std Dev = {std:.2f}")
    
# Define colors for each group
colors = ['red', 'red', 'skyblue', 'skyblue']

# Plot bar diagram with error bars
plt.figure(figsize=(8, 6))
bars = plt.bar(x_positions, means, yerr=std_devs, capsize=5, alpha=0.7, color=colors)

# Adjust y-axis to make room for the legend
plt.ylim(0, max(means) + max(std_devs) + 50000)

# Set x-axis labels
plt.xticks(x_positions, labels)
plt.ylabel('Mean Value')
plt.title('Difference in Pricing Strategies Over 30 Days')

# Add a legend
red_patch = plt.Line2D([0], [0], color='red', lw=4, label='Match Nearest')
blue_patch = plt.Line2D([0], [0], color='skyblue', lw=4, label='DQN Agent')
plt.legend(handles=[red_patch, blue_patch], loc='upper right')

# Show the plot
plt.show()
