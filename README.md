# ENERGY FLOW X (EFX): Engineering Calculation Suite

[<img src="assets/images/short-banner.png" alt="EnergyFlowX" style="width:620px;">](https://energyflowx.com)

> **Professional engineering calculations. From first principles to final numbers.**
> Bridge complex thermodynamic theory and daily engineering practice. Validated, accurate, content-rich, fast, and unit-flexible.

**EnergyFlowX** is a professional-grade web platform for thermophysical property analysis, HVAC process design, fluid mechanics, and browser-native BIM and solar analysis. It is built for HVAC/MEP engineers, mechanical engineers, chemical and process engineers, and the BIM coordinators and PV designers who work alongside them, everyone who needs precise, standards-based numbers and would rather not assume that specific heat is a constant.

| | |
|---|---|
| **Applications** | 41 |
| **Categories** | 7 |
| **Last update** | 2026.09 |
| **Website** | [energyflowx.com](https://energyflowx.com) |

[![Go to EnergyFlowX](https://img.shields.io/badge/VISIT-energyflowx.com-13ADF3?style=for-the-badge)](https://energyflowx.com)

This is not "_just another psychrometrics calculator_". It is a comprehensive engineering software ecosystem, powered by a family of scientific libraries written from scratch, the result of years of development and well over 10,000 hours of personal time. The browser interface you see is merely the crowning jewel, the cherry on top of a very deep cake.

To readers unfamiliar with fluid mechanics and thermodynamics, the calculation forms may look deceptively simple. Trust me, there is nothing simple here once you look behind the curtain.

**No fluid parameter is treated as a constant.** Density, specific heat, viscosity, conductivity, every temperature- and pressure-dependent property is computed from first-principles equations sourced from international standards (IAPWS, ISO, EN, IEC), peer-reviewed literature, or formulations derived independently. The full reference list lives at the end of this document.

[<img src="assets/images/homepage-view.png" alt="EnergyFlowX workspace launchpad" style="width:100%;">](https://energyflowx.com)

---

# TABLE OF CONTENTS

1. [The mission](#1-the-mission)
2. [Why engineers use EFX](#2-why-engineers-use-efx)
3. [Fluids we support](#3-fluids-we-support)
4. [HVAC processes](#4-hvac-processes)
5. [Hydraulics, duct and pipe sizing](#5-hydraulics-duct-and-pipe-sizing)
6. [IFC Lens, BIM in the browser](#6-ifc-lens-bim-in-the-browser)
7. [Elements, the 3D design workspace](#7-elements-the-3d-design-workspace)
8. [The MCP server, EFX inside your AI assistant](#8-the-mcp-server-efx-inside-your-ai-assistant)
9. [Property tables and data tools](#9-property-tables-and-data-tools)
10. [Knowledge, the documentation engineers actually read](#10-knowledge-the-documentation-engineers-actually-read)
11. [Units and flexibility](#11-units-and-flexibility)
12. [Designed for mobile, friendly for wide](#12-designed-for-mobile-friendly-for-wide)
13. [Hydronic, what is being built next](#13-hydronic-what-is-being-built-next)
14. [The engine room, dedicated libraries](#14-the-engine-room-dedicated-libraries)
15. [Engineering practices and numerical methods](#15-engineering-practices-and-numerical-methods)
16. [Architecture and technology](#16-architecture-and-technology)
17. [Security and privacy](#17-security-and-privacy)
18. [Access tiers](#18-access-tiers)
19. [The numbers are computed, not generated](#19-the-numbers-are-computed-not-generated)
20. [Licensing, citation, and attribution](#20-licensing-citation-and-attribution)
21. [Feedback and bug reporting](#21-feedback-and-bug-reporting)
22. [Acknowledgments](#22-acknowledgments)
23. [Reference sources](#23-reference-sources)

---

## 1. THE MISSION

**Liberate engineering calculations.**

Every law of physics was won by brilliant minds who dedicated their lives to chasing the truth, and that knowledge belongs to all of us. It is one of the most precious foundations of our civilisation. Yet the software built on it often sits locked behind licenses that bleed engineers of hundreds to thousands every year, quietly devouring the net margins of the very firms that keep the world running.

Not anymore. Engineers, a heavy cavalry is riding to your aid. Brace, or join the charge.

- **Free to use.** Some tools stay free for good, others are free for testing, and which is which may change over time. Heavy use may be rate limited. In return, please credit and cite the work, share it, and report bugs.
- **Honestly affordable.** A few advanced applications may be paid in the future, or offer limited free access, and some require an active account for testing. Any future pricing will be elastic, affordable, and friendly.

Breaking a monopoly takes a movement. Your trust, your feedback, and spreading the word are what keep calculations free. Use the tools, and tell another engineer.

> _Amicus Plato, sed magis amica veritas._

---

## 2. WHY ENGINEERS USE EFX

EnergyFlowX is built around six promises, and every calculator in the suite is held to them.

- **Validated accuracy.** Results are validated against IAPWS reference formulations, Lemmon et al. Helmholtz-EOS correlations for air, and official property tables using systematic benchmarking. Where applicable, implementations are cross-checked against international standard formulations and published reference data.
- **Fast numerical methods.** Built on robust iterative solvers, including modified Brent-Dekker and Newton-Raphson methods, tuned for convergence stability and computational efficiency.
- **Well tested.** Verified through unit, integration, and regression testing, with independent cross-validation by other engineers wherever possible.
- **Flexible units.** Full SI and Imperial support with consistent internal dimensional handling across every calculation.
- **Independently developed.** Built strictly on science and engineering best practice, with no industrial or commercial influence pulling the numbers.
- **Actively maintained.** Continuously refined, with ongoing improvements, validation updates, and performance work driven by new findings and your feedback.

Each result also ships with a built-in **validation report**, a benchmark of the engine output against reference data, so you can see the agreement instead of taking it on faith. On the BIM side the same principle goes one step further: the solar validation recomputes in your browser on every visit, and the full reproduction is published in this repository for anyone who wants to run it themselves.

---

## 3. FLUIDS WE SUPPORT

EnergyFlowX models **29 fluids across 8 engineering groups**, plus solid-phase ice. Each one returns a full thermodynamic and transport property set, with no constant-property shortcuts. The chemistry is real, the equations of state are reference-grade, and the validity ranges are stated openly.

[<img src="assets/images/natural-gas.png" alt="Natural Gas properties calculator" style="width:100%;">](https://energyflowx.com/fluid-properties/natural-gas/natural-gas)

### Air

| Fluid | Model | Validity | Access |
|---|---|---|---|
| Humid Air | Humid-air mixture model (IAPWS-IF97 water side, Lemmon dry-air EOS, G11-15 virial closure) | −80 to 200 °C, 10 kPa to 5 MPa | Free |
| Dry Air | Lemmon Helmholtz EOS | wide range | Free |

Humid air covers vapour saturation pressure, dew point and wet bulb temperatures, relative humidity, humidity ratio and maximum humidity ratio, specific enthalpy (including water-mist and ice-mist components), density, specific heat, viscosity, thermal conductivity, thermal diffusivity, and Prandtl number, with enhanced fugacity per IAPWS G11-15.

### Water and Steam

| Fluid | Model | Coverage | Access |
|---|---|---|---|
| Water (liquid) | IAPWS-IF97, R12-08, R15-11 | Region 1 plus transport properties | Free |
| Steam | IAPWS-IF97 | Full Regions 1 to 5, backward equations p(h,s), v(p,T) | Free |

Density, enthalpy, entropy, specific heat (Cp, Cv), speed of sound, isothermal compressibility, thermal expansion, viscosity, thermal conductivity, and surface tension, across compressed liquid, superheated vapour, near-critical, two-phase, and high-pressure regions.

### Natural Gas

| Fluid | Model | Output | Access |
|---|---|---|---|
| Natural Gas | GERG-2008 (ISO 20765-2), ISO 6976 | Density, compressibility Z, heat capacities, speed of sound, calorific value, Wobbe index | Free |

A multi-fluid Helmholtz equation of state for mixtures of up to 21 components, with composition presets or a fully custom blend.

### Process Gases

| Fluid | Formula | Model | Validity | Access |
|---|---|---|---|---|
| Hydrogen | H₂ | Helmholtz EOS | −259 to 727 °C, ≤ 100 MPa | Free |
| Carbon Dioxide | CO₂ (R-744) | Span-Wagner EOS | −57 to 827 °C, ≤ 200 MPa | Free |
| Ammonia | NH₃ (R-717) | Helmholtz EOS | −78 to 407 °C, ≤ 50 MPa | Free |
| Propane | C₃H₈ (R-290) | Helmholtz EOS | −188 to 352 °C, ≤ 100 MPa | Free |
| Nitrous Oxide `NEW` | N₂O | Short-form Helmholtz EOS, ECS transport | −91 to 252 °C, ≤ 50 MPa | Free |

Every process gas also reports surface tension at the saturated liquid-vapour interface, from the recommended correlations of Mulero, Cachadiña and Parra (2012). It depends on temperature alone and falls to zero at the critical point. Carbon dioxide viscosity includes its near-critical enhancement.

### Cryogens `NEW`

The gases that industry handles cold and liquid, each on its own reference equation of state rather than on one correlation stretched across the group. Air separation, LNG, cryogenic storage and low-temperature test rigs all live down here, and this is exactly the region where an ideal-gas shortcut stops being an approximation and starts being wrong.

| Fluid | Formula | Model | Validity | Access |
|---|---|---|---|---|
| Nitrogen | N₂ | Span et al. reference EOS | −210 to 727 °C, ≤ 2200 MPa | Free |
| Oxygen | O₂ | Schmidt-Wagner reference EOS | −219 to 727 °C, ≤ 82 MPa | Free |
| Argon | Ar | Tegeler-Span-Wagner reference EOS | −189 to 427 °C, ≤ 1000 MPa | Free |
| Helium | He | Ortiz Vega et al. EOS | −271 to 1227 °C, ≤ 1000 MPa | Free |
| Methane | CH₄ | Setzmann-Wagner reference EOS, LNG | −182 to 352 °C, ≤ 100 MPa | Free |

Helium is modelled as normal-fluid helium I only. Below the lambda point at about 2.18 K the substance becomes a superfluid that this equation does not describe, and the calculator stops there rather than extrapolating into it. Like the process gases, every cryogen reports surface tension at the saturated interface.

### Refrigerants

Eight working fluids, pure and blended, identified by standardised R-numbers, with ISO 817 safety classification surfaced alongside the physics.

| Fluid | Composition | Model | Validity | Access |
|---|---|---|---|---|
| R-134a | C₂H₂F₄ | Helmholtz EOS | −103 to 182 °C, ≤ 40 MPa | Member |
| R-1234ze(E) | C₃H₂F₄ | Helmholtz EOS | −104 to 147 °C, ≤ 100 MPa | Member |
| R-1234yf | C₃H₂F₄ | Helmholtz EOS | −53 to 137 °C, ≤ 30 MPa | Member |
| R-32 | CH₂F₂ | Helmholtz EOS | −23 to 147 °C, ≤ 30 MPa | Member |
| R-125 | C₂HF₅ | Helmholtz EOS | −43 to 167 °C, ≤ 20 MPa | Member |
| R-410A | R-32 / R-125 | Multi-fluid Helmholtz (blend) | −73 to 147 °C, ≤ 35 MPa | Member |
| R-407C | R-32 / R-125 / R-134a | Multi-fluid Helmholtz (blend) | −73 to 147 °C, ≤ 35 MPa | Member |
| R-454B | R-32 / R-1234yf | Multi-fluid Helmholtz (blend) | −73 to 147 °C, ≤ 35 MPa | Member |

The blends are solved as real mixtures on a multi-fluid Helmholtz model with fitted binary parameters, not as pseudo-pure fluids. R-1234yf uses the 2022 international standard formulation of Lemmon and Akasaka, R-454B the 2023 R-32/R-1234yf binary of Bell, and the viscosity of R-32, R-1234yf and R-1234ze(E) comes from dedicated reference correlations. The pure refrigerants also report surface tension at the saturated interface.

### Glycols

| Fluid | Model | Validity | Access |
|---|---|---|---|
| Ethylene Glycol | Aqueous-solution model | freezing point to 100 °C, 0 to 60 % mass | Free |
| Propylene Glycol | Aqueous-solution model | freezing point to 100 °C, 0 to 60 % mass | Free |

### Brines

| Fluid | Model | Validity | Access |
|---|---|---|---|
| Calcium Chloride Brine | Aqueous-solution model | freezing point to 40 °C, 0 to 30 % mass | Member |
| Ethanol Brine | Aqueous-solution model | freezing point to 40 °C, 0 to 60 % mass | Member |
| Methanol Brine | Aqueous-solution model | freezing point to 40 °C, 0 to 60 % mass | Member |
| Potassium Formate Brine | Aqueous-solution model | freezing point to 40 °C, 0 to 48 % mass | Member |

Concentration-dependent freezing-point limits are built in, so the model knows where the fluid actually stops being a liquid.

### Solid Properties

| Material | Model | Coverage | Access |
|---|---|---|---|
| Ice (Ice Ih) | Gibbs energy EOS, IAPWS R10-06 | Density, enthalpy, entropy, heat capacity, compressibility, thermal expansion, melting and sublimation curves | Free |

Every group has its own tab in the [validation report](https://energyflowx.com/reports/validation), where the engine is run against published reference points and the agreement is shown property by property.

---

## 4. HVAC PROCESSES

Beyond raw properties, EnergyFlowX computes the processes engineers actually design around. Every process uses real humid-air thermodynamics, not constant-property approximations, and reports the full state of every air stream involved. All four are **free**, with no account required.

[<img src="assets/images/hvac-process-hr-recovery.png" alt="AHU heat recovery process calculator" style="width:100%;">](https://energyflowx.com/hvac-processes/heat-recovery)

**Air Heating.** Solve for a given input power, a target outlet temperature, or a target outlet relative humidity.

**Air Cooling with condensate discharge.** The same three solving modes, plus an optional coolant secondary-side calculation, with condensate tracked through the energy balance the way a real coil behaves.

**Air Mixing.** Two-stream mixing with full humidity content, or multi-stream recirculation mixing of up to 20 air streams in a single pass.

**AHU Heat Recovery `NEW`.** A serious heat-recovery engine built to EN 308, using the ε-NTU method. Solve from a given effectiveness, for a target supply temperature, or for a target recovered power. It supports sensible, latent, enthalpic, and total recovery, air-to-air and air-to-water configurations, frost and defrost diagnostics, and condensate tracking, with the capacity-rate asymmetry correction that separates a textbook answer from a usable one.

These processes can be reasoned about individually, or chained so that the output of one feeds the input of the next, which is exactly how a real air handling unit is assembled section by section.

---

## 5. HYDRAULICS, DUCT AND PIPE SIZING

The hydraulics suite sizes ventilation ducts and piping against real fluid properties and real market products, not nominal tables.

[<img src="assets/images/hydraulics-ducts.png" alt="Duct sizing calculator with heatmap" style="width:100%;">](https://energyflowx.com/hydraulics/duct-sizing-calculator)

**Duct Sizing** and **Pipe Sizing** (both free) share a multi-criteria sizing engine that is a genuinely rare animal on the market. Most sizing tools force a choice: either a fixed catalogue from one manufacturer, or a generic table, or a standard's nominal series. EnergyFlowX puts **manufacturer data, standard series, and generic geometry into one flexible, universal sizing tool**, switchable on the fly. To the best of our knowledge no other tool does all three in a single calculator. It handles:

- Circular and rectangular cross-sections,
- Flow velocity and Reynolds number,
- Linear pressure loss and linear resistance,
- Colebrook-White friction factor solved iteratively, with a Vatankhah explicit approximation as the initial guess,
- Minor (local) pressure losses via loss coefficients (ζ),
- Linear mass density derived from construction materials and insulation layers,
- A master-data database of real market duct and pipe products, filterable by application, pressure class, leakage class, and material.

On top of the numbers, a **heatmap chart** sweeps a full dimension series at once and adds a layer of insight a single result cannot give. It shows, across the whole catalogue range, exactly where your flow lands in the optimal-velocity band, so the acceptable sizes light up and the rejected ones do not. The acceptance criteria (velocity limit, aspect ratio, distribution-duct zone, pressure-drop budget) are all visible and adjustable, so the tool argues its case rather than just handing you a number.

---

## 6. IFC LENS, BIM IN THE BROWSER

**IFC Lens** (Free) is a full in-browser IFC model viewer. It opens Industry Foundation Classes building models, the open, vendor-neutral BIM exchange standard maintained by buildingSMART, and parses and renders them entirely on your device with WebAssembly and WebGL. Nothing is uploaded to a server, which keeps your design data private and removes the bandwidth limits cloud viewers hit on large files.

[<img src="assets/images/lens-what.webp" alt="IFC Lens with an IFC building model open in a browser tab, the Models panel listing the loaded file and its element count." style="width:100%;">](https://energyflowx.com/ifc-lens)

*A 10.3 MB IFC file with 676 elements, parsed inside the browser tab. The Models panel keeps IFC models, imported CAD and mesh files, Modeler solids, vegetation and OpenStreetMap surroundings as separate layers, each with its own visibility.*

The viewer auto-detects the schema of each file and supports **IFC2x3, IFC4, and IFC4x3**, so models move between authoring tools, analysis software, and facility-management systems without lock-in. Alongside IFC it reads **STEP and STP** CAD parts, which arrive as editable B-rep solids rather than frozen meshes, and the **GLB, glTF, OBJ and STL** mesh formats. Everything you open lands in one inventory, grouped by what it is rather than by when it arrived, and several IFC models can be overlaid as separate disciplines without merging the files.

### Loading and managing models

Drag one or more files onto the viewport, or load them from the toolbar. Multiple models live side by side, each listed with its element count and size, and each can be shown, hidden, or unloaded independently. Without files of your own, a built-in set of discipline samples (architecture, structure, HVAC and more) loads in a click.

### Structure tree, properties, and search

The structure panel browses the model two ways: **Spatial** groups elements by the storey they sit in (the *where*), and **Class** groups them by IFC entity type such as WALL or SLAB (the *what*), each with a live filter. Select any element to frame it and read its full property sets (Psets) and quantities, with copy buttons and an adjustable significant-digits readout. The search box accepts a numeric expressID or a 22-character IFC GlobalId, and on a hit it frames the element and turns the rest of the model to x-ray so an internal component stays visible.

[<img src="assets/images/lens-inspect.webp" alt="The Properties panel showing an element's IFC property sets and its quantity table, beside the CSV takeoff export dialog." style="width:100%;">](https://energyflowx.com/ifc-lens/knowledge/properties)

*Property sets and quantity sets are shown exactly as the file carries them, original names and all, with no re-interpretation. The takeoff exports either the current selection or the whole model to CSV, with the column set and the precision you choose.*

### Navigation and standard views

Orbit, pan, and zoom on desktop or touch, with a live X/Y/Z gizmo (IFC is Z-up). Fit-all, reset-and-centre, an **orthographic / perspective** toggle (orthographic keeps parallel lines parallel for clean measuring), and one-tap **standard views** for Top, Bottom, Front, Back, Left, Right, and Isometric.

### Advanced sectioning and clipping

Three independent ways to cut the model:

- **Quick section planes.** Toggle an X, Y, or Z (elevation) plane and drag its slider or grab the plane in the view. Slide Z down past the roof and you are looking at a clean floor plan.
- **Advanced sectioning with saved views.** Keep only the slab between a lower and upper level along Z-plan, X, or Y, then create a named view that locks the camera to the matching plan or elevation and persists across sessions. Unlock to orbit, and drag the band edges to resize the slab live.
- **Box section (3D crop).** Box the whole model, or centre a crop box on a selected element, then drag the box faces in the view or type exact X/Y/Z bounds.

### Colorize by data

**Color by** IFC Class, Spatial storey, MEP System, IFC Property, Quantity, by model, or by selected GUID/ID. Rule-driven sources share one workflow: pick a value present in the model, or type a wildcard with `*` (for example `IFCWALL*` or `*SUPPLYAIR*`), first matching rule wins, anything unmatched falls into **Other**. Numeric properties and quantities colour by value ranges. In the legend you recolour swatches, set per-group opacity, or exclude a group so it keeps its native material. Each **Apply** snapshots the legend as a reusable **layer**, and layers coexist so you can stack, for instance, a class colouring under a system colouring. Paste the GUIDs from a clash report and spotlight the offenders against the rest of the model.

Colouring also shows what a model is missing. Colour by a property that half the elements do not carry and the gap appears as a block of **Other**, which is easier to read than a schedule full of empty cells.

### MEP systems awareness

IFC Lens reads IFC system data (`IfcSystem`, `IfcDistributionSystem`, and the assignment links), so supply air, exhaust, chilled water, and electrical can each be coloured and isolated as separate systems. The Knowledge pages include a Revit export checklist for the most common reason MEP colouring shows nothing.

### Site, terrain and surroundings

The **Geo** tool places the model in the real world. It reads the georeference straight from the file, either the IfcSite latitude and longitude or an IfcMapConversion with a projected CRS, and falls back to an address search or pasted coordinates when a file carries none. With your consent it drapes an open basemap (OpenStreetMap tiles) and, where one exists, a real **terrain model** under the building, oriented to true north, so the site sits at its actual elevation rather than on a flat plane.

**Measured terrain.** Where a public LiDAR survey covers the site, the ground under the model is measured bare ground at 1 m rather than a surface model: today in England, from the Environment Agency LIDAR Composite DTM (Open Government Licence v3.0), read on our server and placed with Ordnance Survey's OSTN15 transformation, which reproduces Ordnance Survey's published test points to the millimetre. In Scotland, where a public survey has been flown, the ground comes from the Scottish Public Sector LiDAR at 50 cm to 1 m (Open Government Licence v3.0), read on our server for areas up to about 1.4 km across. Switzerland gets swissALTI3D bare-ground terrain. Everywhere else the global Terrain Tiles surface model is used, which follows rooftops and canopy, and the credit line under the map always names the model that was drawn. A survey is a snapshot: ground changed after it was flown reads as it was then.

**Measured neighbours and relief.** Where the Environment Agency's LiDAR covers the site in England, three more things appear, each only where the survey reaches, and in Scotland measured building heights and the relief basemap appear where its public survey reaches (there is no Scottish canopy model). Imported surrounding buildings are measured on our server, surface model minus bare-ground terrain inside each footprint at 1 m, using the pixels where the first and last laser returns agree, so trees over a roof neither raise the height nor hide it silently (such buildings are counted in the panel as possibly reading low). You choose per project whether buildings are drawn from **map data** (the height tag or storey count, with the measurement only where the map has neither) or from **LiDAR** (the measurement, with the map only where the survey has none), and a height you type wins under both. **Measured canopy** adds the trees our server finds in the Environment Agency Vegetation Object Model beside the map's own trees, hiding any map tree inside a measured crown, and switching it off restores them. A **Relief** basemap shades the measured bare ground on our server, so slopes and earthworks read at a glance. The surveys date from 2000 to 2022 (vegetation 2016 to 2021), so anything built or felled since reads as it was then.

**Planning designations and postcodes.** Where the planning data covers the site, today in England, the Geo tool lists the conservation areas, listed buildings, Article 4 direction areas, flood zones and other designations around it, from planning.data.gov.uk (Open Government Licence v3.0). It separates what is on the site (the site location lies inside the outline, or the outline comes within 25 m of it) from what is nearby, with how far and which way, and tints, outlines and names each one on the ground map in its list colour (hatched where kinds overlap, flood zone 3 darker than zone 2). Hovering or picking a designation in the list or on the map highlights it in both, and picking one in the list takes the view there. The PV tool adds one line when a designation on the site may affect rooftop panels. It names designations and points to the local planning authority, never a planning rule, and it always says the record is incomplete: a site with nothing listed may still be designated, and when the data cannot be read the panel says so instead of showing an empty list. In Great Britain a postcode typed into the search resolves from the ONS Postcode Directory, which our server imports from each quarterly release, so a postcode it finds never reaches a third party. Northern Ireland postcodes are not imported, because their data is licensed for internal business use only, and go to the general place search.

The same tool imports the **surroundings**: neighbouring buildings and street trees within a radius you choose, from OpenStreetMap or from 3D city files. A **DXF drawing or a scanned image** can be aligned underneath by two known points or a known distance, which is how a survey or an old plan becomes a tracing underlay. Everything that reveals a location stays behind an explicit opt-in, and the geometry still never leaves your device.

[<img src="assets/images/lens-context.webp" alt="A model placed on an OpenStreetMap basemap, with several hundred surrounding buildings and street trees imported around it." style="width:100%;">](https://energyflowx.com/ifc-lens/knowledge/site-context)

*Surroundings imported within a chosen radius, here 666 buildings and 415 trees. In Elements this same context is what casts shadows onto the model and obstructs the wind field. Map data © OpenStreetMap contributors, ODbL.*

### Measurement and notes

Five measurement modes run on the same client-side geometry, with snapping (green to a vertex, blue to an edge, orange to a face): **Distance** (with the angle to a snapped edge, flagging ⟂ 90° when square), **Area** (exact for any planar outline, concave shapes included), **Angle**, **Volume** (read from the IFC quantity, with a bounding-box fallback), and **Probe** for exact X/Y/Z coordinates relative to the elevation datum.

[<img src="assets/images/lens-measure.webp" alt="Several measurements taken on a model at once: a distance, a polygon area, an angle, a bounding volume and a probed point coordinate." style="width:100%;">](https://energyflowx.com/ifc-lens/knowledge/measuring)

*Distance, area, angle, volume and point-coordinate probes, each snapped to real model geometry rather than to whatever the cursor happens to be over. Measurements persist together, so a set can be read side by side.*

### IDS quality checking, with a builder

**IDS** (Information Delivery Specification) is the buildingSMART standard for machine-readable model requirements, for example "every wall must carry a fire rating". Load an `.ids` file and every rule reports its applicable, pass, and fail counts. Expand a failed rule to see each failing element with the reason it failed, click to frame it, highlight all failures in red, and download a Markdown or HTML report with model metadata and a timestamp. The bundled **IDS Builder** goes the other way: author specifications with autocomplete from the model's real classes and Psets, test them live against the loaded model, and export a valid `.ids` file.

[<img src="assets/images/lens-ids-bcf.webp" alt="The IDS builder editing a specification: an entity applicability facet on IFCWALL, and a required Name attribute matching a regular expression." style="width:100%;">](https://energyflowx.com/ifc-lens/knowledge/ids-and-bcf)

*Authoring a buildingSMART IDS specification against the open model. Applicability and requirement facets autocomplete from what the model contains, and the specification can be tested against it before the `.ids` file is exported.*

### BCF issue coordination

**BCF** (BIM Collaboration Format) is the buildingSMART standard for exchanging issues without sending the model. Author topics with a saved viewpoint, the involved elements, a snapshot, type, status, and priority, then export a `.bcfzip` that opens in Revit, Navisworks, Solibri, or BIMcollab. Open issues someone sent you, restore their exact viewpoint and selection, reply or change status, and export the reviewed file back, all in the browser.

### Projects, notes, and getting the work back out

Models, notes, measurements and view state save into a single **project file**, and a *Save with models embedded* option carries the model bytes along, so the project opens on another machine with nothing else to send. **Notes** are pinned in the scene where the finding is, so they keep their place as the camera moves, and they export as BCF 2.1, which is how a note made here becomes an issue in somebody else's tool.

[<img src="assets/images/lens-work.webp" alt="A finding pinned to the model as an in-scene note, beside the colourise legend and the BCF issue panel it can be exported to." style="width:100%;">](https://energyflowx.com/ifc-lens/knowledge/projects-and-notes)

*A pinned note, the colourise legend that produced the view, and the BCF panel the finding leaves through. A BCF issue carries a viewpoint, a camera position, a snapshot and the elements concerned, not just a comment.*

On the way out there is a quantity takeoff to CSV scoped to the selection or the whole model, geometry export back to **GLB, OBJ and STL**, screenshots, and a **viewport recorder** that captures the 3D view to a WebM video with optional microphone narration.

### Shortcuts, and using the right GPU

Every command has a keyboard shortcut, the full list is documented, and the bindings can be remapped with conflict detection. There is also a page for a common laptop problem. A laptop with two graphics adapters often runs a WebGL viewer on the integrated one. The browser and operating-system settings that move it to the dedicated GPU are written down, because that one switch is usually the biggest performance win.

### The manual, thirteen topic pages

The IFC Lens and Elements manual is published as a documentation cluster of thirteen topic pages under two hubs, [`/ifc-lens/knowledge`](https://energyflowx.com/ifc-lens/knowledge) and [`/elements/knowledge`](https://energyflowx.com/elements/knowledge), covering formats, properties and takeoff, measuring and sectioning, IDS and BCF, site and context, projects and notes, shortcuts and performance, and on the Elements side solar, weather, wind, PV yield, trees and the modeller. Each has its own URL you can send to a colleague.

IFC Lens is built on the open-source [That Open Engine](https://github.com/ThatOpen/) BIM toolkit, the WebAssembly [web-ifc](https://github.com/ThatOpen/engine_web-ifc) parser, and Three.js, all gratefully acknowledged in the references below. The bundled demonstration model is the buildingSMART PCERT Sample Scene.

---

## 7. ELEMENTS, THE 3D DESIGN WORKSPACE

**Elements** `NEW` is the analysis and authoring half of the BIM stack, sharing the same scene, the same models and the same on-device privacy as IFC Lens. Elements puts the building somewhere real, on a date, under a sun and in a wind, and lets you author the geometry that is not in the file yet. Entry is free, and the sun, shadow, wind and tree studies run on your machine. Measured weather (the typical-year download and the EPW parse) and the photovoltaic yield model are the members-only pieces. They run on the server, gated inside their panels.

[<img src="assets/images/el-what.webp" alt="An IFC building shaded by a sun-hours heatmap, with the sun path arc overhead and probe readings on several facades." style="width:100%;">](https://energyflowx.com/elements)

*Sun hours computed on the model's own surfaces over a chosen day or a whole year, read against a 0 to 13 hour scale. Probe points return the value at an exact coordinate, so a facade or a single window can be checked rather than eyeballed.*

### Weather, a real year instead of an assumption

Clear-sky physics assumes a cloudless sky on every day of the year, so it gives the potential of a site, an upper bound rather than what the site will deliver. To move from potential to an expectation for a real place, Elements downloads a measured **typical meteorological year** for the site coordinates, or parses an **EPW** file you already have. Photovoltaic yield never falls back to clear-sky silently. It waits until you have either loaded measured weather or chosen clear-sky on purpose, and every clear-sky figure it reports is labelled as overestimated. The Knowledge page is explicit about what each dataset does and does not tell you, because a TMY is a synthesised representative year rather than a forecast, and treating it as one is how a yield study quietly goes wrong.

### Sun path, shadows and sun hours

The **Solar** tool casts a real sun over the model for the site and a chosen date. A draggable time-of-day scrubber and a play button sweep the day while the sun arc, a seasonal band, a horizon compass, and live hard shadows update as the sun moves. Glazing lets the sun through.

On top of the live shadow it computes **direct sun hours** over the whole day, painted as a heatmap on the ground and on building surfaces, with four readings: plain sun hours, an incidence-weighted exposure score for PV siting, shade hours, and an opt-in clear-sky irradiation in kWh/m². A scoring mode bins the result into suitability tiers, and a compliance mode colours pass or fail against a minimum-hours threshold for right-to-light and overshadowing checks, with named building-code presets. Click a point to read its value, or paste a whole list of coordinates and have every point read and pinned at once.

The sun position uses the NOAA solar algorithm, and the live occlusion is a GPU shadow map checked against a ray-traced closed-form oracle. The validation is published.

[<img src="assets/images/el-solar.webp" alt="A district-scale sun-hours study, the heatmap covering the terrain, the model and the surrounding buildings alike." style="width:100%;">](https://energyflowx.com/elements/knowledge/solar)

*The same study at district scale, with terrain, building and surroundings all carrying the heatmap. Neighbouring blocks shade each other, which is why the context is loaded.*

### Photovoltaic yield, through to LCOE

Lay photovoltaic arrays on a roof, on a facade or on the ground, and Elements takes them from irradiance to a bankable number. There is no default weather. Once the site location is set, the panel asks for a **weather basis** before anything else: load measured weather for a real-site yield, or choose clear-sky deliberately. Clear-sky stays available for comparing layouts, but its yield, its economics and its CSV and PDF reports all state that the figures are overestimated. The chosen irradiance source feeds a **plane-of-array transposition** (isotropic Liu and Jordan, or the Perez anisotropic model with its circumsolar and horizon terms), passes through a cover-glass **incidence-angle modifier**, and meets the **shading** cast by the geometry in the scene, ray-traced rather than allowed for. Shading is charged electrically, not by area: a module's cells are wired in series, so a shadow touching one cell costs the whole bypass-diode group that cell sits in, and loss against shaded area is a step rather than a line. That is also why mounting orientation changes the answer. A low shadow along the bottom edge of a **portrait** module clips all three of its substrings at once, where the same shadow on the same module mounted **landscape** reaches one and leaves two thirds of it working. Cell temperature, inverter clipping and the system loss budget turn irradiation into AC energy, and degradation, a P50/P90 band and a discounted cash flow turn AC energy into money.

A **self-shading tilt and azimuth optimiser** searches the orientation for you, accounting for row-to-row shading rather than ignoring it. Fixed and single-axis tracking mountings are both supported, backtracking included. That row-to-row shading is checked against a closed-form solution for the one arrangement that has one, and the case is published with its scene, its scripts and every measurement behind it in [validation-evidence/ifc_lens/solar_module/row_shading](validation-evidence/ifc_lens/solar_module/row_shading).

[<img src="assets/images/el-pv.webp" alt="Three photovoltaic arrays laid out on a roof and on the ground, with the yield and financial results for the selected array." style="width:100%;">](https://energyflowx.com/elements/knowledge/pv)

*Array layout with a self-shading tilt and azimuth optimiser, here 42 degrees facing due south. Results carry AC energy, specific yield, performance ratio, operating cell temperature, P50 and P90, LCOE, payback, NPV and IRR, and export to CSV or PDF.*

### Wind, screening-level

The **Wind** tool solves a **D3Q19 lattice-Boltzmann** flow field with large-eddy turbulence around the model, live on the GPU. Drive it with a logarithmic or Eurocode terrain-category inlet profile, or with a points table of your own heights and velocities. It paints velocity and pressure on resolve planes and reads values at probe points, for an early read on shelter, funnelling, and exposure between buildings.

The solution runs on a thin slab at a capped Reynolds number, and the Knowledge page names the canonical benchmarks the solver is checked against and states where the line sits between a validated solver and a design-grade wind study. This is a screening aid for orientation and massing, not a certification.

[<img src="assets/images/el-wind.webp" alt="A vertical slice through a wind field around a site, coloured by speed, with the logarithmic inlet profile plotted beside it." style="width:100%;">](https://energyflowx.com/elements/knowledge/wind)

*A lattice-Boltzmann flow field solved live on the GPU. The inlet here is a logarithmic profile, 10 m/s at 10 m reference height over a 0.05 m roughness length.*

### Trees that shade like trees

Trees are modelled as **partial occluders**, with Beer-Lambert attenuation through an ellipsoidal crown and a leaf-density knob that sets its transmittance, so a canopy dims the sun rather than switching it off. A seasonal blend thins a deciduous crown through the year. Place trees singly, fill them into a shape, run them along a boundary or drop them onto a face, and the shade they cast reaches both the sun-hours bake and the PV ray-trace.

[<img src="assets/images/el-veg.webp" alt="Trees placed around a building by area fill and along a boundary line, with the vegetation panel showing species and crown dimensions." style="width:100%;">](https://energyflowx.com/elements/knowledge/vegetation)

*Trees placed singly, filled into a shape, run along a boundary or dropped onto a face, here 95 of them. Species, age, trunk and crown dimensions and leaf density all feed the shade they cast.*

### The Modeler, B-rep CAD in a browser tab

Some of what a study needs is never in the IFC file: a proposed extension, a neighbouring block that has not been built yet, a screen, a canopy. The **Modeler** authors it as true **B-rep** geometry rather than meshes, running an Open CASCADE Technology kernel compiled to WebAssembly in a worker thread. Sketches on work planes, solid primitives, booleans, fillets and chamfers, face pull and scale, mirroring, and **STEP import as editable solids**. Because it is B-rep and not a mesh, a face can be pulled and its dimension typed to an exact value instead of dragged until it looks about right.

[<img src="assets/images/el-modeler.webp" alt="A B-rep solid being edited in the browser modeller, with live dimensions on the move being typed to an exact value." style="width:100%;">](https://energyflowx.com/elements/knowledge/modeler)

*The in-browser B-rep modeller, running an OCCT kernel in a worker thread. Solids, booleans and sketch geometry are true B-rep, so a dimension is typed rather than dragged.*

### Validation you can check yourself

A **Validation** tab checks the analysis tools instead of asking you to trust them. The Solar module is validated three ways, each recomputed live in your browser on every visit: the sun position against NREL SPA published values and an independent ephemeris, the occlusion against a closed-form analytic shadow, and the end-to-end sun hours cross-checked against Ladybug Tools, a recognised open-source solar library, on a controlled scene. The clear-sky irradiation is cross-checked against PVGIS. We are not trying to copy any one program. We implement the same accepted physics independently and show that the answers land in the same place.

The full reproduction (the scene file, the read points as a CSV, the reference scripts, the dependencies, and step-by-step instructions) is published in this repository under [validation-evidence](validation-evidence). Clone it and run it yourself.

---

## 8. THE MCP SERVER, EFX INSIDE YOUR AI ASSISTANT

`NEW` EnergyFlowX exposes a curated, read-only slice of its engine over the **Model Context Protocol**, so an LLM assistant (Claude Code, Claude Desktop, Cursor, VS Code, or any MCP client) can call the same validated physics you get in the browser, **with the method and the validity range attached to every number**. It is the antidote to asking a chatbot for a fluid property and being handed a confident guess.

The server speaks streamable HTTP at `https://energyflowx.com/energy-flow-x/mcp`, and the [`/mcp-server`](https://energyflowx.com/mcp-server) page carries the exact configuration snippet for each client, with API-key management in your account settings.

| Tool | What it answers |
|---|---|
| `get_fluid_properties` | Properties at a state for nearly every supported fluid, including humid air (from RH, humidity ratio, wet bulb or dew point) and steam (from any two of p, T, h, s, x). |
| `get_natural_gas_properties` | GERG-2008 properties plus ISO 6976 calorific value and Wobbe index, from a preset or an explicit composition. |
| `list_fluids` | The catalogue: every fluid, the state inputs it accepts, its validity range, its method, and its access tier. |
| `get_saturation_properties` | Saturation of a pure fluid, boiling temperature at a pressure or the reverse, phase densities, latent heat, critical and triple points. |
| `get_solid_properties` | Ice properties. |
| `convert_units` | Unit conversion, plus a discovery call listing which symbols a quantity accepts. |
| `search_conduit_catalog` | Standard pipes and ducts by code or manufacturer: shape, wall roughness, available nominal sizes. |
| `size_conduit` | Sizes one pipe or duct: velocity, pressure drop, Reynolds number, friction factor, flow regime. |

Every tool is **read-only, idempotent and closed-world**, and advertises itself as such, so a client does not stop to ask permission for a lookup. Inputs carry their own units as strings (`"20oC"`, `"1.5bar"`, `"70degF"`, `"8g/kg"`), and each response key names the unit it actually produced, so what you received is visible in the payload rather than inferred. A parameter sweep is one call with a list of states rather than a loop. The same access policy that gates the website gates the tools: most fluids are open, the refrigerants and brines want a free account.

---

## 9. PROPERTY TABLES AND DATA TOOLS

Sometimes you do not want a single point, you want a table. The property-table generator turns any supported fluid into tabulated data over a varying parameter, with fixed parameters held constant, a configurable start, end, and step, selectable significant digits, and a column picker so you only export what you need.

[<img src="assets/images/table-generation-feature.png" alt="Property table generation" style="width:100%;">](https://energyflowx.com)

Results render in the browser and export straight to CSV, ready for a spreadsheet, a report, or a regression test of your own. Bulk table export asks for a free account, because a table generator is the surface a scraper would reach for first.

---

## 10. KNOWLEDGE, THE DOCUMENTATION ENGINEERS ACTUALLY READ

Every calculator ships with a dedicated **Knowledge** page. Not a tooltip, a real documentation article: the physical model used, how to drive the calculator, identity and safety data, validity ranges, blends and glide behaviour, applications, and a fully cited standards-and-sources panel.

[<img src="assets/images/knowledge-pages.png" alt="EnergyFlowX knowledge and articles" style="width:100%;">](https://energyflowx.com)

The intent is simple. You should be able to defend the number you produced, because the tool tells you exactly which standard it came from and where that standard stops being valid.

The whole set is indexed at [`/knowledge`](https://energyflowx.com/knowledge), which now spans the fluid groups, the HVAC processes, the sizing calculators, and the thirteen-page BIM cluster described above. Every article carries its own cited sources panel, and the numbers quoted in the prose are checked against the engine rather than typed from memory.

---

## 11. UNITS AND FLEXIBILITY

EnergyFlowX speaks both **SI and Imperial**, fluently, with consistent dimensional handling under the hood. Inputs are entered as a value with a unit, validated live, and converted on the fly. Outputs can be overridden per quantity, so pressure in kPa, temperature in K, and flow in m³/min can all coexist on the same screen if that is how your project specifies them.

The whole interface is deliberately **lightweight and fast**. The classic application screens favour vector graphics over heavy raster images, and the pages are built for content density and daily professional use rather than decoration.

---

## 12. DESIGNED FOR MOBILE, FRIENDLY FOR WIDE

Plenty of engineering tools claim to be responsive, then collapse the moment you open them on a phone. EnergyFlowX was **designed, prepared, and tested for a wide variety of mobile devices**, right down to narrow-screen phones, because real engineers check numbers on site, in a plant room, on a train, not only at a desk. The very same layout stretches gracefully the other way too, looking sharp and spacious on wide desktop monitors.

[<img src="assets/images/mobile-view.png" alt="EnergyFlowX mobile view on a narrow-screen phone" style="width:320px;">](https://energyflowx.com)

This is not a desktop layout shrunk until it fits. The workspace, the calculators, the property tables, and even the 3D IFC Lens reflow for touch: dedicated mobile navigation, a search affordance and a share sheet in the header, single-column card grids, tables that scroll cleanly, and full touch gestures in the viewer (one finger to orbit, two to pan, pinch, and twist). Inputs stay large enough to tap, units stay editable, and nothing important hides off-screen.

The result is a tool you can actually trust in your hand, with the same physics and the same precision as the full desktop experience, just folded sensibly onto a smaller screen.

---

## 13. HYDRONIC, WHAT IS BEING BUILT NEXT

Everything above computes a state, a process, or a single conduit. **Hydronic** is the application that computes a whole *network*, and it is the one the rest of the platform has been building toward.

[<img src="assets/images/hydronic-builder.webp" alt="The Hydronic design builder: a piping network drawn on a canvas with equipment blocks, control cables and a results table." style="width:100%;">](https://energyflowx.com/hydronic)

Draw the system, pick the fluid, place sources, demands, vessels, pumps and valves, attach control logic, and solve it. Not a branched tree cut down to something a spreadsheet can handle, but **any topology**, rings and interconnected loops included, with as many sources and demand points as the system actually has, solved numerically with no hand-balancing and no guesswork.

Three things make it different from a sizing tool with a diagram on top:

- **Every utility in one model.** A compressed-air plant whose compressor is water-cooled, with that heat recovered to preheat service water, is normally two or three tools stitched together by hand. Here the systems share one model, air, water, and the heat moving between them.
- **The fluid you actually run.** Glycol at the concentration you really use rather than the nearest table entry. Natural gas of a custom composition. Superheated single-phase steam from reference-grade formulations. The properties come from the same engine as the rest of the suite.
- **Static, or watch it move.** Steady state when that is enough, and transient analysis with a configurable time step and device-activation criteria when it is not, with probes placed anywhere on the network reading exactly what you want to know.

The module rollout starts with **compressed air**, then water networks, heating circuits, HVAC rooms and zones, and steam distribution. The solver underneath, `flow-symphony`, is already built and already runs the multi-fluid, thermally coupled cases described in the engine-room section below.

Hydronic is **not released yet**. The preview page at [energyflowx.com/hydronic](https://energyflowx.com/hydronic) explains the scope, the discipline coverage and the licensing intent, and takes waitlist signups for the Founders' Circle. If you design networks for a living, that page is also where to tell me what you actually need, while it is still cheap to change.

---

## 14. THE ENGINE ROOM, DEDICATED LIBRARIES

EnergyFlowX is not a thin wrapper around someone else's solver. It runs on a purpose-built family of engineering libraries, each one designed, written, and tested from scratch for this exact job.

| Library | Role | Availability |
|---|---|---|
| **[Unitility](https://github.com/pjazdzyk/unitility)** | Physical quantities and units-of-measure framework. Typed `Temperature`, `Pressure`, `MassFlow`, and friends, with safe conversion across the whole suite. | **Open source, free for everyone** |
| **numenor-math** | The numerical foundation. Robust root-finders (modified Brent-Dekker, Newton-Raphson, multivariate Newton), line search, fixed-point iteration, and sparse linear algebra. | Private |
| **eos-engine** | The fluid domain. A general multiparameter Helmholtz equation-of-state kernel with a stable-root density solver and multi-fluid VLE, plus one self-contained pack per fluid family: air, water and steam, industrial gases, cryogens, refrigerants, natural gas, coolants and ice. | Private |
| **flow-symphony** | A universal, domain-generic steady-state hydraulic and pipe-network solver. Solves arbitrary topologies for incompressible and compressible fluids using a Global Gradient Algorithm, with a solved energy equation carrying temperature through the network. | Private |
| **hvac-engine-pro** | The HVAC process engine over that fluid domain. Heating, dry and wet cooling with condensate, mixing, heat recovery, and the device layer that plugs fluids into the hydraulic solver. | Private |
| **solar-engine** | Terrestrial solar and photovoltaic physics. Clear-sky irradiance, plane-of-array transposition, cell temperature, the self-shading orientation optimiser, degradation and finance. | Private |

[![Unitility](https://img.shields.io/badge/UNITILITY-open_source-13ADF3?style=for-the-badge)](https://github.com/pjazdzyk/unitility) &nbsp;
![numenor-math](https://img.shields.io/badge/numenor--math-private-2A3A5C?style=for-the-badge) &nbsp;
![eos-engine](https://img.shields.io/badge/eos--engine-private-2A3A5C?style=for-the-badge) &nbsp;
![flow-symphony](https://img.shields.io/badge/flow--symphony-private-2A3A5C?style=for-the-badge) &nbsp;
![hvac-engine-pro](https://img.shields.io/badge/hvac--engine--pro-private-2A3A5C?style=for-the-badge) &nbsp;
![solar-engine](https://img.shields.io/badge/solar--engine-private-2A3A5C?style=for-the-badge)

**Unitility** is the one member of the family released to the world as open source, free to use in your own projects. The rest are private and power EnergyFlowX from the inside. Together they represent over 7 years of active development and well over 10,000 hours of work on the backbone physics, so that the platform you use stands on equations rather than estimates.

Every one of them is plain Java 21 with no framework dependency, which is deliberate. The physics has to be extractable, embeddable, and testable without a container around it.

---

## 15. ENGINEERING PRACTICES AND NUMERICAL METHODS

Under the hood the platform is a study in doing the boring things correctly.

- **Reference-grade equations of state.** Helmholtz-energy and Gibbs-energy formulations, IAPWS-IF97 with backward equations, GERG-2008 multi-fluid models, and Span-Wagner reference correlations. The right tool for each fluid, not one approximation stretched over all of them.
- **Stable iterative solvers.** Nested root-finding via modified Brent-Dekker and Newton-Raphson, with derivative-based steps where the analytic derivative is known (for example the Churchill friction-factor Jacobian in the hydraulic network solver, while single-conduit sizing reports the Colebrook-White friction factor itself).
- **A real network solver.** The hydraulic core assembles a sparse weighted-graph Laplacian and solves it with a sparse LU factorisation, robust to the indefinite systems that pumps and fans introduce, with a residual-monotone backtracking line search keeping the iteration honest.
- **Validation as a feature.** Engine output is benchmarked against published reference tables, and that benchmark is exposed to you as a validation report rather than hidden in a test folder.
- **Tested top to bottom.** Unit, integration, and regression suites, plus independent cross-validation by practising engineers.

---

## 16. ARCHITECTURE AND TECHNOLOGY

EnergyFlowX runs as a set of independent services with a clean separation of concerns: a user and account service, a calculation service that holds all the physics, and a reverse proxy that serves the frontend.

The calculation backend follows a **hexagonal (ports-and-adapters)** architecture, organised as a modular Maven project with separate API and CORE modules. The API module defines the port interfaces, the CORE infrastructure layer implements them, and the domain layer stays framework-free and extractable. The frontend is a Vue 3 and Quasar single-page application built with Vite, with custom components handling physical quantities, live validation, and unit conversion.

**Frontend**

![Vue.js](https://img.shields.io/badge/Vue%20js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D) &nbsp;
![Quasar](https://img.shields.io/badge/Quasar-1976D2?style=for-the-badge&logo=quasar&logoColor=white) &nbsp;
![Vite](https://img.shields.io/badge/Vite-B73BFE?style=for-the-badge&logo=vite&logoColor=FFD62E) &nbsp;
![JavaScript](https://img.shields.io/badge/JavaScript-323330?style=for-the-badge&logo=javascript&logoColor=F7DF1E) &nbsp;
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white) &nbsp;
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)

**Backend**

![Java 21](https://img.shields.io/badge/Java_21-orange?style=for-the-badge&logo=openidconnect&logoColor=white) &nbsp;
![Maven](https://img.shields.io/badge/apache_maven-C71A36?style=for-the-badge&logo=apachemaven&logoColor=white) &nbsp;
![JUnit5](https://img.shields.io/badge/Junit5-25A162?style=for-the-badge&logo=junit5&logoColor=white) &nbsp;
![Spring Boot](https://img.shields.io/badge/Spring_Boot-F2F4F9?style=for-the-badge&logo=spring-boot) &nbsp;
![Spring Security](https://img.shields.io/badge/Spring_Security-6DB33F?style=for-the-badge&logo=Spring-Security&logoColor=white) &nbsp;
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)

**Infrastructure**

![Nginx](https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white) &nbsp;
![Cloudflare](https://img.shields.io/badge/Cloudflare-F38020?style=for-the-badge&logo=Cloudflare&logoColor=white) &nbsp;
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white) &nbsp;
![SonarCloud](https://img.shields.io/badge/Sonar%20cloud-F3702A?style=for-the-badge&logo=sonarcloud&logoColor=white) &nbsp;
![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)

---

## 17. SECURITY AND PRIVACY

Security follows industry best practice rather than industry folklore.

- Role-based access control (RBAC) for tiered content,
- Session-based authentication using HTTP-only cookies with XSRF protection,
- GDPR-compliant data handling with minimal data collection,
- HTTPS in strict mode across every page,
- Modern encryption for sensitive data, with secrets held in an external cloud key-vault,
- No internal stack traces ever exposed to the client. If you spot a leak, report it.

---

## 18. ACCESS TIERS

Most of EnergyFlowX is free to use right now. A subset of the more advanced applications is marked **Member**, which means an active account is required, often for the current testing phase. Which tools are free and which are gated may shift over time as the platform matures.

- **Free** today includes humid and dry air, water and steam, natural gas, the process gases, the cryogens, the glycols, ice, all four HVAC process calculators, duct and pipe sizing, IFC Lens in full, entry to Elements with its sun, shadow, wind, vegetation and modelling tools, the MCP server for most fluids, the knowledge base, and the validation reports.
- **Member** today includes the refrigerant group, the brine group, bulk property-table export, and the members-only pieces of Elements: measured weather (the typical-year download and the EPW parse) and the photovoltaic yield model.

Access has moved in the free direction since the last revision of this document. The HVAC process calculators and pipe sizing were gated and are now open to everyone.

Register a free account on [energyflowx.com](https://energyflowx.com) and explore.

---

## 19. THE NUMBERS ARE COMPUTED, NOT GENERATED

Every result you see comes from a deterministic algorithm evaluating an established scientific equation, not from a language model predicting a plausible-looking value. There are no LLMs in the calculation path. When a number underpins a building, a coil, or a pipe run, you want a documented equation of state solved to a tolerance, reproducible to the last digit and traceable to its source. That is exactly what the engine delivers, the same inputs always yield the same numbers, and each one can be tied back to the standard it came from.

---

## 20. LICENSING, CITATION, AND ATTRIBUTION

EnergyFlowX, its source code, user interface, data formulations, and underlying methods are the exclusive intellectual property of Synerset and are protected by copyright and applicable law.

**© 2026 Biuro Projektów i Analiz SYNERSET, Piotr Jażdżyk. All rights reserved.** EnergyFlowX™ and Synerset™ are protected trademarks of *Biuro Projektów i Analiz SYNERSET, Piotr Jażdżyk*, based in Poland. Any reproduction, redistribution, automated scraping or ingestion by machine-learning systems, reverse engineering, or derivation of the software, in whole or in part, without prior written permission of the rightsholder is strictly prohibited.

**How to cite.** If EnergyFlowX supports your published work, software, or a design, please cite it as:

```
Piotr Jażdżyk (2026). EnergyFlowX [Computer software]. Synerset. Retrieved from https://energyflowx.com
```

```bibtex
@misc{energyflowx,
  author       = {Piotr Jażdżyk},
  title        = {EnergyFlowX},
  howpublished = {Computer software},
  year         = {2026},
  organization = {Synerset},
  url          = {https://energyflowx.com}
}
```

**Disclaimer.** This is independent, private software developed for educational and general engineering reference. It is not an official IAPWS product, nor is it certified, accredited, or endorsed by IAPWS in any manner. All thermophysical calculations are based on publicly available IAPWS formulations and published scientific correlations, and the implementations are the author's own interpretation of those formulations. Results are validated against recognised standards, but **all calculations must be reviewed and approved by a licensed, chartered, or professional engineer responsible for the design** before use. The software is provided as-is, without warranty of any kind, and the author accepts no liability for decisions made on the basis of these calculations.

---

## 21. FEEDBACK AND BUG REPORTING

This project was built by an engineer, for engineers, and it should be as useful as possible in your daily work. Feedback and ideas are genuinely welcome.

When reporting a bug, please include:

- **Page or functionality**, where it happened,
- **Description**, a clear and detailed account,
- **Input data**, the values used when it triggered,
- **Result and expectation**, what happened versus what you expected,
- **App version**, found at the bottom of the application.

Your feedback is the fuel that drives this project forward. Every suggestion and bug report makes the tool better.

---

## 22. ACKNOWLEDGMENTS

Heartfelt thanks to [Mabas83](https://github.com/mabas83) for everything. Deep gratitude to the [Silesian University of Technology](https://www.polsl.pl/en/) for the knowledge, the scientific guidance, and for shaping me into an engineer. Special thanks to [GreedyJ4ck](https://github.com/greedyj4ck) for discussions and valuable suggestions during frontend development. Big thanks to all of you.

This software is based, in part, on information obtained from the International Association for the Properties of Water and Steam ([iapws.org](https://iapws.org)). EN and ISO formulations were consulted under lawful, read-only access to Polish Standards (PN, including the PN-EN and PN-EN ISO adoptions) provided to members of the Polish Chamber of Civil Engineers ([piib.org.pl](https://www.piib.org.pl/)). EnergyFlowX implements those methods in the author's own independent code and does not reproduce, redistribute, or republish the text, tables, or other protected content of any standard. Any numerical agreement with published data reflects correct physics rather than copied content. Standards are named only for reference (nominative use).

**Third-party open-source software.** The browser-based IFC Lens and Elements are built on the open-source [That Open Engine](https://github.com/ThatOpen/) BIM toolkit by That Open Company (MIT), the WebAssembly [web-ifc](https://github.com/ThatOpen/engine_web-ifc) parser (MPL-2.0), and **Three.js** (MIT). The Elements Modeler runs **Open CASCADE Technology**, the B-rep CAD kernel, compiled to WebAssembly and conveyed to the browser under LGPL-2.1 with the OCCT exception, by way of replicad-opencascadejs and opencascade.js (MIT build tooling).

The **IFC, IDS and BCF standards** are maintained by [buildingSMART International](https://www.buildingsmart.org/) (BCF used under CC BY-ND 4.0). The bundled demonstration model is the **PCERT Sample Scene** (IFC 4.0.2.1), © buildingSMART International, redistributed unmodified under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). **Map data, imagery and data services.** Elements and IFC Lens use the third-party sources below, each under its own licence. The full list, with each licence, credit line and how it is used, is published in section A.4 of [energyflowx.com/third-party-notices.txt](https://energyflowx.com/third-party-notices.txt), generated from the same list as the privacy policy.

- **OpenStreetMap** map tiles, Nominatim place search, and building and tree data through the public Overpass API, © OpenStreetMap contributors, [ODbL](https://www.openstreetmap.org/copyright).
- **Overture Maps** buildings, Overture Maps Foundation, [ODbL with CC BY 4.0 components](https://docs.overturemaps.org/attribution/).
- **Terrain Tiles** by Mapzen, a Linux Foundation project, from the AWS Registry of Open Data, built from USGS, NOAA, Copernicus EU-DEM and further [national sources](https://github.com/tilezen/joerd/blob/master/docs/attribution.md), relayed by our server.
- **swissALTI3D** terrain, © swisstopo, read by our server.
- **Orthophoto** (Ortofotomapa), © Główny Urząd Geodezji i Kartografii.
- **3D BAG** buildings, © 3DBAG by tudelft3d and 3DGI, [CC BY 4.0](https://docs.3dbag.nl/en/copyright/).
- **LIDAR Composite Digital Terrain Model, 1 m**, **LIDAR Composite Digital Surface Model, 1 m** (first and last return) and the **Vegetation Object Model**, © Environment Agency copyright and/or database right 2022. All rights reserved. Used under the [Open Government Licence v3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/), read by our server for terrain, building heights, trees and the relief tiles it shades.
- **Scottish Public Sector LiDAR**, Open Government Licence v3.0, accessed from [registry.opendata.aws/scottish-lidar](https://registry.opendata.aws/scottish-lidar): National LiDAR Programme, Crown copyright Scottish Government © Crown copyright and database right (2025). Outer Hebrides 2019, © SEPA (2019). Phase 1, Crown copyright Scottish Government, SEPA and Scottish Water (2012). Orkney 2023 and phases 4 to 6, contains public sector information licensed under the Open Government Licence v3.0. Read by our server.
- **Planning data**, Ministry of Housing, Communities and Local Government, used under the [Open Government Licence v3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/), read by our server, with each dataset's own attribution shown beside its designations (for example © Historic England 2026. Contains Ordnance Survey data © Crown copyright and database right 2026).
- Coordinate-system definitions from the EPSG Geodetic Parameter Dataset (IOGP), through epsg.io.
- Bundled with our calculation service: the **OSTN15** transformation, © Copyright and database rights Ordnance Survey Limited 2016, © Crown copyright and database rights Land & Property Services 2016 and/or © Ordnance Survey Ireland, 2016, used under the [BSD Licence](https://opensource.org/licenses/bsd-license.php), **Natural Earth** 1:10m map units, public domain, for coarse coverage outlines, and the **ONS Postcode Directory**, Great Britain rows, for postcode search: Contains OS data © Crown copyright and database right 2026. Contains Royal Mail data © Royal Mail copyright and database right 2026. Source: Office for National Statistics licensed under the Open Government Licence v.3.0.
- Typical-meteorological-year weather from **PVGIS**, European Commission Joint Research Centre, fetched by our server.

The solar cross-check is run against **Ladybug Tools**, an open-source solar library, gratefully acknowledged.

---

## 23. REFERENCE SOURCES

The list below is a selection of the most important sources, not the whole library. The full bibliography behind EnergyFlowX runs to dozens more standards, papers, and textbooks. Each calculator's documentation page states the exact standard and validity range it uses.

### Water and Steam, IAPWS formulations

- **[1]** IAPWS R7-97(2012), *Industrial Formulation 1997 for the Thermodynamic Properties of Water and Steam (IF97)*. Covers Regions 1 to 5, boundary equations, backward equations, and uncertainty estimates.
- **[2]** IAPWS G5-01(2026), *Guideline on the Use of Fundamental Physical Constants and Basic Constants of Water*. CODATA 2022 constants, ITS-90 scale, VSMOW isotopic composition, and reference quantities for water substance.
- **[3]** IAPWS SR2-01(2014), *Revised Supplementary Release on Backward Equations p(h,s) for Regions 1 and 2*.
- **[4]** IAPWS SR4-04(2014), *Revised Supplementary Release on Backward Equations p(h,s) for Region 3, Boundary Equations, T_sat(h,s) for Region 4*.
- **[5]** IAPWS SR5-05(2016), *Revised Supplementary Release on Backward Equations v(p,T) for Region 3*. 20 subregions plus 6 auxiliary subregions near the critical point.
- **[6]** IAPWS R6-95(2018), *Revised Release on the IAPWS-95 Formulation*. Fundamental Helmholtz free-energy equation with ideal-gas and residual parts.

### Transport properties, IAPWS

- **[7]** IAPWS R12-08(2008), *Formulation 2008 for Viscosity of Ordinary Water Substance*.
- **[8]** IAPWS R15-11(2011), *Formulation 2011 for Thermal Conductivity of Ordinary Water Substance*.
- **[9]** IAPWS R1-76(2014), *Revised Release on Surface Tension of Ordinary Water Substance*.

### Ice Ih, solid phase, IAPWS

- **[10]** IAPWS R10-06(2009), *Revised Release on the Equation of State 2006 for H₂O Ice Ih*. Gibbs energy EOS with verification values and analytical derivatives.
- **[11]** IAPWS R14-08(2011), *Revised Release on the Pressure along the Melting and Sublimation Curves of Ordinary Water Substance*. Melting pressure for ice phases Ih, III, V, VI, VII, and sublimation pressure from 50 K to the triple point.

### Dry Air

- **[12]** Lemmon E.W., Jacobsen R.T., Penoncello S.G., Friend D.G. (2000), *Thermodynamic Properties of Air and Mixtures of Nitrogen, Argon, and Oxygen from 60 to 2000 K at Pressures to 2000 MPa*. J. Phys. Chem. Ref. Data, Vol. 29, No. 3, 331 to 385.
- **[13]** Lemmon E.W., Jacobsen R.T. (2004), *Viscosity and Thermal Conductivity Equations for Nitrogen, Oxygen, Argon, and Air*. Int. J. Thermophysics, Vol. 25, No. 1, p. 21 to 69.

### Humid Air, IAPWS

- **[14]** IAPWS G11-15(2015), *Guideline on Virial Equation for Fugacity of H₂O in Humid Air*.
- **[15]** IAPWS G9-12(2012), *Guideline on Low-Temperature Extension of IAPWS-95 Formulation for Water Vapor* (50 K to 130 K).

### Natural Gas

- **[16]** Kunz O., Wagner W. (2012), *The GERG-2008 Wide-Range Equation of State for Natural Gases and Other Mixtures*. J. Chem. Eng. Data, Vol. 57(11), 3032 to 3091 (basis of ISO 20765-2). Underpins density, compressibility, heat capacities, and speed of sound for the Natural Gas calculator.

### Process Gases

- **[17]** Span R., Wagner W. (1996), *A New Equation of State for Carbon Dioxide Covering the Fluid Region to 1100 K and 800 MPa*. J. Phys. Chem. Ref. Data, Vol. 25(6), 1509 to 1596. One of the single-component reference models behind the Process Gases group.
- **[18]** Lemmon E.W., Span R. (2006), *Short Fundamental Equations of State for 20 Industrial Fluids*. J. Chem. Eng. Data, Vol. 51(3), 785 to 850. The equation of state used for nitrous oxide.
- **[19]** Huber M.L. (2018), *Models for Viscosity, Thermal Conductivity, and Surface Tension of Selected Pure Fluids*. NIST Internal Report 8209. The extended-corresponding-states transport model behind the nitrous-oxide viscosity and thermal conductivity.
- **[19a]** Mulero A., Cachadiña I., Parra M.I. (2012), *Recommended Correlations for the Surface Tension of Common Fluids*. J. Phys. Chem. Ref. Data, Vol. 41(4), 043105. Surface tension of the process gases, the cryogens and the pure refrigerants except R-1234ze(E).
- **[19b]** Mulero A., Cachadiña I. (2014), surface-tension correlations for several fluids. J. Phys. Chem. Ref. Data, Vol. 43(2), 023104, doi:10.1063/1.4878755. Surface tension of R-1234ze(E).

### Cryogens

- **[20]** Span R., Lemmon E.W., Jacobsen R.T., Wagner W., Yokozeki A. (2000), *A Reference Equation of State for the Thermodynamic Properties of Nitrogen for Temperatures from 63.151 to 1000 K and Pressures to 2200 MPa*. J. Phys. Chem. Ref. Data, Vol. 29(6), 1361 to 1433.
- **[21]** Schmidt R., Wagner W. (1985), *A New Form of the Equation of State for Pure Substances and its Application to Oxygen*. Fluid Phase Equilibria, Vol. 19(3), 175 to 200. Companion property tables in Stewart, Jacobsen and Wagner (1991), J. Phys. Chem. Ref. Data, Vol. 20(5), 917 to 1021.
- **[22]** Tegeler Ch., Span R., Wagner W. (1999), *A New Equation of State for Argon Covering the Fluid Region for Temperatures from the Melting Line to 700 K at Pressures up to 1000 MPa*. J. Phys. Chem. Ref. Data, Vol. 28(3), 779 to 850.
- **[23]** Ortiz Vega D.O., Hall K.R., Holste J.C., Harvey A.H., Lemmon E.W. (2023), *An Equation of State for the Thermodynamic Properties of Helium*. NIST Internal Report 8474. Normal-fluid helium I only, above the lambda point.
- **[24]** Setzmann U., Wagner W. (1991), *A New Equation of State and Tables of Thermodynamic Properties for Methane Covering the Range from the Melting Line to 625 K at Pressures up to 1000 MPa*. J. Phys. Chem. Ref. Data, Vol. 20(6), 1061 to 1155.

### Refrigerants

- **[25]** Tillner-Roth R., Baehr H.D. (1994), *An International Standard Formulation for the Thermodynamic Properties of R-134a*. J. Phys. Chem. Ref. Data, Vol. 23(5), 657 to 729. The foundational model of the Refrigerants group, alongside the pure-fluid and multi-fluid Helmholtz models for the remaining members and blends.
- **[25a]** Lemmon E.W., Akasaka R. (2022), *An International Standard Formulation for 2,3,3,3-Tetrafluoroprop-1-ene (R1234yf) Covering Temperatures from the Triple Point Temperature to 410 K and Pressures Up to 100 MPa*. Int. J. Thermophys., Vol. 43(8), 119.
- **[25b]** Bell I.H. (2023), *Mixture Model for Refrigerant Pairs R-32/1234yf, R-32/1234ze(E), R-1234ze(E)/227ea, R-1234yf/152a, and R-125/1234yf*. J. Phys. Chem. Ref. Data, Vol. 52(1), 013101. The R-32/R-1234yf binary behind R-454B.

### Secondary Working Fluids, glycols and brines

- **[26]** Melinder Å. (2010), *Properties of Secondary Working Fluids for Indirect Systems*, IIR, 2nd ed. The basis for the Glycols and Brines calculators, including concentration-dependent freezing-point limits.

### HVAC Processes and Heat Recovery

- **[27]** Jones W.P. (2001), *Air Conditioning Engineering*, 5th edition. Psychrometric processes, cooling-coil analysis (bypass and contact factors, condensate energy balance), heating, and adiabatic mixing of moist-air streams.
- **[28]** EN 308:2022, *Heat exchangers, test procedures for establishing the performance of air-to-air heat recovery components*. HRC categories, test types, and the temperature/humidity effectiveness and heat-balance correction formulas.
- **[29]** EN 13053:2019, *Ventilation for buildings, air handling units, rating and performance for units, components and sections*.
- **[30]** Kostowski E. (2000), *Przepływ ciepła*, Wydawnictwo Politechniki Śląskiej, Gliwice. The ε-NTU method, flow-arrangement correlations, and capacity-rate (C*) effects used in the heat-recovery asymmetry correction.

### Hydraulics, duct and pipe flow

- **[31]** Zeghadnia L., Robert J.L., Achour B. (2019), *Explicit solutions for turbulent flow friction factor: a review, assessment and approaches classification*. Ain Shams Engineering Journal, Vol. 10(1), 243 to 252. Includes the Vatankhah explicit approximation used as the iterative solver initial guess.
- **[32]** Mitosek M. (2001), *Mechanika płynów w inżynierii i ochronie środowiska*, PWN. Reynolds number, Darcy-Weisbach pressure loss, local losses, linear resistance, and hydraulic diameter.

### Solar irradiance and photovoltaics

- **[33]** Bird R.E., Hulstrom R.L. (1981), *A Simplified Clear Sky Model for Direct and Diffuse Insolation on Horizontal Surfaces*. SERI/TR-642-761. The broadband clear-sky model behind an irradiance study that needs no weather file.
- **[34]** Perez R., Ineichen P., Seals R., Michalsky J., Stewart R. (1990), *Modeling Daylight Availability and Irradiance Components from Direct and Global Irradiance*. Solar Energy, Vol. 44(5), 271 to 289. The anisotropic sky model used for plane-of-array transposition.
- **[35]** Liu B.Y.H., Jordan R.C. (1960), *The Interrelationship and Characteristic Distribution of Direct, Diffuse and Total Solar Radiation*. Solar Energy, Vol. 4(3), 1 to 19. The isotropic transposition alternative.
- **[36]** Kasten F., Young A.T. (1989), *Revised Optical Air Mass Tables and Approximation Formula*. Applied Optics, Vol. 28(22), 4735 to 4738.
- **[37]** Duffie J.A., Beckman W.A., *Solar Engineering of Thermal Processes*. Cover-glass optics and the incidence-angle modifier.
- **[38]** IEC 61215 and IEC 61724-1. The NOCT definition, and the normalised photovoltaic yield quantities (performance ratio, specific yield) the PV results are reported in.
- **[39]** Dobos A.P. (2014), *PVWatts Version 5 Manual*. NREL/TP-6A20-62641. The system loss budget.
- **[40]** PVGIS, European Commission Joint Research Centre. The measured typical-meteorological-year source, and an independent yield cross-check.

### Wind screening

- **[41]** EN 1991-1-4, *Eurocode 1: Actions on structures, Part 1-4: General actions, wind actions*. Referenced for its terrain categories, which drive the inlet profile option.
- **[42]** Richards P.J., Hoxey R.P. (1993), *Appropriate boundary conditions for computational wind engineering models using the k-ε turbulence model*. J. Wind Eng. Ind. Aerodyn., Vol. 46-47, 145 to 153. The equilibrium atmospheric-boundary-layer requirement the inlet is checked against.
- **[43]** Roshko A. (1954), *On the Development of Turbulent Wakes from Vortex Streets*. NACA Report 1191. The vortex-shedding benchmark the wind solver is validated on.

### Geometry and CAD

- **[44]** Open CASCADE Technology, the B-rep CAD kernel behind the Elements Modeler, compiled to WebAssembly and used under LGPL-2.1 with the OCCT exception, via replicad-opencascadejs and opencascade.js.

---

[<img src="assets/images/efx_reddit_banner.png" alt="EnergyFlowX" style="width:100%;">](https://energyflowx.com)

**Created by Piotr Jażdżyk, MSc Eng.** [Read more about the author](https://energyflowx.com/social) · [LinkedIn](https://www.linkedin.com/in/pjazdzyk)

Do not forget to say hello.
</content>
</invoke>
