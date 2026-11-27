"""Build the An-225 archive rig from the pinned FlightGear aircraft (see models/blender/README.md)."""
import argparse
from collections import defaultdict
import json
import math
from pathlib import Path
import xml.etree.ElementTree as ET

import numpy as np
from PIL import Image

from ac3d_lib import b64

ROOT = Path(__file__).resolve().parents[1]
LABELS = {
    "flaps": ("後緣襟翼", "Fowler flaps", "後縁フラップ"),
    "slats": ("前緣增升裝置", "Leading-edge devices", "前縁装置"),
    "spoilers": ("擾流板與減速板", "Spoilers and airbrakes", "スポイラー・エアブレーキ"),
    "ailerons": ("副翼", "Ailerons", "エルロン"),
    "elevators": ("升降舵", "Elevators", "エレベーター"),
    "rudder": ("雙垂尾方向舵", "Twin-fin rudders", "双垂直尾翼の方向舵"),
    "gear": ("起落架與輪艙門", "Undercarriage and doors", "脚と脚扉"),
    "steer": ("滑行轉向", "Ground steering", "地上操向"),
    "wheels": ("機輪轉動", "Wheel rotation", "車輪回転"),
    "reverse": ("反推套筒", "Reverser sleeves", "逆推力スリーブ"),
    "loading": ("裝載：機鼻、跪姿與坡道", "Loading: visor, kneel and ramp", "荷役：機首扉・ニーリング・ランプ"),
}


def meshes(ac):
    """Read triangle corners with independent UVs. The pinned AC has world-space meshes."""
    lines = iter(ac.read_text().splitlines())
    objects = defaultdict(list)
    for line in lines:
        if line.startswith("name "):
            name = line.split('"')[1]
        elif line.startswith("numvert "):
            vertices = [list(map(float, next(lines).split())) for _ in range(int(line.split()[1]))]
        elif line.startswith("refs "):
            polygon = []
            for _ in range(int(line.split()[1])):
                idx, u, v = next(lines).split()
                polygon.append(vertices[int(idx)] + [float(u), 1 - float(v)])
            for i in range(1, len(polygon)-1):
                objects[name].extend((polygon[0], polygon[i], polygon[i+1]))
    return {name: np.array(points) for name, points in objects.items()}


def clip(points, distance):
    """Split both sides at exactly the same seam, interpolating source UVs."""
    sides = ([], [])
    for tri in points.reshape(-1, 3, 5):
        for sign, out in zip((1, -1), sides):
            polygon = []
            for i, end in enumerate(tri):
                start = tri[i-1]
                a, b = sign * distance(start), sign * distance(end)
                if (a > 0) != (b > 0):
                    polygon.append(start + (end-start) * a/(a-b))
                if b > 0:
                    polygon.append(end)
            for j in range(1, len(polygon)-1):
                out.extend((polygon[0], polygon[j], polygon[j+1]))
    return tuple(np.asarray(p) for p in sides)


def fan_stage(original):
    """Fit a 33-blade D-18T fan inside the existing inlet; +AC X points aft."""
    tri = original.reshape(-1, 3, 5)
    low, high = original[:, :3].min(0), original[:, :3].max(0)
    cy, cz = ((low+high)/2)[1:]
    radius = min(high[1:]-low[1:])/2
    radial = np.hypot(tri[:,:,1]-cy, tri[:,:,2]-cz)
    spinner = tri[radial.max(axis=1)<radius*.4].reshape(-1,5)
    assert len(spinner)
    root = radial[radial<radius*.4].max()*.98
    tip = radius*.965   # clear the faceted liner at every rotor phase
    pitch = math.tau/33
    faces = {"Blades": [], "LeadingEdges": []}

    def face(group, a, b, c, d):
        faces[group].extend((a,b,c,a,c,d))

    for i in range(33):
        def point(span, chord, back=False):
            r = root+(tip-root)*span
            # Vary pitch along the span and camber across the chord.
            theta = pitch*(i+.24*span**1.4+chord*(.72-.12*span))
            x = high[0]+radius*(-.20+.06*span+chord*(.20-.07*span)
                                  -.035*math.sin(math.pi*chord)+(.014 if back else 0))
            return [x,cy+r*math.cos(theta),cz+r*math.sin(theta),0.,0.]

        for inner,outer in zip((0,.35,.7),(.35,.7,1)):
            for a,b in ((0,.095),(.095,.52),(.52,1)):
                group = "LeadingEdges" if a==0 else "Blades"
                face(group,point(inner,a),point(inner,b),point(outer,b),point(outer,a))
                face("Blades",point(inner,a,True),point(outer,a,True),point(outer,b,True),point(inner,b,True))
            for edge,group in ((0,"LeadingEdges"),(1,"Blades")):
                face(group,point(inner,edge),point(outer,edge),point(outer,edge,True),point(inner,edge,True))
        for a,b in ((0,.095),(.095,.52),(.52,1)):
            face("Blades",point(1,a),point(1,b),point(1,b,True),point(1,a,True))
    # Recess the opaque fan face behind the blade row as the dark duct interior.
    backing = tri[radial.max(axis=1)>=radius*.4].reshape(-1,5).copy()
    backing[:,0] += radius*.17
    return {"Spinner":spinner, "DuctShadow":backing,
            **{k:np.asarray(v) for k,v in faces.items()}}


