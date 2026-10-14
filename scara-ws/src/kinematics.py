"""
FK/IK for the 4-DOF arm: rail (d1) -> lift (d2) -> shoulder (th3) -> elbow (th4).

FK:
  X = d1 + L1*cos(th3) + L2*cos(th3+th4)
  Y =      L1*sin(th3) + L2*sin(th3+th4)
  Z = -d2

IK is underdetermined (4 joints, 3 output coords) because of the rail, so
d1 is usually treated as given (e.g. a planner parks the carriage near the
target) and the rest is solved as a normal 2-link IK problem.
"""

import numpy as np

L1 = 300.0
L2 = 200.0
RAIL_RANGE = (0.0, 800.0)
LIFT_RANGE = (300.0, 600.0)
R_MIN = abs(L1 - L2)
R_MAX = L1 + L2


def forward_kinematics(d1, d2, th3_deg, th4_deg):
    t3, t4 = np.radians(th3_deg), np.radians(th4_deg)
    X = d1 + L1 * np.cos(t3) + L2 * np.cos(t3 + t4)
    Y = L1 * np.sin(t3) + L2 * np.sin(t3 + t4)
    Z = -d2
    return X, Y, Z


def inverse_kinematics(X, Y, Z, d1=None, elbow="up"):
    """
    d1=None lets the function pick a rail position itself (centers under
    the target, then searches the rail if that doesn't work). Pass a d1
    if you already know where the carriage should be.
    """
    out = {"d1": None, "d2": None, "th3_deg": None, "th4_deg": None,
           "reachable": False, "reason": ""}

    d2 = -Z
    if not (LIFT_RANGE[0] - 1e-6 <= d2 <= LIFT_RANGE[1] + 1e-6):
        out["reason"] = f"Z={Z:.1f} needs d2={d2:.1f}, outside {LIFT_RANGE}"
        return out
    d2 = float(np.clip(d2, *LIFT_RANGE))

    d1_guess = X if d1 is None else d1
    d1_guess = float(np.clip(d1_guess, *RAIL_RANGE))

    def try_d1(d1v):
        xl, yl = X - d1v, Y
        r2 = xl**2 + yl**2
        r = np.sqrt(r2)
        if r < R_MIN - 1e-6 or r > R_MAX + 1e-6:
            return None
        c4 = np.clip((r2 - L1**2 - L2**2) / (2 * L1 * L2), -1.0, 1.0)
        t4 = np.arccos(c4)
        if elbow == "down":
            t4 = -t4
        t3 = np.arctan2(yl, xl) - np.arctan2(L2 * np.sin(t4), L1 + L2 * np.cos(t4))
        return d1v, d2, np.degrees(t3) % 360, np.degrees(t4) % 360

    sol = try_d1(d1_guess)

    if sol is None and d1 is None:
        for d1_try in np.linspace(*RAIL_RANGE, 1601):
            sol = try_d1(d1_try)
            if sol is not None:
                break

    if sol is None:
        out["reason"] = f"target ({X:.1f},{Y:.1f}) unreachable for any d1 in {RAIL_RANGE}"
        return out

    out["d1"], out["d2"], out["th3_deg"], out["th4_deg"] = sol
    out["reachable"] = True
    return out


if __name__ == "__main__":
    # sanity check: FK then IK should get back the same pose
    d1_t, d2_t, th3_t, th4_t = 400.0, 450.0, 45.0, 30.0
    X, Y, Z = forward_kinematics(d1_t, d2_t, th3_t, th4_t)
    print(f"FK(d1={d1_t}, d2={d2_t}, th3={th3_t}, th4={th4_t}) -> "
          f"X={X:.2f}, Y={Y:.2f}, Z={Z:.2f}")

    ik = inverse_kinematics(X, Y, Z, d1=d1_t, elbow="up")
    print("\nIK with d1 fixed at the true value:", ik)
    ok = np.isclose(ik["th3_deg"], th3_t) and np.isclose(ik["th4_deg"], th4_t)
    print("round trip matches:", ok)

    ik_auto = inverse_kinematics(X, Y, Z, d1=None, elbow="up")
    print("\nIK with d1 left free (auto-centered):", ik_auto)
    Xc, Yc, Zc = forward_kinematics(ik_auto["d1"], ik_auto["d2"],
                                     ik_auto["th3_deg"], ik_auto["th4_deg"])
    print(f"FK check on that solution -> X={Xc:.2f}, Y={Yc:.2f}, Z={Zc:.2f}")

    print("\nunreachable target example:", inverse_kinematics(2000, 0, -450, d1=None))

    ik_down = inverse_kinematics(X, Y, Z, d1=d1_t, elbow="down")
    print("\nelbow-down solution at the same target:", ik_down)
