import matplotlib.pyplot as plt
import numpy as np

# Data for Q2, Q3, Q4 2025
quarters = ['Q2 2025', 'Q3 2025', 'Q4 2025']
eps = [0.29, 0.65, 0.85]  # EPS projections
net_income = [650, 1000, 1350]  # Net income projections in millions

# Create figure and axis
fig, ax1 = plt.subplots(figsize=(8, 6))

# Plot EPS on primary y-axis
ax1.plot(quarters, eps, 'b-', marker='o', label='EPS ($)')
ax1.set_xlabel('Quarter')
ax1.set_ylabel('EPS ($)', color='b')
ax1.tick_params(axis='y', labelcolor='b')
ax1.grid(True, linestyle='--', alpha=0.7)

# Create secondary y-axis for net income
ax2 = ax1.twinx()
ax2.plot(quarters, net_income, 'r-', marker='s', label='Net Income ($M)')
ax2.set_ylabel('Net Income ($M)', color='r')
ax2.tick_params(axis='y', labelcolor='r')

# Title and legend
plt.title('Tesla Projected EPS and Net Income (Q2-Q4 2025)')
fig.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=2)

# Adjust layout to prevent overlap
fig.tight_layout()

# Save the plot
plt.savefig('tesla_projections.png')
