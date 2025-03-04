relative_traffic_baseline = [0.11,0.13,0.15,0.19,0.2,0.3,0.5,0.83,0.81,0.72,0.66,0.63,0.63,0.64,0.72,0.87,0.95,1,0.82,0.65,0.49,0.398,0.26,0.2]

import matplotlib.pyplot as plt

# Data
relative_traffic_baseline = [
    0.11, 0.13, 0.15, 0.19, 0.2, 0.3, 0.5, 0.83, 0.81, 0.72, 0.66, 
    0.63, 0.63, 0.64, 0.72, 0.87, 0.95, 1, 0.82, 0.65, 0.49, 0.398, 
    0.26, 0.2
]

# Generate plot
plt.figure(figsize=(10, 6))
plt.plot(relative_traffic_baseline, marker='o', linestyle='-')
plt.title('Average Relative Traffic')
plt.xlabel('Hour of Day')
plt.ylabel('Proportion of Maximum Traffic Level')
plt.grid(True)
plt.legend()
plt.tight_layout()

# Show the plot
plt.show()