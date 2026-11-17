"""blender --background --python-exit-code 1 --python tools/build_dreamlifter_blender.py

Boeing 747-400 LCF Dreamlifter — original educational model (trial v2).
Blender metres, nose +X, Z up, port = +Y, ground z = 0. Exports the editable rigged
.blend and the archive's quantized v2 JSON (length normalised to 12).
Geometry is an interpretation of published dimensions (length 71.68 m, span 64.4 m,
height 21.54 m, hold diameter 8.38 m), with stations checked against Boeing's published
photographs and a public three-view drawing; not Boeing CAD. Helpers are shared with the
Concorde prototype (tools/build_concorde_blender.py).
"""
import sys, json, math
from pathlib import Path
import bpy, bmesh
from mathutils import Vector, Matrix

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_concorde_blender as c

ROOT = c.ROOT
LENGTH = 71.68
c.SCALE = 12 / LENGTH
RIG, OBJECTS = c.RIG, c.OBJECTS
BY_NAME = {}
tr, rod = c.tr, c.rod
X = lambda s: LENGTH / 2 - s          # s = metres aft of the nose
rad = math.radians
M = {}


# ───────────────────────── generic builders ─────────────────────────
def mesh(name, verts, faces, mat, part, joint=None, smooth=True):
    ob = BY_NAME[name] = c.mesh(name, [tuple(v) for v in verts], faces, M[mat], part, joint, smooth)
    return ob


def joint(name, pivot, axis, angle, channel, part, parent=None, probe=None, want=None, motion=None):
    """Hinge empty. With probe/want the sign of `angle` is chosen so that a positive
    control value moves `probe` towards the direction `want`."""
    axis = Vector(axis).normalized()
    if probe is not None:
        moved = Matrix.Rotation(.05, 3, axis) @ (Vector(probe) - Vector(pivot))
        if (moved - (Vector(probe) - Vector(pivot))).dot(Vector(want)) < 0:
            angle = -angle
    c.joint(name, tuple(pivot), tuple(axis), angle, channel, part)
    if motion is not None:
        RIG[name]['motion'] = motion
    if parent:
        ob = RIG[name]['object']
        ob.parent = RIG[parent]['object']
        ob.matrix_parent_inverse = ob.parent.matrix_world.inverted()
        RIG[name]['parent'] = parent


def grid_faces(rows, ring, closed=True, caps=True):
    n = ring if closed else ring - 1
    faces = [(j*ring+k, j*ring+(k+1) % ring, (j+1)*ring+(k+1) % ring, (j+1)*ring+k)
             for j in range(rows-1) for k in range(n)]
    if caps:
        faces += [tuple(reversed(range(ring))), tuple(range((rows-1)*ring, rows*ring))]
    return faces


def revolve(name, centre, profile, mat, part, joint_name=None, sides=40, caps=False):
    """Axisymmetric body about the X axis: profile = [(metres aft of centre, radius)]."""
    cx, cy, cz = centre
    verts = [(cx-d, cy+r*math.cos(k*math.tau/sides), cz+r*math.sin(k*math.tau/sides))
             for d, r in profile for k in range(sides)]
    return mesh(name, verts, grid_faces(len(profile), sides, caps=caps), mat, part, joint_name)


def extrude(name, outline, offset, mat, part, joint_name=None, smooth=False):
    """Closed outline (list of points) swept by ±offset/2."""
    o = Vector(offset) / 2
    verts = [Vector(p)-o for p in outline] + [Vector(p)+o for p in outline]
    n = len(outline)
    faces = [tuple(reversed(range(n))), tuple(range(n, 2*n))] + \
            [(i, (i+1) % n, (i+1) % n+n, i+n) for i in range(n)]
    return mesh(name, verts, faces, mat, part, joint_name, smooth)


# ───────────────────────── fuselage: double-bubble hull ─────────────────────────
# rows: s, lower-lobe radius / centre z, upper-lobe radius / centre z.
# 747 forward body = main lobe + flight-deck hump; LCF = original lower lobe + 8.38 m hold.
DOME0, DOME1 = 9.6, 15.0      # blunt front of the enlarged hold, directly behind the flight deck
TAILCONE = 69.0               # fuselage end; the taller fin overhangs it to 71.68 m
HULL = [(0, .05, 5.0, .03, 5.02), (.6, .95, 5.0, .3, 5.5), (1.5, 1.6, 4.95, .7, 6.0),
        (3, 2.3, 5.0, 1.2, 6.9), (5, 2.85, 5.15, 1.6, 7.6), (7.5, 3.15, 5.32, 1.85, 7.95),
        (DOME0, 3.25, 5.4, 1.9, 8.0)] + \
       [(DOME0+(DOME1-DOME0)*t, 3.25, 5.4, 1.9+2.29*math.sqrt(1-(1-t)**2), 8.0-.09*t)
        for t in (.01, .03, .07, .13, .22, .34, .48, .64, .82, 1)] + \
       [(48.5, 3.25, 5.4, 4.19, 7.91), (52, 3.1, 5.6, 3.9, 7.55), (55, 2.8, 6.0, 3.4, 7.2),
        (58, 2.4, 6.5, 2.75, 7.15), (62, 1.8, 7.1, 1.95, 7.5), (66, 1.05, 7.7, 1.1, 7.95),
        (68.3, .45, 8.05, .45, 8.15), (TAILCONE, .1, 8.15, .1, 8.2)]
