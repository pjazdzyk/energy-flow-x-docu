# Elements, Solar module: clear sky irradiation evidence

This folder holds a reproducible cross check of the Elements **Irradiation** metric, the optional
kWh/m² figure the Solar tool can report alongside direct sun hours, against an independent
clear sky model published by the EU Joint Research Centre.

It is the companion to the [direct sun hours evidence](../README.md) one level up. That case
validates the geometry. This one validates the energy model layered on top of it.

---

## 1. What is being validated, and what is not

The Irradiation metric estimates **clear sky potential**: how much solar energy a surface would
receive under a cloudless sky, from a weather free model. It is not measured yield, it is not a
TMY based estimate, and it does not account for cloud. The tool labels it that way on every view,
and this folder does not claim otherwise.

The model is **Bird and Hulstrom (1981)**, a published, public domain clear sky model from
SERI (now NREL). Two separate things have to be right for the reported number to be right:

1. **The instantaneous model.** Does the code reproduce Bird and Hulstrom's own worked table?
   That is checked to the decimal in the product's live Validation report and in its unit tests.
   It is not what this folder is about, because a model agreeing with its own source paper is a
   port check, not an independent one.
2. **The integration.** The number a user sees is a whole year accumulated. Integrating a correct
   instantaneous model incorrectly is easy to do and hard to see. It produces a plausible figure that
   is wrong. **That is what this folder checks**, against a different model built by different
   people.

---

## 2. The reference, and why it is a ballpark check

**PVGIS** (EU Joint Research Centre) is a free and open solar resource tool. Its clear sky
irradiance comes from the **McClear** model, using the CAMS aerosol climatology. Bird and McClear
are different formulations with different aerosol treatments, so:

> Two independent clear sky models should land within a few percent of each other, **not** match to
> the decimal. A decimal match between Bird and McClear would be the tell of a fudged comparison,
> not a good result.

The percentage is therefore the weaker half of this evidence. **The stronger claim is the
bracketing.** The tool exposes a single **Clarity** knob with three presets, and the Clean and Hazy
presets must *straddle* the PVGIS value at every site. That shows the knob spans a physically
reasonable range of atmospheres, rather than the Average preset having been tuned to hit one
number, which a percentage on its own cannot distinguish.

---

## 3. Method

| | |
| --- | --- |
| Quantity | Annual clear sky **global horizontal** irradiation, kWh/m² |
| Surface | Flat, unobstructed sensor, the simplest apples to apples comparison |
| Year | 2023 |
| Ours | Bird and Hulstrom 1981, integrated over the whole year with the tool's own NOAA solar position math, at Average clarity, plus the Clean and Hazy presets for the band. Fully offline. |
| Reference | PVGIS v5.2 `DRcalc` clear sky output `Gcs(i)` (W/m²): the average day hourly clear sky global irradiance per month, integrated to a daily total, weighted by days in month, summed to annual. |

Three sites, chosen to span latitude, altitude and climate rather than to flatter a model:
Warsaw (52.23 N, 119 m), Madrid (40.42 N, 667 m) and Rome (41.90 N, 21 m).

---

## 4. Result

| Site | PVGIS clear sky (McClear) | Ours, Average | Difference | Ours, Clean to Hazy band | PVGIS in band |
| --- | --- | --- | --- | --- | --- |
| Warsaw (52.23, 21.01, 119 m) | 1607.3 kWh/m² | 1652.7 kWh/m² | **+2.8 %** | 1336 – 1751 | yes |
| Madrid (40.42, −3.70, 667 m) | 2080.8 kWh/m² | 2032.4 kWh/m² | **−2.3 %** | 1687 – 2147 | yes |
| Rome (41.90, 12.50, 21 m) | 1953.7 kWh/m² | 1981.8 kWh/m² | **+1.4 %** | 1641 – 2092 | yes |

Two independent clear sky models agree to within about **3 %** at every site, and the PVGIS value
falls inside our Clean to Hazy band in every case. The residual is the expected spread of two
different clear sky formulations, and of our single Clarity knob against PVGIS's location specific
aerosol climatology. It is not an error term.

### The integration step is checked, not assumed

The year integrates at an hourly step for cost. A coarse step chosen for speed and never verified
is how an integration error hides, so the product's suite carries the hourly total
against a ten minute one as a row of its own: they agree to about **0.002 %**, four orders of
magnitude inside the percent level agreement this comparison is about.

### Re-verified

