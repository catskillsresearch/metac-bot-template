import matplotlib.pyplot as plt

def plot_community_errors(df):
    plt.figure(figsize=(10,6))
    plt.hist(df.error.values, bins=20, alpha=0.7)
    plt.title(f"Forecast Error Distribution\nMean: {df.error.mean():.3f} Median: {df.error.median():.3f}")
    plt.savefig('community_errors.png', dpi=150)
