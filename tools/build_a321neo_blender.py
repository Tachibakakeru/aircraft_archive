"""Build A321neo Cabin Flex / LEAP-1A in Blender and export archive v2.

References: Airbus A321 airport planning, Lufthansa's A321neo side profile,
and the real A321neo frontal and side photographs listed in data/a321n.json.
Dimensions are published. Sections, joints and travel are educational approximations.
"""
import math
import sys
from functools import partial
from pathlib import Path

import bmesh
import bpy
from mathutils import Matrix, Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_dreamlifter_blender as d

c = d.c
LENGTH, HALF_SPAN, HEIGHT = 44.51, 17.90, 11.76
UP, DOWN = d.UP, d.DOWN
rad = math.radians


def station_x(station):
    return LENGTH / 2 - station


HULL = [(0,.018,2.92,.018), (.06,.31,2.94,.24), (.20,.57,2.99,.44),
        (.48,.82,3.02,.67), (.82,1.03,3.08,.87), (1.22,1.22,3.14,1.04),
        (1.54,1.35,3.26,1.20), (1.78,1.44,3.34,1.32), (2.22,1.57,3.47,1.47),
        (2.70,1.69,3.57,1.62), (3.25,1.80,3.64,1.75), (3.90,1.88,3.70,1.85),
        (4.60,1.94,3.75,1.93), (5.3,1.975,3.77,1.975),
        (33.6, 1.975, 3.77, 1.975), (36.4, 1.80, 3.82, 1.78), (38.6, 1.48, 3.99, 1.45),
        (40.6, 1.05, 4.18, 1.07), (42.6, .54, 4.47, .57), (43.8, .23, 4.56, .26),
        (44.51, .08, 4.63, .10)]
FAIRING = [(13.3, 1.72, 2.56, .10), (16.1, 2.00, 2.68, .53), (20.5, 2.22, 2.63, .89),
           (24.4, 2.20, 2.63, .88), (27.6, 2.00, 2.67, .44), (30.5, 1.65, 2.53, .10)]

NOSE_BAY = (1.88, 5.62, .59)
MAIN_BAY = (21.25, 22.69, 2.88)


def open_wheel_bay(ob, start, end, half_width, roof):
    # A closed cutter makes a recessed bay with walls and a roof in the exported mesh.
    bpy.ops.mesh.primitive_cube_add(size=1, location=(station_x((start+end)/2), 0, (roof-.4)/2))
    cutter = bpy.context.object
    cutter.dimensions = (end-start, 2*half_width, roof+.4)
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))
    bm.to_mesh(ob.data)
    bm.free()
    bpy.context.view_layer.objects.active = ob
    cut = ob.modifiers.new('Wheel bay', 'BOOLEAN')
    cut.object = cutter
    cut.operation = 'DIFFERENCE'
    bpy.ops.object.modifier_apply(modifier=cut.name)
    bpy.data.objects.remove(cutter, do_unlink=True)


def open_main_bay(ob):
    open_wheel_bay(ob, *MAIN_BAY, 3.02)
    start, end, _ = MAIN_BAY
    open_wheel_bay(ob, start, end, 1.95, 3.61)


def shell_point(s, angle, side, offset=.018):
    radius, centre, height = c.profile(HULL, s)
    return (station_x(s), side * (radius + offset) * math.cos(rad(angle)),
            centre + (height + offset) * math.sin(rad(angle)))


def glazing(name, start, end, low, high, side, part, mat='glass', offset=.02, rake=0):
    points = [shell_point(start + (end-start)*i/6 + rake*(1-j/4), low+(high-low)*j/4, side, offset)
              for i in range(7) for j in range(5)]
    d.mesh(name, points, d.grid_faces(7, 5, closed=False, caps=False), mat, part, smooth=False)


def outline(name, start, end, low, high, side):
    # Fine, conformal door margins and exit markings, kept as distinct strips.
    for s0, s1, a0, a1 in ((start, start+.026, low, high), (end-.026, end, low, high),
                           (start, end, low, low+.85), (start, end, high-.85, high)):
        glazing(name, s0, s1, a0, a1, side, 'fuselage', 'trim')


