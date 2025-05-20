import matplotlib.pyplot as plt
import numpy as np

# Data for Q1 2025 (current) and Q2 2025–Q1 2027
quarters = ['Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026', 'Q4 2026', 'Q1 2027']
prices = [342.00, 325.00, 335.00, 355.00, 370.00, 390.00, 405.00, 430.00, 450.00]

# Create figure and axis
plt.figure(figsize=(10, 6))
plt.plot(quarters, prices, 'b-', marker='o', linewidth=2, markersize=8, label='Projected Stock Price')

# Add annotations for key points
plt.annotate(f'${prices[0]}', (quarters[0], prices[0]), textcoords="offset points", xytext=(0,10), ha='center', fontsize=10)
plt.annotate(f'${prices[1]} (Dip)', (quarters[1], prices[1]), textcoords="offset points", xytext=(0,-15), ha='center', fontsize=10)
plt.annotate(f'${prices[3]}', (quarters[3], prices[3]), textcoords="offset points", xytext=(0,10), ha='center', fontsize=10)
plt.annotate(f'${prices[-1]}', (quarters[-1], prices[-1]), textcoords="offset points", xytext=(0,10), ha='center', fontsize=10)

# Customize chart
plt.title('TSLA Stock Price Projection (Q2 2025–Q1 2027)', fontsize=14, pad=20)
plt.xlabel('Quarter', fontsize=12)
plt.ylabel('Stock Price ($)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(loc='upper left')
plt.xticks(rotation=45)

# Adjust layout to prevent label cutoff
plt.tight_layout()

# Save the plot as PNG
plt.savefig('tsla_price_projection.png')
