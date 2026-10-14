# ceiling-mounted SCARA arm — kinematics & workspace

Analysis code for the 4-DOF ceiling-mounted SCARA arm (RAAICON 2026 paper).
Joint chain is rail (d1, prismatic) -> lift (d2, prismatic) -> shoulder (th3,
revolute) -> elbow (th4, revolute). L1 = 300mm, L2 = 200mm, rail = 800mm,
lift range = 300-600mm.

## what's here

- `src/kinematics.py` — forward/inverse kinematics, with a few sanity checks
  (FK->IK round trip, elbow up/down, unreachable targets)
- `src/workspace_analysis.py` — compares reachable area of a fixed-base
  SCARA vs. the rail-mounted version, same link lengths for both
- `src/schematic.py` — generates the kinematic diagram figure (IEEE column
  sizes, 600dpi PNG + vector PDF)
- `figures/` — output images from the scripts above

## running it

Needs numpy and matplotlib.

```
pip install numpy matplotlib
python src/workspace_analysis.py
python src/kinematics.py
python src/schematic.py
```

Figures get written to `figures/`.

## workspace result

Fixed-base SCARA: ~754,000 mm² (closed-form annulus, R_min=100mm, R_max=500mm)
Rail-mounted: ~1,586,000 mm² (numerically integrated, since there's no
closed form once the shoulder can slide)

That's about a 110% increase. The gain is from the rail alone — lift range
is identical in both cases so it doesn't affect the X-Y area, it just
relocates the same shape vertically.

## notes

- Workspace area is computed on a 1mm grid rather than Monte Carlo sampling.
  The reachability test itself is exact (derived from the DH-based FK), so
  this is just a deterministic area integration, not a random estimate.
- IK is underdetermined because of the rail (4 joints, 3 position outputs).
  `inverse_kinematics()` either takes a fixed `d1` or searches the rail
  range if none is given.
