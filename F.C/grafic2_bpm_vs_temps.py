"""
GRÀFICA 2 - Pulsacions (BPM) respecte el temps
================================================
Mostra l'evolució de la freqüència cardíaca instantània al llarg del temps,
calculada amb el mètode manual (pendent) i amb scipy, sense filtre.
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
FS       = N_MAX / DURADA_S

# ── Càrrega ───────────────────────────────────────────────────
df     = pd.read_csv(FITXER, header=0)
senyal = df.iloc[:, COLUMNA].dropna().values[:N_MAX].astype(float)
t      = np.linspace(0, DURADA_S, len(senyal))
dist_min = int(0.3 * FS)

# ── Mètode manual (pendent) ───────────────────────────────────
pendents = np.diff(senyal) / np.diff(t)
mitjana = np.mean(senyal)
pics_manual = []
for i in range(1, len(pendents)):
    if pendents[i - 1] > 0 and pendents[i] < 0 and senyal[i] > mitjana:
        pics_manual.append(i)
pics_manual = np.array(pics_manual)
if len(pics_manual) > 1:
    filtrats = [pics_manual[0]]
    for idx in pics_manual[1:]:
        if idx - filtrats[-1] >= dist_min:
            filtrats.append(idx)
    pics_manual = np.array(filtrats)

# ── Mètode scipy ──────────────────────────────────────────────
umbral = senyal.mean() + 0.5 * (senyal.max() - senyal.mean())
pics_scipy, _ = find_peaks(senyal, height=umbral, distance=dist_min)

# ── BPM instantani ────────────────────────────────────────────
def calc_bpm(pics, t):
    if len(pics) < 2:
        return np.array([]), np.array([])
    T   = np.diff(t[pics])          # FC(ppm) = 60/T
    bpm = 60.0 / T
    t_bpm = t[pics[1:]]             # temps associat a cada interval
    return t_bpm, bpm

t_bpm_manual, bpm_manual = calc_bpm(pics_manual, t)
t_bpm_scipy,  bpm_scipy  = calc_bpm(pics_scipy,  t)

# ── Estil ─────────────────────────────────────────────────────
plt.style.use("dark_background")
BG    = "#0d1117"
GRID  = "#21262d"
VERM  = "#f85149"
VERD  = "#3fb950"
GROC  = "#d29922"

fig, axes = plt.subplots(2, 1, figsize=(16, 10), facecolor=BG)
fig.suptitle("Pulsacions (BPM) respecte el Temps",
             fontsize=15, fontweight="bold", color="white", y=0.98)

def estil(ax, titol):
    ax.set_facecolor(BG)
    ax.set_title(titol, color="white", fontsize=12, fontweight="bold", pad=8)
    ax.set_xlabel("Temps (s)", color="#8b949e", fontsize=9)
    ax.set_ylabel("BPM", color="#8b949e", fontsize=9)
    ax.tick_params(colors="#8b949e", labelsize=8)
    ax.spines[:].set_color(GRID)
    ax.grid(color=GRID, linewidth=0.5, alpha=0.7)

# ── Subplot 1: BPM mètode manual ──
ax = axes[0]
if len(t_bpm_manual) > 0:
    ax.plot(t_bpm_manual, bpm_manual, "o-", color=VERM, linewidth=1.5,
            markersize=6, label=f"BPM instantani (n={len(bpm_manual)})")
    ax.axhline(np.mean(bpm_manual), color=GROC, linewidth=1.2, linestyle="--",
               label=f"BPM mitjà = {np.mean(bpm_manual):.1f}")
    ax.set_ylim(bottom=0)
else:
    ax.text(0.5, 0.5, "No s'han detectat prou pics", ha="center", va="center",
            color="#8b949e", transform=ax.transAxes)
estil(ax, "BPM Instantani — Mètode Manual (FC = 60/T)")
ax.legend(fontsize=9, framealpha=0.3)

# ── Subplot 2: BPM scipy ──
ax = axes[1]
if len(t_bpm_scipy) > 0:
    ax.plot(t_bpm_scipy, bpm_scipy, "o-", color=VERD, linewidth=1.5,
            markersize=6, label=f"BPM instantani (n={len(bpm_scipy)})")
    ax.axhline(np.mean(bpm_scipy), color=GROC, linewidth=1.2, linestyle="--",
               label=f"BPM mitjà = {np.mean(bpm_scipy):.1f}")
    ax.set_ylim(bottom=0)
else:
    ax.text(0.5, 0.5, "No s'han detectat prou pics", ha="center", va="center",
            color="#8b949e", transform=ax.transAxes)
estil(ax, "BPM Instantani — Mètode scipy.signal")
ax.legend(fontsize=9, framealpha=0.3)

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig("grafic2_bpm_vs_temps.png", dpi=150, bbox_inches="tight", facecolor=BG)
print("✅ grafic2_bpm_vs_temps.png guardat")
plt.show()