BREAK = 48.5      # swing-tail joint
SIDES = 72


def hull_point(s, theta, lift=0.0):
    """Convex hull of the two lobes, sampled by outward normal direction theta."""
    r1, z1, r2, z2 = c.profile(HULL, s)
    r, z = (r2, z2) if z2*math.sin(theta)+r2 >= z1*math.sin(theta)+r1 else (r1, z1)
    r += lift
    return Vector((X(s), r*math.cos(theta), z+r*math.sin(theta)))


def hull(name, s0, s1, mat, part, joint_name=None, step=.25):
    ss = [s0]                                             # finer rings over the blunt hold dome
    while ss[-1] < s1-1e-6:
        ss.append(min(s1, ss[-1]+(.09 if DOME0 <= ss[-1] < DOME1 else step)))
    ss.reverse(); n = len(ss)                             # tail → nose (increasing x)
    verts = [hull_point(s, k*math.tau/SIDES) for s in ss for k in range(SIDES)]
    return mesh(name, verts, grid_faces(n, SIDES), mat, part, joint_name)


def skin_patch(name, s0, s1, a0, a1, mat, part, side=1, joint_name=None, lift=.02, ns=6, na=6):
    """Conformal panel on the hull (glazing, door outlines, trim)."""
    verts = []
    for j in range(ns+1):
        for k in range(na+1):
            p = hull_point(s0+(s1-s0)*j/ns, rad(a0+(a1-a0)*k/na), lift)
            verts.append((p.x, side*p.y, p.z))
    return mesh(name, verts, grid_faces(ns+1, na+1, closed=False, caps=False), mat, part, joint_name)


# ───────────────────────── lifting surfaces ─────────────────────────
def naca(f, tc):
    return 5*tc*(.2969*math.sqrt(f)-.1260*f-.3516*f*f+.2843*f**3-.1036*f**4)


class Surface:
    """Planform described by callables of the span coordinate u (metres)."""
    def __init__(self, le, te, height, tc, span_axis, up, side=1):
        self.le, self.te, self.height, self.tc = le, te, height, tc
        self.span_axis, self.up, self.side = Vector(span_axis), Vector(up), side

    def point(self, u, f, where=0.0, lift=0.0):
        """where: +1 upper skin, −1 lower skin, 0 chord line."""
        s = self.le(u)+(self.te(u)-self.le(u))*f
        chord = self.te(u)-self.le(u)
        t = max(.012, naca(f, self.tc(u))*chord)*where + lift
        return Vector((X(s), 0, 0)) + self.span_axis*(u*self.side) + self.up*(self.height(u)+t)

    def solid(self, name, us, f0, f1, mat, part, joint_name=None, nf=9):
        fr = [f0+(f1-f0)*(.5-.5*math.cos(math.pi*i/(nf-1))) for i in range(nf)]
        verts = []
        for u in us:
            verts += [self.point(u, f, 1) for f in fr] + [self.point(u, f, -1) for f in reversed(fr)]
        return mesh(name, verts, grid_faces(len(us), 2*nf), mat, part, joint_name)

    def skin_panel(self, name, u0, u1, f0, f1, where, mat, part, joint_name, thick=.035):
        """Thin plate lying on the upper (+1) or lower (−1) skin: spoilers, Krueger flaps."""
        verts = [self.point(u, f, where, lift) for lift in (where*.012, where*(.012+thick))
                 for u, f in ((u0, f0), (u1, f0), (u1, f1), (u0, f1))]
        faces = [(3, 2, 1, 0), (4, 5, 6, 7)]+[(i, (i+1) % 4, (i+1) % 4+4, i+4) for i in range(4)]
        return mesh(name, verts, faces, mat, part, joint_name, smooth=False)

    def hinged(self, name, u0, u1, f0, angle, channel, part, mat, want, slide=None, parent=None):
        """Trailing-edge device from chord fraction f0 to the trailing edge."""
        a, b = self.point(u0, f0), self.point(u1, f0)
        joint(name, a, b-a, angle, channel, part, parent,
              probe=self.point((u0+u1)/2, 1), want=want)
        ob = self.solid(name, [u0, u1], f0, 1, mat, part, name, nf=6)
        if slide:
            ob['slide'], ob['slideEnd'] = slide, 1.0
        return ob

    def fowler(self, name, u0, u1, f0, part):
        """Triple-slotted Fowler flap: fore, mid and aft segments on their own hinges. Each
        slide is solved so a segment's leading edge follows the trailing edge ahead of it."""
        um, cuts = (u0+u1)/2, [f0, f0+.42*(1-f0), f0+.76*(1-f0), 1]
        move, gap = Vector((-.95, 0, -.16)), Vector((-.07, 0, -.05))
        for k, deg in enumerate((18, 34, 52)):
            seg = f'{name}_{k}'
            a, b = self.point(u0, cuts[k]), self.point(u1, cuts[k])
            joint(seg, a, b-a, rad(deg), 'flaps', part, probe=self.point(um, cuts[k+1]), want=DOWN)
            ob = self.solid(seg, [u0, u1], cuts[k], cuts[k+1], 'control', part, seg, nf=5)
            rot = Matrix.Rotation(RIG[seg]['angle'], 3, Vector(RIG[seg]['axis']))
            ob['slide'], ob['slideEnd'] = tuple(rot.inverted() @ move), 1.0
            chord = self.point(um, cuts[k+1])-self.point(um, cuts[k])
            move = move + rot @ chord - chord + gap

    def trailing(self, prefix, f0, u_start, u_end, devices, part, mat, parent=None):
        """Fill the strip aft of f0: movable devices plus fixed fillers in the gaps."""
        u = u_start
        for name, u0, u1, angle, channel, want, slide in sorted(devices, key=lambda d: d[1]):
            if u0-u > .02:
                self.solid(prefix+' fixed trailing edge', [u, u0-.03], f0, 1, mat, part, parent, nf=6)
            if channel == 'flaps':
                self.fowler(name, u0, u1, f0, part)
            else:
                self.hinged(name, u0, u1, f0, angle, channel, part, 'control', want, slide, parent)
            u = u1+.03
        if u_end-u > .02:
            self.solid(prefix+' fixed trailing edge', [u, u_end], f0, 1, mat, part, parent, nf=6)


