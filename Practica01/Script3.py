import numpy as np
import matplotlib.pyplot as plt

"""
    Compute y values for a hyperbola given x values, and parameters a and b.
    Parameters:
        x (array_like): Input values.
        a (float): Parameter defining the distance from the center to the vertices along the x-axis.
        b (float): Parameter defining the distance from the center to the vertices along the y-axis.
    Returns:
        array_like: Computed y values for the given x values.
"""
# Define the hyperbola function
def hyperbola(x, a, b):
    return np.sqrt((x/a)**2 - 1) * b
# Create a range of x values
x_values = np.linspace(-5, 5, 400)
# Define the parameters of the hyperbola
a = 1
b = 1
# Calculate the corresponding y values
y_values = hyperbola(x_values, a, b)
# Plot the hyperbola
plt.figure(figsize=(8, 6))
plt.plot(x_values, y_values, label='Hyperbola: $\sqrt{(x/a)^2 - 1} * b$', color='blue')
plt.plot(x_values, -y_values, color='blue') 
plt.title('Dafne\'s Hyperbola')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(0, color='black', linewidth=0.5)
plt.legend()
plt.axis('equal')  # To have the same scale on both axes
plt.show()
