import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import beta

# ----------------------------------------------------------------------------------
# CONFIGURATION (Professional Financial Gray Style)
# ----------------------------------------------------------------------------------
plt.rcdefaults()

# Palette: "Slate & Teal"
BG_COLOR = '#F5F5F5'        
AXIS_COLOR = '#EBEBEB'      
GRID_COLOR = '#FFFFFF'      
TEXT_COLOR = '#2C3E50'      

COLOR_MAIN = '#008F7A'      
COLOR_RISK = '#C0392B'      
COLOR_NEUTRAL = '#34495E'   
COLOR_BAR_START = '#95A5A6' 

# Style Parameters
plt.rcParams['figure.dpi'] = 150
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['DejaVu Serif', 'Georgia', 'Times New Roman']
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False
plt.rcParams['axes.spines.left'] = False 
plt.rcParams['axes.spines.bottom'] = True
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.color'] = GRID_COLOR
plt.rcParams['grid.linewidth'] = 1.5
plt.rcParams['grid.alpha'] = 1.0 
plt.rcParams['axes.facecolor'] = BG_COLOR
plt.rcParams['figure.facecolor'] = BG_COLOR
plt.rcParams['text.color'] = TEXT_COLOR
plt.rcParams['axes.labelcolor'] = TEXT_COLOR
plt.rcParams['xtick.color'] = TEXT_COLOR
plt.rcParams['ytick.color'] = TEXT_COLOR

