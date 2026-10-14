"""
Compares workspace area of a fixed-base SCARA vs the rail-mounted version.
Same link lengths for both so it's a fair comparison - the only thing that
changes is whether the shoulder can slide along the ceiling rail.

A point is reachable if its distance from the shoulder falls between
|L1-L2| (fully folded) and L1+L2 (fully extended). For the rail version
a point just needs to be reachable from *some* position along the rail,
which turns into a simple min/max distance check since distance-to-point
is convex as you slide along a line.
"""

import numpy as np
import matplotlib.pyplot as plt

L1 = 300.0
L2 = 200.0
RAIL_LEN = 800.0

R_MIN = abs(L1 - L2)
R_MAX = L1 + L2

GRID_RES = 1.0  # mm per cell


def conventional_area_exact():
    return np.pi * (R_MAX**2 - R_MIN**2)


def reachable_mask(X, Y, rail_len):
    # closest point on the rail segment to (x,y), then the distance there
    # is the min; distance to whichever end is farther is the max
    d1_star = np.clip(X, 0.0, rail_len)
    dist_min = np.hypot(X - d1_star, Y)
    dist_end0 = np.hypot(X, Y)
    dist_endL = np.hypot(X - rail_len, Y)
    dist_max = np.maximum(dist_end0, dist_endL)
    return (dist_min <= R_MAX) & (dist_max >= R_MIN)


def grid_area(rail_len, res=GRID_RES):
    margin = 5.0
    xs = np.arange(-R_MAX - margin, rail_len + R_MAX + margin, res)
    ys = np.arange(-R_MAX - margin, R_MAX + margin, res)
    X, Y = np.meshgrid(xs, ys)
    mask = reachable_mask(X, Y, rail_len)
    area = mask.sum() * res**2
    return area, (xs, ys, mask)


THETA = np.linspace(0, 2 * np.pi, 300)


def link_paths(ax, base_x, label=False):
    elbow_x = base_x + L1 * np.cos(THETA)
    elbow_y = L1 * np.sin(THETA)
    out_x = base_x + (L1 + L2) * np.cos(THETA)
    out_y = (L1 + L2) * np.sin(THETA)
    in_x = base_x + R_MIN * np.cos(THETA)
    in_y = R_MIN * np.sin(THETA)

    ax.plot(elbow_x, elbow_y, color="#E69F00", lw=1.3,
            label="link 1 path (elbow)" if label else None)
    ax.plot(out_x, out_y, color="#D55E00", lw=1.3,
            label="link 2 path, extended" if label else None)
    ax.plot(in_x, in_y, color="#7B2D8B", lw=1.1, ls="--",
            label="link 2 path, folded" if label else None)
    ax.plot(base_x, 0, "s", color="0.15", markersize=5, zorder=6)


def save_plot(mask, xs, ys, cmap, title, base_xs, fname, tag):
    fig, ax = plt.subplots(figsize=(6.5, 6))
    ax.imshow(mask, extent=[xs[0], xs[-1], ys[0], ys[-1]],
              origin="lower", cmap=cmap, aspect="equal")
    ax.set_title(title)
    ax.set_xlabel("x (mm)")
    ax.set_ylabel("y (mm)")

    for i, bx in enumerate(base_xs):
        link_paths(ax, bx, label=(i == 0))

    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.12),
              ncol=1, fontsize=8, frameon=False)
    fig.text(0.5, 0.02, tag, ha="center", fontsize=11, fontweight="bold")

    plt.tight_layout(rect=[0, 0.06, 1, 1])
    plt.savefig(fname, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("saved", fname)


if __name__ == "__main__":
    A_conv = conventional_area_exact()
    A_conv_grid, (xs_c, ys_c, mask_c) = grid_area(0.0)
    A_rail, (xs_r, ys_r, mask_r) = grid_area(RAIL_LEN)

    gain = (A_rail - A_conv) / A_conv * 100

    print(f"L1={L1}, L2={L2}, rail={RAIL_LEN}")
    print(f"R_min={R_MIN}, R_max={R_MAX}")
    print(f"conventional area (exact):  {A_conv:,.0f} mm^2")
    print(f"conventional area (grid):   {A_conv_grid:,.0f} mm^2  (sanity check)")
    print(f"rail-mounted area (grid):   {A_rail:,.0f} mm^2")
    print(f"improvement: {gain:.2f}%  ({A_rail/A_conv:.3f}x)")

    save_plot(mask_c, xs_c, ys_c, "Greens",
              f"Conventional SCARA\nArea = {A_conv:,.0f} mm^2",
              [0.0], "figures/workspace_conventional.png", "(a)")

    save_plot(mask_r, xs_r, ys_r, "Blues",
              f"Rail-mounted SCARA\nArea = {A_rail:,.0f} mm^2  (+{gain:.1f}%)",
              [0.0, RAIL_LEN / 2, RAIL_LEN],
              "figures/workspace_ceiling.png", "(b)")
