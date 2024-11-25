import numpy as np
import matplotlib.pyplot as plt

x = np.array([
0,
1,
2,
3,
4,
5,
6,
7,
8,
9,
10,
11,
12,
13,
14,
15,
16,
17,
18,
19,
20,
21,
22,
23,
24,
])
y = np.array([
0.11,
0.13,
0.15,
0.19,
0.2,
0.3,
0.5,
0.83,
0.81,
0.72,
0.66,
0.63,
0.63,
0.64,
0.72,
0.87,
0.95,
1,
0.82,
0.65,
0.49,
0.398,
0.26,
0.2,
0.11,
])

degree = 10 # Adjust this to change how much fitting is done
coefficients = np.polyfit(x, y, degree)
polynomial = np.poly1d(coefficients)

print("Polynomial Equation:")
print(polynomial)

x_fit = np.linspace(min(x), max(x), 500)
y_fit = polynomial(x_fit)

plt.scatter(x, y, label='Data Points', color='red')
plt.plot(x_fit, y_fit, label=f'Polynomial Degree {degree}')
plt.legend()
plt.show()


values_by_hour = [0.11,0.13,0.15,0.19,0.2,0.3,0.5,0.83,0.81,0.72,0.66,0.63,0.63,0.64,0.72,0.87,0.95,1,0.82,0.65,0.49,0.398,0.26,0.2]

# Between hour 0 and 1: +0.02
# Between hour 1 and 2: +0.02
# Between hour 2 and 3: +0.04
