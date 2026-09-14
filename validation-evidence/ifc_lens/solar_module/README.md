# Elements, Solar module validation evidence

This folder holds a reproducible validation of the **EnergyFlowX Elements Solar tool**. It
documents how the tool computes direct sun hours, and shows that the result lands in the same
place as an independent, recognized reference (Ladybug Tools) on a controlled scene that anyone
can rebuild.

You should be able to take the files here, run the same check yourself, and confirm the numbers
rather than take our word for it.

---

## 1. What is being validated

The Elements Solar tool answers a geometric question: for a given location, date and building
geometry, how many hours of direct sun does a point receive over the day. It is a comparative
siting and overshadowing aid. It does not compute measured energy yield or daylight factor.

We validate it on three independent legs, each against a recognized method or source:

1. **Solar position.** Where the sun is in the sky (altitude and azimuth) through the day. The
   tool uses the NOAA solar position algorithm (Meeus, *Astronomical Algorithms*). This is
   cross checked against NREL SPA reference values and an independent VSOP87 ephemeris inside
   the live in app Validation report.
2. **Occlusion.** Whether building geometry blocks the ray from a point to the sun. The live
   heatmap rasterises it with a GPU shadow map. The unit tests check a ray traced oracle (Moller
   Trumbore ray triangle intersection) against a closed form analytic shadow (the gnomon
   relation), and the Solar engine self test checks the shadow map against that oracle.
3. **End to end sun hours.** The two legs combined, counting lit time samples over the day.
   This is the comparison documented in this folder, against Ladybug Tools.

The Solar tool can also report an optional **Irradiation** figure in kWh/m², a clear sky potential
from a weather free model. That is a different claim with a different reference, so it has its own
case: [clear_sky_irradiation](clear_sky_irradiation/), cross checked against PVGIS (EU JRC). This
folder is about the geometry.

The PV tool adds a third claim on top of both: how much of a panel the row in front of it takes
away, which is what sets how close together rows can stand. That has its own case as well,
[row_shading](row_shading/), against a closed form for the one arrangement that has one.

Ladybug Tools is an open source solar analysis library widely used in the AEC community. Its
sun engine is built on NREL Sunpath. Comparing against it is a cross check between two
independent implementations of the same accepted physics. We are not
trying to be identical to Ladybug. We are showing that our independent methodology produces the
same answer to within the spread expected of two valid implementations.

---

## 2. The test scene

A single opaque rectangular box on flat ground. A box has a shadow you can reason about by hand,
and it removes every confound (glazing, messy geometry, sensor auto placement).

| Property | Value |
| --- | --- |
| Box footprint | X from -10 to +10 m, Y from -5 to +5 m (20 by 10 m) |
| Box height | 15 m (Z from 0 to 15) |
| Long axis | east to west |
| Location | Warsaw, 52.23 N, 21.01 E |
| Date | 20 March (equinox, a clean east to west shadow sweep, about 12 h of day) |
| Period | whole day, sunrise to sunset |
| Time step | 5 minutes |
| Orientation | building north is true north, bearing 0, true north is +Y |

Coordinates are in metres, +X east, +Y north, +Z up. The IFC carries the location on its
`IfcSite` (latitude, longitude, true north), so Elements reads the site straight from the file.

Sun hours are read at seven ground points, chosen to span deep shadow to full open sky:

| Point | Position (x, y, z) m | What it tests |
| --- | --- | --- |
| G | (0, 6, 0) | 1 m north of the face, deepest shade |
| A | (0, 8, 0) | 3 m north, the shadow edge (the most sensitive point) |
| B | (0, 12, 0) | 7 m north, shaded midday, lit mornings and evenings |
| C | (0, 20, 0) | 15 m north, near the noon shadow tip |
| D | (0, 35, 0) | 30 m north, open sky |
| E | (30, 0, 0) | 25 m east, open most of the day |
| F | (0, -10, 0) | south side, the sun is in the south, fully open |

The same seven points are in `scene/solar-test-points.csv`, ready to paste into the Elements
"Read at point" list.

---

## 3. Result

Both tools at a 5 minute step on 20 March in Warsaw. Daylight total 145 samples (12.083 h) on both
sides.

