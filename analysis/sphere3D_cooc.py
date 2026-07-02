import pandas as pd
from pathlib import Path
import sqlite3
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress
from mpl_toolkits.mplot3d import Axes3D
import plotly.graph_objects as go


tab=sqlite3.connect("../output.db")

 
# =====================================================
# RECUPERATION DONNEES (SQL déjà exécuté avant)
# =====================================================
query_cooc=open("./requetes/paires_issues_repos.sql").read()
query_errors=open("./requetes/list_issues.sql").read()
cooc = pd.read_sql_query(query_cooc, tab)
errors = pd.read_sql_query(query_errors, tab)

# =====================================================
# TOP 20 LIENS LES PLUS FORTS
# =====================================================

filtered = cooc.nlargest(20, "cooccurrence_count")

print(f"{len(filtered)} liens affichés sur {len(cooc)}")

# =====================================================
# POSITIONNEMENT DES ERREURS SUR UNE SPHERE
# =====================================================

n = len(errors)

indices = np.arange(n)

phi = np.arccos(1 - 2 * (indices + 0.5) / n)
theta = np.pi * (1 + np.sqrt(5)) * indices

x = np.sin(phi) * np.cos(theta)
y = np.sin(phi) * np.sin(theta)
z = np.cos(phi)

positions = {}

for i, (_, row) in enumerate(errors.iterrows()):
    positions[row["error_id"]] = (x[i], y[i], z[i])

# =====================================================
# FONCTION ARC (BEZIER 3D)
# =====================================================

def generate_arc(p1, p2, radius_factor=1.3, n_points=50):

    p1 = np.array(p1)
    p2 = np.array(p2)

    mid = (p1 + p2) / 2
    mid = mid / np.linalg.norm(mid)
    mid *= radius_factor

    t = np.linspace(0, 1, n_points)
    curve = []

    for u in t:
        point = (1-u)**2 * p1 + 2*(1-u)*u * mid + u**2 * p2
        curve.append(point)

    return np.array(curve)

# =====================================================
# FIGURE
# =====================================================

fig = plt.figure(figsize=(14, 12))
ax = fig.add_subplot(111, projection='3d')

# =====================================================
# SPHERE
# =====================================================

u = np.linspace(0, 2*np.pi, 40)
v = np.linspace(0, np.pi, 20)

xs = np.outer(np.cos(u), np.sin(v))
ys = np.outer(np.sin(u), np.sin(v))
zs = np.outer(np.ones_like(u), np.cos(v))

ax.plot_surface(xs, ys, zs, alpha=0.08, linewidth=0)

# =====================================================
# NOEUDS
# =====================================================

ax.scatter(x, y, z, s=140)

# =====================================================
# LABELS (EN GRAS)
# =====================================================

for i, (_, row) in enumerate(errors.iterrows()):

    ax.text(
        x[i] * 1.15,
        y[i] * 1.15,
        z[i] * 1.15,
        row["error_name"],
        fontsize=11,
        fontweight="bold"
    )

# =====================================================
# LIENS
# =====================================================

max_weight = filtered["cooccurrence_count"].max()

for _, row in filtered.iterrows():

    e1 = row["error1"]
    e2 = row["error2"]
    weight = row["cooccurrence_count"]

    x1, y1, z1 = positions[e1]
    x2, y2, z2 = positions[e2]

    linewidth = 2 + 6 * weight / max_weight  # liens épais

    arc = generate_arc(
        (x1, y1, z1),
        (x2, y2, z2),
        radius_factor=1.35
    )

    ax.plot(
        arc[:, 0],
        arc[:, 1],
        arc[:, 2],
        linewidth=linewidth,
        alpha=0.85
    )

# =====================================================
# ESTHETIQUE
# =====================================================

ax.set_title(
    "Top 20 cooccurrences entre erreurs",
    fontsize=16,
    fontweight="bold"
)

ax.set_axis_off()
ax.set_box_aspect([1, 1, 1])

plt.tight_layout()
plt.show()


# TEST 2
n = len(errors)

phi = np.arccos(1 - 2 * (np.arange(n) + 0.5) / n)
theta = np.pi * (1 + np.sqrt(5)) * np.arange(n)

x = np.sin(phi) * np.cos(theta)
y = np.sin(phi) * np.sin(theta)
z = np.cos(phi)
def arc(p1, p2, steps=30):
    p1 = np.array(p1)
    p2 = np.array(p2)

    mid = (p1 + p2) / 2
    mid = mid / np.linalg.norm(mid) * 1.3

    t = np.linspace(0, 1, steps)

    return np.array([
        (1-t_)**2*p1 + 2*(1-t_)*t_*mid + t_**2*p2
        for t_ in t
    ])
fig = go.Figure()
fig.add_trace(go.Scatter3d(
    x=x,
    y=y,
    z=z,
    mode='markers+text',
    text=errors["error_name"],
    textposition="top center",
    marker=dict(size=6)
))
filtered = cooc.nlargest(20, "cooccurrence_count")

for _, row in filtered.iterrows():

    p1 = positions[row["error1"]]
    p2 = positions[row["error2"]]

    curve = arc(p1, p2)

    fig.add_trace(go.Scatter3d(
        x=curve[:,0],
        y=curve[:,1],
        z=curve[:,2],
        mode='lines',
        line=dict(width=2),
        hoverinfo='none'
    ))
fig.update_layout(
    title="Cooccurrences erreurs (3D network)",
    showlegend=False
)

fig.show()
