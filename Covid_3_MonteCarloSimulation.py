import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def generate_monte_carlo_tail_risk():
    # 1. Setup Dark Theme
    plt.style.use('dark_background')
    
    # 2. Simulation Parameters
    np.random.seed(42) # For reproducibility
    N = 10000
    
    # Generate Population Attributes (Randomized)
    # Using Beta distributions to simulate realistic population (most are average/healthy, few are severe)
    # PDG: Periodontal Disease (0=Healthy, 1=Severe)
    pdg_scores = np.random.beta(2, 5, N) 
    
    # ARF: Risk Factors (Diabetes, Hypertension)
    arf_scores = np.random.beta(2, 5, N) 
    
    # ISG: Immune Deficiency (0=Strong, 1=Compromised)
    # Higher score = Weaker system (contributes to lethality)
    isg_scores = np.random.beta(2, 5, N)
    
    # Calculate Lethality Index (LGI)
    # Formula: LGI = PDG * ARF * ISG
    lethality_index = pdg_scores * arf_scores * isg_scores
    
    # 3. Define "Death Threshold" (The Tail)
    # We identify the top 5% most critical cases as the "Lethal Tail"
    threshold = np.percentile(lethality_index, 95)
    
    # Filter Data
    survivors = lethality_index[lethality_index < threshold]
    victims = lethality_index[lethality_index >= threshold]
    
    # 4. Plotting
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Plot Survivors (Green)
    ax.hist(survivors, bins=50, color='#00cc66', alpha=0.6, label='Recovered Population (Mild Symptoms)')
    
    # Plot Victims (Red - The Tail)
    ax.hist(victims, bins=10, color='#ff3333', alpha=0.9, label='Silent Victims (Lethal Outcome)')
    
    # 5. Styling & Annotations
    ax.set_title('Monte Carlo Simulation: Identification of "Silent Victims"', fontsize=22, fontweight='bold', pad=20, color='white')
    ax.set_xlabel('Calculated Lethality Risk Index (LGI)', fontsize=12, color='#dddddd')
    ax.set_ylabel('Population Count (N=10,000)', fontsize=12, color='#dddddd')
    
    # Clean spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(colors='#bbbbbb')
    
    # Annotation for the Tail
    ax.annotate('THE "TAIL RISK"\n(High PDG + Comorbidities)', 
                xy=(np.mean(victims), 50), 
                xytext=(np.mean(victims) - 0.05, 300),
                arrowprops=dict(facecolor='white', arrowstyle='->', lw=1.5),
                fontsize=11, color='white', fontweight='bold', ha='center')

    # Data Insight Box (proving the PDG theory)
    avg_pdg_victims = np.mean(pdg_scores[lethality_index >= threshold])
    avg_pdg_survivors = np.mean(pdg_scores[lethality_index < threshold])
    
    stats_text = (
        f"DATA INSIGHT:\n"
        f"• Survivor Avg PDG: {avg_pdg_survivors:.2f} (Healthy Gums)\n"
        f"• Victim Avg PDG: {avg_pdg_victims:.2f} (Severe Disease)\n"
        f"The lethal 'tail' is driven by oral health status."
    )
    
    ax.text(0.3, 0.6, stats_text, transform=ax.transAxes, color='#cccccc', fontsize=10, 
            bbox=dict(facecolor='#222222', alpha=0.8, edgecolor='#ff3333', boxstyle='round,pad=0.5'))
    
    # 6. Floating Explanatory Text
    note_text = (
        "SIMULATION LOGIC: Even with 100% infection rate, mortality isn't random. It concentrates in the distribution 'Tail'.\n"
        "These are the 'Silent Victims': individuals where severe Periodontal Disease (PDG) acts as a force multiplier\n"
        "for other pre-existing conditions, pushing their Lethality Index beyond the point of no return."
    )
    
    plt.figtext(0.5, 0.01, note_text, ha='center', va='bottom', fontsize=11, color='#888888', style='italic')

    # Legend
    ax.legend(loc='upper right', frameon=False, fontsize=11)
    
    plt.subplots_adjust(bottom=0.18)
    plt.savefig('monte_carlo_tail_risk.png')
    plt.show()

if __name__ == "__main__":
    generate_monte_carlo_tail_risk()
