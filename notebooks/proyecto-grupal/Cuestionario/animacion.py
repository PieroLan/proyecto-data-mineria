# -*- coding: utf-8 -*-
# Fondo estadístico animado para video (1080p)
# Requisitos: pip install matplotlib numpy
# Además, tener 'ffmpeg' instalado para guardar MP4.

import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FFMpegWriter, FuncAnimation

# ------------------ Parámetros generales ------------------
WIDTH, HEIGHT = 1920, 1080
FPS = 30
DURATION_SEC = 16            # duración total
N_FRAMES = FPS * DURATION_SEC
BG_COLOR = "#0b0f14"         # fondo oscuro elegante
FG_FAINT = "#b8c1d1"         # gris suave para grid y ejes
PALETTE = ["#7aa2f7", "#9ece6a", "#f7768e", "#e0af68"]  # puedes cambiarla
OVERLAY_TEXT = ""            # e.g., "Explora Perú • Data Viz"
SEED = 42
np.random.seed(SEED)

# ------------------ Datos base (sintéticos) ------------------
# Serie "económica" suave + ruido
T = np.linspace(0, 8*math.pi, 1200)
trend = 0.02 * np.arange(T.size)
series = 10*np.sin(0.5*T) + 4*np.sin(1.7*T + 1.2) + trend + np.random.normal(0, 0.6, T.size)

# Puntos (x,y) con correlación variable
N_POINTS = 800
angles = np.linspace(0, 2*math.pi, N_POINTS, endpoint=False)
r = 0.8 + 0.2*np.sin(3*angles)
x_base = r*np.cos(angles) + 0.15*np.random.randn(N_POINTS)
y_base = 0.6*r*np.sin(angles) + 0.15*np.random.randn(N_POINTS)

# Barras (categorías) que "respiran"
cats = np.array([f"C{i}" for i in range(1, 9)])
cat_base = np.abs(np.random.normal(10, 4, size=cats.size))
cat_base = (cat_base / cat_base.max()) * 1.0

# Histograma a partir de mezcla de normales
mix_a = np.random.normal(-1.2, 0.7, 3000)
mix_b = np.random.normal(+1.1, 0.5, 2400)
hist_data = np.concatenate([mix_a, mix_b])

# ------------------ Utilidades de interpolación ------------------
def smoothstep(x):
    # Interpolación suave 0→1
    return 3*x**2 - 2*x**3

def ease_in_out_sine(x):
    return 0.5*(1 - math.cos(math.pi*x))

def loop_phase(frame, seg_frames):
    # regresa fase [0,1] dentro del segmento actual
    return (frame % seg_frames) / seg_frames

# ------------------ Configuración de figura ------------------
plt.rcParams.update({
    "figure.figsize": (WIDTH/100, HEIGHT/100),
    "figure.dpi": 100,
    "axes.facecolor": BG_COLOR,
    "figure.facecolor": BG_COLOR,
    "text.color": FG_FAINT,
    "axes.edgecolor": FG_FAINT,
    "axes.labelcolor": FG_FAINT,
    "xtick.color": FG_FAINT,
    "ytick.color": FG_FAINT,
})

fig, ax = plt.subplots()
fig.subplots_adjust(left=0.05, right=0.98, top=0.92, bottom=0.08)

# Títulos y estilo minimal
title = ax.text(0.01, 0.97, "", transform=ax.transAxes, va="top", ha="left", fontsize=22, alpha=0.85)
overlay = ax.text(0.99, 0.03, OVERLAY_TEXT, transform=ax.transAxes, va="bottom", ha="right", fontsize=18, alpha=0.55)
ax.grid(True, alpha=0.15, linewidth=0.8)

# Elementos que iremos reutilizando
line_obj, = ax.plot([], [], linewidth=2.5, alpha=0.95, solid_capstyle="round")
scatter_obj = ax.scatter([], [], s=8, alpha=0.8)
bars = None  # se creará en su escena
hist_poly = None  # polígono del histograma suavizado

