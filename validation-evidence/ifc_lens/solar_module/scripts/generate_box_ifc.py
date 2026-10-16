"""
Generate the georeferenced IFC test box for the IFC Lens vs Ladybug comparison.

One opaque rectangular box, X[-10,10] Y[-5,5] Z[0,15] (metres), on an IfcSite
georeferenced to Warsaw (52.23N, 21.01E) with true north = +Y. Load it into IFC
Lens (the Solar tool reads the site lat/lon) and model the same box in Rhino for
Ladybug.

Run (after `pip install ifcopenshell`):
    python generate_box_ifc.py
"""

import time
import ifcopenshell
import ifcopenshell.guid

f = ifcopenshell.file(schema="IFC4")


def guid():
    return ifcopenshell.guid.new()


def cart(c):
    return f.create_entity("IfcCartesianPoint", Coordinates=[float(x) for x in c])


def dirn(c):
    return f.create_entity("IfcDirection", DirectionRatios=[float(x) for x in c])


def rgb(r, g, b):
    return f.create_entity("IfcColourRgb", Red=float(r), Green=float(g), Blue=float(b))


def paint(item, colour, name):
    """Attach a light surface style (presentation colour) to a geometry item."""
    style = f.create_entity(
        "IfcSurfaceStyle",
        Name=name,
        Side="BOTH",
        Styles=[
            f.create_entity(
                "IfcSurfaceStyleRendering",
                SurfaceColour=colour,
                Transparency=0.0,
                ReflectanceMethod="NOTDEFINED",
            )
        ],
    )
    f.create_entity("IfcStyledItem", Item=item, Styles=[style])


def place3d(origin=(0, 0, 0)):
    return f.create_entity("IfcAxis2Placement3D", Location=cart(origin))


def local(rel_to=None, origin=(0, 0, 0)):
    return f.create_entity("IfcLocalPlacement", PlacementRelTo=rel_to, RelativePlacement=place3d(origin))


# --- owner history (optional in IFC4, but kept for viewer compatibility) ---
person = f.create_entity("IfcPerson", FamilyName="EnergyFlowX")
org = f.create_entity("IfcOrganization", Name="EnergyFlowX")
p_o = f.create_entity("IfcPersonAndOrganization", ThePerson=person, TheOrganization=org)
app = f.create_entity(
    "IfcApplication",
    ApplicationDeveloper=org,
    Version="1.0",
    ApplicationFullName="EnergyFlowX solar test-box generator",
    ApplicationIdentifier="EFX-SolarBox",
)
owner = f.create_entity(
    "IfcOwnerHistory",
    OwningUser=p_o,
    OwningApplication=app,
    ChangeAction="ADDED",
    CreationDate=int(time.time()),
)

# --- units (SI metre + radian) ---
units = f.create_entity(
    "IfcUnitAssignment",
    Units=[
        f.create_entity("IfcSIUnit", UnitType="LENGTHUNIT", Name="METRE"),
        f.create_entity("IfcSIUnit", UnitType="PLANEANGLEUNIT", Name="RADIAN"),
    ],
)

# --- geometric context, true north = +Y ---
ctx = f.create_entity(
    "IfcGeometricRepresentationContext",
    ContextType="Model",
    CoordinateSpaceDimension=3,
    Precision=1e-5,
    WorldCoordinateSystem=place3d((0, 0, 0)),
    TrueNorth=dirn((0, 1)),
)
body = f.create_entity(
    "IfcGeometricRepresentationSubContext",
    ContextIdentifier="Body",
    ContextType="Model",
    ParentContext=ctx,
    TargetView="MODEL_VIEW",
)

# --- project + spatial structure ---
project = f.create_entity(
    "IfcProject",
    GlobalId=guid(),
    OwnerHistory=owner,
    Name="Solar comparison test box",
    UnitsInContext=units,
    RepresentationContexts=[ctx],
)

site = f.create_entity(
    "IfcSite",
    GlobalId=guid(),
    OwnerHistory=owner,
    Name="Warsaw site",
    ObjectPlacement=local(),
    CompositionType="ELEMENT",
    # 52.23N -> 52deg 13' 48"; 21.01E -> 21deg 0' 36"
    RefLatitude=[52, 13, 48, 0],
    RefLongitude=[21, 0, 36, 0],
    RefElevation=110.0,  # Warsaw approx ground elevation (m)
)
building = f.create_entity(
    "IfcBuilding",
    GlobalId=guid(),
    OwnerHistory=owner,
    Name="Test building",
    ObjectPlacement=local(site.ObjectPlacement),
    CompositionType="ELEMENT",
)
storey = f.create_entity(
    "IfcBuildingStorey",
    GlobalId=guid(),
    OwnerHistory=owner,
    Name="Ground",
    ObjectPlacement=local(building.ObjectPlacement),
    CompositionType="ELEMENT",
    Elevation=0.0,
)