def cabin_window(s, side):
    perimeter = [shell_point(s+dx+.058*math.cos(rad(angle)),
                             7.5+dy+2.2*math.sin(rad(angle)),side,.024)
                 for dx,dy,start in ((.057,2.1,0),(-.057,2.1,90),(-.057,-2.1,180),(.057,-2.1,270))
                 for angle in range(start,start+91,15)]
    d.mesh('Cabin window',perimeter,[tuple(range(len(perimeter)))],'glass','fuselage',smooth=False)


# The forward glass is defined in front elevation (distance from centre, height).
# The two side panes are defined in side elevation (station from radome, height).
WINDSCREEN = ((.036,4.16),(1.13,4.18),(.96,4.72),(.036,4.73))
SIDE_PANES = (
    ('Sliding side window', ((1.99,4.13),(2.66,4.10),(2.63,4.71),(2.39,4.70))),
    ('Fixed rear window', ((2.76,4.10),(3.29,4.12),(3.31,4.48),(3.13,4.69),(2.73,4.71))),
)


def front_glass_point(y, z, side, lift):
    # Find where a front-view ray hits the upper nose skin without distorting the outline.
    fore, aft = 1.0, 3.2
    for _ in range(24):
        s = (fore+aft)/2
        radius, mid, height = c.profile(HULL,s)
        skin = mid+height*math.sqrt(max(0,1-(y/radius)**2))
        if skin < z:
            fore = s
        else:
            aft = s
    return (station_x((fore+aft)/2)+lift,side*y,z)


def side_glass_point(s, z, side, lift):
    _, mid, height = c.profile(HULL,s)
    return shell_point(s,math.degrees(math.asin((z-mid)/height)),side,lift)


def cockpit_pane(name, corners, side, project):
    corners = [Vector(point) for point in corners]
    centre = sum(corners, Vector((0, 0)))/len(corners)
    # Sample the straight edges and soften only the corners of the window frame.
    rim = []
    for i, corner in enumerate(corners):
        before = corner.lerp(corners[i-1], .12)
        after = corner.lerp(corners[(i+1) % len(corners)], .12)
        rim.extend(before.lerp(corner,t).lerp(corner.lerp(after,t),t) for t in (0,.5,1))
        next_corner = corners[(i+1) % len(corners)]
        next_start = next_corner.lerp(corner,.12)
        rim.extend(after.lerp(next_start,t/6) for t in range(1,6))

    frame = [project(*p,side,.017) for p in rim]
    frame += [project(*centre.lerp(p,.92),side,.021) for p in rim]
    d.mesh(name+' perimeter',frame,d.grid_faces(2,len(rim),caps=False),'seal','windshield')
    glass = [project(*centre.lerp(p,t),side,.022) for t in (.92,.69,.46,.23,.018) for p in rim]
    faces = d.grid_faces(5,len(rim),caps=False)
    faces.append(tuple(range(4*len(rim),5*len(rim))))
    d.mesh(name,glass,faces,'cockpit_glass','windshield')


def radome_seam():
    count = 72
    verts = [shell_point(.76+.22*math.sin(rad(angle))+delta,angle,1,.010)
             for delta in (-.009,.009) for angle in range(0,360,5)]
    d.mesh('Radome seal',verts,d.grid_faces(2,count,caps=False),'trim','cockpit')


