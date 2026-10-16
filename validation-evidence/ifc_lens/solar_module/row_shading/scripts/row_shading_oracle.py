"""Closed-form inter-row shading for an infinite array of tilted collector rows.

This is the ORACLE the EnergyFlowX ray tracer is checked against. It is deliberately
independent of the product: a few lines of trigonometry, derived from the geometry below,
with no shared code and nothing imported from the tool.

THE DERIVATION, in full, so the result can be checked rather than trusted.

Take rows of collectors of slope length L, tilted b from horizontal, all facing the same
way, spaced a horizontal distance p apart (row to row, measured between corresponding
points). Work in the vertical plane perpendicular to the row axis, where the sun's
elevation becomes the PROFILE ANGLE:

    tan(profile) = tan(elevation) / cos(sun azimuth - collector azimuth)

Put the origin at the lower edge of the shading row. Its upper edge is then at
horizontal offset L*cos(b) and height L*sin(b). The shaded row's lower edge is at
horizontal offset p, so a point a distance s up its slope sits at:

    horizontal  p + s*cos(b)
    height        s*sin(b)

Trace a ray from that point back toward the sun. It rises tan(profile) per unit of
horizontal distance travelled, so at the shading row's upper edge it has reached

    s*sin(b) + (p + s*cos(b) - L*cos(b)) * tan(profile)

The point is shaded when that is below the shading row's upper edge, L*sin(b). Solving
for s gives the shaded slope length, and dividing by L the shaded fraction:

    shaded = [ L*sin(b) - (p - L*cos(b)) * tan(profile) ]
             / [ L * (sin(b) + cos(b) * tan(profile)) ]

clamped to [0, 1]. Shading grows from the LOWER edge upward, which is why a row's bottom
cells are the ones a bypass diode takes out first.

ASSUMPTIONS, all of which the ray tracer drops:
  - rows are infinitely long, so there is no end-of-row light spilling in from the side
  - collectors have zero thickness
  - the ground is flat and the rows are parallel and evenly spaced
  - only the immediately preceding row can shade (true for the pitches used in practice)

Compared with pvlib's shaded_fraction1d (BSD-3-Clause) by pvlib_crosscheck.py in this
folder, where the largest difference is at machine precision. Two independent derivations
agreeing to 1e-16 is a statement about the algebra. The comparison with the ray tracer,
reported in the README, is the statement about the product.

No dependencies beyond the standard library. Run it directly to print the table used in
the README:

    python row_shading_oracle.py
"""

from __future__ import annotations

import math

# The reference case. Chosen so the shading is substantial but not total, and so the
# pitch is one a designer would actually build.
TILT_DEG = 30.0
COLLECTOR_AZIMUTH_DEG = 180.0  # the compass bearing the collectors face; 180 is south
SLOPE_LENGTH_M = 1.0
PITCH_M = 2.5


def profile_angle_deg(sun_elevation_deg: float, sun_azimuth_deg: float,
                      collector_azimuth_deg: float = COLLECTOR_AZIMUTH_DEG) -> float:
    """The sun's elevation projected into the plane perpendicular to the row axis."""
    d = math.radians(sun_azimuth_deg - collector_azimuth_deg)
    cos_d = math.cos(d)
    if cos_d <= 0.0:
        return float("nan")  # the sun is behind the rows: the 1-D model does not apply
    return math.degrees(math.atan2(math.tan(math.radians(sun_elevation_deg)), cos_d))


def shaded_fraction(sun_elevation_deg: float,
                    sun_azimuth_deg: float,
                    tilt_deg: float = TILT_DEG,
                    collector_azimuth_deg: float = COLLECTOR_AZIMUTH_DEG,
                    slope_length_m: float = SLOPE_LENGTH_M,
                    pitch_m: float = PITCH_M) -> float:
    """Fraction of the collector slope in the shadow of the row in front of it.

    Measured from the lower edge upward. 0 is fully lit, 1 is fully shaded.
    Returns 0 when the sun is below the horizon or behind the rows, where this model
    says nothing: the caller decides what an unlit collector means.
    """
    if sun_elevation_deg <= 0.0:
        return 0.0
    d = math.radians(sun_azimuth_deg - collector_azimuth_deg)
    cos_d = math.cos(d)
    if cos_d <= 0.0:
        return 0.0

    b = math.radians(tilt_deg)
    tan_profile = math.tan(math.radians(sun_elevation_deg)) / cos_d

    numerator = slope_length_m * math.sin(b) - (pitch_m - slope_length_m * math.cos(b)) * tan_profile
    denominator = slope_length_m * (math.sin(b) + math.cos(b) * tan_profile)
    if denominator <= 0.0:
        return 0.0
    return min(1.0, max(0.0, numerator / denominator))


def _main() -> None:
    elevations = [8, 10, 12, 15, 18, 20, 25, 30, 35, 40, 50]
    azimuths = [150, 165, 180, 210]
    print(f"# Inter-row shading, closed form")
    print(f"# tilt={TILT_DEG} deg  slope length={SLOPE_LENGTH_M} m  pitch={PITCH_M} m  "
          f"facing={COLLECTOR_AZIMUTH_DEG} deg")
    print("sun_elevation_deg,sun_azimuth_deg,profile_angle_deg,shaded_fraction")
    for az in azimuths:
        for el in elevations:
            print(f"{el},{az},{profile_angle_deg(el, az):.4f},{shaded_fraction(el, az):.6f}")


if __name__ == "__main__":
    _main()
