# Concorde — original Blender educational prototype

`concorde.blend` is the editable source; `../concorde.json` is the existing archive v2 format with optional named articulation channels. No downloaded mesh, airline logo or photographic texture is included. Geometry is an original approximation, not aircraft-manufacturer CAD.

Rebuild from the repository root:

```powershell
blender --background --python-exit-code 1 --python tools/build_concorde_blender.py
python tools/register_concorde_model.py
python tools/make_thumb.py models/concorde.json assets/thumb_concorde.png
python tools/check_model_inventory.py
python tools/check_concorde_model.py
```

Blender uses metres, nose +X and Z up. Export uses nose +X, Y up and normalizes length to 12 archive units. Named mesh objects have `partId` and optional `joint` custom properties. Twelve hinge empties carry independent animation actions between frames 1 (neutral/deployed gear) and 61 (demonstration deflection): nose, six elevons, two rudders and three gear assemblies.

The JSON keeps the existing `surfaces[].pv`, `ax`, `e` representation and adds optional `part`, `channel`, `angle` fields. `controls` supplies translated labels and slider ranges; models without these fields retain the original deploy button behavior.

Known limits: approximate ogival wing and fuselage sections; simplified cabin glazing, intake ramps, engine nozzles and gear bays; visor is a separate mesh attached to the nose, without its independent sliding mechanism. Gear shortening and rotation are illustrative and do not reproduce full hydraulic linkages or door sequencing. Elevon/rudder demonstration angles are not certified operating limits. No horizontal stabilizer is added to this tailless aircraft.

References: [British Airways dimensions](https://www.britishairways.com/content/information/about-ba/history-and-heritage/celebrating-concorde), [Heritage Concorde nose operation](https://www.heritageconcorde.com/nose-and-visor-operations), [Heritage Concorde flight controls](https://www.heritageconcorde.com/concorde-elevons-and-rudder).

## Photo-reference refinement — 2026-09-10

316 meshes / 12 hinges. Revised production-aircraft proportions: forward nose gear,
wing and nacelle longitudinal position, fuselage ground clearance, swept fin and
split rudder. Shape-preserving interpolated shell sections now carry conformal
cabin windows, door outlines and trim. The ogee wing has rounded fixed tips and
six separate elevons; intake shells are tapered and nozzle lips have recessed
interiors instead of solid discs. These are visual approximations, not traced CAD
or accurate simulation mechanisms. Existing visor/gear simplifications still apply.

Visual references inspected (not bundled or used as textures):
- [G-BOAC side photograph, Tony Scruton](https://www.planespotters.net/photo/046614/g-boac-british-airways-bac-concorde-102) — overall stance, cabin and nose.
- [Concorde orthographic views, Julien.scavini, CC BY-SA 3.0](https://commons.wikimedia.org/wiki/File:Concorde_v1.0.png) — comparative proportions and planform, not a pixel-traced mesh.
- [Production Concorde nozzle photograph, Roland Turner, CC BY-SA 2.0](https://commons.wikimedia.org/wiki/File:Concorde_engine_nacelle_detail,_Mus%C3%A9e_de_l%27Air_et_de_l%27Espace,_Le_Bourget,_France._(12599326095).jpg) — paired nozzle lip and recessed interior.

## Retraction and elevon collision correction — 2026-09-10

Current export: 325 meshes, 12 hinge groups. Main bogies and inner pistons translate
0.20 m during the first 30% of the illustrative control travel; the remaining travel
rotates the legs inward. These chosen display values are NOT maintenance rigging
dimensions. Upper braces remain in the longitudinal leg plane. Belly/wing-root bay
fairings contain the stowed mesh, without hiding it. Nose-gear pivot clearance is corrected.
`surfaces[].start` delays rotation; individual `e[].slide` vectors and `slideEnd`
drive local translation before parent rotation. The `.blend` uses matching linear keys.

Elevon groups now lie inside and outside the nacelle span; the nacelle roof bridge is
fixed. Engines do not follow elevon deflection. The regression check samples both
elevon limits and six gear positions, checks lateral clearance from nacelles and
approximate stowed/upper-skin envelopes (not full CAD collision certification).

References: [actual main-gear shortening/inward retraction](https://www.heritageconcorde.com/mainlandinggear),
[engine mountings on fixed wing structure](https://www.heritageconcorde.com/airframe-structure/1000).
