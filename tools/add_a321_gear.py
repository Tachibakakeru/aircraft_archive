"""Add editable, articulated A321 landing gear to the existing FR24 v2 model.

Run from the repository root: python tools/add_a321_gear.py
The FR24 source mesh contains gear doors/wells but no wheels or struts. This
original approximation follows the A321 airport-planning gear layout, not CAD.
https://www.aircraft.airbus.com/sites/g/files/jlcbta126/files/2023-02/Airbus-techdata-AC_A321_0322%20%282%29.pdf
"""
import json
import math
from array import array
from base64 import b64encode
from pathlib import Path


PATH = Path(__file__).resolve().parents[1] / "models/a321.json"
LIFT = 0.42  # Source mesh had engine nacelles at ground level, without wheels.
NOSE_PIVOT = [4.55, 1.10, 0]  # Inside the bay; a strut-top hinge exposes the drag brace.
TAG = "sky-archive-a321-gear-v1"
CREDIT = " + SKY ARCHIVE landing gear reconstruction"
RUBBER = [0.035, 0.040, 0.048, 1]
STEEL = [0.42, 0.48, 0.54, 1]
PISTON = [0.70, 0.75, 0.79, 1]
HUB = [0.57, 0.63, 0.67, 1]
MESHES = []


def add(name, vertices, faces, color):
    MESHES.append((name, vertices, faces, color))


def cylinder(name, a, b, radius, color, sides=16):
    direction = [b[i] - a[i] for i in range(3)]
    length = math.sqrt(sum(v * v for v in direction))
    direction = [v / length for v in direction]
    helper = [0, 1, 0] if abs(direction[1]) < 0.9 else [1, 0, 0]
    u = [direction[1]*helper[2]-direction[2]*helper[1],
         direction[2]*helper[0]-direction[0]*helper[2],
         direction[0]*helper[1]-direction[1]*helper[0]]
    ul = math.sqrt(sum(v*v for v in u))
    u = [v/ul for v in u]
    v = [direction[1]*u[2]-direction[2]*u[1],
         direction[2]*u[0]-direction[0]*u[2],
         direction[0]*u[1]-direction[1]*u[0]]
    verts = [[c[k]+radius*(math.cos(j*math.tau/sides)*u[k]
              +math.sin(j*math.tau/sides)*v[k]) for k in range(3)]
             for c in (a, b) for j in range(sides)]
    faces = [(j, (j+1)%sides, sides+(j+1)%sides, sides+j)
             for j in range(sides)]
    faces += [tuple(reversed(range(sides))), tuple(range(sides, 2*sides))]
    add(name, verts, faces, color)


def tire(name, x, y, z, radius, width):
    # Rounded shoulder and recessed hub; wheel axle is along the wingspan (Z).
    profile = [(-.50, .48), (-.49, .78), (-.34, .98), (-.22, 1),
               (.22, 1), (.34, .98), (.49, .78), (.50, .48)]
    sides = 24
    verts = [[x+radius*rr*math.cos(j*math.tau/sides),
              y+radius*rr*math.sin(j*math.tau/sides), z+width*zz]
             for zz,rr in profile for j in range(sides)]
    faces = [(k*sides+j, k*sides+(j+1)%sides,
              (k+1)*sides+(j+1)%sides, (k+1)*sides+j)
             for k in range(len(profile)-1) for j in range(sides)]
    add(name+" tyre", verts, faces, RUBBER)
    cylinder(name+" hub", (x,y,z-width*.51), (x,y,z+width*.51), radius*.47, HUB, 24)
    cylinder(name+" cap left", (x,y,z-width*.52), (x,y,z-width*.515), radius*.23, STEEL, 16)
    cylinder(name+" cap right", (x,y,z+width*.515), (x,y,z+width*.52), radius*.23, STEEL, 16)


def encode(vertices, faces, color):
    lo = [min(v[k] for v in vertices) for k in range(3)]
    step = [max(1e-9, (max(v[k] for v in vertices)-lo[k])/65535) for k in range(3)]
    q = array('H', [max(0, min(65535, round((v[k]-lo[k])/step[k])))
                    for v in vertices for k in range(3)])
    indices = array('H', [idx for face in faces for j in range(1,len(face)-1)
                          for idx in (face[0],face[j],face[j+1])])
    return dict(q=b64encode(q.tobytes()).decode(), qo=lo, qs=step,
                i=b64encode(indices.tobytes()).decode(), iw=2, c=color, t=0)


def assembly(name, pivot, axis, angle, make):
    MESHES.clear()
    make()
    return dict(id="skygear_"+name, part="gear", channel="gear", t="gear",
                pv=pivot, ax=axis, angle=angle,
                e=[encode(vertices, faces, color)
                   for _,vertices,faces,color in MESHES])