f.create_entity("IfcRelAggregates", GlobalId=guid(), OwnerHistory=owner, RelatingObject=project, RelatedObjects=[site])
f.create_entity("IfcRelAggregates", GlobalId=guid(), OwnerHistory=owner, RelatingObject=site, RelatedObjects=[building])
f.create_entity("IfcRelAggregates", GlobalId=guid(), OwnerHistory=owner, RelatingObject=building, RelatedObjects=[storey])

# --- the box: 20 x 10 rectangle (centred) extruded 15 up ---
profile = f.create_entity(
    "IfcRectangleProfileDef",
    ProfileType="AREA",
    Position=f.create_entity("IfcAxis2Placement2D", Location=f.create_entity("IfcCartesianPoint", Coordinates=[0.0, 0.0])),
    XDim=20.0,
    YDim=10.0,
)
solid = f.create_entity(
    "IfcExtrudedAreaSolid",
    SweptArea=profile,
    Position=place3d((0, 0, 0)),
    ExtrudedDirection=dirn((0, 0, 1)),
    Depth=15.0,
)
shape = f.create_entity(
    "IfcShapeRepresentation",
    ContextOfItems=body,
    RepresentationIdentifier="Body",
    RepresentationType="SweptSolid",
    Items=[solid],
)
pds = f.create_entity("IfcProductDefinitionShape", Representations=[shape])

box = f.create_entity(
    "IfcBuildingElementProxy",
    GlobalId=guid(),
    OwnerHistory=owner,
    Name="Test box 20x10x15 (opaque)",
    ObjectPlacement=local(storey.ObjectPlacement),
    Representation=pds,
)

# --- flat ground: a ZERO-THICKNESS 120 x 120 m light-gray surface at Z=0, so the
# heatmap has a terrain to render on. SAFE for the validation now: the point
# reader RAY-TRACES sun-hours against the building only (glazing + ground-coplanar
# faces excluded), so the ground plane does NOT change any probed value. It is a
# pure visual canvas. Zero thickness keeps the scene minimum exactly at Z=0 so the
# ground-sensor grid sits on the surface (no self-shadow from a slab underside). ---
GROUND = 120.0
gh = GROUND / 2.0
ground_coords = f.create_entity(
    "IfcCartesianPointList3D",
    CoordList=[[-gh, -gh, 0.0], [gh, -gh, 0.0], [gh, gh, 0.0], [-gh, gh, 0.0]],
)
ground_faceset = f.create_entity(
    "IfcTriangulatedFaceSet",
    Coordinates=ground_coords,
    CoordIndex=[[1, 2, 3], [1, 3, 4]],  # 1-based; two tris span the square
    Closed=False,
)
paint(ground_faceset, rgb(0.80, 0.82, 0.84), "GroundLightGray")  # light gray ground
ground_shape = f.create_entity(
    "IfcShapeRepresentation",
    ContextOfItems=body,
    RepresentationIdentifier="Body",
    RepresentationType="Tessellation",
    Items=[ground_faceset],
)
ground_pds = f.create_entity("IfcProductDefinitionShape", Representations=[ground_shape])
ground = f.create_entity(
    "IfcSlab",
    GlobalId=guid(),
    OwnerHistory=owner,
    Name="Ground plane 120x120 (flat)",
    ObjectPlacement=local(storey.ObjectPlacement),
    Representation=ground_pds,
    PredefinedType="BASESLAB",
)

f.create_entity(
    "IfcRelContainedInSpatialStructure",
    GlobalId=guid(),
    OwnerHistory=owner,
    Name="Storey contents",
    RelatingStructure=storey,
    RelatedElements=[box, ground],
)

OUT = "solar-test-box.ifc"
f.write(OUT)
print(
    f"wrote {OUT}: box X[-10,10] Y[-5,5] Z[0,15] m on a {GROUND:.0f}x{GROUND:.0f} m flat "
    f"light-gray ground at Z=0 (visual only, points ray-trace the box), "
    f"site 52.23N 21.01E, true north +Y"
)
