"""
Draws the kinematic schematic (rail -> lift -> shoulder -> elbow -> EE)
sized for IEEE columns. Saves a single-column (3.5in) and double-column
(7.16in) version, each as PNG (600dpi) and vector PDF.
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Arial", "Helvetica", "DejaVu Sans"]
plt.rcParams["axes.linewidth"] = 0.8
plt.rcParams["pdf.fonttype"] = 42  # embed real text, not outlines
plt.rcParams["ps.fonttype"] = 42

INK = "#000000"
AXIS_COLOR = "#404040"
JOINT_EDGE = "#2E5C8A"
JOINT_FILL = "#EAF1FA"
LINK1_COLOR = "#1B8F68"
LINK2_COLOR = "#B33E12"


def build_figure(width_in, fs=1.0):
    fig, ax = plt.subplots(figsize=(width_in, width_in * 0.58))
    ax.set_xlim(0.15, 10.1)
    ax.set_ylim(1.55, 6.55)
    ax.set_aspect("equal")
    ax.axis("off")

    dim_fs, lbl_fs, small_fs, leg_fs = 9 * fs, 9 * fs, 8 * fs, 8.5 * fs

    # rail (J1)
    rail_y = 5.9
    ax.annotate("", xy=(4.6, rail_y + 0.36), xytext=(0.75, rail_y + 0.36),
                arrowprops=dict(arrowstyle="<->,head_width=2.2,head_length=3.5",
                                 color=INK, lw=1.1, shrinkA=0, shrinkB=0))
    ax.text(2.675, rail_y + 0.5, "800 mm", ha="center", fontsize=dim_fs)

    ax.add_patch(mpatches.FancyBboxPatch((0.75, rail_y - 0.085), 3.85, 0.17,
                 boxstyle="round,pad=0,rounding_size=0.02",
                 fc="#d6d6d6", ec="0.3", lw=0.7))
    ax.text(0.62, rail_y, "rail", ha="right", va="center", fontsize=small_fs, color="0.25")

    ax.add_patch(mpatches.FancyBboxPatch((2.15, rail_y - 0.22), 0.55, 0.44,
                 boxstyle="round,pad=0.015,rounding_size=0.04",
                 fc=JOINT_FILL, ec=JOINT_EDGE, lw=1.2))
    ax.text(2.425, rail_y, "J1", ha="center", va="center", fontsize=lbl_fs,
            color=JOINT_EDGE, fontweight="bold")

    # lift (J2)
    ax.plot([2.32, 2.32], [3.35, rail_y - 0.22], color=AXIS_COLOR, lw=0.8)
    ax.plot([2.53, 2.53], [3.35, rail_y - 0.22], color=AXIS_COLOR, lw=0.8)

    ax.annotate("", xy=(1.55, 5.15), xytext=(1.55, 3.65),
                arrowprops=dict(arrowstyle="<->,head_width=2.2,head_length=3.5",
                                 color=INK, lw=1.1, shrinkA=0, shrinkB=0))
    ax.text(0.98, 4.4, "300\u2013600 mm", ha="center", va="center", fontsize=dim_fs)

    ax.add_patch(mpatches.FancyBboxPatch((2.05, 4.0), 0.75, 0.4,
                 boxstyle="round,pad=0.015,rounding_size=0.04",
                 fc=JOINT_FILL, ec=JOINT_EDGE, lw=1.2))
    ax.text(2.425, 4.2, "J2", ha="center", va="center", fontsize=lbl_fs,
            color=JOINT_EDGE, fontweight="bold")
    ax.text(2.92, 4.2, "lift", ha="left", va="center", fontsize=small_fs, color="0.25")

    # shoulder (J3)
    j3 = (2.425, 3.05)
    ax.plot([j3[0], j3[0]], [3.35, j3[1] + 0.24], color=AXIS_COLOR, lw=0.8, ls=(0, (3, 2)))
    ax.add_patch(mpatches.Circle(j3, 0.24, fill=False, ls=(0, (3, 2)), ec="0.3", lw=1.0))
    ax.plot(*j3, "o", color=INK, markersize=3.2, zorder=6)
    ax.text(1.32, 3.2, "J3 \u00B7 360\u00B0", ha="center", fontsize=lbl_fs)
    ax.text(1.32, 2.98, "(shoulder)", ha="center", fontsize=small_fs, color="0.3")
    ax.annotate("", xy=(j3[0] + 0.42, j3[1]), xytext=j3,
                arrowprops=dict(arrowstyle="-|>,head_width=2.4,head_length=4",
                                 color="0.25", lw=1.0, shrinkA=0, shrinkB=0))
    ax.annotate("", xy=(j3[0], j3[1] - 0.42), xytext=j3,
                arrowprops=dict(arrowstyle="-|>,head_width=2.4,head_length=4",
                                 color="0.25", lw=1.0, shrinkA=0, shrinkB=0))
    ax.text(j3[0] - 0.12, j3[1] - 0.6, "z", fontsize=small_fs, color="0.25", style="italic")

    # link 1
    j4 = (5.3, 3.05)
    ax.plot([j3[0], j4[0]], [j3[1], j4[1]], color=LINK1_COLOR, lw=4.6,
            solid_capstyle="round", zorder=2)
    ax.text((j3[0] + j4[0]) / 2, j3[1] + 0.3, "L1 = 300 mm", ha="center", fontsize=dim_fs)

    # elbow (J4)
    ax.add_patch(mpatches.Circle(j4, 0.24, fill=False, ls=(0, (3, 2)), ec="0.3", lw=1.0))
    ax.plot(*j4, "o", color=INK, markersize=3.2, zorder=6)
    ax.text(5.3, 3.64, "J4 \u00B7 360\u00B0", ha="center", fontsize=lbl_fs)
    ax.text(5.3, 3.42, "(elbow)", ha="center", fontsize=small_fs, color="0.3")
    ax.annotate("", xy=(j4[0] + 0.42, j4[1]), xytext=j4,
                arrowprops=dict(arrowstyle="-|>,head_width=2.4,head_length=4",
                                 color="0.25", lw=1.0, shrinkA=0, shrinkB=0))
    ax.annotate("", xy=(j4[0], j4[1] - 0.42), xytext=j4,
                arrowprops=dict(arrowstyle="-|>,head_width=2.4,head_length=4",
                                 color="0.25", lw=1.0, shrinkA=0, shrinkB=0))
    ax.text(j4[0] + 0.1, j4[1] - 0.6, "z", fontsize=small_fs, color="0.25", style="italic")

    # link 2
    ee = (7.0, 3.05)
    ax.plot([j4[0], ee[0]], [j4[1], ee[1]], color=LINK2_COLOR, lw=4.6,
            solid_capstyle="round", zorder=2)
    ax.text((j4[0] + ee[0]) / 2, j4[1] + 0.3, "L2 = 200 mm", ha="center", fontsize=dim_fs)

    # end effector
    ax.plot(*ee, "o", mfc="white", mec=INK, markersize=6.5, mew=1.2, zorder=6)
    ax.text(ee[0] + 0.3, ee[1], "EE", fontsize=lbl_fs, va="center")

    legend = [
        Line2D([0], [0], marker="s", color="none", markerfacecolor=JOINT_FILL,
               markeredgecolor=JOINT_EDGE, markeredgewidth=1.2, markersize=10,
               label="prismatic joint"),
        Line2D([0], [0], marker="o", color="none", markerfacecolor="none",
               markeredgecolor="0.3", markeredgewidth=1.1, markersize=10,
               linestyle=(0, (3, 2)), label="revolute joint (360\u00B0)"),
        Line2D([0], [0], color=LINK1_COLOR, lw=4.4, solid_capstyle="round", label="link"),
    ]
    ax.legend(handles=legend, loc="upper center", bbox_to_anchor=(0.5, -0.06),
              ncol=3, fontsize=leg_fs, frameon=False, handletextpad=0.6,
              columnspacing=1.8, borderaxespad=0)

    plt.tight_layout(rect=[0, 0.07, 1, 1])
    return fig


if __name__ == "__main__":
    fig = build_figure(3.5, fs=1.0)
    fig.savefig("figures/schematic_1col.png", dpi=600, bbox_inches="tight")
    fig.savefig("figures/schematic_1col.pdf", bbox_inches="tight")
    plt.close(fig)

    fig = build_figure(7.16, fs=1.15)
    fig.savefig("figures/schematic_2col.png", dpi=600, bbox_inches="tight")
    fig.savefig("figures/schematic_2col.pdf", bbox_inches="tight")
    plt.close(fig)

    print("done")