def main_gear(side):
    x, z = .15, side*1.025
    cylinder("outer oleo", (x,.96,z), (x,.42,z), .061, STEEL)
    cylinder("chrome piston", (x,.49,z), (x,.21,z), .041, PISTON)
    cylinder("forward drag strut", (x-.35,.88,z), (x-.07,.42,z), .024, STEEL)
    cylinder("aft brace", (x+.32,.86,z), (x+.06,.48,z), .021, STEEL)
    cylinder("torque link upper", (x,.46,z), (x-.10,.32,z), .016, STEEL)
    cylinder("torque link lower", (x-.10,.32,z), (x,.23,z), .016, STEEL)
    cylinder("axle", (x,.171,z-.205), (x,.171,z+.205), .030, STEEL)
    # Airbus A321: 1.270 m tire OD; twin-wheel track 0.927 m.
    for j, offset in enumerate((-.125,.125)):
        tire("main wheel "+str(j+1), x, .171, z+offset, .171, .122)


def nose_gear():
    x = 4.74
    cylinder("nose oleo", (x,.97,0), (x,.35,0), .050, STEEL)
    cylinder("nose piston", (x,.43,0), (x,.14,0), .035, PISTON)
    cylinder("nose drag strut", (x-.36,.90,0), (x-.05,.42,0), .023, STEEL)
    cylinder("nose torque link upper", (x,.40,0), (x-.08,.31,0), .014, STEEL)
    cylinder("nose torque link lower", (x-.08,.31,0), (x,.16,0), .014, STEEL)
    cylinder("nose axle", (x,.112,-.13), (x,.112,.13), .024, STEEL)
    # Airbus A321 nose wheel track is 0.500 m.
    for j, offset in enumerate((-.0675,.0675)):
        tire("nose wheel "+str(j+1), x, .112, offset, .112, .060)


def run():
    model = json.loads(PATH.read_text(encoding="utf-8"))
    marker = model["meta"].get("gearAddon")
    if marker and marker != TAG:
        raise ValueError("Unknown gear add-on; refusing to alter the model")
    if marker:
        model["surfaces"] = [s for s in model["surfaces"] if not s.get("id", "").startswith("skygear_")]
        model["controls"] = [c for c in model["controls"] if c["id"] != "gear"]
        model["meta"]["source"] = model["meta"]["source"].removesuffix(CREDIT)
    else:
        # Move the source flight-pose airframe upward so real wheels, not engines,
        # touch the floor. Existing surface geometry and hotspots move together.
        for entries in model["parts"].values():
            for entry in entries:
                entry["qo"][1] += LIFT
        for surface in model["surfaces"]:
            surface["pv"][1] += LIFT
            for entry in surface["e"]:
                entry["qo"][1] += LIFT
        for anchor in model["anchors"].values():
            anchor[1] += LIFT

    model["surfaces"] += [
        assembly("left_main", [.15,.96,-1.025], [1,0,0], -math.radians(80.5), lambda: main_gear(-1)),
        assembly("right_main", [.15,.96,1.025], [1,0,0], math.radians(80.5), lambda: main_gear(1)),
        assembly("nose", NOSE_PIVOT, [0,0,1], math.radians(92), nose_gear),
    ]
    model["controls"] = [dict(id="gear", label=dict(zh="起落架收放示意", en="Gear retraction demo",
                                                    ja="脚格納デモ"), min=0, max=1, step=.01)]
    model["meta"]["gearAddon"] = TAG
    model["meta"]["source"] += CREDIT
    gears = [s for s in model["surfaces"] if s.get("channel") == "gear"]
    assert len(gears) == 3 and sum(len(s["e"]) for s in gears) >= 36
    assert sum(e["c"] == RUBBER for s in gears for e in s["e"]) == 6
    assert min(e["qo"][1] for s in gears for e in s["e"]) == 0
    assert min(e["qo"][1] for e in model["parts"]["engine"]) >= LIFT - 1e-6
    # Extended tires touch y=0; fully stowed wheel centers fit inside the hull.
    for side in (-1, 1):
        angle = side * math.radians(80.5)
        for offset in (-.125, .125):
            y, z = .171-.96, offset
            stowed_y = .96 + y*math.cos(angle)-z*math.sin(angle)
            stowed_z = side*1.025 + y*math.sin(angle)+z*math.cos(angle)
            assert stowed_y > .65 and abs(stowed_z) < .6
    nose_dx, nose_dy = 4.74-NOSE_PIVOT[0], .112-NOSE_PIVOT[1]
    nose_angle = math.radians(92)
    nose_x = NOSE_PIVOT[0] + nose_dx*math.cos(nose_angle)-nose_dy*math.sin(nose_angle)
    nose_y = NOSE_PIVOT[1] + nose_dx*math.sin(nose_angle)+nose_dy*math.cos(nose_angle)
    assert 5.3 < nose_x < 5.8 and nose_y > 1.2
    PATH.write_text(json.dumps(model, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print("A321: six wheels, three articulated assemblies, existing airframe retained")


if __name__ == "__main__":
    run()
