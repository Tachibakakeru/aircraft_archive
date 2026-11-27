"""Check clearance of all door skins against every tyre. Run with Blender in background."""
import json
from array import array
from base64 import b64decode
from pathlib import Path
from mathutils import Matrix, Vector
from mathutils.bvhtree import BVHTree

model = json.loads(Path("models/an225.json").read_text(encoding="utf8"))
rig = model["surfaces"]
meshes = []
for s in rig:
    for e in s["e"]:
        name = e["name"]
        if not name.endswith(("Door","Tyre")): continue
        q,idx = array("H"),array("H")
        q.frombytes(b64decode(e["q"]))
        idx.frombytes(b64decode(e["i"]))
        verts = [Vector([q[i+j]*e["qs"][j]+e["qo"][j] for j in range(3)]) for i in range(0,len(q),3)]
        faces = [idx[i:i+3] for i in range(0,len(idx),3)]
        meshes.append((name,s["id"],verts,faces))
doors = [n for n,*_ in meshes if n.endswith("Door")]
tyres = [n for n,*_ in meshes if n.endswith("Tyre")]
hits = {}
for step in range(101):
    transforms = {}
    for s in rig:
        t=step/100 if s["channel"]=="gear" else 0
        for (a,y),(b,z) in zip(s.get("motion",[]),s.get("motion",[])[1:]):
            if a<=t<=b:
                t=y+(z-y)*(t-a)/(b-a)
                break
        p = Vector(s["pv"])
        local = Matrix.Translation(p)@Matrix.Rotation(s["angle"]*t,4,Vector(s["ax"]))@Matrix.Translation(-p)
        transforms[s["id"]] = transforms[s["parent"]]@local if "parent" in s else local
    trees = {n:BVHTree.FromPolygons([transforms[k]@v for v in vs],fs,all_triangles=True) for n,k,vs,fs in meshes}
    for d in doors:
        for w in tyres:
            if trees[d].overlap(trees[w]):
                hits.setdefault((d,w),[]).append(step)
for k,v in hits.items():
    if '-1-' in k[0] or '-NG-' in k[0]:print(k,min(v),max(v))
print("Overlapping pairs:",len(hits))
assert not hits
