# Elements, Solar module: inter-row shading evidence

This folder holds a reproducible check of the ray-traced **inter-row shading** in the PV tool
against a closed-form solution for the same geometry, derived independently and itself checked
against [pvlib](https://pvlib-python.readthedocs.io/).

It is the third case in this module. The [direct sun hours evidence](../README.md) validates the
shadow geometry against Ladybug Tools, the [clear sky evidence](../clear_sky_irradiation/README.md)
validates the energy model layered on top of it, and this one validates the thing that decides
how close together rows can stand: how much of a collector its neighbour takes away.

---

## 1. What is being validated, and why this one is worth doing

The tool ray-traces shadows through whatever geometry you loaded. That is the right approach for a
real site, where the obstructions are buildings, terrain, trees and other arrays, and no closed form
exists. It is also the approach with no independent answer to check against, which is why this
case is constructed.

For **one** arrangement, a regular grid of parallel rows on flat ground, the answer can be written
down in closed form. So this folder builds that arrangement in the product, traces it, and compares.

> A ray tracer that gets the one case with an analytic answer wrong is wrong everywhere. Getting it
> right does not prove the general case, and this folder does not claim that it does. It removes a
> whole class of error from the one geometry that a user is most likely to build, and it puts a
> number on the residual instead of a reassurance.

**Row spacing is where this matters commercially.** The tool's spacing optimiser trades panel count
against self-shading. If the shading model is biased, the recommended pitch is biased with it, and
the error lands in the capital cost of a real array.

---

## 2. The oracle, and why it is not just a second copy of our own code

`scripts/row_shading_oracle.py` is a closed form for the shaded fraction of a tilted collector
standing behind an identical row. It is about fifteen lines of trigonometry, derived from the
geometry rather than ported from anywhere, and the full derivation is written out in the file so it
can be checked rather than taken on faith. It shares no code with the product and imports nothing.

That makes it clean-room. It also means an error in our algebra would go straight into the oracle,
and the oracle would then validate the ray tracer against our own mistake. So the oracle is itself checked:

```text
$ python scripts/pvlib_crosscheck.py
axis_azimuth=   90  rotation= +30.0  max|difference| = 8.882e-16   mean = 9.720e-17
axis_azimuth=  270  rotation= -30.0  max|difference| = 8.882e-16   mean = 1.034e-16

PASS: the two derivations agree to 8.882e-16, which is floating-point noise.
```

against `pvlib.shading.shaded_fraction1d`, which implements Anderson and Jensen (2024) and is
maintained by a different community. pvlib is BSD-3-Clause and is used here as a reference
implementation, not vendored.

Both of pvlib's equivalent sign conventions are checked, because picking the one that happened to
agree would be the kind of fitting this file exists to rule out.

That agreement says the algebra is right. It says nothing about the product,
because neither implementation is the product. The number that matters is in section 4.

---

## 3. Method

| | |
| --- | --- |
| Quantity | Shaded fraction of a collector's slope length, measured from its lower edge |
| Scene | 21 columns by 3 rows, panels edge to edge, on flat ground. Full definition in [`scene/array.json`](scene/array.json) |
| Measured on | The centre panel of the middle row: the panel furthest from every edge, where the "infinitely long row" idealisation is least strained |
| Collector | 1.6 m along the row axis, 1.0 m up the slope, 30 degrees tilt, facing due south |
| Pitch | 2.5 m row to row |
| Sun | 44 positions: elevations 8 to 50 degrees at azimuths 150, 165, 180 and 210. Directions are set explicitly rather than derived from a date, so the case depends on no ephemeris and has no timezone to get wrong |
| Ours | The product's own ray tracer, through the same BVH and the same face sampler a real run uses |
| Reference | `scripts/row_shading_oracle.py`, cross-checked against pvlib |

Everything in [`scene/engine-vs-closed-form.csv`](scene/engine-vs-closed-form.csv): 528 rows, every
sun position at every quality setting and both panel thicknesses.

---

## 4. Result

![Ray-traced inter-row shading against the closed form](figures/row-shading-vs-closed-form.png)

Largest disagreement in shaded fraction, over all 44 sun positions:

| Sub-samples per axis | 4 cm panel, as built | 0.4 mm panel, thickness removed |
| --- | --- | --- |
| 3 (product default) | 0.139 | 0.139 |
| 5 | 0.115 | 0.093 |
| 7 (product maximum) | 0.082 | 0.063 |
| 21 | 0.041 | 0.021 |
| 41 | 0.032 | 0.012 |
| 81 | 0.036 | **0.006** |

The residual comes from two effects, sampling and thickness.

**Sampling.** The tool computes a lit fraction by sampling a grid of points across the panel face,
so the answer it can express is quantised: with 7 sub-samples per axis the shaded fraction can only
land on multiples of about 0.14. The disagreement at a single sun position is therefore bounded by
half a step, and that is what the numbers above show. Take the thickness away and refine the grid,
and it falls steadily toward zero: 0.139, 0.093, 0.063, 0.021, 0.012, 0.006. Once the grid is fine
enough to resolve the shadow edge, each doubling roughly halves it (21 to 41 is a factor of 0.57,
41 to 81 a factor of 0.49), which is first-order convergence. That is a quadrature error
converging, which is what tells it apart from a modelling error. A modelling error does not shrink
with finer sampling.

**Thickness.** The product builds a panel as a solid 4 cm box, because that is what a panel is. The
closed form assumes a surface of zero thickness. A thicker collector casts a longer shadow, so the
ray tracer shades slightly more, and refinement does not remove it. The orange curve flattens
out at about 0.03 while the dark one keeps falling. Once the grid is fine enough to resolve the
shadow edge (21 sub-samples and above), the difference at the built thickness is never negative
at any of the 44 sun positions. The tool never claims less shade than the idealisation. It claims
slightly more, and it is right to.

**At the quality the product ships**, the difference straddles zero (worst case -0.039 to
+0.082 at 7 sub-samples) because the quantisation noise is larger than the thickness bias and runs
both ways. It is noise around the right answer, not a bias, and it averages out over the thousands
of sun positions in an annual run. **Read the per-position numbers as a bound on a single instant,
never as an error on an annual yield.**

---

## 5. What this does not establish

- **Nothing about irregular geometry.** A closed form exists only for parallel rows of identical
  collectors on flat ground. Buildings, terrain, trees and mixed arrays are why the product
  ray-traces, and they have no analytic answer to check against.
- **Nothing about the diffuse component.** This case is beam shading only. The sky-diffuse and
  ground-reflected terms are checked separately, against their own closed forms, in the product's
  live validation report.
- **Nothing about what shading costs in energy.** The step from a shaded fraction to a lost kilowatt
  hour runs through the bypass-diode model, the cell temperature and the inverter, each validated
  on its own. A correct shaded fraction is necessary, not sufficient.
- **Nothing about end-of-row panels.** The measurement is taken at the centre of the array on
  purpose. A panel at the end of a row is lit from the side in a way an infinite row is not, and the
  closed form has nothing to say about it.

---

## 6. Reproducing it

```bash
cd scripts
python -m venv .venv && source .venv/bin/activate   # Windows: .venv/Scripts/activate
pip install -r requirements.txt

python row_shading_oracle.py     # the closed form, no dependencies at all
python pvlib_crosscheck.py       # checks that closed form against pvlib
python evidence_figure.py        # redraws the figure from the CSV
```

The ray-traced column of the CSV comes from the `solar-engine` test suite, which is not public. The
scene is fully specified in `scene/array.json`, so the same case can be rebuilt in any tool that
traces shadows, and the closed form here will answer it.

---

## 7. References

- Anderson, K. S. and Jensen, A. R. (2024). *Shaded fraction and backtracking in single-axis
  trackers on rolling terrain.* Journal of Renewable and Sustainable Energy 16(2), 023504.
  <https://doi.org/10.1063/5.0202220>. The model behind pvlib's `shaded_fraction1d`.
- Holmgren, W. F., Hansen, C. W. and Mikofski, M. A. (2018). *pvlib python: a python package for
  modeling solar energy systems.* Journal of Open Source Software 3(29), 884.
  <https://doi.org/10.21105/joss.00884>

The closed form in `row_shading_oracle.py` is our own derivation. It is elementary geometry and is
written out in full in that file so it can be checked line by line.