def build_body():
    shell = c.loft('A321neo pressure shell', [(station_x(s), y, z, r) for s,y,z,r in c.sampled(HULL, .16)],
                   d.M['white'], 'fuselage', sides=72)
    fairing = c.loft('Wing-body and main gear fairing',
           [(station_x(s), y, z, r) for s,y,z,r in c.sampled(FAIRING, .28)],
           d.M['white'], 'fuselage')
    start, end, width = NOSE_BAY
    open_wheel_bay(shell, start, 4.78, width, 3.72)
    open_wheel_bay(shell, 4.77, end, .275, 3.51)
    for ob in (shell, fairing):
        open_main_bay(ob)
    radome_seam()
    for side in (-1, 1):
        cockpit_pane('Front windscreen',WINDSCREEN,side,front_glass_point)
        for name, corners in SIDE_PANES:
            cockpit_pane(name,corners,side,side_glass_point)
        arm = front_glass_point(.68,4.19,side,.043)
        blade = front_glass_point(.44,4.26,side,.040)
        c.rod('Windscreen wiper arm',arm,blade,.010,d.M['seal'],'windshield',sides=8)
        c.rod('Windscreen wiper blade',front_glass_point(.22,4.25,side,.052),
              front_glass_point(.64,4.27,side,.052),.009,d.M['seal'],'windshield',sides=8)
        exits = [(4.64,5.63,-28,29), (19.52,20.15,-5,19), (20.72,21.35,-5,19),
                 (27.95,28.8,-26,26), (37.35,38.29,-30,29)]
        for i in range(54):
            s = 6.78 + i * .56
            if any(lo-.16 < s < hi+.16 for lo,hi,_,_ in exits):
                continue
            cabin_window(s,side)
        for s0,s1,a0,a1 in exits:
            outline('Cabin Flex door / exit',s0,s1,a0,a1,side)
        if side < 0:
            for s0,s1 in ((9.25,10.98),(31.0,32.72),(34.85,35.70)):
                outline('Starboard cargo hatch',s0,s1,-49,-10,side)


def wing_le(y):
    return 16.28 + .52*y


def wing_te(y):
    return 23.24 + .030*y if y < 6.45 else 23.4335 + .304*(y-6.45)


def hinge_for(panel, name, u0, u1, chord, angle, channel, want):
    a, b = panel.point(u0, chord), panel.point(u1, chord)
    d.joint(name, a, b-a, rad(angle), channel, 'wing', probe=panel.point((u0+u1)/2, .96),
            want=want)


def move_panel(ob, joint_id, offset):
    rig = d.RIG[joint_id]
    rotation = Matrix.Rotation(rig['angle'], 3, Vector(rig['axis']))
    ob['slide'] = tuple(rotation.inverted() @ Vector(offset))


def flaps(wing, tag, u0, u1):
    first = f'flap_{tag}_main'
    hinge_for(wing, first, u0, u1, .69, 33, 'flaps', DOWN)
    main = wing.solid('Flap main element', [u0,u1], .69, .895, 'control', 'wing', first)
    move_panel(main, first, (-.72,0,-.10))
    second = f'flap_{tag}_aft'
    hinge_for(wing, second, u0, u1, .903, 52, 'flaps', DOWN)
    ob = wing.solid('Flap aft element', [u0,u1], .903, 1, 'control', 'wing', second)
    um = (u0+u1)/2
    first_chord = wing.point(um,.895) - wing.point(um,.69)
    rotate = Matrix.Rotation(d.RIG[first]['angle'], 3, Vector(d.RIG[first]['axis']))
    move_panel(ob, second, Vector((-.79,0,-.15)) + rotate @ first_chord - first_chord)
    return main


def build_sharklet(wing, tag):
    root = 16.88
    chord = wing.te(root)-wing.le(root)
    # The nearly horizontal root blends into a curved, swept and tapered blade.
    sections = [(0,0,0,1), (.23,.025,.050,.94), (.54,.15,.13,.84),
                (.78,.41,.24,.71), (.91,.77,.38,.59), (.97,1.23,.54,.46),
                (.970,1.68,.72,.35), (1.00,2.13,.98,.25), (1.02,2.40,1.16,.15)]
    fractions = [(.5-.5*math.cos(math.pi*i/14)) for i in range(15)]
    verts = []
    for i, (span, rise, sweep, scale) in enumerate(sections):
        prev, nxt = sections[max(0,i-1)], sections[min(i+1,len(sections)-1)]
        tangent = Vector((0, wing.side*(nxt[0]-prev[0]), nxt[1]-prev[1])).normalized()
        normal = Vector((0, -wing.side*tangent.z, wing.side*tangent.y))
        for sign, fr in ((1,fractions),(-1,reversed(fractions))):
            for f in fr:
                thick = max(.004, d.naca(f, wing.tc(root))*chord*scale)
                vertex = Vector((station_x(wing.le(root)+sweep+chord*f*scale),
                                 wing.side*(root+span), wing.height(root)+rise)) + normal*thick*sign
                vertex.y = wing.side*min(HALF_SPAN, abs(vertex.y))
                verts.append(vertex)
    d.mesh('Blended Sharklet '+tag, verts, d.grid_faces(len(sections),30), 'white', 'wingtip')