def generate_risk_architecture_plots_final_v19():
    print("Generando Gráfica 1A: The Bimodal Reality...")
    
    # ----------------------------------------------------------------------------------
    # GRAPH 1A: THE BIMODAL REALITY
    # ----------------------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.set_facecolor(BG_COLOR)
    
    np.random.seed(42)
    data_cured = np.random.beta(0.5, 5, 4000) 
    data_loss = np.random.beta(5, 0.5, 3000) 
    lgd_data = np.concatenate([data_cured, data_loss])
    
    ax.hist(lgd_data, bins=60, density=True, color=COLOR_MAIN, edgecolor=BG_COLOR, alpha=0.8)
    
    ax.annotate('Dominant Mode: Cures\n(Near 0% Loss)', 
                xy=(0.05, 3), xytext=(0.25, 4.5),
                arrowprops=dict(facecolor=COLOR_NEUTRAL, arrowstyle='->', lw=1.5),
                ha='center', color=TEXT_COLOR, fontsize=11, fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.4", fc="white", ec="#dcdcdc", alpha=0.8))

    ax.annotate('Secondary Mode: Write-offs\n(Near 100% Loss)', 
                xy=(0.95, 2.5), xytext=(0.75, 4),
                arrowprops=dict(facecolor=COLOR_NEUTRAL, arrowstyle='->', lw=1.5),
                ha='center', color=TEXT_COLOR, fontsize=11, fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.4", fc="white", ec="#dcdcdc", alpha=0.8))

    ax.set_title('Figure 1A. The Bimodal Distribution of Credit Loss', fontsize=16, fontweight='bold', pad=20, loc='left')
    ax.set_xlabel('Loss Magnitude (LGD)', fontsize=12, labelpad=10)
    ax.set_ylabel('Probability Density', fontsize=12, labelpad=10)
    ax.set_yticks([]) 
    
    plt.tight_layout()
    plt.savefig('graph1a_gray.png')
    plt.show()

    print("Generando Gráfica 1B: The Modeling Solution...")
    
    # ----------------------------------------------------------------------------------
    # GRAPH 1B: THE MODELING SOLUTION
    # ----------------------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.set_facecolor(BG_COLOR)
    
    ax.hist(lgd_data, bins=60, density=True, color='#bdc3c7', edgecolor=BG_COLOR, alpha=0.5)
    
    avg_lgd = np.mean(lgd_data)
    ax.axvline(avg_lgd, color=COLOR_RISK, linewidth=2.5, linestyle='--', label=f'Static Average ({avg_lgd:.0%})')
    
    x = np.linspace(0, 1, 200)
    a, b, loc, scale = beta.fit(lgd_data)
    p = beta.pdf(x, a, b, loc, scale)
    ax.plot(x, p, color=COLOR_MAIN, linewidth=3.5, label='Beta Regression Fit')
    
    ax.annotate('THE "DANGER ZONE"\n(Average assumes losses here,\nbut reality is binary)', 
                xy=(avg_lgd, 0.8),          
                xytext=(avg_lgd + 0.15, 5), 
                arrowprops=dict(edgecolor=COLOR_RISK, arrowstyle='->', lw=1.5),
                ha='left', color=COLOR_RISK, fontsize=11, fontstyle='italic',
                bbox=dict(boxstyle="round,pad=0.4", fc="white", ec=COLOR_RISK, alpha=0.8))

    ax.set_title('Figure 1B. Parametric Fit vs. Static Average', fontsize=16, fontweight='bold', pad=20, loc='left')
    ax.set_xlabel('Loss Magnitude (LGD)', fontsize=12, labelpad=10)
    ax.set_ylim(0, 8) 
    ax.set_yticks([])
    
    legend = ax.legend(loc='upper left', bbox_to_anchor=(0.12, 0.98), frameon=True, fancybox=True, facecolor='white', edgecolor='#dcdcdc', fontsize=10)
    
    plt.tight_layout()
    plt.savefig('graph1b_gray.png')
    plt.show()

    print("Generando Gráfica 2: Capital Release Waterfall...")
    
    # ----------------------------------------------------------------------------------
    # GRAPH 2: THE CAPITAL RELEASE WATERFALL
    # ----------------------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_facecolor(BG_COLOR)
    
    steps = ['Current\nReserves', 'LGD\nOptim.', 'EAD\nPrecision', 'BBM\nIntervention', 'Optimized\nCapital']
    values = [100, -18, -12, -15, 55] 
    running_total = 0
    
    for i, (step, val) in enumerate(zip(steps, values)):
        color = COLOR_BAR_START if i == 0 else (COLOR_MAIN if val < 0 else COLOR_NEUTRAL)
        if i == len(steps)-1: color = COLOR_NEUTRAL
        
        bottom = running_total if i == 0 or i == len(steps)-1 else running_total + val
        height = val if i == 0 or i == len(steps)-1 else abs(val)
        if i == len(steps)-1: bottom = 0
        
        ax.bar(i, height, bottom=bottom, color=color, edgecolor='white', linewidth=1, width=0.6, zorder=3)
        
        if i > 0:
            ax.plot([i-1.3, i+0.3], [running_total, running_total], color=TEXT_COLOR, linestyle='-', linewidth=1, alpha=0.3, zorder=1)
            
        label_text = f"{val}" if i == 0 or i == len(steps)-1 else f"-{abs(val)}"
        label_y = bottom + height + 2 
        if val < 0: label_y = bottom - 5
        
        ax.text(i, label_y, label_text, ha='center', va='center', color=TEXT_COLOR, fontweight='bold', fontsize=11)
        
        if val < 0: running_total += val
        else: running_total = val
    
    ax.annotate('45% Capital Release\n(Direct EBITDA Impact)', 
                xy=(3.75, 20),       
                xytext=(2.0, 20),    
                arrowprops=dict(edgecolor=COLOR_NEUTRAL, facecolor=COLOR_NEUTRAL, arrowstyle='-|>', lw=1.5), 
                ha='center', va='center', color=COLOR_NEUTRAL, fontweight='bold', fontsize=12,
                bbox=dict(boxstyle="square,pad=0.4", fc="white", ec="none", alpha=0.7))
                
    ax.set_title('Figure 2. Economic Capital Optimization Waterfall', fontsize=16, fontweight='bold', pad=20, loc='left')
    ax.set_ylabel('Index (Base 100 = Current Reserves)', fontsize=12, labelpad=10)
    ax.set_xticks(range(len(steps)))
    ax.set_xticklabels(steps, fontsize=11)
    
    # ADJUSTED NOTE POSITION AND MARGINS
    # Increased bottom margin to make space for the note
    plt.subplots_adjust(bottom=0.2)
    # Placed note lower (y=0.05) to clear x-axis labels
    plt.figtext(0.1, 0.05, "Source: Internal Methodology. Values normalized to base 100.", ha="left", fontsize=9, color='#7f8c8d', style='italic')
    
    plt.savefig('graph2_gray.png')
    plt.show()

    print("Generando Gráfica 3: Efficient Frontier...")
    
    # ----------------------------------------------------------------------------------
    # GRAPH 3: THE EFFICIENT FRONTIER
    # ----------------------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_facecolor(BG_COLOR)
    
    np.random.seed(10)
    capital = np.random.normal(50, 10, 200)
    return_val = capital * 0.4 + np.random.normal(0, 3, 200)
    old_cap, old_ret = 70, 25 
    new_cap, new_ret = 45, 38 
    
    ax.scatter(capital, return_val, c='#95a5a6', alpha=0.5, s=40, label='Industry Peers', edgecolors='white', linewidth=0.5)
    
    ax.annotate('', xy=(new_cap, new_ret), xytext=(old_cap, old_ret),
                arrowprops=dict(edgecolor=COLOR_MAIN, arrowstyle='-|>', lw=2.5, mutation_scale=25, connectionstyle="arc3,rad=-0.2"))
                
    ax.scatter(old_cap, old_ret, s=200, c='white', edgecolors=COLOR_RISK, linewidth=2.5, zorder=10, label='Traditional Model')
    ax.scatter(new_cap, new_ret, s=200, c=COLOR_MAIN, edgecolors='white', linewidth=1.5, zorder=10, label='Predictive Architecture')
    
    # Label 1: Inefficient Capital (X=70, Y=15)
    ax.annotate("Inefficient Capital\n(Traditional)", 
                xy=(old_cap, old_ret), 
                xytext=(70, 15), 
                ha='center', color=COLOR_RISK, fontsize=11, fontweight='bold',
                arrowprops=dict(edgecolor=COLOR_RISK, arrowstyle='->', alpha=0.6),
                bbox=dict(boxstyle="square,pad=0.3", fc="white", ec="#dcdcdc", alpha=0.8))
                
    # Label 2: RAROC Optimized (Y=25, X=30)
    ax.annotate("RAROC Optimized\n(Predictive)", 
                xy=(new_cap, new_ret), 
                xytext=(30, 25), 
                ha='right', color=COLOR_MAIN, fontsize=11, fontweight='bold',
                arrowprops=dict(edgecolor=COLOR_MAIN, arrowstyle='->', alpha=0.6),
                bbox=dict(boxstyle="square,pad=0.3", fc="white", ec="#dcdcdc", alpha=0.8))
                
    ax.set_title('Figure 3. The Efficient Frontier Shift', fontsize=16, fontweight='bold', pad=20, loc='left')
    ax.set_xlabel('Economic Capital Usage ($M)', fontsize=12, labelpad=10)
    ax.set_ylabel('Net Income ($M)', fontsize=12, labelpad=10)
    
    legend = ax.legend(loc='upper left', frameon=True, fancybox=True, facecolor='white', edgecolor='#dcdcdc', fontsize=10)
    
    plt.tight_layout()
    plt.savefig('graph3_gray.png')
    plt.show()
    print("¡Todas las gráficas generadas y ajustadas!")

if __name__ == "__main__":
    generate_risk_architecture_plots_final_v19()