# 747-400 wing: 41.5° leading-edge sweep, trailing-edge kink at the inboard nacelle, 7° dihedral.
HALF_SPAN, KINK, TIP_START = 32.2, 11.7, 30.2
wing_le = lambda y: 18.1+.8847*y
wing_te = lambda y: 34.6+.308*y if y <= KINK else 38.2+.6*(y-KINK)
wing_z = lambda y: 3.55+max(0, y-3.25)*math.tan(rad(7))
wing_tc = lambda y: .13-.05*y/HALF_SPAN
UP, DOWN, AFT, FWD, PORT = (0, 0, 1), (0, 0, -1), (-1, 0, 0), (1, 0, 0), (0, 1, 0)


def build_wing(side):
    w = Surface(wing_le, wing_te, wing_z, wing_tc, (0, 1, 0), UP, side)
    tag = 'L' if side > 0 else 'R'
    BOX = .68
    w.solid(f'Wing box {tag}', [0, 3.25, KINK, 20.8, TIP_START], 0, BOX, 'white', 'wing')
    w.solid(f'Wingtip {tag}', [TIP_START, 31.6, HALF_SPAN], 0, 1, 'white', 'wingtip')
    # Triple-slotted Fowler flaps, inboard high-speed and outboard low-speed ailerons.
    flap = lambda n, a, b: (f'flap_{tag}_{n}', a, b, 0, 'flaps', DOWN, None)
    ail = lambda n, a, b: (f'aileron_{tag}_{n}', a, b, rad(20)*side, 'ailerons', DOWN, None)
    w.trailing(f'Wing {tag}', BOX, 3.6, TIP_START,
               [flap('in', 3.9, 11.0), ail('in', 11.2, 13.0), flap('out', 13.2, 21.5), ail('out', 21.8, 28.2)],
               'wing', 'white')
    # Flap-track (canoe) fairings: fixed nose under the wing box, tail riding on the fore flap.
    for n, (y, flap_id) in enumerate(((5.6, 'in'), (9.4, 'in'), (14.9, 'out'), (19.6, 'out'))):
        hinge = w.point(y, BOX, -1)
        centre = (hinge.x+2.4, hinge.y, hinge.z-.16)
        fore = f'flap_{tag}_{flap_id}_0'
        revolve(f'Flap track fairing {tag}{n}', centre, [(0, .02), (.3, .16), (1.0, .27), (2.4, .31)],
                'white', 'wing', sides=16)
        ob = revolve(f'Flap track fairing tail {tag}{n}', centre, [(2.4, .31), (3.6, .27), (4.7, .15), (5.3, .02)],
                     'white', 'wing', fore, sides=16)
        ob['slide'], ob['slideEnd'] = tuple(BY_NAME[fore]['slide']), 1.0
    # Six spoiler panels per wing ahead of the flaps (two inboard, four outboard).
    spans = [(4.6, 7.6), (7.7, 10.7), (13.5, 15.4), (15.5, 17.4), (17.5, 19.4), (19.5, 21.4)]
    for n, (a, b) in enumerate(spans):
        name = f'spoiler_{tag}_{n}'
        p0, p1 = w.point(a, .56, 1), w.point(b, .56, 1)
        joint(name, p0, p1-p0, rad(45), 'spoilers', 'wing', probe=w.point((a+b)/2, BOX, 1), want=UP)
        w.skin_panel(name, a, b, .56, BOX-.005, 1, 'control', 'wing', name)
    # Leading edge: 3 inboard Krueger flaps + 11 outboard variable-camber Krueger flaps per wing.
    kr = [(4.4, 6.5), (6.6, 8.7), (8.8, 10.6)] + \
         [(12.8+i*1.42, 12.8+i*1.42+1.36) for i in range(5)] + \
         [(22.0+i*1.37, 22.0+i*1.37+1.31) for i in range(6)]
    for n, (a, b) in enumerate(kr):
        name = f'krueger_{tag}_{n:02}'
        p0, p1 = w.point(a, .015, -1), w.point(b, .015, -1)
        joint(name, p0, p1-p0, rad(125), 'slats', 'wing', probe=w.point((a+b)/2, .11, -1), want=DOWN)
        w.skin_panel(name, a, b, .015, .11, -1, 'control', 'wing', name)
    return w