def flap_fairing(wing, y, flap):
    s = wing.le(y)+(wing.te(y)-wing.le(y))*.69
    z = wing.point(y,.69,-1).z
    centre = (station_x(s),wing.side*y,z-.24)
    d.revolve('Fixed flap track fairing',centre,
              [(-1.33,.025),(-.96,.16),(-.48,.205),(-.23,.175)],'white','wing',sides=20,caps=True)
    cover = d.revolve('Moving flap track fairing tail',centre,
                      [(-.17,.17),(.20,.18),(.63,.128),(1.04,.018)],'white','wing',
                      flap['joint'],sides=20,caps=True)
    cover['slide'] = tuple(flap['slide'])


def wing_surface(side):
    return d.Surface(wing_le, wing_te, lambda y: 2.91 + max(0,y-2)*.124,
                     lambda y: .123-.038*y/HALF_SPAN, (0,1,0), UP, side)


def main_bay_shoulders(wing):
    start, end, outer = MAIN_BAY
    fore, aft = 19.1, 23.22
    stations = [fore+(aft-fore)*i/42 for i in range(43)]
    section = c.sampled([(1.90,3.91),(2.00,3.75),(2.13,3.54),(2.36,3.34),
                         (2.61,3.23),(outer+.02,3.16),(outer+.24,3.13)],.05)

    def ease(value):
        value = max(0,min(1,value))
        return value*value*(3-2*value)

    verts = []
    for s in stations:
        blend = ease((s-fore)/(start-.08-fore))*ease((aft-s)/(aft-end-.06))
        for y,z in section:
            fraction = (s-wing_le(y))/(wing_te(y)-wing_le(y))
            upper = wing.point(y,fraction,1).z
            height = upper+.008+blend*max(0,z-upper-.008)*ease((outer+.24-y)/.18)
            verts.append((station_x(s),wing.side*y,height))
    d.mesh('Fixed main wheel bay shoulder',verts,
           d.grid_faces(len(stations),len(section),closed=False,caps=False),'white','wing')


def build_wing(side):
    tag = 'L' if side > 0 else 'R'
    wing = wing_surface(side)
    stations = [0, 1.96, 3.1, 6.45, 9.1, 12.5, 15.1, 16.9]
    box = wing.solid('Wing box '+tag, stations, .165, .685, 'white', 'wing')
    open_main_bay(box)
    wing.solid('Wing root leading edge '+tag, [0,2.12], 0, .165, 'white', 'wing')
    for i, (u0,u1) in enumerate(zip((2.12,4.9,7.52,10.4,13.45),(4.84,7.45,10.33,13.38,16.9)),1):
        joint = f'slat_{tag}_{i}'
        a,b = wing.point(u0,.12), wing.point(u1,.12)
        d.joint(joint,a,b-a,rad(22),'slats','wing',probe=wing.point((u0+u1)/2,0),want=DOWN)
        ob = wing.solid('Leading-edge slat', [u0,u1], 0,.165,'control','wing',joint,nf=7)
        move_panel(ob,joint,(.40,0,-.08))
    root = wing.solid('Fixed inboard trailing edge', [0,2.12], .685,1,'white','wing')
    open_main_bay(root)
    main_bay_shoulders(wing)
    inboard = flaps(wing,tag+'_inboard',2.14,6.37)
    outboard = flaps(wing,tag+'_outboard',6.49,12.27)
    wing.hinged(f'aileron_{tag}',12.40,16.58,.68,rad(23),'ailerons','wing','control',
                DOWN if side>0 else UP)
    wing.solid('Fixed tip trailing edge',[16.61,16.9],.68,1,'white','wing')
    for i, (u0,u1) in enumerate(zip((2.88,4.65,6.51,8.16,9.89),(4.59,6.45,8.10,9.83,11.43)),1):
        joint = f'spoiler_{tag}_{i}'
        a,b = wing.point(u0,.54,1), wing.point(u1,.54,1)
        d.joint(joint,a,b-a,rad(48),'spoilers','wing',probe=wing.point((u0+u1)/2,.68,1),want=UP)
        wing.skin_panel('Upper wing spoiler',u0,u1,.54,.675,1,'control','wing',joint,.025)
    for y, flap in ((4.1,inboard),(7.7,outboard),(10.9,outboard)):
        flap_fairing(wing,y,flap)
    build_sharklet(wing,tag)


