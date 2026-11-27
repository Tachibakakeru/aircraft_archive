"""Check archive-coordinate poses against An-225 dimensions, wheel travel and ramp contact."""
import json
from base64 import b64decode
from pathlib import Path

import numpy as np
from scipy.spatial.transform import Rotation

ROOT = Path(__file__).resolve().parents[1]
model = json.loads((ROOT/"models/an225.json").read_text(encoding="utf8"))
surfaces = model["surfaces"]


def pose(**controls):
    matrices = {}
    clouds = {}
    for s in surfaces:
        amount = controls.get(s["channel"], 0)
        motion = s.get("motion")
        travel = np.interp(amount, *np.transpose(motion)) if motion else amount
        axis = np.array(s["ax"])
        rotation = Rotation.from_rotvec(axis/np.linalg.norm(axis)*s["angle"]*travel).as_matrix()
        center = np.array(s["pv"])
        transform = np.eye(4)
        transform[:3,:3] = rotation
        transform[:3,3] = center-rotation@center
        if s.get("parent"):
            transform = matrices[s["parent"]]@transform
        matrices[s["id"]] = transform
        for entry in s["e"]:
            xyz = np.frombuffer(b64decode(entry["q"]),"<u2").reshape(-1,3)*entry["qs"]+entry["qo"]
            if "slide" in entry:
                start = entry.get("slideStart",0)
                xyz += np.array(entry["slide"])*np.clip((amount-start)/(entry.get("slideEnd",1)-start),0,1)
            clouds[entry["name"]] = xyz@transform[:3,:3].T+transform[:3,3]
    return clouds


if __name__=="__main__":
    down = pose()
    dimensions = np.ptp(np.vstack(list(down.values())),axis=0)*7
    assert np.allclose(dimensions, [84,18.2,88.4], atol=.02), dimensions
    print("Length, height, span (m):", dimensions)
    tyres = [n for n in down if n.endswith("Tyre")]
    assert len(tyres)==32 and sum(s.get("rpm",0)!=0 for s in surfaces)==6
    stowed = pose(gear=1)
    for n in tyres:
        assert abs(down[n][:,1].min())<.002, n
        assert stowed[n][:,1].min()>.18, (n,stowed[n][:,1].min())
    tip = pose(loading=1)["Ramp-1"][:,1].min()*7
    print("Ramp tip above apron (m):", tip)
    assert abs(tip)<.01, tip
    for key in ("Support-1","Support--1"):
        assert abs(pose(loading=1)[key][:,1].min()*7)<.01
    for g in np.linspace(0,1,41):
        cargo_pose = pose(loading=g)
        assert min(cargo_pose[n][:,1].min() for n in tyres) > -.002
        values = pose(gear=g)
        lowest = min(values[n][:,1].min() for n in tyres)
        assert lowest>-.04, (g,lowest)
    print("32 tyre paths, six rotor pivots and 41 gear positions checked.")
