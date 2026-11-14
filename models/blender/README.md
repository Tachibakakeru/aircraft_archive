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

# Boeing 747-400 LCF Dreamlifter — original Blender educational prototype (trial v2, 2026-11-15)

`dreamlifter.blend` is the editable source; `../dreamlifter.json` is the archive v2 export. No downloaded mesh,
logo or photographic texture is included; geometry is an original approximation, not Boeing CAD.

```powershell
D:blender.exe --background --python-exit-code 1 --python tools/build_dreamlifter_blender.py
python tools/make_thumb.py models/dreamlifter.json assets/thumb_dreamlifter.png
python tools/check_model_inventory.py
cd tools; python check_dreamlifter_model.py
```

Built with Blender 5.2.1 LTS, sharing the Concorde helper functions. Metres, nose +X, Z up, port +Y, ground z = 0;
export normalises length (71.68 m) to 12 units. Published figures used: length 71.68 m, span 64.4 m,
height 21.54 m, cargo hold diameter 8.38 m, stabilizer span 22.17 m, 747-400 engine stations and gear layout.

193 meshes, 64 hinge groups on 8 slider channels:

| Channel | Hinges | Notes |
|---|---|---|
| `flaps` | 4 | inboard/outboard Fowler flaps, 30° with 1.15 m aft travel (triple-slotted flap shown as one panel) |
| `slats` | 28 | 3 Krueger + 11 variable-camber Krueger panels per wing, folding out from the lower skin |
| `spoilers` | 12 | 6 per wing, 45° |
| `ailerons` | 4 | inboard high-speed + outboard, left/right opposite, ±20° |
| `elevators` | 4 | inboard/outboard each side, ±22° |
| `rudder` | 2 | upper/lower, ±25° |
| `gear` | 7 | nose (forward), 2 wing gear (inboard), 2 body gear (forward) + 2 nested truck-levelling joints; 18 wheels |
| `swingtail` | 3 | aft fuselage, fin and stabilizer share the port-side hinge line, 93° |

New optional v2 field `surfaces[].parent`: a hinge can hang from another hinge (rudder and elevators ride on the
swing tail; body-gear trucks stay level while the leg swings). The viewer's takeoff demo now also drives
`flaps`/`slats` slider channels.

Known limits of this trial: fuselage is a convex double-lobe hull (no crease detail, no cargo-loader fittings);
the tail support is ground equipment and is not modelled; gear doors move together with the gear rather than in
sequence; Krueger linkage, gear retraction angles and the 93° tail swing are illustrative, not rigging data; livery is a neutral
white/blue scheme without logos. The span follows Boeing's published 64.4 m.

References (dimensions only, nothing bundled): Boeing published Dreamlifter figures already recorded in `data/dreamlifter.json`, and general 747-400 airport-planning dimensions. Trial v2 was compared by eye against Boeing Images catalogue photos (BI224697 in-flight render, BI223381 in flight) and Wikimedia Commons files `B747 LCF.JPG`, `Boeing 747-400(LCF) Dreamlifter.jpg` and the three-view `Boeing 747 LCF Dreamlifter.jpg`; stations were measured from those in a browser and no image is bundled. v2 changes: blunt hold dome starting 9.6 m aft of the nose, swing break at 48.5 m, tail cone ending at 69.0 m with the fin tip overhanging to 71.68 m, re-stationed fin and stabilizer, two port-side hinge fairings, triple-slotted flaps, flap-track fairings, gear doors, blue nacelles, no cheat line. Re-check these sources before refining the shape.