def build_tail():
    base, tip, hinge = 4.98, 11.58, .755
    fin = d.Surface(lambda z: 37.03+.785*(z-5.64),lambda z: 42.24+.241*(z-5.64),
                    lambda _:0,lambda z:.092-.028*(z-base)/(HEIGHT-base),UP,(0,1,0))
    fin.solid('Swept vertical stabilizer',[base,5.50,6.20,8.70,10.40,tip],
              0,hinge,'blue','vstab')
    fin.hinged('rudder',5.50,tip,hinge,rad(27),'rudder','vstab','control',(0,1,0))
    fin.solid('Fin root trailing edge',[base,5.49],hinge,1,'blue','vstab')
    cap = d.Surface(lambda z:fin.le(z)+.16*((z-tip)/(HEIGHT-tip))**2,
                    lambda z:fin.te(z)-.035*((z-tip)/(HEIGHT-tip))**2,
                    lambda _:0,lambda z:fin.tc(z)*(1-.50*(z-tip)/(HEIGHT-tip)),UP,(0,1,0))
    cap.solid('Rounded fin cap',[tip,11.69,HEIGHT],0,1,'blue','vstab')
    fillet = d.Surface(lambda z: 35.58+.20*(z-5.40)+1.78*((z-5.40)/.75)**.55,
                       lambda z: fin.le(z)+.52,lambda _:0,lambda _:.16,UP,(0,1,0))
    fillet.solid('Dorsal fin root fillet',[5.40,5.45,5.56,5.74,5.94,6.15],0,1,'blue','vstab')
    for side in (-1,1):
        tag = 'L' if side>0 else 'R'
        h = d.Surface(lambda y: 36.3+.65*y,lambda y: 43.85+.054*y,
                      lambda y: 4.35+.10*y,lambda _:.096,(0,1,0),UP,side)
        parent = f'trim_{tag}'
        d.joint(parent,h.point(1.3,.29),(0,1,0),rad(8),'trim','hstab')
        h.solid('Trimmable horizontal stabilizer '+tag,[.45,1.4,3.6,6.22],0,.73,'white','hstab',parent)
        h.hinged(f'elevator_{tag}',1.04,6.10,.73,rad(27),'elevators','hstab','control',DOWN,parent=parent)
        h.solid('Tailplane tip',[6.11,6.22],.73,1,'white','hstab',parent)


def build_engine(side):
    tag = 'L' if side>0 else 'R'
    x,y,z = station_x(13.3), side*5.23, 1.87
    centre = (x,y,z)
    d.revolve('LEAP-1A nacelle intake',centre,[(0,1.03),(0,1.16),(.13,1.27),(.41,1.32),
                (1.28,1.33),(2.06,1.27),(2.06,1.13),(.50,1.03),(0,1.03)],'white','engine')
    d.revolve('Inlet lip',centre,[(.002,1.04),(.001,1.15),(.08,1.24),(.14,1.25)],'steel','engine')
    d.revolve('Fan duct',centre,[(.08,1.035),(.56,1.00),(.72,.98)],'dark','engine')
    c.rod('Fan disk',(x-.72,y,z),(x-.78,y,z),.984,d.M['dark'],'engine',sides=40)
    fan = c.rotor(f'leap_1a_rotor_{tag}',centre,37)
    c.rotor_blades('LEAP-1A swept fan blade row',centre,
                   [(.68,.22,-.10),(.65,.93,.025),(.68,.97,.11),(.70,.35,.17)],
                   18,.028,d.M['steel'],fan)
    d.revolve('Fan spinner',centre,[(.45,.025),(.61,.15),(.76,.25),(.84,.25)],'steel','engine',fan,caps=True)
    d.revolve('Cascade and tailpipe',centre,[(2.02,1.08),(2.46,1.07),(2.99,.83),
                (3.54,.73),(3.73,.55),(3.9,.30)],'dark','engine',caps=True)
    for k in range(18):
        theta = math.tau*k/18
        yy,zz = y+1.087*math.cos(theta),z+1.087*math.sin(theta)
        c.rod('Reverser cascade rail',(x-2.02,yy,zz),(x-2.51,yy,zz),.014,d.M['steel'],'engine',sides=8)
    joint = f'reverser_{tag}'
    d.joint(joint,centre,(1,0,0),0,'reverse','engine')
    sleeve = d.revolve('Translating reverser sleeve',centre,
                       [(2.05,1.14),(2.05,1.27),(2.42,1.24),(2.97,1.12),(3.13,.99),(3.13,.91)],
                       'white','engine',joint)
    sleeve['slide'] = (-.48,0,0)
    d.extrude('Engine pylon',[(x-.48,y,z+1.16),(x-4.90,y,3.40),(x-6.50,y,3.39),(x-3.32,y,z+.69)],
              (0,.47,0),'white','engine')