Sun hours can only ever be a whole number of time steps, so the table is given in **samples** as
well as hours. Samples separate a residual you can explain from one you cannot. Rounding the hours
to two decimals (as the first version of this table did) introduces 0.0033 h of transcription
error, which is 4 % of a one sample tolerance, and on the one point that differs it pushed an otherwise correct comparison over the line.

| Point | Position (x, y, z) m | Elements | Ladybug | Difference |
| --- | --- | --- | --- | --- |
| G | (0, 6, 0) | 13 (1.083 h) | 13 (1.083 h) | 0 |
| A | (0, 8, 0) | 34 (2.833 h) | 35 (2.917 h) | **1 sample** |
| B | (0, 12, 0) | 67 (5.583 h) | 67 (5.583 h) | 0 |
| C | (0, 20, 0) | 101 (8.417 h) | 101 (8.417 h) | 0 |
| D | (0, 35, 0) | 145 (12.083 h) | 145 (12.083 h) | 0 |
| E | (30, 0, 0) | 130 (10.833 h) | 130 (10.833 h) | 0 |
| F | (0, -10, 0) | 145 (12.083 h) | 145 (12.083 h) | 0 |

Six of seven points are identical. The seventh, point A, differs by exactly one 5 minute sample.

**Why A and only A.** A sits right on the moving shadow edge. Whether one particular 5 minute sample
lands on the lit or the shaded side of that edge is decided by the sun position to a fraction of a
degree. Elements uses the NOAA solar equations, Ladybug uses NREL SPA. They differ by about 0.01
degrees, enough to flip A's one boundary sample, and nothing else. The other six points are either
fully open or deeply shaded, so a few seconds never flips them. One sample is therefore the finest
agreement two independent solar position algorithms can be expected to reach at a shadow edge, and
it is the tolerance the automated check uses. A 1 minute step shrinks the residual further.

### Re-verified, and now automated

This comparison was originally produced by hand in June 2026. It was re-run on 2026-09-07, after
three months of engine work including a full audit that touched the solar and occluder paths, and
every one of the seven points was unchanged.

**Both sides were re-run, not just ours.** The Ladybug column was regenerated on 2026-09-07 with
`ladybug-core` 0.44.52 on Python 3.13.7 and reproduced `scene/ladybug-reference.csv` exactly, row
for row. A reference nobody re-runs can be a transcription error, a figure from a version of the
library that no longer behaves that way, or wrong, and the comparison would still look clean.

Between June and September nothing recomputed these numbers, so a regression would have moved them
silently while this page went on showing June's table. The comparison is now a test in the
EnergyFlowX test suite (`src/utils/bim/validation/__tests__/endToEndSunHours.test.js`),
run on every commit, pinned to the exact sample counts above. Flipping the sun vector's north-south
sign, for example, fails it immediately.

The same run also cross checks the occlusion step a second way: the ray versus triangle tracer is
compared against an independent slab method (ray/AABB interval clipping, sharing no code) over a
grid of 528 ground points across the whole shadow sweep, where exact agreement is required. Seven
points show the shadow is about the right size in seven places. The grid shows it is the right
shape.

### Figures

Ladybug Tools, computed and rendered from the ladybug-core Python library:

![Ladybug direct sun hours](figures/ladybug-direct-sun-hours.png)

EnergyFlowX Elements, the live in browser tool on the same scene:

![Elements direct sun hours](figures/ifc-lens-direct-sun-hours.png)

---

## 4. Reproduce it yourself

### A. The reference (Ladybug Tools), no Rhino needed

Ladybug Tools is a Python library under the hood. You can run the reference without Rhino or
Grasshopper at all.

```bash
python -m venv .venv
# Windows:  .venv\Scripts\activate
# macOS/Linux:  source .venv/bin/activate
pip install -r scripts/requirements.txt

python scripts/ladybug_reference.py     # prints the reference sun hours at the 7 points
python scripts/lb_evidence_figure.py    # renders figures/ladybug-direct-sun-hours.png
```

`ladybug_reference.py` uses the Ladybug `Sunpath` engine for the sun positions (the same NREL
based engine the Grasshopper "Direct Sun Hours" component uses) and a ray versus axis aligned
box test for the occlusion.

It prints the reference **in samples**, then the same rows in the exact format of
`scene/ladybug-reference.csv`, so you can diff your run against the committed reference rather
than read the numbers off by eye:

