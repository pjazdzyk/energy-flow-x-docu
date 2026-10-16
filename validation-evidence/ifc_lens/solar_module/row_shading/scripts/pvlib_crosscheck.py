"""Check the closed form in row_shading_oracle.py against pvlib, an independent implementation.

WHY THIS EXISTS. row_shading_oracle.py is a few lines of trigonometry we derived ourselves.
That keeps it independent of the product, which is the point, but it also means an error in the algebra
would go straight into the oracle and the oracle would then agree with the ray tracer
for the wrong reason. So the oracle is itself checked, against pvlib's
`shading.shaded_fraction1d`, which implements Anderson and Jensen (2024) and is maintained
by a different community entirely.

pvlib is BSD-3-Clause. It is used here as a reference implementation, not vendored.

WHAT AGREEMENT HERE DOES AND DOES NOT MEAN. Two implementations of the same geometry
agreeing to machine precision says the algebra is right. It says nothing at all about the
product, because neither of them is the product. The number that matters is in the README:
how far the ray tracer, which models a finite array of thick panels, sits from this
infinite-thin-row idealisation, and whether the difference has the sign and the size the
physics says it should.

Run:
    pip install -r requirements.txt
    python pvlib_crosscheck.py
"""

from __future__ import annotations

import sys

import numpy as np

try:
    from pvlib import shading
except ImportError:  # pragma: no cover
    sys.exit("pvlib is not installed. Run: pip install -r requirements.txt")

from row_shading_oracle import (
    COLLECTOR_AZIMUTH_DEG,
    PITCH_M,
    SLOPE_LENGTH_M,
    TILT_DEG,
    shaded_fraction,
)

# pvlib describes a fixed-tilt array as the degenerate case of a tracker: an axis running
# along the rows, with the collector at a fixed rotation about it. For rows facing south
# the axis runs east-west, and a right-handed rotation about the east-pointing axis tilts
# the collector up toward the south. Hence axis_azimuth=90 with a POSITIVE rotation. The
# equivalent statement is axis_azimuth=270 with a negative rotation, and this script
# checks both, because picking the convention that happens to agree would be exactly the
# kind of fitting this file exists to rule out.
CONVENTIONS = [(90.0, TILT_DEG), (270.0, -TILT_DEG)]

ELEVATIONS = np.array([5, 8, 10, 12, 15, 18, 20, 25, 30, 35, 40, 50, 60], dtype=float)
AZIMUTHS = np.array([120, 135, 150, 165, 180, 195, 210, 225, 240], dtype=float)


def main() -> int:
    elev, azim = np.meshgrid(ELEVATIONS, AZIMUTHS, indexing="ij")
    ours = np.vectorize(shaded_fraction)(elev, azim)

    print(f"tilt={TILT_DEG} deg  slope length={SLOPE_LENGTH_M} m  pitch={PITCH_M} m  "
          f"facing={COLLECTOR_AZIMUTH_DEG} deg")
    print(f"{elev.size} sun positions, of which {(ours > 0).sum()} are partly shaded\n")

    worst = 0.0
    for axis_azimuth, rotation in CONVENTIONS:
        theirs = np.asarray(
            shading.shaded_fraction1d(
                solar_zenith=90.0 - elev,
                solar_azimuth=azim,
                axis_azimuth=axis_azimuth,
                shaded_row_rotation=rotation,
                collector_width=SLOPE_LENGTH_M,
                pitch=PITCH_M,
            ),
            dtype=float,
        )
        # Compare only where the sun is up and in front of the rows. Elsewhere the collector
        # is not lit at all and the two libraries are free to report anything.
        lit = (elev > 0) & (np.cos(np.radians(azim - COLLECTOR_AZIMUTH_DEG)) > 0)
        diff = np.abs(theirs - ours)[lit]
        worst = max(worst, float(diff.max()))
        print(f"axis_azimuth={axis_azimuth:5.0f}  rotation={rotation:+6.1f}  "
              f"max|difference| = {diff.max():.3e}   mean = {diff.mean():.3e}")

    print()
    if worst < 1e-12:
        print(f"PASS: the two derivations agree to {worst:.3e}, which is floating-point noise.")
        return 0
    print(f"FAIL: largest disagreement {worst:.3e}. The oracle and pvlib have parted company.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