def part(name):
    if "Engine" in name: return "engine"
    if "Rudder" in name or "TailFin" in name: return "vstab"
    if "Elevator" in name or "TailPlane" in name: return "hstab"
    if "-MG-" in name or "-NG-" in name or "WheelWell" in name: return "gear"
    if "Windows" in name or name.startswith("CP-"): return "cockpit"
    if any(s in name for s in ("Wing", "Flap", "Aileron", "Spoiler")): return "wing"
    return "fuselage"


def fg_vector(x, y, z):
    return np.array([-x, z, y])


def vector(node, suffix=""):
    return fg_vector(*(float(node.findtext(c+suffix, "0")) for c in "xyz"))


def build(source):
    folder = source / "Models"
    objects = meshes(folder / "AN225.ac")
    all_points = np.vstack(list(objects.values()))[:, :3]
    lo, hi = all_points.min(0), all_points.max(0)
    origin = np.array([-(hi[0]+lo[0])/2, lo[1], -(hi[2]+lo[2])/2])
    # Calibrate the three axes to the published 84 m length, 88.4 m span and 18.2 m height.
    scale = 12 / 84 * np.array([84, 18.2, 88.4]) / (hi-lo)
    ac_axes = np.array([-1, 1, -1])

    def position(aircraft):
        return ((aircraft-origin)*scale).round(7).tolist()

    def pack(points, color=None):
        vertices, indices = np.unique(points, axis=0, return_inverse=True)
        xyz = (vertices[:,:3]*ac_axes-origin)*scale
        base = xyz.min(0)
        step = np.maximum(np.ptp(xyz,axis=0), 1e-9)/65535
        entry = dict(q=b64(np.rint((xyz-base)/step).astype('<u2')), qo=base.tolist(),
                     qs=step.tolist(), i=b64(indices.astype('<u2')), iw=2,
                     c=color or [1,1,1,1], t=int(color is None))
        assert len(vertices) < 65536
        if color is None:
            entry["u"] = b64(np.rint(vertices[:,3:].clip(0,1)*65535).astype('<u2'))
        return entry

    parts = {key: [] for key in ("fuselage","cockpit","wing","engine","vstab","hstab","gear")}
    surfaces = []
    paths = defaultdict(list)
    translations = defaultdict(lambda: np.zeros(3))
    def joint(key, channel, center, axis, degrees, **extras):
        return dict(id=key, channel=channel, pv=position(center), ax=(np.asarray(axis)*scale / np.linalg.norm(np.asarray(axis)*scale)).tolist(),
                    angle=math.radians(degrees), **extras)

    for i, anim in enumerate(ET.parse(folder / "AN-225-Mrija.xml").findall("animation")):
        prop, kind = anim.findtext("property",""), anim.findtext("type")
        names = set(anim.findall("object-name"))
        names = {n.text for n in names}
        if not names or kind not in ("rotate","translate","spin"): continue
        if "compression" in prop: continue
        if prop.startswith("gear/"): channel = "gear"
        elif "left-aileron" in prop or "right-aileron" in prop: channel = "ailerons"
        elif "rudder-pos" in prop: channel = "rudder"
        elif "elevator-pos" in prop: channel = "elevators"
        elif "flap-pos" in prop: channel = "flaps"
        else:
            channel = {"0":"slats", "1":"spoilers", "2":"wheels","4":"steer"}.get(prop.split("[")[-1].rstrip("]"))
        if channel is None: continue
        axis = vector(anim.find("axis"))
        factor = float(anim.findtext("factor","1"))
        if kind == "translate":
            for name in names: translations[name] += axis / np.linalg.norm(axis)*scale*factor
            continue
        curve = [(float(e.findtext("ind")),float(e.findtext("dep"))) for e in anim.findall("interpolation/entry")]
        extra = {}
        if curve:
            if channel=="gear": curve = sorted((1-x,y) for x,y in curve)
            factor = max(abs(y) for _,y in curve) or 1
            extra["motion"] = [[x,y/factor] for x,y in curve]
        if channel=="ailerons" and "right-" in prop: factor *= -1
        if channel=="wheels":
            factor = 360
            names.update(n.replace("Tyre","Hub") for n in list(names))
        if channel=="elevators":
            names.update(n.replace("-T","-C") for n in list(names))
        j = joint(f"{channel}-{i}",channel,vector(anim.find("center"),"-m"),axis,factor,**extra)
        # The simulator hides the moving wheels and substitutes a closed-door mesh.
        # Our continuous rig retains the wheels. Tune the virtual pivots and folded
        # doors to clear those meshes throughout the travel (see BVH regression).
        if channel == "gear":
            if any("-MG-" in n and n.endswith("UDoor") for n in names):
                j["angle"] *= 1.32
            elif any(n.endswith("LDoor") for n in names):
                j["angle"] *= .45
            elif any("-NG-IS-Door" in n for n in names):
                j["angle"] *= -1
            elif any("-MG-" in n and n.endswith("Tyre") for n in names):
                j["pv"][2] *= .80
                j["pv"][1] -= .035
            elif any("-NG-" in n and n.endswith("Tyre") for n in names):
                j["pv"][1] += .09
        for name in names: paths[name].append(j)

    # Cut the visor below the fixed flight deck. Preserve UV continuity across the hinge seam.
    objects["Fuselage"], objects["Visor"] = clip(objects["Fuselage"], lambda p:p[0]+21.8+.75*p[1])
    cargo = joint("visor","loading",np.array([24.5,3.6,0]),[0,0,1],82,
                  motion=[[0,0],[.45,1],[1,1]])
    paths["Visor"].append(cargo)
    for name in ("Fuselage_LLogos", "Fuselage_RLogos"):
        objects[name], objects[name+"-visor"] = clip(objects[name], lambda p:p[0]+21.8+.75*p[1])
        paths[name+"-visor"].append(cargo)
    # Simplified two-section loading ramp stowed along the hold floor.
    def quad(a,b,c,d):
        return np.array([list(v)+[0.,0.] for v in (a,b,c,a,c,d)])
    width = 3.05
    sill = -20.65
    floor = -1.47
    # Two telescoping sections slide forward after the door has cleared.
    for i in range(2):
        start, end = sill-.04*i, sill+5.1-.04*i
        y = floor+.06*i
        key = f"Ramp-{i}"
        objects[key] = quad((start,y,-width),(end,y,-width),(end,y,width),(start,y,width))
        # Stow in floor; noseward movement followed by a small downward slope.
        paths[key].append(joint(key,"loading",np.array([-sill,floor,0]),[0,0,1],-6.5,
                                motion=[[0,0],[.55,0],[1,1]]))
    objects["Hold-floor"] = quad((sill,floor,-3.16),(22,floor,-3.16),(22,floor,3.16),(sill,floor,3.16))
    for s in (-1,1):
        z = s*3.16
        objects[f"Hold-wall-{s}"] = quad((sill,floor,z),(22,floor,z),(22,2.85,z),(sill,2.85,z))
    objects["Hold-bulkhead"] = quad((22,floor,-3.16),(22,2.85,-3.16),(22,2.85,3.16),(22,floor,3.16))
    # Front support shoes come down while the forward gear folds. Keep them inside
    # the hull in flight; the exact jack station and stroke are illustrative.
    for side in (-1, 1):
        cx, cz = -17.6, side*2.38
        ring = [(cx+.26*math.cos(a), cz+.26*math.sin(a)) for a in np.linspace(0,2*math.pi,13)]
        faces = []
        for (x,z),(xx,zz) in zip(ring,ring[1:]):
            faces.append(quad((x,-.95,z),(xx,-.95,zz),(xx,.58,zz),(x,.58,z)))
            faces.append(quad((cx,-.95,cz),(x,-.95,z),(xx,-.95,zz),(cx,-.95,cz))[:3])
        key = f"Support-{side}"
        objects[key] = np.vstack(faces)
        paths[key].append(joint(key,"loading",origin,[0,0,1],0))
        translations[key] = np.array([0,-2.348,0])*scale
    for name in list(objects):
        if name.endswith("-Fan"):
            pts = objects[name][:,:3]
            center = (pts.min(0)+pts.max(0))/2*ac_axes
            rotor = joint(name,"rotor",center,[1,0,0],0,rpm=185)
            for component, mesh in fan_stage(objects.pop(name)).items():
                key = name+"-"+component
                objects[key] = mesh
                if component != "DuctShadow":
                    paths[key].append(rotor)
        if name.endswith("-Casing"):
            pts = objects[name]
            cut = np.quantile(pts[:,0],.65)
            key = name+"-Sleeve"
            objects[key],objects[name] = clip(pts, lambda p:p[0]-cut)
            translations[key] = np.array([-.56,0,0])*scale
            paths[key].append(joint(key,"reverse",origin,[1,0,0],0))
    controls = [dict(id=k,label=dict(zip(("zh","en","ja"),v)),min=-1 if k in
                ("ailerons","elevators","rudder","steer") else 0,max=1,step=.01) for k,v in LABELS.items()]
    # Share hinge nodes across skins. Place steering and tyre rotation below gear retraction.
    nodes = {}
    anchors = defaultdict(list)
    for name, points in objects.items():
        if name.endswith("CDoor"): continue  # alternate fully-closed duplicate skin
        pid = part(name)
        anchors[pid].append(points[:,:3])
        seq = paths[name]
        slide = translations.get(name)
        if slide is not None and not seq:
            seq.append(joint(name+"-slide","flaps",origin,[1,0,0],0))
        seq.sort(key=lambda j: {"gear":0,"steer":1,"wheels":2}.get(j["channel"],0))
        # Kneel the airframe about the main gear and retract the two nose legs.
        if "-MG-" not in name or "Door" in name or "Well" in name:
            seq.insert(0,joint("kneel-"+pid,"loading",np.array([-8.,-4.1,0]),[0,0,1],-3,
                               motion=[[0,0],[.2,0],[.55,1],[1,1]]))
        if "-NG-" in name and any(s in name for s in ("Tyre","Strut","Hub")):
            z = np.sign(points[:,2].mean())*-.93
            seq.insert(1,joint("kneel-leg-"+name[0],"loading",np.array([19.5,-2.2,z]),[0,0,1],90,
                               motion=[[0,0],[.15,0],[.32,.65],[.55,1],[1,1]]))
        parent = None
        for spec in seq:
            key = spec["id"]
            if key not in nodes:
                node = dict(spec,part=pid,e=[])
                if parent: node["parent"] = parent
                surfaces.append(node)
                nodes[key] = node
            parent = key
        color = [.34,.36,.38,1] if name.startswith(("Hold-","Ramp-","Support-")) else None
        if "-Fan-" in name:
            metal = {"Spinner": [.23,.25,.27], "Blades": [.32,.35,.38],
                     "LeadingEdges": [.62,.66,.69], "DuctShadow": [.027,.032,.038]}
            color = metal[name.rsplit("-",1)[1]]+[1]
        entry = pack(points,color)
        entry["name"] = name
        if "Logos" in name or name in ("Engine_Stripes","Wing_ID","TailFin_Flag"):
            entry["alphaTest"] = .45
        if slide is not None: entry["slide"] = slide.tolist()
        if name.startswith("Support-"):
            entry.update(slideStart=.18, slideEnd=.55)
        if name.startswith("Ramp-"):
            entry["slide"] = [(5.1 if name.endswith("0") else 10.1)*scale[0],0,0]
            entry["slideStart"] = .55
        (nodes[parent]["e"] if parent else parts[pid]).append(entry)

    image = Image.open(folder/"AN225-tx-001.rgb")
    image.save(ROOT/"assets/an225-flightgear.png", optimize=True)
    model = dict(meta=dict(format=2,model="an225",wheelRadius=float(.655*scale[1]),source="FlightGear An-225 / Lee Elliott & Herbert Wagner (GPL); SKY ARCHIVE loading rig"),
                 texture="assets/an225-flightgear.png",parts=parts,surfaces=surfaces,controls=controls,
                 anchors={p:position((np.vstack(v).min(0)+np.vstack(v).max(0))/2*ac_axes) for p,v in anchors.items()})
    (ROOT/"models/an225.json").write_text(json.dumps(model,ensure_ascii=False,separators=(",",":")),encoding="utf-8")


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source",type=Path)
    build(parser.parse_args().source)