def fan_cowl(centre, tag):
    x,y,z = centre
    profile = [(1.01,1.474),(1.4,1.49),(1.82,1.485),(2.16,1.477)]
    rows, arcs = len(profile), 29
    for side in (-1,1):
        hinge = f'fan_cowl_{tag}_{"left" if side > 0 else "right"}'
        pivot = (x-1.58,y+side*.324,z+1.446)
        joint(hinge,pivot,(1,0,0),side*rad(52),'fan_cowl','engine')
        angles = [rad(-89.55+(77.4+89.55)*i/(arcs-1)) for i in range(arcs)]
        verts = [(x-depth,y+side*(radius+offset)*math.cos(a),z+(radius+offset)*math.sin(a))
                 for offset in (0,-.034) for depth,radius in profile for a in angles]
        size = rows*arcs
        faces = grid_faces(rows,arcs,closed=False,caps=False)
        faces += [tuple(size+k for k in reversed(face)) for face in faces]
        rim = list(range(arcs)) + [(i+1)*arcs-1 for i in range(1,rows)]
        rim += list(range(size-2,size-arcs-1,-1)) + [i*arcs for i in range(rows-2,0,-1)]
        faces.extend((i,j,j+size,i+size) for i,j in zip(rim,rim[1:]+rim[:1]))
        mesh(f'PW4062 fan cowl door {hinge}',verts,faces,'blue','engine',hinge)

    crown = [rad(77.75+24.5*i/12) for i in range(13)]
    verts = [(x-depth,y+radius*math.cos(a),z+radius*math.sin(a))
             for depth,radius in profile for a in crown]
    mesh(f'Fixed fan cowl crown {tag}',verts,grid_faces(rows,len(crown),closed=False,caps=False),'blue','engine')
    revolve(f'Fan case {tag}',centre,[(1.00,1.32),(1.13,1.34),(1.97,1.31),(2.17,1.33)],'metal','engine')
    for i,depth in enumerate((1.16,1.55,1.98),1):
        revolve(f'Fan case flange {tag} {i}',centre,
                [(depth-.014,1.328),(depth-.014,1.369),(depth+.014,1.369),
                 (depth+.014,1.328)],'dark','engine',sides=40)
    for side in (-1,1):
        c.rod(f'Fan case service line {tag}',(x-1.10,y+side*1.285,z-.20),
              (x-2.08,y+side*1.285,z-.16),.020,M['blue'],'engine',sides=8)


