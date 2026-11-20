from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


ROOT = Path(__file__).resolve().parents[1]
fig = plt.figure(figsize=(9.5, 6.5))
ax = fig.add_axes([.02, .02, .96, .96])
ax.set(xlim=(0, 12), ylim=(0, 7.5))
ax.axis("off")
ax.text(.35, 7.15, "LLM-directed review with bounded authority", fontsize=17,
        fontweight="bold", color="#14334B")
boxes = {
    "request": (.35, 5.6, 3.0, .95, "User request\nplain-language task\n+ tool budget"),
    "gate": (4.25, 5.6, 3.1, .95, "Input validation\ndataset / intent / limits"),
    "model": (4.25, 3.45, 3.1, 1.25, "llm_decision\nMiniMax-M3 + tools\nselect next action\nor final answer"),
    "state": (.35, 3.3, 3.0, 1.55, "Fresh run-local state\nmessages + counters\nobservations + trace\nframe: tools only"),
    "tool": (8.5, 3.35, 3.1, 1.45, "read_only_tool\nvalidate model request\nexecute one tool\nor return feedback"),
    "final": (4.1, .85, 3.4, 1.25, "Human-review output\nanswer if available\ncounts + coverage/status\nNO data changes"),
}
for name, (x, y, w, h, label) in boxes.items():
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08",
                               edgecolor="#24526D", linewidth=1.3,
                               facecolor="#DDEEF3" if name == "model" else "#F5F8FA"))
    ax.text(x+w/2, y+h/2, label, ha="center", va="center", fontsize=12)


def arrow(start, end, label="", text_xy=None, color="#24526D"):
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=13,
                               linewidth=1.25, color=color))
    if label:
        ax.text(*text_xy, label, ha="center", va="center", fontsize=9, color=color)


arrow((3.45, 6.08), (4.15, 6.08))
arrow((5.8, 5.5), (5.8, 4.8))
arrow((3.45, 4.15), (4.15, 4.15), "messages", (3.8, 4.5))
arrow((4.15, 3.75), (3.45, 3.75))
arrow((7.45, 4.35), (8.4, 4.35), "LLM choice", (7.93, 4.65))
arrow((8.4, 3.8), (7.45, 3.8), "ToolMessage", (7.95, 3.48))
arrow((5.8, 3.35), (5.8, 2.2), "LLM finishes", (4.95, 2.8))
arrow((9.1, 3.2), (7.6, 1.85), "terminal guard\nor budget stop", (9.3, 2.35), "#87511D")
ax.text(.4, 2.55, "Six tool capabilities\nload / profile / missing\nduplicates / numeric /\ncategories", fontsize=12, color="#14334B", va="top")
ax.text(.4, .35, "Schematic of implemented components, not a runtime recording. "
        "Only user text and aggregate observations reach the provider.", fontsize=9, color="#425C6D")
fig.savefig(ROOT / "outputs/architecture_diagram.png", dpi=190, bbox_inches="tight", facecolor="white")
plt.close(fig)
