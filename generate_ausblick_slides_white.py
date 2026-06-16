"""
Erzeugt eine helle (weiße) Alternative der Ausblick-Folien.
Nutzt das bestehende Layout aus generate_ausblick_slides.py,
überschreibt nur Farbschema und Ausgabedateinamen.
"""
from __future__ import annotations

import os

import generate_ausblick_slides as base
import matplotlib.image as mpimg
import numpy as np
from matplotlib.patches import FancyBboxPatch


# --- Helles Theme (Alternative) ---
base.BG = "#f5f5f5"
base.PANEL = "#ffffff"
base.PANEL_2 = "#ffffff"
base.PANEL_3 = "#ffffff"

# In der Basiskomposition wird WHITE häufig als Textfarbe genutzt.
# Für die White-Version setzen wir WHITE absichtlich auf dunklen Text.
base.WHITE = "#111111"
base.BLACK = "#111111"
base.GRAY = "#575757"
base.MID_GRAY = "#7a7a7a"
base.LIGHT_GRAY = "#2f2f2f"
base.BORDER = "#d6d6d6"
base.SOFT = "#eeeeee"

base.RED = "#d6001c"
base.RED_DARK = "#a10016"

base.USER_COLORS = {
    "Admin": "#d9d9d9",
    "Techniker": "#f6b9c2",
    "Bewohner": "#e3e3e3",
    "Gast": "#d6d6d6",
    "Entwickler": "#f4c7ce",
}

base.PRIO_COLORS = {
    "Hoch": base.RED,
    "Mittel": "#8a8a8a",
    "Niedrig": "#b3b3b3",
}


def _hex_to_rgb01(hex_color: str):
    c = hex_color.lstrip("#")
    if len(c) != 6:
        return (0.0, 0.0, 0.0)
    return (int(c[0:2], 16) / 255.0, int(c[2:4], 16) / 255.0, int(c[4:6], 16) / 255.0)


def badge_high_contrast(ax, x, y, w, h, text, fc, tc=None, ec="#202020", fs=9.5, weight="bold"):
    """Badge with automatic high-contrast text color for white theme."""
    box = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.08",
        facecolor=fc,
        edgecolor=ec,
        linewidth=1.2,
    )
    ax.add_patch(box)

    if tc is None:
        r, g, b = _hex_to_rgb01(fc)
        # Perceived luminance threshold.
        luminance = (0.299 * r) + (0.587 * g) + (0.114 * b)
        tc = "#111111" if luminance > 0.55 else "#ffffff"

    ax.text(
        x + (w / 2),
        y + (h / 2),
        text,
        ha="center",
        va="center",
        fontsize=fs,
        color=tc,
        fontweight=weight,
    )


def save_slide_white(fig, base_name: str):
    png_path = os.path.join(base.OUT_DIR, f"{base_name}_White.png")
    pdf_path = os.path.join(base.OUT_DIR, f"{base_name}_White.pdf")
    fig.savefig(png_path, dpi=base.DPI, facecolor=fig.get_facecolor(), pad_inches=0)
    fig.savefig(pdf_path, facecolor=fig.get_facecolor(), pad_inches=0)
    return png_path, pdf_path


def add_logo_white(fig):
    """Render logo as black-on-white for the white slide variant."""
    if not os.path.exists(base.LOGO_PATH):
        return

    img = mpimg.imread(base.LOGO_PATH).astype(float)
    if img.max() > 1.0:
        img /= 255.0

    rgb = img[..., :3]
    inverted = 1.0 - rgb

    if img.shape[-1] == 4:
        alpha = img[..., 3:4]
        # Keep transparent pixels white while inverting visible logo pixels.
        visible = (inverted * alpha) + (1.0 * (1.0 - alpha))
        logo_img = np.concatenate([visible, np.ones_like(alpha)], axis=-1)
    else:
        logo_img = inverted

    logo_ax = fig.add_axes([0.80, 0.905, 0.17, 0.07])
    logo_ax.set_facecolor("#ffffff")
    logo_ax.imshow(logo_img)
    logo_ax.axis("off")


# Save-Funktion für diese Session überschreiben.
base.save_slide = save_slide_white
base.add_logo = add_logo_white
base.badge = badge_high_contrast


if __name__ == "__main__":
    print("Generiere Ausblick-Folien im White-Design ...\n")
    paths = [
        base.create_slide1(),
        base.create_slide2(),
        base.create_slide3(),
        base.create_slide4(),
    ]
    print("\nFertig (White-Alternative):")
    for idx, path in enumerate(paths, start=1):
        print(f"  {idx}) {os.path.basename(path)}")