def build_engine(side, y, n):
    """PW4062: hollow inlet with fan and spinner, short fan cowl, core cowl, exhaust plug, pylon."""
    zc = wing_z(y)-2.2
    s0 = wing_le(y)-4.4
    centre = (X(s0), side*y, zc)
    tag = f'{"L" if side > 0 else "R"}{n}'
    revolve(f'Fixed inlet outer barrel {tag}',centre,[(.02,1.20),(0,1.27),(.1,1.36),(.5,1.45),
            (.99,1.474)],'blue','engine')
    fan_cowl(centre,tag)
    revolve(f'Fixed aft nacelle shell {tag}',centre,[(2.18,1.477),(3.0,1.46),(3.9,1.36),
            (3.95,1.30)],'blue','engine')
    revolve(f'Inlet lip {tag}', centre, [(0, 1.27), (.02, 1.20), (.25, 1.17), (.95, 1.16)], 'metal', 'engine')
    revolve(f'Fan disc {tag}', centre, [(.95, 1.16), (.96, .32)], 'dark', 'engine')
    fan = c.rotor(f'pw4062_rotor_{tag}',centre,29)
    revolve(f'Spinner {tag}', centre, [(.97, .34), (.75, .27), (.5, .15), (.36, .01)], 'metal', 'engine', fan)
    c.rotor_blades(f'PW4062 fan blade row {tag}',centre,
                   [(.81,.28,-.050),(.72,1.12,.060),(.86,1.12,.102),(.90,.28,.031)],
                   38,.030,M['metal'],fan)
    revolve(f'Fan exit {tag}', centre, [(3.95, 1.30), (3.6, 1.26), (3.6, .96)], 'dark', 'engine')
    revolve(f'Core cowl {tag}', centre, [(3.6, .96), (4.3, .93), (5.5, .62), (5.55, .58)], 'metal', 'engine')
    revolve(f'Exhaust plug {tag}', centre, [(5.3, .56), (5.55, .42), (6.4, .16), (6.7, .01)], 'dark', 'engine')
    le = wing_le(y)
    pts = [(X(s0+.9), zc+1.44), (X(le-.6), wing_z(y)-.05), (X(le+2.6), wing_z(y)-.40),
           (X(le+3.6), wing_z(y)-.55), (X(s0+4.6), zc+.90), (X(s0+3.4), zc+1.38)]
    extrude(f'Pylon {tag}', [(x, side*y, z) for x, z in pts], (0, .42, 0), 'white', 'engine')


# ───────────────────────── landing gear ─────────────────────────
TYRE_R, TYRE_W = .62, .44


def wheel(name, centre, mat_joint, r=TYRE_R, w=TYRE_W):
    x, y, z = centre
    rod(name+' tyre', (x, y-w/2, z), (x, y+w/2, z), r, M['rubber'], 'gear', mat_joint, 28)
    rod(name+' hub', (x, y-w/2-.006, z), (x, y+w/2+.006, z), r*.46, M['steel'], 'gear', mat_joint, 20)


def bogie(name, centre, joint_name, axle=.72, track=.56):
    x, y, z = centre
    rod(name+' truck beam', (x-axle, y, z), (x+axle, y, z), .13, M['steel'], 'gear', joint_name)
    for dx in (-axle, axle):
        rod(name+' axle', (x+dx, y-track, z), (x+dx, y+track, z), .09, M['steel'], 'gear', joint_name)
        for dy in (-track, track):
            wheel(name, (x+dx, y+dy, z), joint_name)


def build_gear():
    # Nose gear: twin wheels, retracts forward.
    pv, wc = Vector((X(7.6), 0, 3.1)), Vector((X(7.45), 0, TYRE_R))
    joint('nose_gear', pv, (0, 1, 0), rad(100), 'gear', 'gear', probe=wc, want=FWD)
    rod('Nose strut', pv, wc, .13, M['steel'], 'gear', 'nose_gear')
    rod('Nose drag brace', pv+Vector((1.5, 0, -.1)), pv.lerp(wc, .55), .07, M['steel'], 'gear', 'nose_gear')
    rod('Nose axle', wc-Vector((0, .5, 0)), wc+Vector((0, .5, 0)), .08, M['steel'], 'gear', 'nose_gear')
    for y in (-.5, .5):
        wheel('Nose', (wc.x, y, wc.z), 'nose_gear')
    for side in (-1, 1):
        tag = 'L' if side > 0 else 'R'
        # Wing gear: trunnion on the rear spar, swings inboard and slightly forward.
        pv, wc = Vector((X(30.9), side*5.5, 3.45)), Vector((X(31.5), side*5.5, TYRE_R))
        p0, p1 = wc-pv, Vector((.55, -side*2.75, -.10))
        name = f'wing_gear_{tag}'
        joint(name, pv, p0.cross(p1), p0.angle(p1), 'gear', 'gear')
        rod(name+' oleo', pv, wc, .17, M['steel'], 'gear', name)
        rod(name+' drag brace', pv+Vector((1.3, 0, -.1)), pv.lerp(wc, .5), .08, M['steel'], 'gear', name)   # near the swing axis: stays inside the wing when stowed
        bogie(name, wc, name)
        # Body gear: retracts forward; the truck is a nested joint that stays level.
        pv, wc = Vector((X(35.5), side*1.9, 3.0)), Vector((X(34.6), side*1.9, TYRE_R))
        name = f'body_gear_{tag}'
        swing = rad(74)
        joint(name, pv, (0, 1, 0), swing, 'gear', 'gear', probe=wc, want=FWD)
        rod(name+' oleo', pv, wc, .17, M['steel'], 'gear', name)
        rod(name+' drag brace', pv+Vector((1.4, 0, 0)), pv.lerp(wc, .5), .08, M['steel'], 'gear', name)
        joint(name+'_truck', wc, (0, 1, 0), -RIG[name]['angle'], 'gear', 'gear', parent=name)
        bogie(name, wc, name+'_truck')


