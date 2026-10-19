# Corrections

Corrections that changed a result a user may have relied on, newest first. Open defects are listed on
[energyflowx.com/known-issues](https://energyflowx.com/known-issues) until they are fixed.

## 2026-10-17 · Duct sizing: two duct series withdrawn

Two duct series were withdrawn from the catalogue:

- the thick-wall PVC series of one maker (CHWENT_P_PVC_CIRC_TCK), because the maker prints no such series;
- the rectangular series of another (AWENT_F_TPF_RECT), because the maker prints fixed profile pairs and not free
  rectangular sizes.

The duct tool now answers a request for either series with not found. If you sized a duct from either series, check
the size against the maker data of the duct you intend to install.

## 2026-10-17 · Compressed-air treatment: the water rank uses a new scale

The water rank of compressed air was renumbered on purpose, when the water grading moved to our own scale of
dew-point bands. For the same air the rank now reads one lower:

- discharge air: 7 became 6;
- ambient, aftercooler and separator outlets: 6 became 5;
- a dryer at +3 °C pressure dew point: 4 became 3.

A result, report or saved study made before the change shows the old numbers, so do not compare ranks across the two.
