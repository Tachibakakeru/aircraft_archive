"""Check exported geometry, hinges and fleet registration using only the stdlib."""
import json
import math
from array import array
from base64 import b64decode
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def vertices(entry):
    q=array('H',b64decode(entry['q']))
    return [tuple(q[i+k]*entry['qs'][k]+entry['qo'][k] for k in range(3)) for i in range(0,len(q),3)]


def posed(surface, entry, amount):
    start=surface.get('start',0)
    turn=max(0,min(1,(amount-start)/(1-start))) if start else amount
    angle=surface['angle']*turn
    c,s=math.cos(angle),math.sin(angle)
    ax=surface['ax']; pivot=surface['pv']
    slide=entry.get('slide',[0,0,0]); t=max(0,min(1,amount/entry.get('slideEnd',1)))
    for p in vertices(entry):
        v=[p[k]+slide[k]*t-pivot[k] for k in range(3)]
        cross=(ax[1]*v[2]-ax[2]*v[1],ax[2]*v[0]-ax[0]*v[2],ax[0]*v[1]-ax[1]*v[0])
        dot=sum(ax[k]*v[k] for k in range(3))
        yield tuple(pivot[k]+v[k]*c+cross[k]*s+ax[k]*dot*(1-c) for k in range(3))

def check():
    model=json.loads((ROOT/'models/concorde.json').read_text())
    assert model['meta']['format']==2
    assert len(model['surfaces'])==12
    channels={c['id'] for c in model['controls']}
    points=[]
    entries=[e for entries in model['parts'].values() for e in entries]
    for s in model['surfaces']:
        assert s['part'] in model['parts'] and s['channel'] in channels and s['e']
        assert abs(sum(v*v for v in s['ax'])-1)<1e-6
        assert len(s['pv'])==3 and all(math.isfinite(v) for v in s['pv'])
        entries.extend(s['e'])
    for e in entries:
        q=array('H',b64decode(e['q'])); idx=array('H',b64decode(e['i']))
        assert len(q)%3==0 and len(idx)%3==0 and max(idx)<len(q)//3
        pos=[tuple(q[i+k]*e['qs'][k]+e['qo'][k] for k in range(3)) for i in range(0,len(q),3)]
        assert all(math.isfinite(v) for p in pos for v in p)
        points.extend(pos)
    bounds=[(min(p[k] for p in points),max(p[k] for p in points)) for k in range(3)]
    assert abs(bounds[0][1]-bounds[0][0]-12)<.01, bounds
    assert abs(bounds[2][1]-bounds[2][0]-25.6*12/61.66)<.01, bounds
    assert abs(bounds[1][0])<.001, bounds
    scale=12/61.66
    assert abs(bounds[1][1]/scale-12)<.03, bounds
    hinges={s['id']:s for s in model['surfaces']}
    assert abs(hinges['nose_gear']['pv'][0]/scale-12)<.01
    assert abs(hinges['main_gear_1']['pv'][0]/scale+6.4)<.01
    assert abs(abs(hinges['main_gear_1']['pv'][2])/scale-3.85)<.01
    # Full travel, not just the neutral mesh: engine spans must never be swept by elevons.
    engines=[p for e in model['parts']['engine'] for p in vertices(e)]
    nacelle_min=min(abs(p[2])/scale for p in engines)
    nacelle_max=max(abs(p[2])/scale for p in engines)
    for s in model['surfaces']:
        if s['channel']=='elevons':
            for amount in (-1,-.5,0,.5,1):
                lateral=[abs(p[2])/scale for e in s['e'] for p in posed(s,e,amount)]
                assert max(lateral)<nacelle_min or min(lateral)>nacelle_max, s['id']
        if s['channel']=='gear':
            for amount in (0,.15,.3,.5,.75,1):
                for e in s['e']:
                    for x,height,lateral in posed(s,e,amount):
                        x,height,lateral=x/scale,height/scale,abs(lateral)/scale
                        # Upper skin envelopes: catches the old rigid brace above the wing.
                        roof=4.65
                        if lateral<1.435: roof=max(roof,5.4+1.66*math.sqrt(1-(lateral/1.435)**2))
                        if -8.1<=x<=-4.9 and lateral<2.1:
                            roof=max(roof,min(4.43,4.1+1.2*math.sqrt(1-(lateral/2.1)**2)))
                        assert height<roof+.02,(s['id'],amount,x,height,lateral)
                        if amount==1:
                            body=(lateral/1.435)**2+((height-5.4)/1.66)**2<=1.02
                            bay=-8.1<=x<=-4.9 and height<=4.45 and (lateral/2.1)**2+((height-4.1)/1.2)**2<=1.02
                            root_bay=-7.2<x<-4.65 and 1.45<lateral<4.04 and 3.62<height<4.42
                            wing=-14<x<0 and 1<lateral<4.1 and 4.16<height<4.65
                            assert body or bay or root_bay or wing,(s['id'],'outside stowed envelope',x,height,lateral)
    # Regression: old outer elevons projected in front of the wing leading edge.
    for s in model['surfaces']:
        if s['channel']=='elevons':
            assert abs(s['pv'][0]/scale+14.43)<.01
            for e in s['e']:
                assert e['qo'][0] < s['pv'][0]
    nose=next(s for s in model['surfaces'] if s['id']=='nose')
    assert abs(math.degrees(nose['angle'])-12.5)<1e-6 and nose['ax'][2]<0
    fleet=json.loads((ROOT/'data/fleet.json').read_text(encoding='utf-8'))
    assert next(a for a in fleet['aircraft'] if a['id']=='concorde')['has3d']
    assert (ROOT/'models/blender/concorde.blend').is_file()
    assert (ROOT/'assets/thumb_concorde.png').is_file()
    print(f'Concorde OK: {len(entries)} meshes, 12 hinges, metre ratios, ground contact, valid v2 indices.')

if __name__=='__main__': check()