GEAR_TRAVEL = [(0, 0), (.15, 0), (.8, 1), (1, 1)]
DOOR_TRAVEL = [(0, -.85), (.8, -.85), (1, 1)]
NOSE_DOOR_TRAVEL = [(0, 0), (.8, 0), (1, 1)]
FOLDING_DOOR_TRAVEL = [(0, 0), (.15, 1), (.8, 1), (1, 0)]


def door(name, s0, s1, y, z, drop, toward, motion=DOOR_TRAVEL):
    """Bay panel hangs from the open hinge line at travel zero."""
    a, b = Vector((X(s0), y, z)), Vector((X(s1), y, z))
    down = Vector((0, 0, -drop))
    joint(name, a, b-a, rad(90), 'gear', 'gear', probe=a+down, want=(0, toward, 0), motion=motion)
    extrude(name, [a, b, b+down, a+down], (0, .05, 0), 'white', 'gear', name)


def build_doors():
    for side in (-1, 1):
        tag = 'L' if side > 0 else 'R'
        door(f'nose_door_{tag}', 5.5, 8.4, side*.84, 2.2, .84, -side, NOSE_DOOR_TRAVEL)
        door(f'body_door_{tag}_in', 33.2, 36.8, side*1.01, 1.82, .89, side)
        door(f'body_door_{tag}_out', 33.2, 36.8, side*2.79, 2.05, .89, -side)
        # The wing wheel well has a two-leaf door. Both sections are flush in
        # the closed pose, then fold clear before the gear starts to move.
        x0, x1 = X(29.6), X(32.2)
        y, z = side*1.9, 1.95
        for suffix, width, y0, angle, parent in (
                ('in', 1.10, y, -85, None),
                ('out', .83, y+side*1.10, 169, f'wing_door_{tag}_in')):
            leaf = f'wing_door_{tag}_{suffix}'
            y1 = y0+side*width
            joint(leaf, (x0,y0,z), (1,0,0), side*rad(angle), 'gear', 'gear', parent=parent,
                  motion=FOLDING_DOOR_TRAVEL)
            extrude(leaf, [(x0,y0,z),(x1,y0,z),(x1,y1,z),(x0,y1,z)], (0,0,.042), 'white', 'gear', leaf)
        # Strut-mounted door travels with the wing gear leg.
        pv = Vector((X(30.9), side*5.5, 3.45))
        extrude(f'Wing gear strut door {tag}', [pv+Vector((dx, side*.3, dz)) for dx, dz in
                ((-.75, -.2), (.75, -.2), (.75, -1.75), (-.75, -1.75))], (0, .05, 0), 'white', 'gear', f'wing_gear_{tag}')


def recalc_normals():
    for ob in OBJECTS:
        bm = bmesh.new()
        bm.from_mesh(ob.data)
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        bm.to_mesh(ob.data)
        bm.free()


