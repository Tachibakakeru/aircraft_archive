"""Blender --background --python tools/build_concorde_blender.py

Original educational Concorde model, metres in Blender, nose +X, Z up.
Exports editable rigged .blend and the archive's quantized v2 JSON.
Geometry is an interpretation of published dimensions, not CAD or flight simulation.
"""
import bpy
import json
import math
from array import array
from base64 import b64encode
from pathlib import Path
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
SCALE = 12 / 61.66
RIG = {}
OBJECTS = []


def profile(rows, x):
    """Shape-preserving cubic sections; no overshoot at the cylindrical cabin."""
    i = next((i for i in range(len(rows)-1) if x <= rows[i+1][0]), len(rows)-2)
    a,b = rows[i:i+2]
    h=b[0]-a[0]; t=max(0,min(1,(x-a[0])/h))
    result=[]
    for k in range(1,len(a)):
        d=(b[k]-a[k])/h
        prev=(a[k]-rows[i-1][k])/(a[0]-rows[i-1][0]) if i else d
        nxt=(rows[i+2][k]-b[k])/(rows[i+2][0]-b[0]) if i+2<len(rows) else d
        m0=2*prev*d/(prev+d) if prev*d>0 else 0
        m1=2*nxt*d/(nxt+d) if nxt*d>0 else 0
        result.append((2*t**3-3*t*t+1)*a[k]+(t**3-2*t*t+t)*h*m0
                      +(-2*t**3+3*t*t)*b[k]+(t**3-t*t)*h*m1)
    return result


def sampled(rows, step=.25):
    xs=[a[0]+(b[0]-a[0])*j/max(1,math.ceil((b[0]-a[0])/step))
        for a,b in zip(rows,rows[1:]) for j in range(max(1,math.ceil((b[0]-a[0])/step)))]
    return [(x,*profile(rows,x)) for x in xs]+[rows[-1]]


def tr(zh, en, ja):
    return dict(zh=zh, en=en, ja=ja)


def material(name, color, metal=0.0):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1)
    m.use_nodes = True
    p = m.node_tree.nodes.get('Principled BSDF')
    p.inputs['Base Color'].default_value = (*color, 1)
    p.inputs['Metallic'].default_value = metal
    p.inputs['Roughness'].default_value = .34
    return m


def mesh(name, verts, faces, mat, part, joint=None, smooth=False):
    data = bpy.data.meshes.new(name)
    data.from_pydata(verts, [], faces)
    data.update()
    ob = bpy.data.objects.new(name, data)
    bpy.context.collection.objects.link(ob)
    data.materials.append(mat)
    ob['partId'] = part
    if joint:
        ob.parent = RIG[joint]['object']
        ob.matrix_parent_inverse = ob.parent.matrix_world.inverted()
        ob['joint'] = joint
    for p in data.polygons:
        p.use_smooth = smooth
    OBJECTS.append(ob)
    return ob


def joint(name, pivot, axis, angle, channel, part):
    ob = bpy.data.objects.new(name, None)
    bpy.context.collection.objects.link(ob)
    ob.location = pivot
    ob.empty_display_type = 'ARROWS'
    ob.empty_display_size = .8
    bpy.context.view_layer.update()
    RIG[name] = dict(object=ob, pivot=pivot, axis=axis, angle=angle, channel=channel, part=part)


def loft(name, stations, mat, part, joint_name=None, sides=48):
    # x, lateral radius, vertical centre, vertical radius
    verts = [(x, ry*math.cos(a*2*math.pi/sides), z+rz*math.sin(a*2*math.pi/sides))
             for x, ry, z, rz in stations for a in range(sides)]
    faces = [(j*sides+k, j*sides+(k+1)%sides, (j+1)*sides+(k+1)%sides, (j+1)*sides+k)
             for j in range(len(stations)-1) for k in range(sides)]
    faces += [tuple(reversed(range(sides))), tuple(range((len(stations)-1)*sides, len(stations)*sides))]
    return mesh(name, verts, faces, mat, part, joint_name, True)


