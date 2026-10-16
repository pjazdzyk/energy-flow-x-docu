"""
Ladybug Tools evidence figure: direct sun-hours on the comparison test box.

Renders the same scene and 7 sample points as ladybug_reference.py, but as a
figure for the IFC Lens Validation evidence card, computed with the Ladybug
Tools Python library (`ladybug-core`, AGPL-3.0, Sunpath routine). Same occlusion
method as ladybug_reference.py, rendered by our own script (nothing reproduced
from a vendor UI).

NOTE: do NOT name this module `ladybug_*`, because ladybug's __init__ auto-imports
any top-level `ladybug*` module as an extension and crashes on it.

Left panel : axonometric 3D view, opaque box + the 7 points coloured by
             direct sun-hours, with a handful of equinox sun rays for context.
Right panel: plan (top-down) view, box footprint + the same coloured points.

Run (venv with ladybug-core, ladybug-geometry, matplotlib):
    python lb_evidence_figure.py
Writes: solar-ladybug-evidence.png next to this script.

Scene (metres, +X east, +Y north, +Z up):
    box  X[-10,10]  Y[-5,5]  Z[0,15]  (opaque, no glazing)
    site Warsaw 52.23N 21.01E, date 20 March (equinox), whole day, 5-min step.
"""

import os
from importlib.metadata import version as pkg_version

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from ladybug.sunpath import Sunpath

LB_VERSION = pkg_version("ladybug-core")

LAT, LON, TZ = 52.23, 21.01, 1  # Warsaw, standard time (whole-day total is TZ-independent)
MONTH, DAY = 3, 20
STEP_MIN = 5

BOX_MIN = (-10.0, -5.0, 0.0)
BOX_MAX = (10.0, 5.0, 15.0)

# Ground sample points (X, Y, Z). North of the box is where the shadow falls.
POINTS = {
    "G": (0.0, 6.0, 0.0),
    "A": (0.0, 8.0, 0.0),
    "B": (0.0, 12.0, 0.0),
    "C": (0.0, 20.0, 0.0),
    "D": (0.0, 35.0, 0.0),
    "E": (30.0, 0.0, 0.0),
    "F": (0.0, -10.0, 0.0),
}

EPS = 1e-9


def ray_hits_box(origin, direction):
    """Slab-method ray vs axis-aligned box (forward ray, t > 0)."""
    tmin, tmax = -float("inf"), float("inf")
    for i in range(3):
        o, d = origin[i], direction[i]
        lo, hi = BOX_MIN[i], BOX_MAX[i]
        if abs(d) < EPS:
            if o < lo - EPS or o > hi + EPS:
                return False
        else:
            t1, t2 = (lo - o) / d, (hi - o) / d
            if t1 > t2:
                t1, t2 = t2, t1
            tmin = max(tmin, t1)
            tmax = min(tmax, t2)
            if tmin > tmax:
                return False
    return tmax > EPS and tmax >= tmin


def collect_suns():
    sp = Sunpath(LAT, LON, time_zone=TZ)
    suns, minute = [], 0
    while minute < 24 * 60:
        sun = sp.calculate_sun(MONTH, DAY, minute / 60.0)
        if sun.altitude > 0:
            v = sun.sun_vector_reversed  # points TOWARD the sun
            suns.append((v.x, v.y, v.z))
        minute += STEP_MIN
    return suns


def sun_hours(point, suns, weight_h):
    lit = 0.0
    for (vx, vy, vz) in suns:
        if vz <= 0:
            continue
        if not ray_hits_box(point, (vx, vy, vz)):
            lit += weight_h
    return lit


def box_faces():
    x0, y0, z0 = BOX_MIN
    x1, y1, z1 = BOX_MAX
    c = [
        (x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),
        (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1),
    ]
    idx = [
        (0, 1, 2, 3), (4, 5, 6, 7), (0, 1, 5, 4),
        (2, 3, 7, 6), (1, 2, 6, 5), (0, 3, 7, 4),
    ]
    return [[c[i] for i in f] for f in idx]