# ───────────────────────── assembly ─────────────────────────
def build():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for key, name, color, metal in [
            ('white', 'Boeing white airframe', (.90, .92, .94), 0), ('blue', 'Boeing blue trim', (.02, .16, .42), 0),
            ('control', 'Flight control surfaces', (.72, .76, .81), 0), ('glass', 'Flight deck glazing', (.03, .07, .11), .3),
            ('dark', 'Fan and exhaust interior', (.03, .034, .04), 0), ('metal', 'Bare metal lip and core', (.55, .58, .62), .8),
            ('steel', 'Gear steel', (.42, .48, .54), .75), ('rubber', 'Tyres', (.018, .02, .023), 0)]:
        M[key] = c.material(name, color, metal)

    # Swing tail: three hinge groups share the port-side hinge line so each part stays selectable.
    hinge = (X(BREAK), 4.19, 7.91)
    tail_probe = (X(TAILCONE), 0, 8)
    for part in ('fuselage', 'vstab', 'hstab'):
        joint('swing_'+part, hinge, (0, 0, 1), rad(93), 'swingtail', part, probe=tail_probe, want=PORT)

    hull('Flight deck and nose section', 0, DOME0, 'white', 'cockpit')
    hull('Enlarged cargo fuselage', DOME0, BREAK, 'white', 'fuselage')
    hull('Swing tail fuselage', BREAK+.04, TAILCONE, 'white', 'fuselage', 'swing_fuselage')
    for s in (BREAK-.2, BREAK+.04):                                       # joint frames either side of the break
        verts = [hull_point(s+d, k*math.tau/SIDES, .03) for d in (0, .16) for k in range(SIDES)]
        mesh('Swing-tail joint frame', verts, grid_faces(2, SIDES, caps=False), 'control', 'fuselage',
             'swing_fuselage' if s > BREAK else None)
    # Port-side hinge fairings straddling the break (upper and lower), as on the real aircraft.
    for deg in (35, -14):
        p = hull_point(BREAK, rad(deg), -.1)
        revolve('Swing-tail hinge fairing', (p.x+1.5, p.y, p.z), [(0, .02), (.35, .3), (1.0, .45), (2.0, .45),
                (2.65, .3), (3.0, .02)], 'white', 'fuselage', sides=20)
    # Wing-to-body fairing also houses the stowed main gear.
    c.loft('Wing-to-body fairing', c.sampled([(X(41), .8, 3.3, .3), (X(39), 3.6, 3.25, 1.25), (X(36), 4.35, 3.2, 1.45),
           (X(24), 4.35, 3.2, 1.45), (X(21), 3.8, 3.3, 1.3), (X(19), .8, 3.5, .3)], .4), M['white'], 'fuselage')
    # Flight deck glazing, the nose's main-deck window row and door outlines; all-white body, no logos.
    for side in (-1, 1):
        skin_patch('Windshield', 4.45, 5.55, 38, 86, 'glass', 'windshield', side)
        skin_patch('Side window 1', 5.7, 6.45, 30, 62, 'glass', 'windshield', side)
        skin_patch('Side window 2', 6.6, 7.2, 30, 56, 'glass', 'windshield', side)
        for n in range(11):
            skin_patch('Nose window', 2.2+n*.48, 2.42+n*.48, 11, 17, 'glass', 'cockpit', side, lift=.012, ns=1, na=1)
        for s0, s1, a0, a1 in ((8.3, 8.35, -8, 26), (9.25, 9.3, -8, 26), (8.3, 9.3, 25, 26), (8.3, 9.3, -8, -7)):
            skin_patch('Crew door outline', s0, s1, a0, a1, 'control', 'cockpit', side, lift=.012)

    for side in (1, -1):
        build_wing(side)
        for n, y in enumerate((11.7, 20.8)):
            build_engine(side, y, n+1)

    # Vertical tail (1.5 m taller than the 747-400); its tip overhangs the tail cone to 71.68 m.
    fin = Surface(lambda z: 56.9+1.147*(z-10.9), lambda z: 65.3+.6*(z-10.9), lambda z: 0, lambda z: .10,
                  (0, 0, 1), (0, 1, 0))
    fin.solid('Vertical stabilizer', [8.8, 15, 21.2], 0, .70, 'blue', 'vstab', 'swing_vstab')
    fin.solid('Fin cap', [21.2, 21.54], 0, 1, 'blue', 'vstab', 'swing_vstab')
    fin.trailing('Fin', .70, 8.8, 21.2, [('rudder_lower', 9.9, 15.6, rad(25), 'rudder', PORT, None),
                 ('rudder_upper', 15.7, 21.15, rad(25), 'rudder', PORT, None)], 'vstab', 'blue', 'swing_vstab')
    # Horizontal stabilizer, 22.17 m span, inboard and outboard elevators each side.
    for side in (1, -1):
        tag = 'L' if side > 0 else 'R'
        hs = Surface(lambda y: 58.9+.734*(y-1), lambda y: 65.8+.317*(y-1), lambda y: 7.6+y*math.tan(rad(7)),
                     lambda y: .09, (0, 1, 0), UP, side)
        hs.solid(f'Horizontal stabilizer {tag}', [0, 5.5, 10.6], 0, .72, 'white', 'hstab', 'swing_hstab')
        hs.solid(f'Stabilizer tip {tag}', [10.6, 11.085], 0, 1, 'white', 'hstab', 'swing_hstab')
        hs.trailing(f'Stabilizer {tag}', .72, 1.6, 10.6,
                    [(f'elevator_{tag}_in', 1.8, 5.6, rad(22), 'elevators', DOWN, None),
                     (f'elevator_{tag}_out', 5.7, 10.55, rad(22), 'elevators', DOWN, None)],
                    'hstab', 'white', 'swing_hstab')
    build_gear()
    for rig in RIG.values():
        if rig['channel'] == 'gear':
            rig['motion'] = GEAR_TRAVEL
    build_doors()
    recalc_normals()


CONTROLS = [
    ('fan_cowl', tr('引擎風扇整流罩', 'Engine fan cowls', 'エンジン・ファンカウル'), 0),
    ('flaps', tr('襟翼', 'Flaps', 'フラップ'), 0),
    ('slats', tr('前緣克魯格襟翼', 'Leading-edge Krueger flaps', '前縁クルーガーフラップ'), 0),
    ('spoilers', tr('擾流板', 'Spoilers', 'スポイラー'), 0),
    ('ailerons', tr('副翼（內側＋外側）', 'Ailerons (inboard + outboard)', 'エルロン（内側＋外側）'), -1),
    ('elevators', tr('升降舵', 'Elevators', 'エレベーター'), -1),
    ('rudder', tr('方向舵（上下兩段）', 'Rudder (upper + lower)', 'ラダー（上下2分割）'), -1),
    ('gear', tr('起落架收放（18 輪）', 'Landing gear (18 wheels)', '降着装置（18輪）'), 0),
    ('swingtail', tr('擺尾式貨艙門', 'Swing-tail cargo door', 'スイングテール貨物扉'), 0)]