```bash
python scripts/ladybug_reference.py | sed -n '/csv form/,$p' | tail -n +2 > mine.csv
grep -v '^#' scene/ladybug-reference.csv | diff -u - mine.csv    # no output = identical
```

It also carries a control point 280 m from the box, which must see the whole day. If the box ever
shades a point it cannot possibly reach, the script stops rather than printing a reference nobody
should use.

If you prefer the full visual Grasshopper route, the equivalent component graph is: **Sunpath**
(location from the IFC site, 20 March, whole day, 5 minute step) → **Direct Sun Hours**, with the
box as the context geometry and the seven points from `scene/solar-test-points.csv` as the analysis
points. Set the sun vectors from the same Sunpath component, so the sun positions are identical to
the script's. Either route gives the numbers in the table above.

### B. EnergyFlowX Elements, headless (no browser, no account)

The solar position and the ray occlusion are pure, dependency free kernels, so the whole day
integrates in milliseconds outside the browser. In a clone of the EnergyFlowX UI repository:

```bash
npm ci
node scripts/run-vitest.mjs run src/utils/bim/validation/__tests__/endToEndSunHours.test.js
```

That test computes the Elements column of the table above from scratch and asserts the exact sample
counts, so a pass is the reproduction. `src/utils/bim/validation/endToEndSunHours.js` holds the
scene, the reference and the comparison. `scene/ladybug-reference.csv` here is the same reference in
machine readable form.

This route checks the physics and the geometry. It does **not** exercise the GPU shadow map the live
heatmap rasterises with, which needs WebGL. That path is checked in the browser by the Solar tool's
own engine self test, against the same closed form oracle. Route C below is the one that exercises
it end to end.

### C. EnergyFlowX Elements, in your browser

1. Open Elements at <https://energyflowx.com/elements>.
2. Load `scene/solar-test-box.ifc`. The location reads from the file automatically.
3. Open the **Solar** tool. Set the date to **20 March**, the period to the whole day, and both
   the ground step and building step to **5 min**. Run the simulation.
4. Open **"Or paste a point list (CSV)"** and paste the seven lines from
   `scene/solar-test-points.csv` (or just `x, y, z` per line). Press **Place and read**.
5. The table lists the sun hours at each point. They will match the table above.

### D. Rebuild the IFC scene from scratch (optional)

```bash
python scripts/generate_box_ifc.py      # writes solar-test-box.ifc
```

This writes the exact georeferenced box with `ifcopenshell`, so you can confirm the geometry and
the site location are nothing more than what is described here.

---

## 5. Files in this folder

```text
solar_module/
  README.md                     this document
  figures/
    ladybug-direct-sun-hours.png    Ladybug Tools result (reference)
    ifc-lens-direct-sun-hours.png   EnergyFlowX Elements result
  scene/
    solar-test-box.ifc              the test scene (box on flat ground, Warsaw site)
    solar-test-points.csv           the 7 read points, paste ready
    ladybug-reference.csv           the reference result, machine readable (samples + hours)
  scripts/
    requirements.txt                Python dependencies
    ladybug_reference.py            reference sun hours from the Ladybug library
    lb_evidence_figure.py           renders the Ladybug figure
    generate_box_ifc.py             rebuilds the test IFC
  clear_sky_irradiation/        a separate case: the optional kWh/m2 metric vs PVGIS
  row_shading/                  a separate case: ray-traced inter-row shading vs a closed form
```

---

## 6. Licensing and attribution

The reference figures and numbers are computed by the scripts in this folder from the
**Ladybug Tools** open source Python library (`ladybug-core`), which is itself based on NREL
Sunpath. Ladybug Tools is named here for nominative reference only. Nothing of its source,
user interface, data or documentation is reproduced. The numerical agreement reflects correct
shared physics, not copied content.

- **Ladybug Tools** <https://www.ladybug.tools> (open source).
- **NREL Solar Position Algorithm**, Reda I. and Andreas A. (2004), *Solar Energy* 76(5),
  577 to 589.
- **NOAA solar position equations**, after Meeus J., *Astronomical Algorithms*.

EnergyFlowX, Elements and the Solar tool are the property of Synerset. See the repository
root for the full license and citation terms.
</content>