def main():
    weight_h = STEP_MIN / 60.0
    suns = collect_suns()
    daylight_h = len(suns) * weight_h

    names = list(POINTS.keys())
    pts = [POINTS[n] for n in names]
    hours = [sun_hours(p, suns, weight_h) for p in pts]

    norm = Normalize(vmin=0.0, vmax=daylight_h)
    cmap = matplotlib.colormaps["YlOrRd"]
    colors = [cmap(norm(h)) for h in hours]

    fig = plt.figure(figsize=(13.5, 6.0))
    fig.suptitle(
        f"Direct sun-hours, Warsaw (52.23 N, 21.01 E), 20 March equinox, 5-min step\n"
        f"Ladybug Tools (ladybug-core {LB_VERSION}), opaque box, "
        f"daylight {daylight_h:.2f} h",
        fontsize=11,
    )

    # --- 3D axonometric ---
    ax = fig.add_subplot(1, 2, 1, projection="3d")
    faces = Poly3DCollection(
        box_faces(), facecolor="#9fb0c4", edgecolor="#25324f", alpha=0.55, linewidths=0.6
    )
    ax.add_collection3d(faces)

    # A few equinox sun rays grazing the box top (visual context only).
    apex = ((BOX_MIN[0] + BOX_MAX[0]) / 2, BOX_MAX[1], BOX_MAX[2])
    for (vx, vy, vz) in suns[:: max(1, len(suns) // 9)]:
        L = 26.0
        ax.plot(
            [apex[0], apex[0] + vx * L],
            [apex[1], apex[1] + vy * L],
            [apex[2], apex[2] + vz * L],
            color="#f0b73a", lw=0.7, alpha=0.5,
        )

    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    zs = [p[2] for p in pts]
    ax.scatter(xs, ys, zs, c=colors, s=70, edgecolor="#25324f", depthshade=False)
    for n, p, h in zip(names, pts, hours):
        ax.text(p[0], p[1], p[2] + 3.0, f"{n} {h:.2f}h", fontsize=7.5, ha="center")

    ax.set_xlabel("X  (E +)")
    ax.set_ylabel("Y  (N +)")
    ax.set_zlabel("Z  (up)")
    ax.set_box_aspect((1, 1, 0.5))
    ax.view_init(elev=24, azim=-58)
    ax.set_title("Axonometric", fontsize=10)

    # --- Plan (top-down) ---
    ax2 = fig.add_subplot(1, 2, 2)
    bx = [BOX_MIN[0], BOX_MAX[0], BOX_MAX[0], BOX_MIN[0], BOX_MIN[0]]
    by = [BOX_MIN[1], BOX_MIN[1], BOX_MAX[1], BOX_MAX[1], BOX_MIN[1]]
    ax2.fill(bx, by, facecolor="#9fb0c4", edgecolor="#25324f", alpha=0.7, linewidth=1.0)
    ax2.text(0, 0, "opaque\nbox", ha="center", va="center", fontsize=8, color="#25324f")
    sc = ax2.scatter(xs, ys, c=hours, cmap=cmap, norm=norm, s=120,
                     edgecolor="#25324f", zorder=3)
    # Push each label well clear of its marker with a thin leader line, so the
    # text never sits on top of the coloured point.
    for n, p, h in zip(names, pts, hours):
        ax2.annotate(
            f"{n}  {h:.2f}h",
            (p[0], p[1]),
            textcoords="offset points",
            xytext=(16, 12),
            fontsize=8,
            ha="left",
            arrowprops=dict(arrowstyle="-", color="#9aa3b2", lw=0.6, shrinkA=0, shrinkB=4),
        )
    ax2.annotate("N", (0.04, 0.97), xycoords="axes fraction", xytext=(0, -14),
                 textcoords="offset points", ha="left", fontsize=10, fontweight="bold")
    ax2.annotate("", xy=(0.04, 0.97), xytext=(0.04, 0.86), xycoords="axes fraction",
                 arrowprops=dict(arrowstyle="->", color="#25324f"))
    ax2.set_xlabel("X  (E +)  [m]")
    ax2.set_ylabel("Y  (N +)  [m]")
    ax2.set_aspect("equal", adjustable="datalim")
    ax2.set_title("Plan", fontsize=10)
    ax2.grid(True, color="#e4e9f0")
    cbar = fig.colorbar(sc, ax=ax2, fraction=0.046, pad=0.04)
    cbar.set_label("direct sun-hours")

    fig.tight_layout(rect=(0, 0, 1, 0.92))
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "solar-ladybug-evidence.png")
    fig.savefig(out, dpi=150)
    print("wrote", out)
    print(f"daylight {daylight_h:.2f} h; "
          + ", ".join(f"{n} {h:.2f}" for n, h in zip(names, hours)))


if __name__ == "__main__":
    main()
