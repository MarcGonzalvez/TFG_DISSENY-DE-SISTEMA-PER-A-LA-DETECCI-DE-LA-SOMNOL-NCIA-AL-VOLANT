"""
GRÀFICA 3 - Filtre passa banda (0.5 Hz – 2.5 Hz) i efecte sobre BPM
=====================================================================
Compara el senyal original vs filtrat, i els BPM resultants amb
els dos mètodes de detecció de pics.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks, butter, filtfilt

# ── Configuració ──────────────────────────────────────────────
FITXER   = "dades_pulsacions2.csv"
COLUMNA  = 1
N_MAX    = 10_000
DURADA_S = 20.0
FS       = N_MAX / DURADA_S   # 500 Hz

F_LOW    = 0.5    # Hz — freqüència inferior de tall
F_HIGH   = 2.5   # Hz — freqüència superior de tall

# ── Càrrega ───────────────────────────────────────────────────
df     = pd.read_csv(FITXER, header=0)
senyal = df.iloc[:, COLUMNA].dropna().values[:N_MAX].astype(float)
t      = np.linspace(0, DURADA_S, len(senyal))
dist_min = int(0.3 * FS)

# ── Filtre Butterworth passa banda ────────────────────────────
nyq = FS / 2.0
b, a = butter(1, [F_LOW / nyq, F_HIGH / nyq], btype="band")
senyal_filtrat = filtfilt(b, a, senyal)

# ── Detecció de pics en senyal filtrat ────────────────────────
# Mètode manual (pendent)
pendents = np.diff(senyal_filtrat) / np.diff(t)
mitjana_f = np.mean(senyal_filtrat)
pics_manual = []
for i in range(1, len(pendents)):
    if pendents[i - 1] > 0 and pendents[i] < 0 and senyal_filtrat[i] > mitjana_f:
        pics_manual.append(i)
pics_manual = np.array(pics_manual)
if len(pics_manual) > 1:
    filtrats = [pics_manual[0]]
    for idx in pics_manual[1:]:
        if idx - filtrats[-1] >= dist_min:
            filtrats.append(idx)
    pics_manual = np.array(filtrats)

# Mètode scipy
umbral_f = senyal_filtrat.mean() + 0.5 * (senyal_filtrat.max() - senyal_filtrat.mean())
pics_scipy, _ = find_peaks(senyal_filtrat, height=umbral_f, distance=dist_min)

# ── BPM instantani ────────────────────────────────────────────
def calc_bpm(pics, t):
    if len(pics) < 2:
        return np.array([]), np.array([])
    bpm   = 60.0 / np.diff(t[pics])
    t_bpm = t[pics[1:]]
    return t_bpm, bpm

t_bpm_manual, bpm_manual = calc_bpm(pics_manual, t)
t_bpm_scipy,  bpm_scipy  = calc_bpm(pics_scipy,  t)

# ── Estil ─────────────────────────────────────────────────────
plt.style.use("dark_background")
BG    = "#0d1117"
GRID  = "#21262d"
BLAU  = "#58a6ff"
TARONJA = "#e3b341"
VERM  = "#f85149"
VERD  = "#3fb950"
GROC  = "#d29922"
VIOLA = "#bc8cff"

fig, axes = plt.subplots(3, 1, figsize=(16, 14), facecolor=BG)
fig.suptitle(f"Filtre Passa Banda ({F_LOW}–{F_HIGH} Hz) i Efecte sobre BPM",
             fontsize=15, fontweight="bold", color="white", y=0.99)

def estil(ax, titol, ylabel="Amplitud"):
    ax.set_facecolor(BG)
    ax.set_title(titol, color="white", fontsize=12, fontweight="bold", pad=8)
    ax.set_xlabel("Temps (s)", color="#8b949e", fontsize=9)
    ax.set_ylabel(ylabel, color="#8b949e", fontsize=9)
    ax.tick_params(colors="#8b949e", labelsize=8)
    ax.spines[:].set_color(GRID)
    ax.grid(color=GRID, linewidth=0.5, alpha=0.7)

# ── Subplot 1: original vs filtrat ──
ax = axes[0]
ax.plot(t, senyal, color=BLAU, linewidth=0.5, alpha=0.5, label="Senyal original")
ax.plot(t, senyal_filtrat, color=TARONJA, linewidth=1.0, label="Senyal filtrat (passa banda)")
estil(ax, f"Senyal Original vs Filtrat (Butterworth 1r ordre, {F_LOW}–{F_HIGH} Hz)")
ax.legend(fontsize=9, framealpha=0.3)

# ── Subplot 2: senyal filtrat + pics ──
ax = axes[1]
ax.plot(t, senyal_filtrat, color=TARONJA, linewidth=0.8, alpha=0.9, label="Senyal filtrat")
if len(pics_manual) > 0:
    ax.plot(t[pics_manual], senyal_filtrat[pics_manual], "v", color=VERM,
            markersize=7, zorder=5, label=f"Pics manual ({len(pics_manual)})")
if len(pics_scipy) > 0:
    ax.plot(t[pics_scipy], senyal_filtrat[pics_scipy], "^", color=VERD,
            markersize=6, zorder=5, label=f"Pics scipy ({len(pics_scipy)})")
ax.axhline(umbral_f, color="#6e7681", linewidth=0.8, linestyle="--",
           label=f"Umbral scipy ({umbral_f:.3f})")
estil(ax, "Pics Detectats sobre Senyal Filtrat")
ax.legend(fontsize=9, framealpha=0.3)

# ── Subplot 3: BPM dels dos mètodes sobre filtrat ──
ax = axes[2]
if len(t_bpm_manual) > 0:
    ax.plot(t_bpm_manual, bpm_manual, "o-", color=VERM, linewidth=1.5,
            markersize=6, label=f"BPM manual — mitjà: {np.mean(bpm_manual):.1f} bpm")
if len(t_bpm_scipy) > 0:
    ax.plot(t_bpm_scipy, bpm_scipy, "s-", color=VERD, linewidth=1.5,
            markersize=5, label=f"BPM scipy  — mitjà: {np.mean(bpm_scipy):.1f} bpm")
if len(t_bpm_manual) > 0:
    ax.axhline(np.mean(bpm_manual), color=VERM, linewidth=0.8, linestyle="--", alpha=0.5)
if len(t_bpm_scipy) > 0:
    ax.axhline(np.mean(bpm_scipy),  color=VERD, linewidth=0.8, linestyle="--", alpha=0.5)
ax.set_ylim(bottom=0)
estil(ax, "BPM Instantani sobre Senyal Filtrat (FC = 60/T)", ylabel="BPM")
ax.legend(fontsize=9, framealpha=0.3)

plt.tight_layout(rect=[0, 0, 1, 0.97])
plt.savefig("grafic3_passabanda.png", dpi=150, bbox_inches="tight", facecolor=BG)
print("✅ grafic3_passabanda.png guardat")
plt.show()
