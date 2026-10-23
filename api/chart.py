import matplotlib
matplotlib.use('Agg') # Required for headless environments like Termux
import matplotlib.pyplot as plt
import pandas as pd

def generate_chart(df, price, nearest_level, filename="chart.png"):
    plot_df = df.tail(50).copy()
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Draw Candlesticks
    for i, row in plot_df.iterrows():
        color = 'green' if row['close'] >= row['open'] else 'red'
        ax.plot([i, i], [row['low'], row['high']], color=color, linewidth=1)
        ax.plot([i, i], [row['open'], row['close']], color=color, linewidth=4)

    # Draw Level
    if nearest_level:
        level_price = nearest_level['price']
        level_type = nearest_level['type'].upper()
        ax.axhline(y=level_price, color='blue' if level_type == 'SUPPORT' else 'purple', 
                   linestyle='--', linewidth=2, label=f"{level_type}: {level_price:.2f}")

    ax.set_title("XAU/USD (PAXG Proxy) - H1", fontsize=14)
    ax.set_ylabel("Price")
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.savefig(filename, bbox_inches='tight', dpi=100)
    plt.close()
    return filename
