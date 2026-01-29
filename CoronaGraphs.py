import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ----------------------------------------------------------------------------------
# CONFIGURATION (Dark Mode - Final English Edition)
# ----------------------------------------------------------------------------------
plt.style.use('dark_background')

# Customizing rcParams for a more spacious, elegant look
plt.rcParams['figure.dpi'] = 100
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False
plt.rcParams['axes.spines.left'] = False 
plt.rcParams['axes.spines.bottom'] = True
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 0.2
plt.rcParams['grid.linestyle'] = '--'

def generate_final_english_graphs():
    # 1. DATA
    countries = ['Spain', 'Italy', 'Switzerland', 'USA', 'Germany', 'France', 'South Korea', 'Brazil', 'Colombia', 'Russia']
    infected = np.array([252, 191, 223, 75, 102, 80, 20, 4, 2, 10])
    dentists = np.array([57, 51, 47, 61, 78, 63, 50, 109, 91, 45])
    nurses = np.array([574, 550, 1700, 900, 1300, 1000, 700, 100, 60, 800])

    # ----------------------------------------------------------------------------------
    # GRAPH 1: THE DENTAL HYPOTHESIS (Maximum Space & Visible Labels)
    # ----------------------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(16, 10))
    
    # Scatter with glow effect
    ax.scatter(dentists, infected, s=500, c='#222222', edgecolor='none', alpha=0.5) 
    # USA specific fix: Ensure USA point is plotted normally, but we handle the label carefully
    ax.scatter(dentists, infected, c=infected, cmap='Reds', s=350, edgecolors='white', linewidth=1.5, alpha=1.0, zorder=10)
    
    # Trendline
    sns.regplot(x=dentists, y=infected, ax=ax, scatter=False, color='#00cc99', 
                line_kws={'linewidth': 2, 'linestyle': '--', 'alpha': 0.6})

    # SPACIOUS LABELING with Manual Offsets
    offsets = {
        'Spain': (0, 25),    
        'Italy': (-30, -25),  
        'Switzerland': (20, 20),     
        'USA': (40, 0),        # Pushed further right to avoid being behind point
        'Germany': (0, 25),   
        'France': (-30, 10),  
        'South Korea': (0, -35), 
        'Brazil': (0, 25),   
        'Colombia': (0, 25),   
        'Russia': (-30, -20)    
    }

    for i, txt in enumerate(countries):
        x_pos, y_pos = dentists[i], infected[i]
        x_off, y_off = offsets.get(txt, (0, 20))
        
        # Ensure label is drawn ON TOP of everything (zorder high)
        ax.annotate(txt, 
                    xy=(x_pos, y_pos), 
                    xytext=(x_off, y_off), textcoords='offset points',
                    ha='center', va='center', color='white', fontweight='bold', fontsize=11,
                    arrowprops=dict(facecolor='#aaaaaa', arrowstyle='-', alpha=0.5),
                    bbox=dict(boxstyle="round,pad=0.4", fc="#1a1a1a", ec="#444444", alpha=1.0),
                    zorder=20) 

    ax.set_title('The Dental Hypothesis: Inverse Correlation', fontsize=26, fontweight='bold', color='white', pad=40)
    ax.set_xlabel('Dentists per 100k Inhabitants', fontsize=14, color='#bbbbbb', labelpad=20)
    ax.set_ylabel('COVID-19 Infections per 100k Inhabitants', fontsize=14, color='#bbbbbb', labelpad=20)
    
    ax.set_xlim(min(dentists)-20, max(dentists)+20)
    ax.set_ylim(min(infected)-40, max(infected)+60)
    
    ax.tick_params(axis='both', which='major', labelsize=11, colors='#888888', pad=10)
    
    plt.figtext(0.5, 0.03, 
                "EMPIRICAL EVIDENCE: Higher oral health culture correlates with lower viral impact.", 
                ha='center', fontsize=12, color='#666666', style='italic')

    plt.subplots_adjust(top=0.85, bottom=0.15, left=0.1, right=0.9)
    plt.savefig('graph1_dental_hypothesis.png')
    plt.show()

    # ----------------------------------------------------------------------------------
    # GRAPH 2: CROSS VALIDATION (With Confidence Intervals & Spacing)
    # ----------------------------------------------------------------------------------
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 9))
    # Increase vertical space for title (top=0.8) and horizontal space (wspace=0.3)
    plt.subplots_adjust(top=0.80, wspace=0.3, bottom=0.15) 
    
    # Plot A: Dentists (With CI)
    sns.regplot(x=dentists, y=infected, ax=ax1, color='#00cc99', scatter_kws={'s': 150, 'edgecolor':'white'}, ci=95)
    ax1.set_title('Dentists (Protective Factor)', fontsize=18, fontweight='bold', color='#aaffdd', pad=25)
    ax1.set_xlabel('Professional Density', fontsize=12, color='#888888', labelpad=15)
    ax1.set_ylabel('Infection Rate', fontsize=12, color='#888888', labelpad=15)
    
    # Plot B: Nurses (With CI)
    sns.regplot(x=nurses, y=infected, ax=ax2, color='#ff5555', scatter_kws={'s': 150, 'edgecolor':'white'}, ci=95)
    ax2.set_title('Nurses (No Clear Correlation)', fontsize=18, fontweight='bold', color='#ffaaaa', pad=25)
    ax2.set_xlabel('Professional Density', fontsize=12, color='#888888', labelpad=15)
    ax2.set_ylabel('') 
    
    # Insights
    ax1.text(0.5, 0.92, "Strong Inverse\nCorrelation", transform=ax1.transAxes, ha='center', color='#00cc99', fontsize=12,
             bbox=dict(boxstyle="round,pad=0.4", fc="#222222", ec="#00cc99", alpha=0.8))
    
    ax2.text(0.5, 0.92, "Scattered Relation\n(Spurious)", transform=ax2.transAxes, ha='center', color='#ff5555', fontsize=12,
             bbox=dict(boxstyle="round,pad=0.4", fc="#222222", ec="#ff5555", alpha=0.8))

    plt.suptitle('Cross-Validation of Variables', fontsize=26, fontweight='bold', color='white')
    
    plt.savefig('graph2_cross_validation.png')
    plt.show()

    # ----------------------------------------------------------------------------------
    # GRAPH 3: BIOLOGICAL MECHANISM (Revised Layout)
    # ----------------------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(16, 9))
    
    dias = np.linspace(0, 14, 200)
    carga_sana = 10 * np.exp(-0.5 * (dias - 2)**2) 
    carga_periodontal = 100 / (1 + np.exp(-1.5 * (dias - 7))) 
    
    # Lines
    ax.plot(dias, carga_sana, color='#00cc99', linewidth=4)
    ax.plot(dias, carga_periodontal, color='#ff3333', linewidth=5)
    
    # Direct Labeling (Above lines as requested)
    # Healthy Patient - Above the green peak
    ax.text(2, 15, "Healthy Patient", color='#00cc99', fontsize=14, fontweight='bold', ha='center',
            bbox=dict(boxstyle="round,pad=0.2", fc="#1a1a1a", ec="none", alpha=0.7))
    
    # Periodontitis Patient - Above the red curve (later stage)
    ax.text(12, 105, "Periodontitis Patient", color='#ff3333', fontsize=14, fontweight='bold', ha='center',
             bbox=dict(boxstyle="round,pad=0.2", fc="#1a1a1a", ec="none", alpha=0.7))

    # Zone styling
    ax.axvspan(0, 5, color='#222222', alpha=0.8) 
    ax.text(2.5, 95, "INCUBATION PHASE", ha='center', color='#666666', fontsize=12)
    
    # Annotations
    ax.annotate('Hygiene Control', 
                xy=(3, 8), xytext=(5, 30),
                arrowprops=dict(facecolor='#00cc99', arrowstyle='->', lw=2, connectionstyle="arc3,rad=-0.2"),
                ha='left', color='#00cc99', fontsize=12, fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.6", fc="#1a1a1a", ec="none"))
    
    # EXPLOSION Label to the RIGHT
    ax.annotate('VIRAL LOAD EXPLOSION', 
                xy=(8, 70), xytext=(12, 60), # Moved text to x=12 (Right side)
                arrowprops=dict(facecolor='#ff3333', arrowstyle='->', lw=2, connectionstyle="arc3,rad=0.2"),
                ha='center', color='#ff3333', fontsize=12, fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.6", fc="#1a1a1a", ec="none"))

    ax.set_title('The Biological Mechanism', fontsize=26, fontweight='bold', color='white', pad=40)
    
    ax.set_yticks([]) 
    ax.set_ylabel('Viral Load (Conceptual)', fontsize=14, color='#888888', labelpad=20)
    ax.set_xlabel('Days since Exposure', fontsize=14, color='#888888', labelpad=20)
    
    ax.grid(axis='x', visible=False)
    ax.grid(axis='y', linestyle='-', alpha=0.1)
    
    plt.subplots_adjust(top=0.85, bottom=0.15, left=0.1, right=0.9)
    plt.savefig('graph3_biological_mechanism.png')
    plt.show()

if __name__ == "__main__":
    generate_final_english_graphs()