# ------------------ Escenas y tiempos ------------------
# 4 escenas iguales en duración
SCENES = ["LÍNEA", "DISPERSIÓN", "BARRAS", "HISTOGRAMA"]
SEG_FRAMES = N_FRAMES // len(SCENES)

def set_scene_limits(scene):
    if scene == "LÍNEA":
        ax.set_xlim(0, 400)
        ax.set_ylim(series.min()-3, series.max()+3)
        ax.set_xlabel("")
        ax.set_ylabel("")
    elif scene == "DISPERSIÓN":
        ax.set_xlim(-1.8, 1.8)
        ax.set_ylim(-1.5, 1.5)
        ax.set_xlabel("")
        ax.set_ylabel("")
    elif scene == "BARRAS":
        ax.set_xlim(-0.5, len(cats)-0.5)
        ax.set_ylim(0, 1.25)
        ax.set_xlabel("")
        ax.set_ylabel("")
    elif scene == "HISTOGRAMA":
        ax.set_xlim(-3.5, 3.5)
        ax.set_ylim(0, 0.6)
        ax.set_xlabel("")
        ax.set_ylabel("")

def init():
    ax.cla()
    ax.set_facecolor(BG_COLOR)
    ax.grid(True, alpha=0.15, linewidth=0.8)
    return []

def update(frame):
    scene_idx = (frame // SEG_FRAMES) % len(SCENES)
    scene = SCENES[scene_idx]
    local_f = frame % SEG_FRAMES
    u = loop_phase(frame, SEG_FRAMES)          # 0→1 en la escena
    e = ease_in_out_sine(u)                    # easing suave
    ax.cla()
    ax.set_facecolor(BG_COLOR)
    ax.grid(True, alpha=0.15, linewidth=0.8)

    # Título minimal y overlay
    title = ax.text(0.01, 0.97, f"{scene}", transform=ax.transAxes, va="top", ha="left",
                    fontsize=22, alpha=0.85)
    overlay = ax.text(0.99, 0.03, OVERLAY_TEXT, transform=ax.transAxes, va="bottom", ha="right",
                      fontsize=18, alpha=0.55)

    artists = [title, overlay]

    if scene == "LÍNEA":
        set_scene_limits(scene)
        # ventana que avanza sobre la serie
        window = 300
        start = int((len(series)-window) * u)
        start = np.clip(start, 0, len(series)-window-1)
        end = start + window
        y = series[start:end]
        x = np.arange(start, end) - start

        # un ligero cambio de color con el tiempo
        color = PALETTE[0]
        (line_obj,) = ax.plot(x, y, linewidth=2.8, alpha=0.95, color=color)
        # línea fantasmal atrasada para estela
        trail = max(0, start-40)
        if trail < start:
            x2 = np.arange(trail, start) - trail
            y2 = series[trail:start]
            ax.plot(x2, y2, linewidth=1.8, alpha=0.25, color=color)

        # banda de intervalo simulada
        roll = np.convolve(y, np.ones(25)/25, mode="same")
        sd = 0.6 + 0.3*np.sin(2*math.pi*u)
        ax.fill_between(x, roll-sd, roll+sd, alpha=0.10, color=color)

        artists += [line_obj]

    elif scene == "DISPERSIÓN":
        set_scene_limits(scene)
        # rotación lenta + respira el tamaño
        theta = 2*math.pi*u
        rot = np.array([[math.cos(theta), -math.sin(theta)],
                        [math.sin(theta),  math.cos(theta)]])
        pts = np.vstack([x_base, y_base])
        pts_rot = rot @ pts
        size = 10 + 8*np.sin(2*math.pi*u)
        col = PALETTE[1]
        scatter_obj = ax.scatter(pts_rot[0], pts_rot[1], s=size, alpha=0.85, color=col)

        # línea de tendencia "móvil"
        xs = pts_rot[0]
        ys = pts_rot[1]
        m = np.cov(xs, ys)[0,1] / (np.var(xs)+1e-9)
        b = ys.mean() - m*xs.mean()
        xline = np.linspace(xs.min(), xs.max(), 200)
        yline = m*xline + b
        ax.p
