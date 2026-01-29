import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, genpareto, t

# ----------------------------------------------------------------------------------
# CONFIGURATION (Dark Mode - High Contrast)
# ----------------------------------------------------------------------------------
plt.style.use('dark_background')

def generate_clean_evt_plots():
    # 1. DATA GENERATION (Simulating Fat-Tailed Market)
    np.random.seed(42)
    n = 10000
    # Student-t (df=3) creates realistic heavy tails
    data = t.rvs(df=3, size=n) * 0.02 
    losses = -data # Convert to positive "loss" magnitude for visualization
    losses = losses[losses > 0]
    
    # 2. CALIBRATION (EVT - Peaks Over Threshold)
    u = np.percentile(losses, 95)
    excesses = losses[losses > u] - u
    xi, loc, sigma = genpareto.fit(excesses, floc=0)
    
    # ----------------------------------------------------------------------------------
    # PLOT 1: DISTRIBUTION FIT (Fixed Overlaps)
    # ----------------------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(13, 8)) # Taller for better spacing
    
    # Histogram (Data)
    tail_range = np.linspace(u, max(losses), 1000)
    ax.hist(losses, bins=100, density=True, alpha=0.4, color='#444444', label='Actual Market Losses')
    
    # Gaussian Fit (Blue)
    mu_norm, std_norm = norm.fit(losses)
    gaussian_pdf = norm.pdf(tail_range, mu_norm, std_norm)
    ax.plot(tail_range, gaussian_pdf, color='#00ccff', linestyle='--', linewidth=2.5, label='Normal Dist. (Gaussian)')
    
    # EVT Fit (Red)
    prob_exceed_u = len(excesses) / len(losses)
    gpd_pdf = (genpareto.pdf(tail_range - u, xi, 0, sigma)) * prob_exceed_u
    ax.plot(tail_range, gpd_pdf, color='#ff3333', linewidth=3.5, label='EVT (Generalized Pareto)')
    
    # Formatting & Zoom
    ax.set_title('The Architecture of Ruin: Normal vs. EVT Tail Fit', fontsize=22, fontweight='bold', color='white', pad=25)
    ax.set_xlabel('Loss Magnitude (%)', fontsize=13, color='#cccccc')
    ax.set_ylabel('Probability Density', fontsize=13, color='#cccccc')
    
    # Zoom into the tail (starting a bit before u)
    zoom_start = u * 0.8
    ax.set_xlim(zoom_start, max(losses)*0.6) # Cut off extreme outliers for readability
    ax.set_ylim(0, max(gpd_pdf[0], gaussian_pdf[0]) * 1.5) # Add 50% headroom for text
    
    # Smart Annotation (Placed high up in empty space)
    ax.annotate(
        'The "Underestimation Gap"\n(Gaussian predicts ~0% risk here)', 
        xy=(u*1.3, gaussian_pdf[10]),  # Pointing at the gap
        xytext=(u*1.6, max(gpd_pdf)*0.8), # Text far away in safe zone
        arrowprops=dict(facecolor='#cccccc', arrowstyle='->', connectionstyle="arc3,rad=-0.2"),
        fontsize=12, color='#ffffff', fontweight='bold',
        bbox=dict(boxstyle="round,pad=0.3", fc="#222222", ec="#444444", alpha=0.8)
    )
    
    ax.legend(loc='upper right', frameon=True, fontsize=12, facecolor='#222222', edgecolor='#444444')
    
    # Bottom Note
    note = (f"INSIGHT: The Blue line (Gaussian) drops to zero too fast, ignoring reality.\n"
            f"The Red line (EVT) stays elevated, capturing the 'Fat Tail' structural risk.")
    plt.figtext(0.5, 0.02, note, ha='center', fontsize=11, color='#aaaaaa', style='italic')
    
    plt.subplots_adjust(bottom=0.15)
    plt.savefig('evt_tail_fit_clean.png')
    plt.show()

    # ----------------------------------------------------------------------------------
    # PLOT 2: VaR & CAPITAL GAP (Fixed Overlaps)
    # ----------------------------------------------------------------------------------
    # Calculate Metrics
    alpha = 0.99
    var_normal = norm.ppf(alpha, mu_norm, std_norm)
    n_total = len(losses)
    n_u = len(excesses)
    var_evt = u + (sigma/xi) * ( ((n_total/n_u)*(1-alpha))**(-xi) - 1 )
    es_evt = (var_evt + sigma - xi * u) / (1 - xi)
    
    fig, ax = plt.subplots(figsize=(13, 8))
    
    # Histogram Background
    ax.hist(losses, bins=120, density=True, alpha=0.3, color='gray')
    ax.set_xlim(0, max(losses)*0.5) # Focus on the relevant section
    ax.set_ylim(0, 5) # Controlled height
    
    # Lines
    ax.axvline(var_normal, color='#00ccff', linestyle='--', linewidth=2.5)
    ax.axvline(var_evt, color='#ff9900', linewidth=3)
    ax.axvline(es_evt, color='#ff3333', linestyle=':', linewidth=3)
    
    # Shaded Gap
    ax.axvspan(var_normal, var_evt, color='#ff9900', alpha=0.2)
    
    # Legend with VALUES (Cleaner than putting text on lines)
    legend_elements = [
        plt.Line2D([0], [0], color='#00ccff', lw=2.5, ls='--', label=f'Gaussian VaR (99%): {var_normal:.2f}%'),
        plt.Line2D([0], [0], color='#ff9900', lw=3, label=f'EVT VaR (99%): {var_evt:.2f}%'),
        plt.Line2D([0], [0], color='#ff3333', lw=3, ls=':', label=f'Expected Shortfall (ES): {es_evt:.2f}%'),
        plt.Rectangle((0,0),1,1, fc='#ff9900', alpha=0.2, label='Capital Gap (Uncovered Risk)')
    ]
    ax.legend(handles=legend_elements, loc='upper right', frameon=True, fontsize=11, facecolor='#222222', edgecolor='#444444')
    
    # Annotation for Capital Gap (Placed HIGH above the bars)
    gap_pct = var_evt - var_normal
    mid_point = (var_normal + var_evt) / 2
    
    ax.annotate(
        f'CAPITAL GAP\n(+{gap_pct:.2f}% Reserves Needed)', 
        xy=(mid_point, 0.5), # Pointing to the middle of the gap
        xytext=(mid_point, 3.5), # Text sits high up in empty space
        arrowprops=dict(facecolor='#ff9900', arrowstyle='->', lw=2),
        ha='center', fontsize=11, fontweight='bold', color='#ff9900',
        bbox=dict(boxstyle="round,pad=0.3", fc="#222222", ec="#ff9900", alpha=0.9)
    )

    ax.set_title('Quantifying the "Black Swan": The Capital Gap', fontsize=22, fontweight='bold', color='white', pad=25)
    ax.set_xlabel('Loss Magnitude (%)', fontsize=13, color='#cccccc')
    ax.set_ylabel('Frequency Density', fontsize=13, color='#cccccc')
    
    # Bottom Note
    note2 = (f"INTERPRETATION: Standard models (Blue) stop too early. EVT (Orange) demands higher reserves.\n"
             f"The 'Capital Gap' represents the funds required to survive the 1% extreme event.")
    plt.figtext(0.5, 0.02, note2, ha='center', fontsize=11, color='#aaaaaa', style='italic')
    
    plt.subplots_adjust(bottom=0.15)
    plt.savefig('evt_capital_gap_clean.png')
    plt.show()

if __name__ == "__main__":
    generate_clean_evt_plots()
