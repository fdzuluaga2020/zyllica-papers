import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def generate_landscape_heatmap():
    # 1. Setup Dark Theme
    plt.style.use('dark_background')
    
    # 2. Define Data
    exposure_levels = np.linspace(0, 1, 100)
    periodontal_health = np.linspace(0, 1, 100)
    X, Y = np.meshgrid(exposure_levels, periodontal_health)
    
    # Risk Calculation
    risk_matrix = X * Y
    
    # 3. Create Plot (LANDSCAPE orientation)
    # figsize=(12, 7) creates the wide format
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Heatmap
    im = ax.imshow(risk_matrix, 
                   extent=[0, 100, 0, 100], 
                   origin='lower', 
                   cmap='Reds', 
                   aspect='auto',
                   alpha=0.85)
    
    # 4. Labels & Styling
    ax.set_title('COVID-19 Risk Model: The "Death Zone"', fontsize=22, fontweight='bold', pad=20, color='white')
    ax.set_xlabel('Social Exposure Level (%)', fontsize=12, color='#dddddd')
    ax.set_ylabel('Periodontal Disease Severity (%)', fontsize=12, color='#dddddd')
    
    # Ticks styling
    ax.tick_params(axis='both', colors='#bbbbbb')
    
    # Colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Estimated Lethality Probability', rotation=270, labelpad=25, color='#dddddd', fontsize=11)
    cbar.ax.yaxis.set_tick_params(color='#dddddd')
    plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='#bbbbbb')
    
    # 5. Visual Annotations
    # "Death Zone"
    ax.text(98, 96, 'DEATH ZONE', 
             color='white', ha='right', va='top', 
             fontweight='bold', fontsize=16,
             bbox=dict(facecolor='#ff0000', alpha=0.4, edgecolor='none', boxstyle='round,pad=0.4'))
    
    ax.text(98, 86, 'Max Exposure +\nCritical Oral Health', 
             color='#ffcccc', ha='right', va='top', fontsize=11, style='italic')

    # "Safe Zone"
    ax.text(2, 4, 'SAFE ZONE', 
             color='#ccffcc', ha='left', va='bottom', 
             fontweight='bold', fontsize=14)
    
    # Grid
    ax.grid(color='gray', linestyle=':', linewidth=0.5, alpha=0.2)
    
    # 6. Explanatory Note (FLOATING TEXT - No Box)
    note_text = (
        "INTERPRETATION: High Social Exposure (X-axis) becomes lethal mainly when intersected with poor Periodontal Health (Y-axis).\n"
        "Improving oral health reduces risk significantly, even if exposure remains high."
    )
    
    # Using plt.figtext without bbox creates the "floating" effect
    plt.figtext(0.5, 0.02, note_text, ha='center', va='bottom', fontsize=11, color='#888888', style='italic')

    # Adjust layout to make room for text at bottom
    plt.subplots_adjust(bottom=0.15)
    
    plt.show()

if __name__ == "__main__":
    generate_landscape_heatmap()