def prism(name, outline, thick, mat, part, joint_name=None):
    verts = [(x,y,z+dz) for dz in (-thick/2, thick/2) for x,y,z in outline]
    n = len(outline)
    faces = [tuple(reversed(range(n))), tuple(range(n,n*2))]
    faces += [(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
    return mesh(name, verts, faces, mat, part, joint_name)


def rod(name, a, b, radius, mat, part, joint_name=None, sides=16):
    axis = (Vector(b)-Vector(a)).normalized()
    u = axis.cross(Vector((0,0,1)))
    if u.length < .1:
        u = axis.cross(Vector((0,1,0)))
    u.normalize()
    v = axis.cross(u)
    verts = [tuple(Vector(c)+radius*(math.cos(i*math.tau/sides)*u+math.sin(i*math.tau/sides)*v))
             for c in (a,b) for i in range(sides)]
    faces = [(i,(i+1)%sides,(i+1)%sides+sides,i+sides) for i in range(sides)]
    faces += [tuple(reversed(range(sides))),tuple(range(sides,sides*2))]
    return mesh(name, verts, faces, mat, part, joint_name, True)


def build():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    white = material('Ivory heat-reflecting airframe',(.86,.89,.92))
    gray = material('Flight controls',(.66,.71,.77))
    glass = material('Blue-black glazing',(.025,.07,.11),.3)
    dark = material('Intake and exhaust',(.025,.029,.033))
    rubber = material('Tyres',(.018,.02,.023))
    steel = material('Gear steel',(.42,.48,.54),.75)
    stripe = material('Archive navy trim',(.025,.08,.16))
    # Production silhouette checked against G-BOAC photos and orthographic views.
    shell=[(-30.83,.015,6.4,.02),(-28,.32,6.03,.37),(-24,.76,5.63,.88),
           (-19,1.19,5.4,1.36),(-13,1.435,5.4,1.66),(12,1.435,5.4,1.66),
           (18,1.38,5.4,1.64),(21,1.26,5.4,1.56),(23,1.1,5.36,1.4),(24,.98,5.32,1.21)]
    nose=[(24,.98,5.32,1.21),(25,.81,5.23,.97),(26.5,.57,5.11,.65),
          (28,.34,4.99,.36),(29.5,.15,4.86,.14),(30.83,.008,4.76,.008)]
    joint('nose', (24,0,5.32), (0,1,0), math.radians(12.5), 'nose', 'nose')
    loft('Fuselage pressure shell',sampled(shell),white,'fuselage',sides=64)
    loft('Droop nose fairing',sampled(nose,.12),white,'nose','nose',sides=64)
    def skin(x,z,side):
        ry,zc,rz=profile(shell,x)
        return (x,side*(ry*math.sqrt(max(0,1-((z-zc)/rz)**2))+.012),z)
    # Cockpit panes and visor are separate selectable mesh objects, not a texture.
    for side in (-1,1):
        for name,xa,xb,aa,ab in [('Windscreen',23.12,23.94,40,83),
                                ('Pilot side window',22.15,22.99,27,51),
                                ('Rear side window',21.35,22.02,25,47)]:
            verts=[]
            for j in range(5):
                x=xa+(xb-xa)*j/4
                ry,z,rz=profile(shell,x)
                for k in range(5):
                    angle=math.radians(aa+(ab-aa)*k/4)
                    verts.append((x,side*(ry+.018)*math.cos(angle),z+(rz+.018)*math.sin(angle)))
            mesh(name+str(side),verts,[(j*5+k,j*5+k+1,(j+1)*5+k+1,(j+1)*5+k) for j in range(4) for k in range(4)],glass,'cockpit')
        visor=[]
        for j in range(13):
            x=24.04+j*.19
            ry,z,rz=profile(nose,x)
            for k in range(7):
                angle=math.radians(38+48*k/6)
                visor.append((x,side*(ry+.014)*math.cos(angle),z+(rz+.014)*math.sin(angle)))
        mesh('Nose visor '+str(side),visor,
             [(j*7+k,j*7+k+1,(j+1)*7+k+1,(j+1)*7+k) for j in range(12) for k in range(6)],glass,'nose','nose')
        for i in range(40):
            x = 16.6-i*.79
            verts=[skin(x+.095*math.cos(t*math.tau/16),5.98+.135*math.sin(t*math.tau/16),side) for t in range(16)]
            mesh(f'Cabin window {side} {i:02}',verts,[tuple(range(16))],glass,'fuselage')
        # Subtle trim and door outlines: original neutral scheme, no airline logos.
        mesh('Cabin stripe '+str(side),[skin(18-j*.4,z,side) for j in range(91) for z in (5.5,5.54)],
             [(j*2,j*2+1,j*2+3,j*2+2) for j in range(90)],stripe,'fuselage')
        for x in (18,-14.8):
            outline=[(x,4.8),(x,6.25),(x+.10,6.35),(x+.63,6.35),(x+.73,6.25),
                     (x+.73,4.8),(x+.63,4.7),(x+.1,4.7)]
            for a,b in zip(outline,outline[1:]+outline[:1]):
                for j in range(5):
                    pts=[skin(a[0]+(b[0]-a[0])*t,a[1]+(b[1]-a[1])*t,side) for t in (j/5,(j+1)/5)]
                    rod('Door outline',*pts,.011,gray,'fuselage',sides=6)
    # Ogival leading edge, thin cambered delta. Each side has three separate elevons.
    leading=[(1,13.3),(2,9.9),(4,3.2),(6,-2.2),(8,-6.3),(10,-10.0),
             (11.6,-12.9),(12.4,-14.2),(12.8,-15.0)]
    # Hinge lies ahead of the trailing edge, never ahead of the leading edge.
    # Outer tip is fixed; elevons stop short of the rounded tip closure.
    stations=sampled(leading,.12)
    fractions=(0,.04,.12,.28,.5,.72,.9,1)
    for side in (-1,1):
        verts=[]
        for y,lead in stations:
            end=-14.4 if y<=11.65 else -14.4-(y-11.65)/1.15*1.25
            assert lead>end, (y,lead,end)
            half=max(.018,(lead-end)*.014)
            for f,sign in [(f,1) for f in fractions]+[(f,-1) for f in reversed(fractions)]:
                x=lead+(end-lead)*f
                z=4.4-.10*(y/12.8)**2+sign*(.009+half*math.sin(math.pi*f)**.75)
                verts.append((x,side*y,z))
        ring=len(fractions)*2
        faces=[(j*ring+k,j*ring+(k+1)%ring,(j+1)*ring+(k+1)%ring,(j+1)*ring+k) for j in range(len(stations)-1) for k in range(ring)]
        faces += [tuple(reversed(range(ring))),tuple(range((len(stations)-1)*ring,len(stations)*ring))]
        mesh('Ogival delta '+str(side),verts,faces,white,'wing',smooth=True)
        # One inboard group and two outboard groups; the nacelle roof is fixed.
        for n,(ya,yb) in enumerate(((1.46,4.02),(7.78,9.65),(9.69,11.65))):
            name=f'elevon_{side}_{n}'
            za=4.4-.10*(ya/12.8)**2; zb=4.4-.10*(yb/12.8)**2
            joint(name,(-14.43,side*ya,za),(0,1,0),math.radians(15),'elevons','wing')
            prism(name,[(-14.43,side*ya,za),(-14.43,side*yb,zb),
                       (-16.65+.025*yb,side*yb,zb),(-16.65+.025*ya,side*ya,za)],.055,white,'wing',name)
        for ya,yb in ((1.0,1.43),(4.05,7.75)):
            za=4.4-.10*(ya/12.8)**2; zb=4.4-.10*(yb/12.8)**2
            prism('Fixed trailing nacelle bridge', [(-14.4,side*ya,za),(-14.4,side*yb,zb),
                  (-16.65+.025*yb,side*yb,zb),(-16.65+.025*ya,side*ya,za)],.055,white,'wing')
        prism('Rounded fixed wingtip '+str(side),[(-14.4,side*11.67,4.317),
              (-15.65,side*12.8,4.30),(-16.05,side*12.55,4.304),
              (-16.28,side*12.1,4.31),(-16.35,side*11.67,4.317)],.035,white,'wing')
    # Four Olympus jets housed in two paired rectangular intake/nacelle groups.
    for side in (-1,1):
        for n,y in enumerate((5.0,6.75)):
            y*=side
            # Open octagonal shell, narrowing from intake to exhaust; no solid front cap.
            rings=[(-4.8,.86,3.12,4.34),(-7,.89,2.91,4.34),
                   (-12,.88,2.91,4.27),(-15.4,.77,3.03,4.21)]
            verts=[]
            for x,r,bot,top in rings:
                verts.extend((x,y+dy,z) for dy,z in [(-r+.09,bot),(r-.09,bot),(r,bot+.09),
                    (r,top-.09),(r-.09,top),(-r+.09,top),(-r,top-.09),(-r,bot+.09)])
            mesh('Tapered Olympus nacelle',verts,
                 [(j*8+k,j*8+(k+1)%8,(j+1)*8+(k+1)%8,(j+1)*8+k) for j in range(3) for k in range(8)],white,'engine')
            mesh('Recessed intake throat',[(-5.3,y-.77,3.19),(-5.3,y+.77,3.19),
                 (-5.3,y+.77,4.26),(-5.3,y-.77,4.26)],[(0,1,2,3)],dark,'engine')
            mesh('Intake compression ramp',[(-4.81,y-.76,4.24),(-4.81,y+.76,4.24),
                 (-5.25,y+.76,3.92),(-5.25,y-.76,3.92)],[(0,1,2,3)],gray,'engine')
            # Hollow nozzle: outer lip -> inner throat -> recessed dark interior.
            verts=[]
            for x,r in [(-15.3,.71),(-16.65,.69),(-16.65,.59),(-15.55,.51)]:
                verts.extend((x,y+r*math.cos(k*math.tau/48),3.60+r*.88*math.sin(k*math.tau/48)) for k in range(48))
            mesh('Hollow Olympus nozzle',verts,
                 [(j*48+k,j*48+(k+1)%48,(j+1)*48+(k+1)%48,(j+1)*48+k) for j in range(3) for k in range(48)],steel,'engine',smooth=True)
            rod('Recessed nozzle interior',(-15.54,y,3.60),(-15.56,y,3.60),.50,dark,'engine',sides=48)
    # Vertical stabilizer, two independently rigged rudder sections. No horizontal tail.
    # Curved dorsal root and swept two-piece rudder, not a rectangular slab.
    fin_outline=[(-12.4,0,6.8),(-16.0,0,7.95),(-18.5,0,9.18),
                 (-20.15,0,10.76),(-21.95,0,12.0),(-23.65,0,12.0),(-23.65,0,6.7)]
    def fin_plate(name,outline,thick,mat,joint_name=None):
        n=len(outline)
        verts=[(x,sign*thick*(.5 if z>11.8 else 1),z) for sign in (-1,1) for x,y,z in outline]
        return mesh(name,verts,[tuple(reversed(range(n))),tuple(range(n,n*2))]+
                    [(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],mat,'vstab',joint_name)
    fin_plate('Swept fin and dorsal fillet',fin_outline,.13,white)
    for n,(za,zb) in enumerate(((6.72,9.68),(9.72,11.98))):
        name='rudder_'+str(n)
        joint(name,(-23.68,0,za),(0,0,1),math.radians(20),'rudder','vstab')
        rear=lambda z: -26.15+(z-6.7)*.23
        fin_plate(name,[(-23.69,0,za),(-23.69,0,zb),(rear(zb),0,zb),(rear(za),0,za)],.10,white,name)
    # Gear deployed at rest. Four wheels on each main bogie, two nose wheels.
    # ponytail: approximate bay fairing and telescoping oleo, not hydraulic linkage CAD.
    bay=loft('Main gear belly fairing',sampled([(-8.7,.9,4.25,.15),(-8.1,2.1,4.1,1.2),
         (-4.9,2.1,4.1,1.2),(-4.2,.9,4.25,.15)],.15),white,'fuselage')
    for vertex in bay.data.vertices: vertex.co.z=min(vertex.co.z,4.43)
    for side in (-1,1):
        name='main_gear_'+str(side)
        y=side*3.85
        prism('Main gear wing-root bay '+str(side),[(-7.6,side*1.45,4.02),
              (-7.2,side*4.04,4.02),(-4.65,side*4.04,4.02),(-4.35,side*1.45,4.02)],
              .80,white,'fuselage')
        joint(name,(-6.4,y,3.85),(1,0,0),-side*math.pi/2,'gear','gear')
        RIG[name]['start']=.30
        rod(name+' barrel',(-6.4,y,3.85),(-6.4,y,1.8),.16,steel,'gear',name)
        # Brace remains in the longitudinal leg plane, rather than sweeping above the wing.
        rod(name+' brace',(-4.9,y,3.85),(-6.4,y,2.1),.08,steel,'gear',name)
        sliding_start=len(OBJECTS)
        rod(name+' sliding piston',(-6.4,y,2.6),(-6.4,y,.85),.115,steel,'gear',name)
        rod(name+' bogie',(-7.05,y,.63),(-5.75,y,.63),.13,steel,'gear',name)
        for x in (-7.05,-5.75):
            for yy in (y-.45,y+.45):
                rod(name+' tyre',(x,yy-.18,.60),(x,yy+.18,.60),.60,rubber,'gear',name,32)
                rod(name+' hub',(x,yy-.185,.60),(x,yy+.185,.60),.27,steel,'gear',name,24)
        for ob in OBJECTS[sliding_start:]:
            ob['slide']=(0,0,.20)
            ob['slideEnd']=.30
    joint('nose_gear',(12,0,4.25),(0,1,0),math.pi/2,'gear','gear')
    rod('Nose oleo',(12,0,4.25),(12,0,.60),.12,steel,'gear','nose_gear')
    rod('Nose brace',(10.6,0,3.85),(12,0,1.6),.07,steel,'gear','nose_gear')
    for y in (-.29,.29):
        rod('Nose tyre',(12,y-.12,.43),(12,y+.12,.43),.43,rubber,'gear','nose_gear',32)
        rod('Nose hub',(12,y-.125,.43),(12,y+.125,.43),.19,steel,'gear','nose_gear',24)
    # Tail bumper wheel pair (fixed visual detail in this first version).
    rod('Tail bumper',(-24.4,0,4.75),(-25,0,4.0),.065,steel,'gear')
    for y in (-.16,.16):
        rod('Tail wheel',(-25,y-.08,3.9),(-25,y+.08,3.9),.22,rubber,'gear',sides=20)


def world(v):
    return (v[0]*SCALE,v[2]*SCALE,-v[1]*SCALE)


def encode(ob):
    ob.data.calc_loop_triangles()
    pos=[world(ob.matrix_world @ v.co) for v in ob.data.vertices]
    lo=[min(v[k] for v in pos) for k in range(3)]
    step=[max(1e-9,(max(v[k] for v in pos)-lo[k])/65535) for k in range(3)]
    q=array('H',[max(0,min(65535,round((v[k]-lo[k])/step[k]))) for v in pos for k in range(3)])
    idx=array('H',[i for t in ob.data.loop_triangles for i in t.vertices])
    entry=dict(q=b64encode(q.tobytes()).decode(),qo=lo,qs=step,
                i=b64encode(idx.tobytes()).decode(),iw=2,c=list(ob.data.materials[0].diffuse_color),t=0)
    if 'slide' in ob:
        entry.update(slide=world(ob['slide']),slideEnd=ob['slideEnd'])
    return entry


def export():
    bpy.context.view_layer.update()
    parts={p:[] for p in ('fuselage','cockpit','nose','wing','engine','vstab','gear')}
    surfaces=[]
    for ob in OBJECTS:
        if 'joint' not in ob:
            parts[ob['partId']].append(encode(ob))
    for name,r in RIG.items():
        surfaces.append(dict(id=name,part=r['part'],channel=r['channel'],pv=world(r['pivot']),
                       ax=world(Vector(r['axis'])/SCALE),angle=r['angle'],start=r.get('start',0),
                       e=[encode(ob) for ob in OBJECTS if ob.get('joint')==name]))
    controls=[dict(id='nose',label=tr('機鼻下垂','Droop nose','機首下げ'),min=0,max=1,step=.01),
              dict(id='elevons',label=tr('六片襟副翼','Six elevons','6枚のエレボン'),min=-1,max=1,step=.01),
              dict(id='rudder',label=tr('雙段方向舵','Split rudder','上下ラダー'),min=-1,max=1,step=.01),
              dict(id='gear',label=tr('起落架收起示意','Gear retraction demo','脚格納デモ'),min=0,max=1,step=.01)]
    anchors={p:world(v) for p,v in dict(fuselage=(3,0,7.1),cockpit=(23,0,6.8),nose=(27,0,5.7),
              wing=(-10,-9,4.5),engine=(-10,-5,3.5),vstab=(-23,0,10),gear=(-6.4,-3.85,1)).items()}
    out=dict(meta=dict(format=2,model='concorde',source='SKY ARCHIVE / Blender — original educational prototype',
                       units='normalized: length 12; source metres',prototype=True),texture=None,parts=parts,
             anchors=anchors,surfaces=surfaces,controls=controls)
    assert len(surfaces)==12 and sum(len(s['e']) for s in surfaces)>12
    assert all(s['part'] in parts and s['e'] for s in surfaces)
    assert all(abs(sum(a*a for a in s['ax'])-1)<1e-6 for s in surfaces)
    (ROOT/'models/concorde.json').write_text(json.dumps(out,separators=(',',':')),encoding='utf-8')
    # Each joint has its own editable action, hinge origin and keyframes.
    for r in RIG.values():
        ob=r['object']; ob.rotation_mode='AXIS_ANGLE'
        ob.rotation_axis_angle=(0,*r['axis']); ob.keyframe_insert('rotation_axis_angle',frame=1)
        if r.get('start'):
            ob.keyframe_insert('rotation_axis_angle',frame=1+60*r['start'])
        ob.rotation_axis_angle=(r['angle'],*r['axis']); ob.keyframe_insert('rotation_axis_angle',frame=61)
        for fc in ob.animation_data.action.fcurves:
            for point in fc.keyframe_points: point.interpolation='LINEAR'
    for ob in OBJECTS:
        if 'slide' in ob:
            ob.location=(0,0,0); ob.keyframe_insert('location',frame=1)
            ob.location=ob['slide']; ob.keyframe_insert('location',frame=1+60*ob['slideEnd'])
            ob.keyframe_insert('location',frame=61)
            for fc in ob.animation_data.action.fcurves:
                for point in fc.keyframe_points: point.interpolation='LINEAR'
    scene=bpy.context.scene
    scene.frame_end=61
    scene.frame_set(1)
    scene.unit_settings.system='METRIC'
    bpy.context.preferences.filepaths.save_version=0
    for screen in bpy.data.screens:
        for area in screen.areas:
            if area.type=='VIEW_3D':
                area.spaces.active.region_3d.view_distance=80
                area.spaces.active.region_3d.view_location=(0,0,3)
                area.spaces.active.region_3d.view_rotation=Vector((1,-1,.6)).to_track_quat('Z','Y')
    dest=ROOT/'models/blender'
    dest.mkdir(exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(dest/'concorde.blend'))
    print(f'Concorde: {len(OBJECTS)} meshes, {len(surfaces)} animated joints, v2 exported')


if __name__=='__main__':
    build()
    export()
