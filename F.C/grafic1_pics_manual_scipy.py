"""
GRÀFICA 1 - Detecció de pics: mètode manual (pendent) vs scipy.signal
======================================================================
Mostra els dos mètodes de detecció de pics en subplots separats.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# ── Configuració ──────────────────────────────────────────────
FITXER   = "dades_pulsacions2.csv"
COLUMNA  = 1
N_MAX    = 10_000
DURADA_S = 20.0
FS       = N_MAX / DURADA_S   # 500 Hz

# ── Càrrega de dades ──────────────────────────────────────────
df     = pd.read_csv(FITXER, header=0)
senyal = df.iloc[:, COLUMNA].dropna().values[:N_MAX].astype(float)
t      = np.linspace(0, DURADA_S, len(senyal))
N      = len(senyal)

# ══════════════════════════════════════════════════════════════
# MÈTODE 1: Detecció manual per canvi de pendent (p = Δy/Δx)
# ══════════════════════════════════════════════════════════════
pendents = np.diff(senyal) / np.diff(t)   # p = (y2-y1)/(x2-x1)

pics_manual = []
for i in range(1, len(pendents)):
    if pendents[i - 1] > 0 and pendents[i] < 0:   # pendent + → pendent -
        pics_manual.append(i)

pics_manual = np.array(pics_manual)

# Filtre per distància mínima entre pics (≥ 300 ms)
dist_min = int(0.3 * FS)
if len(pics_manual) > 1:
    filtrats = [pics_manual[0]]
    for idx in pics_manual[1:]:
        if idx - filtrats[-1] >= dist_min:
            filtrats.append(idx)
    pics_manual = np.array(filtrats)

# Càlcul BPM mètode manual
if len(pics_manual) >= 2:
    T_manual  = np.diff(t[pics_manual])          # període entre pics (s)
    bpm_manual = 60.0 / T_manual
    bpm_mitja_manual = np.mean(bpm_manual)
else:
    bpm_mitja_manual = None

# ══════════════════════════════════════════════════════════════
# MÈTODE 2: Detecció amb scipy find_peaks
# ══════════════════════════════════════════════════════════════
umbral = senyal.mean() + 0.5 * (senyal.max() - senyal.mean())
pics_scipy, _ = find_peaks(senyal, height=umbral, distance=dist_min)

if len(pics_scipy) >= 2:
    T_scipy   = np.diff(t[pics_scipy])
    bpm_scipy = 60.0 / T_scipy
    bpm_mitja_scipy = np.mean(bpm_scipy)
else:
    bpm_mitja_scipy = None

# ── Estil ─────────────────────────────────────────────────────
plt.style.use("dark_background")
BG   = "#0d1117"
GRID = "#21262d"
BLAU = "#58a6ff"
VERM = "#f85149"
VERD = "#3fb950"

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 10), facecolor=BG)
fig.suptitle("Detecció de Pics: Mètode canvi de pendent vs scipy.signal",
             fontsize=15, fontweight="bold", color="white", y=0.98)

def estil(ax, titol):
    ax.set_facecolor(BG)
    ax.set_title(titol, color="white", fontsize=12, fontweight="bold", pad=8)
    ax.set_xlabel("Temps (s)", color="#8b949e", fontsize=9)
    ax.set_ylabel("Amplitud", color="#8b949e", fontsize=9)
    ax.tick_params(colors="#8b949e", labelsize=8)
    ax.spines[:].set_color(GRID)
    ax.grid(color=GRID, linewidth=0.5, alpha=0.7)

# ── Subplot 1: mètode manual ──
ax1.plot(t, senyal, color=BLAU, linewidth=0.7, alpha=0.85, label="Senyal")
if len(pics_manual) > 0:
    ax1.plot(t[pics_manual], senyal[pics_manual], "v", color=VERM,
             markersize=8, zorder=5,
             label=f"Pics ({len(pics_manual)})")
bpm_txt = f" | BPM mitjà = {bpm_mitja_manual:.1f}" if bpm_mitja_manual else ""
estil(ax1, f"Mètode canvi de pendent Δy/Δx{bpm_txt}")
ax1.legend(fontsize=9, framealpha=0.3, loc="upper left")

# ── Subplot 2: scipy ──
ax2.plot(t, senyal, color=BLAU, linewidth=0.7, alpha=0.85, label="Senyal")
if len(pics_scipy) > 0:
    ax2.plot(t[pics_scipy], senyal[pics_scipy], "v", color=VERD,
             markersize=8, zorder=5,
             label=f"Pics ({len(pics_scipy)})")
ax2.axhline(umbral, color="#6e7681", linewidth=0.8, linestyle="--",
            label=f"Umbral ({umbral:.2f})")
bpm_txt2 = f" | BPM mitjà = {bpm_mitja_scipy:.1f}" if bpm_mitja_scipy else ""
estil(ax2, f"Mètode scipy.signal find_peaks{bpm_txt2}")
ax2.legend(fontsize=9, framealpha=0.3, loc="upper left")

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig("grafic1_pics_manual_scipy.png", dpi=150, bbox_inches="tight", facecolor=BG)
print("✅ grafic1_pics_manual_scipy.png guardat")
plt.show()