def lower_shell(profile, s, y):
    width, center, radius = c.profile(profile, s)
    return center - radius * math.sqrt(1 - (y/width)**2)


def outer_main_door(wing, s, y):
    outer = MAIN_BAY[2]
    fraction = (s-wing_le(outer))/(wing_te(outer)-wing_le(outer))
    root = lower_shell(FAIRING,s,2.04)
    tip = wing.point(outer,fraction,-1).z
    return root+(tip-root)*(y-2.04)/(outer-2.04)


def bay_panel(name, start, end, inner, outer, side, underside, angle=0,
              hinge_outside=False, hinge_aft=False, joint=None):
    """A curved closed door follows the lower skin and opens on a straight hinge."""
    if joint is None:
        joint = name
        if hinge_aft:
            a = Vector((station_x(end),side*inner,underside(end,inner)))
            b = Vector((station_x(end),side*outer,underside(end,outer)))
            probe = Vector((station_x(start),side*inner,underside(start,inner)))
            d.joint(name,a,b-a,rad(angle),'gear','gear',probe=probe,want=DOWN,motion=d.FOLDING_DOOR_TRAVEL)
        else:
            hinge = outer if hinge_outside else inner
            # Put the belly hinge on the outer face so the two door lips clear each other.
            lip = 0 if hinge_outside else -.030
            a = Vector((station_x(start),side*hinge,underside(start,hinge)+lip))
            b = Vector((station_x(end),side*hinge,underside(end,hinge)+lip))
            d.joint(name,a,b-a,rad(angle),'gear','gear',motion=d.FOLDING_DOOR_TRAVEL)
    rows, cols = 13, 7
    verts = []
    for offset in (-.024,.004):
        for i in range(rows):
            s = start+(end-start)*i/(rows-1)
            for j in range(cols):
                y = inner+(outer-inner)*j/(cols-1)
                verts.append((station_x(s),side*y,underside(s,y)+offset))
    size = rows*cols
    faces = d.grid_faces(rows,cols,closed=False,caps=False)
    faces += [tuple(size+index for index in reversed(face)) for face in faces]
    outline = list(range(cols)) + [i*cols+cols-1 for i in range(1,rows)]
    outline += list(range(size-2,size-cols-1,-1)) + [i*cols for i in reversed(range(1,rows-1))]
    for i,j in zip(outline,outline[1:]+outline[:1]):
        faces.append((i,j,j+size,i+size))
    d.mesh(name,verts,faces,'control','gear',joint,smooth=True)


