"""
Ladybug Tools reference: direct sun-hours on the comparison test box.

Computes the reference values for the IFC Lens vs Ladybug comparison documented
in ../README.md, using the Ladybug Tools Python library (`ladybug`, AGPL-3.0) and
its Sunpath routine for the sun positions. Opaque-box shadowing is a ray /
axis-aligned-box intersection (sun vectors from Sunpath plus geometric
occlusion). Ladybug Tools is named for comparison only.

REPORTS SAMPLES FIRST, hours second, and that is the whole point of this script's
output shape. Both tools march the same 5-minute grid, so every sun-hour either
can report is a whole number of samples; the hours are a presentation of that
integer. Printing only hours (as this did) means anyone reproducing the reference
has to divide by 1/12 h and round to recover what was actually computed, against a
tolerance of ONE sample, and a two-decimal transcription of a sample count is
already 4% of that budget. ../scene/ladybug-reference.csv records the integers, so
this script must be able to produce them.

Run (after `pip install -r requirements.txt`):
    python ladybug_reference.py

Scene (metres, +X east, +Y north, +Z up):
    box  X[-10,10]  Y[-5,5]  Z[0,15]  (opaque, no glazing)
    site Warsaw 52.23N 21.01E, date 20 March (equinox), whole day, 5-min step.
"""

from ladybug.sunpath import Sunpath

LAT, LON, TZ = 52.23, 21.01, 1  # Warsaw, standard time (whole-day total is TZ-independent)
MONTH, DAY = 3, 20
STEP_MIN = 5

# Axis-aligned opaque box.
BOX_MIN = (-10.0, -5.0, 0.0)
BOX_MAX = (10.0, 5.0, 15.0)

# Ground sample points (X, Y, Z). North of the box is where the shadow falls.
# Keyed by the SAME single-letter ids used in ../scene/solar-test-points.csv,
# ../scene/ladybug-reference.csv and the README table, so the four line up row for
# row without anyone having to match "G (0,6)  1m N of face" to "G" by eye.
POINTS = {
    "G": ((0.0, 6.0, 0.0), "1 m north of the face - deepest shade"),
    "A": ((0.0, 8.0, 0.0), "3 m north - ON the moving shadow edge - the most sensitive point"),
    "B": ((0.0, 12.0, 0.0), "7 m north - shaded midday - lit mornings and evenings"),
    "C": ((0.0, 20.0, 0.0), "15 m north - near the noon shadow tip"),
    "D": ((0.0, 35.0, 0.0), "30 m north - open sky"),
    "E": ((30.0, 0.0, 0.0), "25 m east - open most of the day"),
    "F": ((0.0, -10.0, 0.0), "south side - fully open"),
    # Far away from the box: unobstructed, so it must come back at full daylight.
    # It is the control, not a read point: if it is ever short of DAYLIGHT the box
    # is shading something it cannot possibly reach and no other row means anything.
    "OPEN": ((200.0, 200.0, 0.0), "control - no box in the way"),
}

EPS = 1e-9


def ray_hits_box(origin, direction):
    """Slab-method ray vs axis-aligned box. Returns True if the forward ray from
    `origin` along unit `direction` pierces the box (t > 0)."""
    tmin, tmax = -float("inf"), float("inf")
    for i in range(3):
        o, d = origin[i], direction[i]
        lo, hi = BOX_MIN[i], BOX_MAX[i]
        if abs(d) < EPS:
            if o < lo - EPS or o > hi + EPS:
                return False  # parallel and outside this slab
        else:
            t1, t2 = (lo - o) / d, (hi - o) / d
            if t1 > t2:
                t1, t2 = t2, t1
            tmin = max(tmin, t1)
            tmax = min(tmax, t2)
            if tmin > tmax:
                return False
    return tmax > EPS and tmax >= tmin


def main():
    sp = Sunpath(LAT, LON, time_zone=TZ)
    weight_h = STEP_MIN / 60.0

    # Collect daylight sun vectors (toward the sun) across the calendar day.
    suns = []
    minute = 0
    while minute < 24 * 60:
        sun = sp.calculate_sun(MONTH, DAY, minute / 60.0)
        if sun.altitude > 0:
            v = sun.sun_vector_reversed  # points TOWARD the sun
            suns.append((v.x, v.y, v.z, sun.altitude, sun.azimuth))
        minute += STEP_MIN

    daylight_samples = len(suns)
    alts = [s[3] for s in suns]
    print(f"Ladybug Sunpath: {daylight_samples} daylight samples @ {STEP_MIN} min "
          f"= {daylight_samples * weight_h:.3f} h daylight; max alt {max(alts):.2f} deg")

    # SAMPLES is the reference column. Hours and % daylight are presentations of it.
    print(f"\n{'point':<6}{'position':>16}{'samples':>9}{'hours':>9}{'% daylight':>12}  note")
    print("-" * 78)
    rows = []
    for name, (p, note) in POINTS.items():
        lit = 0
        for (vx, vy, vz, _alt, _az) in suns:
            if vz <= 0:
                continue
            if not ray_hits_box(p, (vx, vy, vz)):
                lit += 1
        pct = 100.0 * lit / daylight_samples if daylight_samples else 0.0
        pos = f"({p[0]:g},{p[1]:g},{p[2]:g})"
        print(f"{name:<6}{pos:>16}{lit:>9d}{lit * weight_h:>9.3f}{pct:>11.1f}%  {note}")
        rows.append((name, p, lit, note))

    # The control must see the whole day. A box that shades a point 280 m away is
    # a broken occlusion test, and every row above it would be quietly wrong.
    open_lit = next(lit for name, _p, lit, _n in rows if name == "OPEN")
    if open_lit != daylight_samples:
        raise SystemExit(
            f"CONTROL FAILED: the unobstructed point saw {open_lit} of "
            f"{daylight_samples} daylight samples. The reference is not usable."
        )

    # The machine-readable form the EnergyFlowX suite is pinned to, so a re-run can
    # be diffed against ../scene/ladybug-reference.csv rather than read off by eye.
    print("\n--- ../scene/ladybug-reference.csv form ---")
    print("point,x_m,y_m,z_m,samples,hours,description")
    for name, p, lit, note in rows:
        if name == "OPEN":
            continue
        print(f"{name},{p[0]:g},{p[1]:g},{p[2]:g},{lit},{lit * weight_h:.3f},{note}")
    print(f"DAYLIGHT,,,,{daylight_samples},{daylight_samples * weight_h:.3f},"
          f"daylight on the day - both tools")


if __name__ == "__main__":
    main()
