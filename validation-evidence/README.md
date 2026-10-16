# Validation evidence

Documented, reproducible comparisons of EnergyFlowX tools with references. Each folder holds a
controlled test case, the result of a reference, the EnergyFlowX result on the same
case, and everything needed to reproduce both (scene files, scripts, dependencies, and step by
step instructions).

The goal is that any engineer can take a folder, run the same comparison, and see the numbers
rather than trust a claim. Results are for review by a professional engineer, who remains
responsible, and none of them is a design certification. The tools named (Ladybug Tools, PVGIS,
pvlib) are used for comparison only and are not affiliated with EnergyFlowX.

## Index

| Area | Module | What it shows | Automated |
| --- | --- | --- | --- |
| [ifc_lens](ifc_lens/solar_module) | Solar, geometry | Direct sun hours compared with Ladybug Tools on a controlled box scene: 6 of 7 points identical, 1 differs by one 5 minute sample | yes, re-run on every commit |
| [ifc_lens](ifc_lens/solar_module/clear_sky_irradiation) | Solar, irradiation | Annual clear sky irradiation compared with PVGIS, a different clear sky model: within 2.8 % at three sites, and our clarity band brackets the PVGIS value | yes, re-run on every commit |
| [ifc_lens](ifc_lens/solar_module/row_shading) | PV, shading | Ray-traced inter-row shading compared with a closed form for the one geometry that has one: the residual falls with finer sampling toward a floor set by the panel's own thickness | yes, re-run on every commit |

More modules and tools will be added here as they mature.

## A note on what a comparison means here

A case in this folder is only evidence if someone else can re-run it and get the same answer, so
each one records the reference in a form that cannot drift: exact counts rather than rounded
figures, with the script and pinned dependencies that produced them. Where the EnergyFlowX side can
be recomputed without a browser, it is also wired into the product's own test suite, so the
comparison fails loudly if the engine moves rather than sitting here going stale.

**Both sides get re-run, not just ours.** A reference nobody ever re-executes is a number, not a
reference: it can be a transcription slip, or a figure from a version of a tool that no longer
behaves that way, and the comparison against it would look immaculate either way. Each case records
when its reference was last regenerated from the original source, and against which version.

**The reference scripts here compute the reference only.** A comparison script that computes both
columns and is committed beside its own output can no longer fail, so the EnergyFlowX column always
comes from the product, independently, by a route each case documents.

Cases carry their tolerance and the reason for it. "Differs by one sampling step" says what the
comparison can resolve. "Agrees closely" says nothing.

## How each case is structured

- `figures/` the reference result and the EnergyFlowX result, side by side.
- `scene/` the input geometry and any read points.
- `scripts/` the code and dependencies to reproduce the reference and rebuild the scene.
- `README.md` the method, the result table, and reproduction steps.

See the [repository root README](../README.md) for the project, licensing, and citation terms.