def build_gear():
    # Keep the open bay panels outside the wheel sweep, then shut them after the wheels stow.
    nose_pivot = Vector((station_x(5.07),0,2.70))
    for tag, pivot, wheel, axis, angle, radius, width, track, want in [
            ('nose',nose_pivot,Vector((station_x(5.07),0,.315)),(0,1,0),92,.315,.185,.25,d.FWD),
            *[(tag,Vector((station_x(21.54),side*3.76,3.24)),
               Vector((station_x(21.97),side*3.795,.5842)),(1,0,0),80.5,.5842,.4318,.46355,(0,-side,0))
              for side,tag in ((1,'L'),(-1,'R'))]]:
        joint = f'gear_{tag}'
        d.joint(joint,pivot,axis,rad(angle),'gear','gear',probe=wheel,want=want,motion=d.GEAR_TRAVEL)
        c.rod('Gear outer oleo',pivot,pivot.lerp(wheel,.61),.10 if tag=='nose' else .154,d.M['steel'],'gear',joint)
        c.rod('Gear inner oleo',pivot.lerp(wheel,.52),wheel,.075 if tag=='nose' else .105,d.M['steel'],'gear',joint)
        brace = pivot+Vector((.65 if tag=='nose' else .33,0,.02))
        c.rod('Gear drag brace',brace,pivot.lerp(wheel,.52),.058,d.M['steel'],'gear',joint)
        c.rod('Gear axle',wheel-Vector((0,track,0)),wheel+Vector((0,track,0)),.062,d.M['steel'],'gear',joint)
        for side in (-1,1):
            d.wheel(tag,wheel+Vector((0,side*track,0)),joint,radius,width)
    for side,tag in ((1,'L'),(-1,'R')):
        nose_skin = partial(lower_shell,HULL)
        belly_skin = partial(lower_shell,FAIRING)
        start, end, width = NOSE_BAY
        bay_panel(f'nose_door_{tag}',start+.012,4.77,.012,width-.012,side,nose_skin,-side*86,hinge_outside=True)
        bay_panel(f'Nose leg panel {tag}',4.79,end-.012,.007,.259,side,nose_skin,joint='gear_nose')
        start, end, outer = MAIN_BAY
        bay_panel(f'main_door_{tag}',start+.012,end-.012,.012,2.04,side,belly_skin,side*86)
        bay_panel(f'outer_main_door_{tag}',start+.012,end-.012,2.05,outer-.009,side,
                  partial(outer_main_door,wing_surface(side)),105,hinge_aft=True)


CONTROLS = [
    ('flaps',c.tr('襟翼','Double-slotted flaps','二重隙間フラップ'),0),
    ('slats',c.tr('前緣縫翼','Leading-edge slats','前縁スラット'),0),
    ('spoilers',c.tr('擾流板','Spoilers','スポイラー'),0),
    ('ailerons',c.tr('副翼','Ailerons','エルロン'),-1),
    ('elevators',c.tr('升降舵','Elevators','エレベーター'),-1),
    ('rudder',c.tr('方向舵','Rudder','ラダー'),-1),
    ('trim',c.tr('水平安定面配平','Horizontal stabilizer trim','水平安定板トリム'),-1),
    ('gear',c.tr('起落架與輪艙門','Landing gear and doors','降着装置と扉'),0),
    ('reverse',c.tr('反推套筒','Thrust reverser sleeves','逆推力装置スリーブ'),0),
]


def build():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    c.SCALE = 12 / LENGTH
    d.X = station_x
    for key, rgb in dict(white=(.91,.94,.97),control=(.73,.80,.85),glass=(.022,.053,.079),
                         seal=(.043,.054,.066),cockpit_glass=(.061,.107,.146),
                         dark=(.032,.045,.06),steel=(.36,.44,.52),blue=(.055,.27,.58),
                         trim=(.30,.41,.52),rubber=(.020,.025,.031)).items():
        d.M[key] = c.material(key,rgb,.45 if key=='steel' else 0)
    build_body()
    for side in (-1,1):
        build_wing(side)
        build_engine(side)
    build_tail()
    build_gear()
    assert all(abs(rig['angle']) <= math.pi for rig in d.RIG.values()), 'Hinge angles must be in radians'
    d.recalc_normals()
    anchors = {part:(station_x(s),y,z) for part,(s,y,z) in dict(
        cockpit=(3.7,0,5.51),windshield=(2.2,.84,4.62),fuselage=(12,0,5.8),
        engine=(14.6,5.23,1.87),wingtip=(26.0,17.7,5.4),wing=(23,9,3.6),
        vstab=(39,0,10.4),hstab=(41.3,4.9,4.8),gear=(22.09,3.8,1)).items()}
    lo, hi = d.export_model('a321n','a321neo','SKY ARCHIVE / Blender — A321neo ACF LEAP-1A v5',CONTROLS,anchors)
    assert abs(hi[0]-lo[0]-LENGTH)<.03 and abs(hi[1]-lo[1]-2*HALF_SPAN)<.025
    assert abs(hi[2]-HEIGHT)<.03 and abs(lo[2])<.02


if __name__ == '__main__':
    build()
