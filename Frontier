import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as sco
import matplotlib.lines as mlines

# ----------------------------------------------------------------------------------
# CONFIGURATION (Dark Mode - High Contrast)
# ----------------------------------------------------------------------------------
plt.style.use('dark_background')

def generate_perfected_plots():
    # 1. DATA SETUP
    projects = ['Alpha (Core)', 'Beta (Cloud)', 'Gamma (AI)', 'Delta (Asia)', 'Epsilon (Security)']
    n_assets = len(projects)
    
    # Expected Returns & Volatility
    mean_returns = np.array([0.08, 0.12, 0.25, 0.18, 0.00]) 
    volatilities = np.array([0.05, 0.10, 0.35, 0.25, 0.05])
    
    # Correlation Matrix
    corr_matrix = np.array([
        [1.0, 0.3, 0.1, 0.2, -0.1], 
        [0.3, 1.0, 0.4, 0.6, 0.0],  
        [0.1, 0.4, 1.0, 0.3, 0.1],  
        [0.2, 0.6, 0.3, 1.0, 0.1],  
        [-0.1, 0.0, 0.1, 0.1, 1.0]  
    ])
    
    cov_matrix = np.outer(volatilities, volatilities) * corr_matrix
    rf = 0.03 

    # ----------------------------------------------------------------------------------
    # OPTIMIZATION
    # ----------------------------------------------------------------------------------
    def portfolio_volatility(weights):
        return np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    
    def portfolio_return(weights):
        return np.sum(mean_returns * weights)
    
    def min_sharpe(weights):
        return -(portfolio_return(weights) - rf) / portfolio_volatility(weights)
    
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bounds = tuple((0, 1) for _ in range(n_assets))
    init_guess = n_assets * [1. / n_assets,]
    
    opt_result = sco.minimize(min_sharpe, init_guess, method='SLSQP', bounds=bounds, constraints=constraints)
    opt_weights = opt_result.x
    
    # CEO's Intuition Portfolio
    ceo_weights = np.array([0.30, 0.066, 0.50, 0.066, 0.066]) 
    
    # Calculate Metrics
    opt_ret = portfolio_return(opt_weights)
    opt_vol = portfolio_volatility(opt_weights)
    ceo_ret = portfolio_return(ceo_weights)
    ceo_vol = portfolio_volatility(ceo_weights)

    # ----------------------------------------------------------------------------------
    # PLOT 1: THE EFFICIENT FRONTIER (Fixed Labels)
    # ----------------------------------------------------------------------------------
    fig_ef, ax_ef = plt.subplots(figsize=(14, 8))
    
    # Background Cloud
    num_ports = 5000
    all_vol = np.zeros(num_ports)
    all_ret = np.zeros(num_ports)
    all_sharpe = np.zeros(num_ports)
    
    np.random.seed(42)
    for i in range(num_ports):
        w = np.random.random(n_assets)
        w /= np.sum(w)
        all_ret[i] = np.sum(mean_returns * w)
        all_vol[i] = np.sqrt(np.dot(w.T, np.dot(cov_matrix, w)))
        all_sharpe[i] = (all_ret[i] - rf) / all_vol[i]
        
    sc = ax_ef.scatter(all_vol, all_ret, c=all_sharpe, cmap='viridis', alpha=0.4, s=15, edgecolors='none')
    cbar = plt.colorbar(sc, ax=ax_ef)
    cbar.set_label('Sharpe Ratio (Efficiency)', rotation=270, labelpad=20, color='#dddddd')
    cbar.ax.yaxis.set_tick_params(color='#dddddd')
    plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='#bbbbbb')
    
    # Markers
    ax_ef.scatter(ceo_vol, ceo_ret, color='#ff3333', s=250, marker='X', label="CEO's Intuition", zorder=10, edgecolors='white', linewidth=1.5)
    ax_ef.scatter(opt_vol, opt_ret, color='#00ff00', s=300, marker='*', label="Algorithmic Optimal", zorder=10, edgecolors='white', linewidth=1.5)
    
    # --- FIXED ANNOTATIONS ---
    
    # 1. CEO Annotation (Moved slightly right to be safe)
    ax_ef.annotate('Sub-optimal', 
                   xy=(ceo_vol, ceo_ret), 
                   xytext=(ceo_vol + 0.04, ceo_ret - 0.02), # Shifted right
                   arrowprops=dict(facecolor='#ff3333', arrowstyle='->', lw=1.5),
                   color='#ffcccc', fontweight='bold', 
                   bbox=dict(boxstyle="round,pad=0.4", fc="#222222", ec="#ff3333", alpha=0.9))
    
    # 2. Efficient Frontier Annotation (MOVED TO RIGHT OF POINT)
    # Previosuly it was to the left (negative offset), causing axis overlap.
    # Now we place it at opt_vol + 0.06 (Right side)
    ax_ef.annotate('Efficient Frontier\n(Max Sharpe)', 
                   xy=(opt_vol, opt_ret), 
                   xytext=(opt_vol + 0.06, opt_ret - 0.01), # Placed to the RIGHT
                   arrowprops=dict(facecolor='#00ff00', arrowstyle='->', lw=1.5),
                   color='#ccffcc', fontweight='bold', 
                   bbox=dict(boxstyle="round,pad=0.4", fc="#222222", ec="#00ff00", alpha=0.9))

    ax_ef.set_title('The Efficient Frontier: Transforming Strategy into Math', fontsize=22, fontweight='bold', color='white', pad=25)
    ax_ef.set_xlabel('Portfolio Risk (Volatility)', fontsize=13, color='#cccccc')
    ax_ef.set_ylabel('Expected Return (ROI)', fontsize=13, color='#cccccc')
    
    # Ensure Axis Limits give enough breathing room
    ax_ef.set_xlim(left=0) # Start at 0 to see the gap
    
    ax_ef.grid(color='gray', linestyle=':', linewidth=0.5, alpha=0.3)
    
    legend = ax_ef.legend(loc='lower right', frameon=True, fontsize=12, facecolor='#222222', edgecolor='#555555')
    for text in legend.get_texts(): text.set_color("white")
    
    plt.subplots_adjust(bottom=0.15)
    plt.savefig('efficient_frontier_perfect.png')
    plt.show()

    # ----------------------------------------------------------------------------------
    # PLOT 2: DUMBBELL PLOT (Maintained as requested)
    # ----------------------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(14, 8))
    
    ceo_pct = ceo_weights * 100
    opt_pct = opt_weights * 100
    y_pos = np.arange(len(projects))
    
    for i in range(len(projects)):
        ax.hlines(y=i, xmin=min(ceo_pct[i], opt_pct[i]), xmax=max(ceo_pct[i], opt_pct[i]), 
                  color='#666666', alpha=0.6, linewidth=3, zorder=1)
        
        if abs(opt_pct[i] - ceo_pct[i]) > 1:
            mid_point = (ceo_pct[i] + opt_pct[i]) / 2
            marker = '>' if opt_pct[i] > ceo_pct[i] else '<'
            color = '#00ff00' if opt_pct[i] > ceo_pct[i] else '#ff5555' 
            ax.plot(mid_point, i, marker=marker, color=color, markersize=8, zorder=2)

    ax.scatter(ceo_pct, y_pos, color='#ff5555', s=200, label="CEO's Intuition", zorder=3, edgecolors='white', marker='X')
    ax.scatter(opt_pct, y_pos, color='#00ff00', s=200, label="Algorithmic Optimal", zorder=3, edgecolors='white', marker='o')
    
    for i in range(len(projects)):
        ax.annotate(f'{ceo_pct[i]:.1f}%', xy=(ceo_pct[i], i), xytext=(0, -25), textcoords="offset points",
                    ha='center', va='top', color='#ffaaaa', fontsize=10, fontweight='bold',
                    bbox=dict(boxstyle="round,pad=0.2", fc="#222222", ec="none", alpha=0.7))
        
        ax.annotate(f'{opt_pct[i]:.1f}%', xy=(opt_pct[i], i), xytext=(0, 25), textcoords="offset points",
                    ha='center', va='bottom', color='#aaffdd', fontsize=10, fontweight='bold',
                    bbox=dict(boxstyle="round,pad=0.2", fc="#222222", ec="none", alpha=0.7))
        
        if "Delta" in projects[i]:
             ax.annotate('REJECTED', xy=(opt_pct[i], i), xytext=(opt_pct[i] + 8, i),
                        arrowprops=dict(facecolor='#ff5555', arrowstyle='->'),
                        ha='left', va='center', color='#ff5555', fontsize=10, fontweight='bold')

    ax.set_yticks(y_pos)
    ax.set_yticklabels(projects, fontsize=14, color='white', fontweight='bold')
    ax.set_xlabel('Capital Allocation (% of Budget)', fontsize=13, color='#cccccc')
    ax.set_title('Strategic Shift: From Intuition to Algorithm', fontsize=22, fontweight='bold', color='white', pad=25)
    
    legend = ax.legend(loc='upper right', frameon=True, fontsize=12, facecolor='#222222', edgecolor='#555555')
    for text in legend.get_texts(): text.set_color("white")
    
    ax.grid(axis='x', color='gray', linestyle='--', linewidth=0.5, alpha=0.3)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_color('#555555')
    ax.tick_params(axis='x', colors='#cccccc')
    
    plt.figtext(0.5, 0.02, 
                "VISUALIZATION: The 'Dumbbell Plot' highlights the magnitude of the strategic correction.\nNotice the complete rejection of 'Delta' (Redundant) and the stabilization of 'Gamma'.", 
                ha='center', fontsize=11, color='#aaaaaa', style='italic')
    
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.15)
    plt.savefig('dumbbell_allocation_final.png')
    plt.show()

if __name__ == "__main__":
    generate_perfected_plots()
