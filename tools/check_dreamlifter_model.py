"""Check the exported Dreamlifter: dimensions, hinges, ground contact and stowed gear envelope (stdlib only)."""
import json
import math
from pathlib import Path
from check_concorde_model import vertices

ROOT = Path(__file__).resolve().parents[1]
M = 71.68 / 12          # archive units → metres


def rotate(p, s, amount):
    a = s['angle'] * amount
    c, sn = math.cos(a), math.sin(a)
    ax, pv = s['ax'], s['pv']
    v = [p[k] - pv[k] for k in range(3)]
    cr = (ax[1]*v[2]-ax[2]*v[1], ax[2]*v[0]-ax[0]*v[2], ax[0]*v[1]-ax[1]*v[0])
    d = sum(ax[k]*v[k] for k in range(3))
    return tuple(pv[k] + v[k]*c + cr[k]*sn + ax[k]*d*(1-c) for k in range(3))


def check():
    model = json.loads((ROOT/'models/dreamlifter.json').read_text())
    by_id = {s['id']: s for s in model['surfaces']}
    channels = {c['id'] for c in model['controls']}
    rest = [p for es in model['parts'].values() for e in es for p in vertices(e)]
    for s in model['surfaces']:
        assert s['channel'] in channels and s['part'] in model['parts'] and s['e'], s['id']
        assert abs(sum(v*v for v in s['ax'])-1) < 1e-6, s['id']
        assert 'parent' not in s or s['parent'] in by_id, s['id']
        rest += [p for e in s['e'] for p in vertices(e)]
    lo = [min(p[k] for p in rest)*M for k in range(3)]
    hi = [max(p[k] for p in rest)*M for k in range(3)]
    assert abs(hi[0]-lo[0]-71.68) < .1 and abs(hi[2]-lo[2]-64.4) < .2 and abs(hi[1]-21.54) < .1, (lo, hi)
    assert abs(lo[1]) < .03, lo                                   # tyres touch the ground
    counts = {c: sum(s['channel'] == c for s in model['surfaces']) for c in channels}
    assert counts['flaps'] == 12 and counts['gear'] == 15 and counts['spoilers'] == 12 and counts['slats'] == 28, counts
    assert counts['ailerons'] == 4 and counts['elevators'] == 4 and counts['rudder'] == 2, counts
    tyres = 0
    for s in model['surfaces']:
        if s['channel'] != 'gear':
            continue
        for e in s['e']:
            pts = list(vertices(e))
            tyre = e['c'][0] < .05 and len(pts) == 56             # 28-sided tyre cylinders
            tyres += tyre
            for amount in (.25, .5, .75, 1):
                for p in pts:
                    q, node = rotate(p, s, amount), s
                    while 'parent' in node:
                        node = by_id[node['parent']]
                        q = rotate(q, node, amount)
                    x, y, z = (v*M for v in q)
                    assert amount < 1 or y < 4.7, (s['id'], x, y, z)   # nothing pokes through the wing / fairing top
                    if amount == 1 and tyre:                      # tyres stow inside nose / wing-to-body fairing
                        nose = s['id'] == 'nose_gear'
                        assert y > (2.2 if nose else 1.75) and abs(z) < (2.9 if nose else 4.35), (s['id'], x, y, z)
    assert tyres == 18, tyres
    print(f"Dreamlifter OK: {len(model['surfaces'])} hinges, {sum(counts.values())} channel bindings, 18 tyres, "
          f"{hi[0]-lo[0]:.2f} × {hi[2]-lo[2]:.2f} × {hi[1]:.2f} m")


if __name__ == '__main__':
    check()