def export_model(model_id, blend_name, source, control_specs, anchor_points):
    bpy.context.view_layer.update()
    world = c.world
    parts = {p: [] for p in ('cockpit', 'windshield', 'fuselage', 'engine', 'wingtip', 'wing', 'vstab', 'hstab', 'gear')}
    for ob in OBJECTS:
        if 'joint' not in ob:
            parts[ob['partId']].append(c.encode(ob))
    surfaces = []
    for name, r in RIG.items():
        entry = dict(id=name, part=r['part'], channel=r['channel'], pv=world(r['pivot']),
                     ax=world(Vector(r['axis'])/c.SCALE), angle=r['angle'], start=0,
                     e=[c.encode(ob) for ob in OBJECTS if ob.get('joint') == name])
        if r.get('parent'):
            entry['parent'] = r['parent']
        if 'motion' in r:
            entry['motion'] = r['motion']
        if 'rpm' in r:
            entry['rpm'] = r['rpm']
        surfaces.append(entry)
    assert all(s['e'] for s in surfaces), [s['id'] for s in surfaces if not s['e']]
    ids = [s['id'] for s in surfaces]
    assert all(ids.index(s['parent']) < i for i, s in enumerate(surfaces) if 'parent' in s)   # parents first
    # Children of the swing tail must hang from the swing joint of their own part.
    for s in surfaces:
        if s.get('parent', '').startswith('swing_'):
            assert s['parent'] == 'swing_'+s['part'], s['id']
    controls = [dict(id=i, label=label, min=lo, max=1, step=.01) for i, label, lo in control_specs]
    assert {s['channel'] for s in surfaces if 'rpm' not in s} == {x['id'] for x in controls}
    anchors = {p: world(v) for p, v in anchor_points.items()}
    out = dict(meta=dict(format=2, model=model_id,
                         source=source,
                         units='normalized: length 12; source metres', prototype=True),
               texture=None, parts=parts, anchors=anchors, surfaces=surfaces, controls=controls)
    (ROOT/f'models/{model_id}.json').write_text(json.dumps(out, separators=(',', ':')), encoding='utf-8')
    # Editable .blend uses the same piecewise linear travel as the viewer.
    bpy.context.preferences.edit.keyframe_new_interpolation_type = 'LINEAR'
    for r in RIG.values():
        c.keyframe_joint(r,r.get('motion', [(0,0),(1,1)]))
    for ob in OBJECTS:
        if 'slide' in ob:
            ob.keyframe_insert('location', frame=1)
            ob.location = Vector(ob.location)+Vector(ob['slide'])
            ob.keyframe_insert('location', frame=1+60*ob.get('slideEnd', 1))
    scene = bpy.context.scene
    scene.frame_end = 61; scene.frame_set(1)
    scene.unit_settings.system = 'METRIC'
    bpy.context.preferences.filepaths.save_version = 0
    bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/f'models/blender/{blend_name}.blend'))
    lo = [min(v.co[k] for ob in OBJECTS for v in ob.data.vertices) for k in range(3)]   # rest pose, world = local
    hi = [max(v.co[k] for ob in OBJECTS for v in ob.data.vertices) for k in range(3)]
    print(f'{model_id}: {len(OBJECTS)} meshes, {len(surfaces)} hinges; '
          f'length {hi[0]-lo[0]:.2f} m, span {hi[1]-lo[1]:.2f} m, height {hi[2]:.2f} m, ground {lo[2]:.3f} m')
    return lo, hi


def export():
    anchors = dict(cockpit=(X(4), 0, 8.6), windshield=(X(5), 1.3, 8.8), fuselage=(X(30), 0, 12.3),
                   engine=(X(27), 11.7, 2.6), wingtip=(X(47), 31.5, 7.2), wing=(X(36), 15, 5.2),
                   vstab=(X(66), 0, 18), hstab=(X(65), 7, 8.8), gear=(X(31.5), 5.5, 1))
    lo, hi = export_model('dreamlifter', 'dreamlifter',
                          'SKY ARCHIVE / Blender — Dreamlifter with opening fan cowls', CONTROLS, anchors)
    assert abs(hi[0]-lo[0]-LENGTH) < .05 and abs(hi[1]-lo[1]-64.4) < .1 and abs(hi[2]-21.54) < .1 and abs(lo[2]) < .02


if __name__ == '__main__':
    build()
    export()
