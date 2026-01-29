import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# ----------------------------------------------------------------------------------
# CONFIGURATION (Dark Mode Style)
# ----------------------------------------------------------------------------------
plt.style.use('dark_background')

def generate_stochastic_forecast_plots():
    # 1. PARAMETERS (Based on the Paper's logic)
    S0 = 100       # Initial Value ($100)
    mu = 0.08      # Drift (8% expected annual return)
    sigma = 0.20   # Volatility (20% standard deviation)
    T = 1.0        # Time horizon (1 year)
    dt = 1/252     # Daily time steps
    N = int(T/dt)  # Total steps
    sims = 5000    # Number of Monte Carlo simulations

    # 2. CORE SIMULATION (Geometric Brownian Motion)
    # S_t = S_{t-1} * exp((mu - 0.5*sigma^2)*dt + sigma*sqrt(dt)*Z)
    
    # Initialize matrix [Days x Simulations]
    paths = np.zeros((N, sims))
    paths[0] = S0
    
    np.random.seed(42) # For reproducibility
    
    for t in range(1, N):
        Z = np.random.standard_normal(sims) # Random shocks
        drift = (mu - 0.5 * sigma**2) * dt
        shock = sigma * np.sqrt(dt) * Z
        paths[t] = paths[t-1] * np.exp(drift + shock)

    # ----------------------------------------------------------------------------------
    # PLOT A: THE CONE OF UNCERTAINTY
    # ----------------------------------------------------------------------------------
    # Calculate Percentiles over time
    p5 = np.percentile(paths, 5, axis=1)   # 95% VaR Line (Worst case)
    p50 = np.percentile(paths, 50, axis=1) # Median (Realistic Expectation)
    p95 = np.percentile(paths, 95, axis=1) # Best case
    
    time_axis = np.linspace(0, T, N)
    
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Plot random individual paths (faint background)
    ax.plot(time_axis, paths[:, :200], color='cyan', alpha=0.03, lw=0.5)
    
    # Plot Statistical Cone
    ax.plot(time_axis, p95, color='#00ff00', lw=2, ls='--', label='Upside Potential (95th %)')
    ax.plot(time_axis, p50, color='white', lw=3, label='Median Forecast')
    ax.plot(time_axis, p5, color='#ff3333', lw=2, ls='--', label='Downside Risk (VaR 95%)')
    
    # Fill the Cone area
    ax.fill_between(time_axis, p5, p95, color='cyan', alpha=0.1)
    
    # Styling
    ax.set_title('The Geometry of Risk: "Cone of Uncertainty"', fontsize=20, fontweight='bold', color='white', pad=20)
    ax.set_xlabel('Time Horizon (Years)', fontsize=12, color='#cccccc')
    ax.set_ylabel('Projected Value', fontsize=12, color='#cccccc')
    ax.legend(loc='upper left', frameon=False, fontsize=11)
    ax.grid(color='gray', linestyle=':', linewidth=0.5, alpha=0.3)
    
    # Annotation
    final_var = p5[-1]
    ax.annotate(f'RISK FLOOR:\n${final_var:.2f}', xy=(1, final_var), xytext=(1.02, final_var),
                arrowprops=dict(facecolor='#ff3333', arrowstyle='->'), color='#ff3333', fontweight='bold')
    
    plt.tight_layout()
    plt.show() # Shows Plot A

    # ----------------------------------------------------------------------------------
    # PLOT B: TERMINAL DISTRIBUTION (TAIL RISK)
    # ----------------------------------------------------------------------------------
    final_values = paths[-1]
    var_95 = np.percentile(final_values, 5)
    cvar_95 = final_values[final_values <= var_95].mean() # Conditional VaR (Avg of the tail)
    
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Histogram
    n, bins, patches = ax.hist(final_values, bins=80, color='#00cc99', alpha=0.6, edgecolor='none')
    
    # Color the "Death Zone" (Tail Risk) in Red
    for c, p in zip(bins, patches):
        if c < var_95:
            plt.setp(p, 'facecolor', '#ff3333', 'alpha', 0.9)
            
    # Vertical Lines
    ax.axvline(var_95, color='white', ls='--', lw=2, label=f'VaR (95%): ${var_95:.2f}')
    ax.axvline(cvar_95, color='yellow', ls=':', lw=2, label=f'CVaR (Expected Loss): ${cvar_95:.2f}')
    ax.axvline(np.mean(final_values), color='white', lw=2, label=f'Mean: ${np.mean(final_values):.2f}')
    
    # Styling
    ax.set_title('Tail Risk Analysis: Identifying Extreme Loss Scenarios', fontsize=20, fontweight='bold', color='white', pad=20)
    ax.set_xlabel('Final Asset Value', fontsize=12, color='#cccccc')
    ax.set_ylabel('Frequency', fontsize=12, color='#cccccc')
    ax.legend(loc='upper right', frameon=False, fontsize=11)
    
    # Floating Note
    note = (
        "INTERPRETATION: The red area represents the 5% worst-case scenarios.\n"
        f"While the average outcome is profitable, the CVaR indicates that in a crisis,\n"
        f"the asset value could drop to ${cvar_95:.0f} on average."
    )
    plt.figtext(0.5, 0.02, note, ha='center', fontsize=11, color='#aaaaaa', style='italic')
    
    plt.subplots_adjust(bottom=0.15)
    plt.show() # Shows Plot B

if __name__ == "__main__":
    generate_stochastic_forecast_plots()
