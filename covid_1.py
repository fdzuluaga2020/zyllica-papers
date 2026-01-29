import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager
import matplotlib.ticker as ticker

# --- 1. CONFIGURACIÓN DE ESTÉTICA "ZYLLICA PREMIUM" ---
COLOR_BG = '#0E1117'
COLOR_PLOT = '#0E1117'
COLOR_TEXT = '#E0E0E0'
COLOR_GRID = '#2A2D33'
COLOR_STRATEGY_A = '#FF6B6B' 
COLOR_STRATEGY_B = '#4BF4A0' 

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['DejaVu Serif', 'Liberation Serif', 'Times New Roman']
plt.rcParams['axes.facecolor'] = COLOR_PLOT
plt.rcParams['figure.facecolor'] = COLOR_BG
plt.rcParams['text.color'] = COLOR_TEXT
plt.rcParams['axes.labelcolor'] = COLOR_TEXT
plt.rcParams['xtick.color'] = COLOR_TEXT
plt.rcParams['ytick.color'] = COLOR_TEXT
plt.rcParams['grid.color'] = COLOR_GRID
plt.rcParams['axes.edgecolor'] = COLOR_GRID

# --- 2. DATOS ---
def calculate_risk(IF, EL, ER, PDG, ARF, ISG):
    return IF * (EL * ER) * (PDG * ARF * ISG)

intensity = np.linspace(0, 0.99, 100) 

risk_lockdown = calculate_risk(IF=0.8, EL=1.0 - intensity, ER=0.5, PDG=0.8, ARF=0.5, ISG=0.5)
risk_clinical = calculate_risk(IF=0.8, EL=0.9, ER=0.5, PDG=1.0 - intensity, ARF=0.5, ISG=0.5)

# --- 3. PLOTTING (SEMI-LOG) ---
fig, ax = plt.subplots(figsize=(12, 7))

# Escala Logarítmica
ax.set_yscale('log')

# Líneas
ax.plot(intensity * 100, risk_lockdown, color=COLOR_STRATEGY_A, linewidth=6, alpha=0.15)
ax.plot(intensity * 100, risk_lockdown, label='Strategy A: Strict Lockdown (Reduces Exposure)', 
        color=COLOR_STRATEGY_A, linewidth=2.5, linestyle='--')

ax.plot(intensity * 100, risk_clinical, color=COLOR_STRATEGY_B, linewidth=6, alpha=0.15)
ax.plot(intensity * 100, risk_clinical, label='Strategy B: Periodontal Care (Reduces Lethality)', 
        color=COLOR_STRATEGY_B, linewidth=2.5)

# --- 4. ESTILIZADO FINO ---

ax.set_title('Public Policy Sensitivity Analysis: COVID-19 (Log Scale)', 
             fontsize=20, fontweight='bold', pad=25, color='white')

# Fuentes Sans-Serif para los ejes (más legible)
font_labels = {'family': 'sans-serif', 'weight': 'normal', 'size': 11}
ax.set_xlabel('Policy Implementation Intensity (%)', fontdict=font_labels, labelpad=15) # Más padding aquí
ax.set_ylabel('Expected Lethal Victims Index (Log Scale)', fontdict=font_labels, labelpad=10)

# Formato limpio de números (0.01 en vez de 10^-2)
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: '{:g}'.format(y)))
ax.yaxis.set_minor_formatter(ticker.NullFormatter()) 

# Límites y Bordes
ax.set_ylim(0.001, 0.2) 
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_linewidth(0.5)
ax.spines['bottom'].set_linewidth(0.5)

# Grid
ax.grid(True, which="both", linestyle='--', linewidth=0.5, alpha=0.3)

# Leyenda
legend = ax.legend(frameon=False, fontsize=11, loc='upper right')
for text in legend.get_texts():
    text.set_color(COLOR_TEXT)

# Anotación (Flecha)
ax.annotate('Critical Divergence:\nGap widens significantly\nat higher intensities', 
            xy=(80, 0.008), xytext=(45, 0.003),
            arrowprops=dict(arrowstyle="->", color=COLOR_TEXT, connectionstyle="arc3,rad=-0.2", linewidth=1.5),
            color=COLOR_TEXT, fontsize=10, style='italic', family='sans-serif')

# --- 5. NOTA INTERPRETATIVA (Sin líneas molestas) ---
note_text = (
    "INTERPRETATION (LOG SCALE): This chart utilizes a semi-logarithmic scale to visualize the rate of risk reduction. "
    "The curvature indicates that while both strategies are linear in nature, Strategy B (Clinical Intervention)\n"
    "maintains a superior safety margin relative to Strategy A as policy intensity increases toward 100%."
)

# Ajustamos margins (bottom=0.20) para dar espacio real entre el eje X y la nota
plt.subplots_adjust(bottom=0.20, top=0.88)

plt.figtext(0.5, 0.02, note_text, ha="center", fontsize=9, family='sans-serif', color="#888888", style='italic')

plt.show()