Recorded **2026-06-21**. Both sides were re-run on **2026-09-07**: the PVGIS reference was
re-fetched from the live service and came back identical to the recorded figures, and our side is
recomputed from scratch on every run of the product's test suite and on every load of the
Validation page.

### Figures, and what they are not

**These two screenshots show the tools, not the comparison.** The numbers in section 4 come from
the script and the test suite, both of which anyone can run. The figures show where in each tool
the quantity lives, and their captions describe only what is on screen, so they do not imply an
agreement they do not show.

The PVGIS **Daily radiation** tool at Warsaw with **Clear-sky irradiance** ticked, showing the
average day profile for **June**, one of the twelve months the script sums to the annual figure.
Note the interactive tool here is on PVGIS 5.3 with the SARAH3 database, while the recorded
reference comes from the `v5_2` DRcalc API endpoint:

![PVGIS clear sky](figures/pvgis-clear-sky.png)

The Elements Irradiation metric in use: an **urban** scene at Warsaw, 2023, Average clarity, ground
albedo 0.2. The open ground points read about **1600 to 1617 kWh/m²**, a little under the
1652.7 kWh/m² in the table above. The difference is expected. The comparison figure is an **unobstructed** horizontal sensor over the **full** year, while this run
is inside a city (surrounding buildings take part of the sky from even the most open point) over
01 January to 30 December. It is what the metric looks like in the tool, not the comparison case:

![Elements annual clear sky](figures/ifc-lens-annual-clear-sky.png)

---

## 5. Reproduce it yourself

### A. The reference (PVGIS)

No dependencies beyond Node 18 or newer, and a network connection:

```bash
node scripts/pvgis_reference.mjs
```

It queries the PVGIS `DRcalc` endpoint month by month, integrates the clear sky series, and prints
the annual figure per site, then the same rows in the exact format of `scene/pvgis-reference.csv`
so you can diff your run against the recorded reference:

```bash
node scripts/pvgis_reference.mjs | sed -n '/csv form/,$p' | tail -n +2 > mine.csv
grep -v '^#' scene/pvgis-reference.csv | diff -u - mine.csv    # no output = identical
```

To check a figure by hand instead, open the PVGIS
[Daily radiation](https://joint-research-centre.ec.europa.eu/photovoltaic-geographical-information-system-pvgis/pvgis-tools/daily-radiation_en)
tool, enter the latitude and longitude, tick **Clear-sky**, and read `Gcs` for each month.

**The script deliberately computes only the reference half.** A comparison script that computes
both columns and is committed next to its own output can no longer fail. Our column comes from the
product, independently, below.

### B. EnergyFlowX, headless

The clear sky model and the solar position math are pure, dependency free kernels, so a whole year
integrates outside the browser in a fraction of a second. In a clone of the EnergyFlowX UI
repository:

```bash
npm ci
node scripts/run-vitest.mjs run src/utils/bim/validation/__tests__/clearSkyAnnual.test.js
```

That test integrates the year from scratch, compares it against the recorded PVGIS figures, asserts
the bracketing at every site, and checks the integration step against a finer one. A pass is the
reproduction.

### C. EnergyFlowX, in your browser

Open the Elements Validation report and read **Pillar 04, Clear sky irradiance**. Our column there
is integrated live in your browser on page load, from the same kernel the tool uses, so it cannot
show a stale number. Only the PVGIS column is recorded.

---

## 6. Files in this folder

```text
clear_sky_irradiation/
  README.md                        this document
  figures/
    pvgis-clear-sky.png                PVGIS clear-sky output (reference)
    ifc-lens-annual-clear-sky.png      EnergyFlowX Elements on the same site
  scene/
    pvgis-reference.csv                the reference result, machine readable
  scripts/
    pvgis_reference.mjs                fetches and integrates the PVGIS reference
```

---

## 7. Licensing and attribution

- **Bird, R. E. and Hulstrom, R. L. (1981)**, *A Simplified Clear Sky Model for Direct and Diffuse
  Insolation on Horizontal Surfaces*, SERI/TR-642-761. Public domain (US DOE / SERI, now NREL).
- **PVGIS**, European Commission Joint Research Centre. Free and open, named here for nominative
  reference only. It is used for this one off comparison. No PVGIS data is bundled into or depended
  on by the application, and nothing of its source, interface or documentation is reproduced.

EnergyFlowX, Elements and the Solar tool are the property of Synerset. See the repository root
for the full license and citation terms.
