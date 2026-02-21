"""
ForkLion Visualizer - Full Trait Rendering
Every DNA trait produces visible SVG differences.
"""

import math
import hashlib
from typing import Dict, List, Optional
from src.genetics import LionDNA, TraitCategory, Rarity


class LionVisualizer:
    """Generates expressive SVG lion art from DNA traits."""

    # Body color palettes
    BODY_COLORS = {
        "brown":    {"main": "#CD853F", "shadow": "#8B4513", "highlight": "#DEB887", "mane": "#8B4513", "mane2": "#6B3410"},
        "tan":      {"main": "#D2B48C", "shadow": "#B8956E", "highlight": "#F4E4C1", "mane": "#A0784C", "mane2": "#7A5A3A"},
        "beige":    {"main": "#F5F5DC", "shadow": "#D4D4B8", "highlight": "#FFFFF0", "mane": "#C8B88A", "mane2": "#A09068"},
        "golden":   {"main": "#DAA520", "shadow": "#B8860B", "highlight": "#FFD700", "mane": "#B8860B", "mane2": "#8B6508"},
        "white":    {"main": "#F8F8F8", "shadow": "#D8D8D8", "highlight": "#FFFFFF", "mane": "#E0D8D0", "mane2": "#C8C0B8"},
        "black":    {"main": "#3A3A3A", "shadow": "#1A1A1A", "highlight": "#5A5A5A", "mane": "#1A1A1A", "mane2": "#0A0A0A"},
        "gray":     {"main": "#A0A0A0", "shadow": "#707070", "highlight": "#C8C8C8", "mane": "#606060", "mane2": "#404040"},
        "silver":   {"main": "#C0C0C0", "shadow": "#909090", "highlight": "#E8E8E8", "mane": "#808080", "mane2": "#606060"},
        "copper":   {"main": "#B87333", "shadow": "#8B5A2B", "highlight": "#DA8A4A", "mane": "#7A4A1A", "mane2": "#5A3A10"},
        "bronze":   {"main": "#CD7F32", "shadow": "#A0622A", "highlight": "#E0A050", "mane": "#7A4A1A", "mane2": "#5A3210"},
        "blue":     {"main": "#4A90D9", "shadow": "#2A6AB0", "highlight": "#7AB8FF", "mane": "#2A5A90", "mane2": "#1A3A60"},
        "purple":   {"main": "#9B59B6", "shadow": "#6C3483", "highlight": "#C39BD3", "mane": "#5B2C6F", "mane2": "#3B1C4F"},
        "green":    {"main": "#5DAE8B", "shadow": "#3D8E6B", "highlight": "#8DD8B0", "mane": "#2D6E4B", "mane2": "#1D4E3B"},
        "pink":     {"main": "#E8829A", "shadow": "#C8627A", "highlight": "#FFB0C8", "mane": "#A84060", "mane2": "#882848"},
        "rainbow":  {"main": "#FFB347", "shadow": "#FF6B6B", "highlight": "#FFFF88", "mane": "#9B59B6", "mane2": "#4A90D9"},
        "galaxy":   {"main": "#2C1654", "shadow": "#1A0A30", "highlight": "#6C3FA0", "mane": "#0D0D2B", "mane2": "#1A0530"},
        "holographic": {"main": "#E0E8F0", "shadow": "#A0D0E0", "highlight": "#F0F8FF", "mane": "#C0A8D8", "mane2": "#90D8C0"},
        "crystal":  {"main": "#D4F1F9", "shadow": "#88CCE8", "highlight": "#EAFBFF", "mane": "#70B8D8", "mane2": "#5098B8"},
    }

    # Background configs
    BG_COLORS = {
        "white":       ("#FFF5E6", None),
        "blue_sky":    (None, "sky"),
        "green_grass": (None, "grass"),
        "sunset":      (None, "sunset"),
        "forest":      (None, "forest"),
        "beach":       (None, "beach"),
        "mountains":   (None, "mountains"),
        "city":        (None, "city"),
        "space":       (None, "space"),
        "underwater":  (None, "underwater"),
        "volcano":     (None, "volcano"),
        "aurora":      (None, "aurora_bg"),
        "multiverse":  (None, "multiverse"),
        "black_hole":  (None, "black_hole"),
        "dimension_rift": (None, "dimension_rift"),
        "heaven":      (None, "heaven"),
    }

    @classmethod
    def generate_svg(cls, dna: LionDNA, width: int = 400, height: int = 400) -> str:
        traits = {
            "body_color": dna.traits.get(TraitCategory.BODY_COLOR),
            "expression": dna.traits.get(TraitCategory.FACE_EXPRESSION),
            "accessory": dna.traits.get(TraitCategory.ACCESSORY),
            "pattern": dna.traits.get(TraitCategory.PATTERN),
            "background": dna.traits.get(TraitCategory.BACKGROUND),
            "special": dna.traits.get(TraitCategory.SPECIAL),
        }
        t = {k: (v.value if v else "none") for k, v in traits.items()}
        seed = int(dna.dna_hash[:8], 16) if dna.dna_hash else 12345
        cx, cy = width // 2, height // 2

        colors = cls.BODY_COLORS.get(t["body_color"], cls.BODY_COLORS["brown"])

        parts = [
            f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">',
            cls._defs(t, colors, width, height),
            cls._background(t["background"], width, height, seed),
            cls._body(colors, t["pattern"], cx, cy, seed),
            cls._face(t["expression"], cx, cy, colors),
            cls._accessory(t["accessory"], cx, cy, colors),
            cls._special(t["special"], width, height, seed),
            "</svg>",
        ]
        return "\n".join(parts)

    @classmethod
    def generate_thumbnail(cls, dna: LionDNA, size: int = 100) -> str:
        return cls.generate_svg(dna, width=size, height=size)

    # ── defs ──────────────────────────────────────────────────────
    @classmethod
    def _defs(cls, t: dict, colors: dict, w: int, h: int) -> str:
        d = ['<defs>']
        d.append('<filter id="shadow" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="2" dy="4" stdDeviation="3" flood-opacity="0.3"/></filter>')

        # Glow filter for special=glow or legendary body colors
        d.append('<filter id="glow"><feGaussianBlur in="SourceGraphic" stdDeviation="8" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')
        d.append('<filter id="glow-strong"><feGaussianBlur in="SourceGraphic" stdDeviation="15" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')

        # Background gradients
        d.append('<linearGradient id="bg-sky" x1="0%" y1="0%" x2="0%" y2="100%"><stop offset="0%" stop-color="#87CEEB"/><stop offset="100%" stop-color="#E0F4FF"/></linearGradient>')
        d.append('<linearGradient id="bg-sunset" x1="0%" y1="0%" x2="0%" y2="100%"><stop offset="0%" stop-color="#FF4500"/><stop offset="40%" stop-color="#FF8C00"/><stop offset="100%" stop-color="#FFD700"/></linearGradient>')
        d.append('<linearGradient id="bg-forest" x1="0%" y1="0%" x2="0%" y2="100%"><stop offset="0%" stop-color="#2D5016"/><stop offset="100%" stop-color="#4A7A2E"/></linearGradient>')
        d.append('<linearGradient id="bg-grass" x1="0%" y1="0%" x2="0%" y2="100%"><stop offset="0%" stop-color="#87CEEB"/><stop offset="60%" stop-color="#87CEEB"/><stop offset="60%" stop-color="#7CCD7C"/><stop offset="100%" stop-color="#4A8B3F"/></linearGradient>')
        d.append('<linearGradient id="bg-beach" x1="0%" y1="0%" x2="0%" y2="100%"><stop offset="0%" stop-color="#87CEEB"/><stop offset="50%" stop-color="#87CEEB"/><stop offset="50%" stop-color="#F4D03F"/><stop offset="100%" stop-color="#E8C430"/></linearGradient>')
        d.append('<linearGradient id="bg-space" x1="0%" y1="0%" x2="0%" y2="100%"><stop offset="0%" stop-color="#0B0B2B"/><stop offset="100%" stop-color="#1A1A4A"/></linearGradient>')
        d.append('<linearGradient id="bg-underwater" x1="0%" y1="0%" x2="0%" y2="100%"><stop offset="0%" stop-color="#006994"/><stop offset="100%" stop-color="#003050"/></linearGradient>')
        d.append('<linearGradient id="bg-volcano" x1="0%" y1="0%" x2="0%" y2="100%"><stop offset="0%" stop-color="#1A0A00"/><stop offset="60%" stop-color="#4A1A00"/><stop offset="100%" stop-color="#FF4500"/></linearGradient>')
        d.append('<linearGradient id="bg-aurora-bg" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#0B1A30"/><stop offset="33%" stop-color="#1A4A3A"/><stop offset="66%" stop-color="#2A1A5A"/><stop offset="100%" stop-color="#0B1A30"/></linearGradient>')
        d.append('<linearGradient id="bg-multiverse" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#FF006E"/><stop offset="25%" stop-color="#8338EC"/><stop offset="50%" stop-color="#3A86FF"/><stop offset="75%" stop-color="#06D6A0"/><stop offset="100%" stop-color="#FFD166"/></linearGradient>')
        d.append('<radialGradient id="bg-black-hole" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="#000000"/><stop offset="60%" stop-color="#1A0530"/><stop offset="100%" stop-color="#4A1A70"/></radialGradient>')
        d.append('<linearGradient id="bg-dimension" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#FF0080"/><stop offset="50%" stop-color="#0000FF"/><stop offset="100%" stop-color="#00FF80"/></linearGradient>')
        d.append('<linearGradient id="bg-heaven" x1="0%" y1="0%" x2="0%" y2="100%"><stop offset="0%" stop-color="#FFFDE0"/><stop offset="100%" stop-color="#FFF8E1"/></linearGradient>')
        d.append('<linearGradient id="bg-mountains" x1="0%" y1="0%" x2="0%" y2="100%"><stop offset="0%" stop-color="#87CEEB"/><stop offset="100%" stop-color="#B0C4DE"/></linearGradient>')
        d.append('<linearGradient id="bg-city" x1="0%" y1="0%" x2="0%" y2="100%"><stop offset="0%" stop-color="#1A1A2E"/><stop offset="100%" stop-color="#16213E"/></linearGradient>')

        # Pattern clip
        d.append(f'<clipPath id="body-clip"><circle cx="{w//2}" cy="{h//2}" r="88"/></clipPath>')

        # Rainbow gradient for special bodies
        if t.get("body_color") == "rainbow":
            d.append(f'<linearGradient id="rainbow-mane" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#FF6B6B"/><stop offset="20%" stop-color="#FFB347"/><stop offset="40%" stop-color="#FFFF88"/><stop offset="60%" stop-color="#88FF88"/><stop offset="80%" stop-color="#88BBFF"/><stop offset="100%" stop-color="#BB88FF"/></linearGradient>')

        d.append('</defs>')
        return "\n".join(d)

    # ── background ────────────────────────────────────────────────
    @classmethod
    def _background(cls, bg: str, w: int, h: int, seed: int) -> str:
        p = []

        simple_fills = {
            "white": "#FFF5E6",
            "blue_sky": "url(#bg-sky)",
            "green_grass": "url(#bg-grass)",
            "sunset": "url(#bg-sunset)",
            "forest": "url(#bg-forest)",
            "beach": "url(#bg-beach)",
            "space": "url(#bg-space)",
            "underwater": "url(#bg-underwater)",
            "volcano": "url(#bg-volcano)",
            "aurora": "url(#bg-aurora-bg)",
            "multiverse": "url(#bg-multiverse)",
            "black_hole": "url(#bg-black-hole)",
            "dimension_rift": "url(#bg-dimension)",
            "heaven": "url(#bg-heaven)",
            "mountains": "url(#bg-mountains)",
            "city": "url(#bg-city)",
        }

        fill = simple_fills.get(bg, "#FFF5E6")
        p.append(f'<rect width="{w}" height="{h}" fill="{fill}"/>')

        # Scene elements
        if bg == "blue_sky":
            # Clouds
            for i in range(3):
                cx = 60 + ((seed + i * 137) % (w - 120))
                cy = 30 + ((seed + i * 53) % 80)
                p.append(f'<ellipse cx="{cx}" cy="{cy}" rx="40" ry="18" fill="white" opacity="0.7"/>')
                p.append(f'<ellipse cx="{cx+25}" cy="{cy-5}" rx="30" ry="15" fill="white" opacity="0.6"/>')

        elif bg == "sunset":
            # Sun
            p.append(f'<circle cx="{w//2}" cy="{h//2+40}" r="60" fill="#FFD700" opacity="0.5"/>')

        elif bg == "green_grass" or bg == "savanna":
            # Sun + grass blades
            p.append(f'<circle cx="{w-60}" cy="50" r="30" fill="#FFD700" opacity="0.8"/>')
            for i in range(8):
                x = 20 + ((seed + i * 47) % (w - 40))
                p.append(f'<line x1="{x}" y1="{h}" x2="{x-5}" y2="{h-20}" stroke="#5A8A3A" stroke-width="2"/>')

        elif bg == "forest":
            # Trees in background
            for i in range(5):
                tx = 30 + ((seed + i * 71) % (w - 60))
                th = 60 + (seed + i * 31) % 40
                p.append(f'<polygon points="{tx},{h-th} {tx-15},{h-10} {tx+15},{h-10}" fill="#1A4010" opacity="0.5"/>')
                p.append(f'<rect x="{tx-3}" y="{h-15}" width="6" height="15" fill="#5A3A1A" opacity="0.5"/>')

        elif bg == "beach":
            # Waves
            p.append(f'<path d="M0 {h//2-10} Q{w//4} {h//2-25} {w//2} {h//2-10} T{w} {h//2-10}" stroke="#5DADE2" stroke-width="2" fill="none" opacity="0.5"/>')

        elif bg == "mountains":
            # Mountain peaks
            p.append(f'<polygon points="0,{h} 80,{h-180} 160,{h}" fill="#6C7A89" opacity="0.6"/>')
            p.append(f'<polygon points="100,{h} 200,{h-220} 300,{h}" fill="#7F8C8D" opacity="0.5"/>')
            p.append(f'<polygon points="250,{h} 340,{h-160} 400,{h}" fill="#6C7A89" opacity="0.6"/>')
            # Snow caps
            p.append(f'<polygon points="65,{h-165} 80,{h-180} 95,{h-165}" fill="white" opacity="0.8"/>')
            p.append(f'<polygon points="180,{h-200} 200,{h-220} 220,{h-200}" fill="white" opacity="0.8"/>')

        elif bg == "city":
            # Building silhouettes
            buildings = [(20,140), (60,180), (100,120), (140,200), (180,150),
                         (220,190), (260,130), (300,170), (340,160), (370,140)]
            for bx, bh in buildings:
                bw = 30 + (seed + bx) % 15
                p.append(f'<rect x="{bx}" y="{h-bh}" width="{bw}" height="{bh}" fill="#0F3460" opacity="0.7"/>')
                # Windows
                for wy in range(h - bh + 10, h - 10, 20):
                    for wx in range(bx + 5, bx + bw - 5, 10):
                        lit = ((seed + wx + wy) % 3) != 0
                        p.append(f'<rect x="{wx}" y="{wy}" width="5" height="8" fill="{"#FFD700" if lit else "#1A1A2E"}" opacity="0.8"/>')

        elif bg == "space":
            # Stars
            for i in range(30):
                sx = (seed * (i + 1) * 7) % w
                sy = (seed * (i + 1) * 13) % h
                sr = 1 + (i % 3)
                p.append(f'<circle cx="{sx}" cy="{sy}" r="{sr}" fill="white" opacity="{0.4 + (i%5)*0.12}"/>')
            # Nebula glow
            p.append(f'<circle cx="{w//3}" cy="{h//3}" r="80" fill="#9B59B6" opacity="0.08"/>')
            p.append(f'<circle cx="{w*2//3}" cy="{h*2//3}" r="60" fill="#3498DB" opacity="0.08"/>')

        elif bg == "underwater":
            # Bubbles
            for i in range(12):
                bx = (seed * (i+1) * 11) % w
                by = (seed * (i+1) * 17) % h
                br = 3 + i % 6
                p.append(f'<circle cx="{bx}" cy="{by}" r="{br}" fill="none" stroke="#80D0E0" stroke-width="1" opacity="0.4"/>')
            # Seaweed
            for i in range(4):
                sx = 40 + (seed + i * 97) % (w - 80)
                p.append(f'<path d="M{sx} {h} Q{sx+10} {h-40} {sx-5} {h-70} Q{sx+15} {h-100} {sx} {h-120}" stroke="#2E8B57" stroke-width="4" fill="none" opacity="0.5"/>')

        elif bg == "volcano":
            # Lava glow
            p.append(f'<circle cx="{w//2}" cy="{h}" r="120" fill="#FF4500" opacity="0.15"/>')
            # Embers
            for i in range(8):
                ex = (seed * (i+1) * 23) % w
                ey = (seed * (i+1) * 37) % h
                p.append(f'<circle cx="{ex}" cy="{ey}" r="2" fill="#FF6347" opacity="0.6"/>')

        elif bg == "aurora":
            # Wavy aurora bands
            for i in range(3):
                y = 40 + i * 50
                color = ["#00FF88", "#8800FF", "#00AAFF"][i]
                p.append(f'<path d="M0 {y} Q100 {y-30} 200 {y+10} T400 {y}" stroke="{color}" stroke-width="20" fill="none" opacity="0.15"/>')
            # Stars
            for i in range(15):
                sx = (seed * (i+1) * 7) % w
                sy = (seed * (i+1) * 13) % (h // 2)
                p.append(f'<circle cx="{sx}" cy="{sy}" r="1.5" fill="white" opacity="0.6"/>')

        elif bg == "heaven":
            # Soft clouds
            for i in range(5):
                cx = (seed * (i+1) * 41) % w
                cy = (seed * (i+1) * 29) % h
                p.append(f'<ellipse cx="{cx}" cy="{cy}" rx="50" ry="20" fill="white" opacity="0.3"/>')
            # Rays
            for i in range(6):
                angle = i * 30 - 75
                p.append(f'<line x1="{w//2}" y1="0" x2="{w//2 + int(200*math.sin(math.radians(angle)))}" y2="{int(200*math.cos(math.radians(angle)))}" stroke="#FFD700" stroke-width="3" opacity="0.1"/>')

        elif bg == "black_hole":
            # Accretion disk
            p.append(f'<ellipse cx="{w//2}" cy="{h//2}" rx="180" ry="40" fill="none" stroke="#9B59B6" stroke-width="3" opacity="0.3" transform="rotate(-20 {w//2} {h//2})"/>')
            p.append(f'<ellipse cx="{w//2}" cy="{h//2}" rx="150" ry="30" fill="none" stroke="#FF6B6B" stroke-width="2" opacity="0.2" transform="rotate(-20 {w//2} {h//2})"/>')

        elif bg == "multiverse":
            # Portals
            for i in range(3):
                px = 50 + (seed * (i+1) * 43) % (w - 100)
                py = 50 + (seed * (i+1) * 67) % (h - 100)
                p.append(f'<circle cx="{px}" cy="{py}" r="25" fill="none" stroke="white" stroke-width="2" opacity="0.2"/>')

        elif bg == "dimension_rift":
            # Cracks
            p.append(f'<path d="M{w//2} 0 L{w//2+20} {h//3} L{w//2-10} {h*2//3} L{w//2+5} {h}" stroke="white" stroke-width="3" fill="none" opacity="0.3"/>')

        return "\n".join(p)

    # ── body + mane ───────────────────────────────────────────────
    @classmethod
    def _body(cls, c: dict, pattern: str, cx: int, cy: int, seed: int) -> str:
        p = []
        mane_fill = c["mane"]
        if c.get("mane") == "#9B59B6":  # rainbow special
            mane_fill = "url(#rainbow-mane)" if True else c["mane"]

        # Mane petals
        for i in range(16):
            angle = i * 22.5
            rx, ry = 130 + (seed + i * 7) % 20, 55 + (seed + i * 11) % 15
            p.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{c["mane"]}" '
                     f'transform="rotate({angle} {cx} {cy})" opacity="0.75"/>')

        # Inner mane ring
        p.append(f'<circle cx="{cx}" cy="{cy}" r="110" fill="{c["mane2"]}" opacity="0.5"/>')

        # Ears
        for dx in [-68, 68]:
            ex, ey = cx + dx, cy - 68
            p.append(f'<circle cx="{ex}" cy="{ey}" r="22" fill="{c["main"]}"/>')
            p.append(f'<circle cx="{ex}" cy="{ey}" r="12" fill="{c["highlight"]}" opacity="0.5"/>')

        # Head
        p.append(f'<circle cx="{cx}" cy="{cy}" r="90" fill="{c["main"]}" filter="url(#shadow)"/>')

        # Cheeks
        p.append(f'<ellipse cx="{cx}" cy="{cy+30}" rx="48" ry="38" fill="{c["highlight"]}" opacity="0.5"/>')

        # Pattern overlay (clipped to head)
        p.append(cls._pattern(pattern, cx, cy, c, seed))

        return "\n".join(p)

    # ── pattern ───────────────────────────────────────────────────
    @classmethod
    def _pattern(cls, pattern: str, cx: int, cy: int, c: dict, seed: int) -> str:
        if pattern == "solid" or pattern == "none":
            return ""
        p = ['<g clip-path="url(#body-clip)" opacity="0.3">']
        dark = c["shadow"]

        if pattern == "spots":
            for i in range(12):
                sx = cx - 60 + (seed * (i+1) * 13) % 120
                sy = cy - 60 + (seed * (i+1) * 17) % 120
                sr = 5 + (seed + i) % 8
                p.append(f'<circle cx="{sx}" cy="{sy}" r="{sr}" fill="{dark}"/>')

        elif pattern == "stripes":
            for i in range(7):
                y = cy - 70 + i * 24
                p.append(f'<rect x="{cx-85}" y="{y}" width="170" height="8" rx="4" fill="{dark}"/>')

        elif pattern == "gradient":
            p.append(f'<rect x="{cx-90}" y="{cy-90}" width="180" height="180" fill="{dark}" opacity="0.5">'
                     f'<animate attributeName="opacity" values="0.1;0.4;0.1" dur="3s" repeatCount="indefinite"/></rect>')
            # Simpler: just a gradient overlay
            p[-1] = f'<ellipse cx="{cx}" cy="{cy+40}" rx="88" ry="60" fill="{dark}" opacity="0.25"/>'

        elif pattern == "swirls":
            p.append(f'<path d="M{cx-40} {cy} Q{cx-20} {cy-40} {cx} {cy} T{cx+40} {cy}" stroke="{dark}" stroke-width="4" fill="none"/>')
            p.append(f'<path d="M{cx-30} {cy+20} Q{cx} {cy-10} {cx+30} {cy+20}" stroke="{dark}" stroke-width="3" fill="none"/>')

        elif pattern == "stars":
            for i in range(8):
                sx = cx - 50 + (seed * (i+1) * 19) % 100
                sy = cy - 50 + (seed * (i+1) * 23) % 100
                p.append(cls._star_shape(sx, sy, 6, 3, dark))

        elif pattern == "hearts":
            for i in range(6):
                hx = cx - 45 + (seed * (i+1) * 31) % 90
                hy = cy - 45 + (seed * (i+1) * 37) % 90
                p.append(cls._heart_shape(hx, hy, 8, dark))

        elif pattern == "diamonds":
            for i in range(8):
                dx = cx - 50 + (seed * (i+1) * 41) % 100
                dy = cy - 50 + (seed * (i+1) * 43) % 100
                s = 8
                p.append(f'<polygon points="{dx},{dy-s} {dx+s},{dy} {dx},{dy+s} {dx-s},{dy}" fill="{dark}"/>')

        elif pattern == "fractals":
            # Triangular fractal-ish pattern
            for i in range(10):
                fx = cx - 50 + (seed * (i+1) * 47) % 100
                fy = cy - 50 + (seed * (i+1) * 53) % 100
                s = 6 + i % 5
                p.append(f'<polygon points="{fx},{fy-s} {fx+s},{fy+s} {fx-s},{fy+s}" fill="{dark}" opacity="0.6"/>')

        elif pattern == "nebula":
            for i in range(4):
                nx = cx - 40 + (seed * (i+1) * 59) % 80
                ny = cy - 40 + (seed * (i+1) * 61) % 80
                colors = ["#9B59B6", "#3498DB", "#E74C3C", "#2ECC71"]
                p.append(f'<circle cx="{nx}" cy="{ny}" r="{15+i*5}" fill="{colors[i]}" opacity="0.15"/>')

        elif pattern == "lightning":
            p.append(f'<path d="M{cx-20} {cy-60} L{cx-5} {cy-10} L{cx-15} {cy-10} L{cx+10} {cy+50}" stroke="#FFD700" stroke-width="3" fill="none"/>')

        elif pattern == "flames":
            for i in range(5):
                fx = cx - 30 + i * 15
                p.append(f'<path d="M{fx} {cy+60} Q{fx+5} {cy+20} {fx-3} {cy+10} Q{fx+8} {cy-10} {fx+2} {cy-20}" stroke="#FF4500" stroke-width="2" fill="none" opacity="0.6"/>')

        elif pattern in ("aurora", "quantum", "cosmic_dust", "void"):
            # Legendary patterns: luminous overlay
            colors_map = {
                "aurora": ["#00FF88", "#8800FF", "#00AAFF"],
                "quantum": ["#00FFFF", "#FF00FF", "#FFFF00"],
                "cosmic_dust": ["#FFD700", "#FF69B4", "#87CEEB"],
                "void": ["#2C003E", "#000000", "#1A001A"],
            }
            cols = colors_map.get(pattern, ["#888"])
            for i, col in enumerate(cols):
                ny = cy - 30 + i * 30
                p.append(f'<ellipse cx="{cx}" cy="{ny}" rx="80" ry="20" fill="{col}" opacity="0.15"/>')

        else:
            # Rosettes / patches / fallback
            for i in range(8):
                rx = cx - 50 + (seed * (i+1) * 67) % 100
                ry_pos = cy - 50 + (seed * (i+1) * 71) % 100
                r = 8 + i % 5
                p.append(f'<circle cx="{rx}" cy="{ry_pos}" r="{r}" fill="none" stroke="{dark}" stroke-width="2"/>')

        p.append('</g>')
        return "\n".join(p)

    # ── face ──────────────────────────────────────────────────────
    @classmethod
    def _face(cls, expr: str, cx: int, cy: int, colors: dict) -> str:
        p = []
        eye_y = cy - 12

        # ── Eyes ──
        if expr == "sleepy":
            # Half-closed eyes
            p.append(f'<line x1="{cx-40}" y1="{eye_y}" x2="{cx-20}" y2="{eye_y}" stroke="#000" stroke-width="3" stroke-linecap="round"/>')
            p.append(f'<line x1="{cx+20}" y1="{eye_y}" x2="{cx+40}" y2="{eye_y}" stroke="#000" stroke-width="3" stroke-linecap="round"/>')
        elif expr == "surprised":
            # Wide open circles
            for dx in [-30, 30]:
                p.append(f'<circle cx="{cx+dx}" cy="{eye_y}" r="14" fill="white" stroke="#000" stroke-width="2"/>')
                p.append(f'<circle cx="{cx+dx}" cy="{eye_y}" r="6" fill="#000"/>')
                p.append(f'<circle cx="{cx+dx+2}" cy="{eye_y-3}" r="2" fill="white"/>')
        elif expr == "winking":
            # Left eye normal, right wink
            p.append(f'<ellipse cx="{cx-30}" cy="{eye_y}" rx="11" ry="10" fill="#FFD700"/>')
            p.append(f'<circle cx="{cx-30}" cy="{eye_y}" r="4" fill="#000"/>')
            p.append(f'<path d="M{cx+20} {eye_y} Q{cx+30} {eye_y-8} {cx+40} {eye_y}" stroke="#000" stroke-width="2.5" fill="none" stroke-linecap="round"/>')
        elif expr == "angry":
            # Furrowed brows, sharp eyes
            for dx in [-30, 30]:
                p.append(f'<ellipse cx="{cx+dx}" cy="{eye_y}" rx="11" ry="8" fill="#FF4444"/>')
                p.append(f'<circle cx="{cx+dx}" cy="{eye_y}" r="4" fill="#000"/>')
            # Angry brows
            p.append(f'<line x1="{cx-42}" y1="{eye_y-14}" x2="{cx-18}" y2="{eye_y-20}" stroke="#000" stroke-width="3" stroke-linecap="round"/>')
            p.append(f'<line x1="{cx+42}" y1="{eye_y-14}" x2="{cx+18}" y2="{eye_y-20}" stroke="#000" stroke-width="3" stroke-linecap="round"/>')
        elif expr == "cool":
            # Confident half-lidded
            for dx in [-30, 30]:
                p.append(f'<ellipse cx="{cx+dx}" cy="{eye_y}" rx="12" ry="7" fill="#FFD700"/>')
                p.append(f'<ellipse cx="{cx+dx}" cy="{eye_y}" r="4" fill="#000"/>')
                p.append(f'<line x1="{cx+dx-14}" y1="{eye_y-8}" x2="{cx+dx+14}" y2="{eye_y-8}" stroke="#000" stroke-width="2"/>')
        elif expr in ("zen", "enlightened", "cosmic", "divine"):
            # Closed peaceful eyes
            for dx in [-30, 30]:
                p.append(f'<path d="M{cx+dx-12} {eye_y} Q{cx+dx} {eye_y-10} {cx+dx+12} {eye_y}" stroke="#000" stroke-width="2.5" fill="none" stroke-linecap="round"/>')
            if expr in ("enlightened", "divine"):
                # Third eye
                p.append(f'<circle cx="{cx}" cy="{eye_y-25}" r="4" fill="#FFD700" opacity="0.7"/>')
            if expr == "cosmic":
                # Starry closed eyes
                for dx in [-30, 30]:
                    p.append(f'<circle cx="{cx+dx}" cy="{eye_y+4}" r="2" fill="#FFD700" opacity="0.5"/>')
        elif expr == "laughing":
            # Squinting happy
            for dx in [-30, 30]:
                p.append(f'<path d="M{cx+dx-12} {eye_y+2} Q{cx+dx} {eye_y-10} {cx+dx+12} {eye_y+2}" stroke="#000" stroke-width="2.5" fill="none" stroke-linecap="round"/>')
        elif expr == "legendary":
            # Glowing eyes
            for dx in [-30, 30]:
                p.append(f'<circle cx="{cx+dx}" cy="{eye_y}" r="12" fill="#FFD700" opacity="0.4"/>')
                p.append(f'<circle cx="{cx+dx}" cy="{eye_y}" r="8" fill="#FFF"/>')
                p.append(f'<circle cx="{cx+dx}" cy="{eye_y}" r="4" fill="#FFD700"/>')
        else:
            # Default / happy / neutral / curious / excited / mischievous / wise / fierce
            eye_color = "#FFD700"
            pupil_r = 4
            if expr == "fierce":
                eye_color = "#FF6600"
                pupil_r = 3
            elif expr == "excited":
                pupil_r = 5
            elif expr == "mischievous":
                eye_color = "#88DD44"

            for dx in [-30, 30]:
                p.append(f'<ellipse cx="{cx+dx}" cy="{eye_y}" rx="12" ry="10" fill="{eye_color}"/>')
                p.append(f'<circle cx="{cx+dx}" cy="{eye_y}" r="{pupil_r}" fill="#000"/>')
                p.append(f'<circle cx="{cx+dx+2}" cy="{eye_y-2}" r="2" fill="white" opacity="0.7"/>')

            if expr == "wise":
                # Small spectacle-like lines
                p.append(f'<circle cx="{cx-30}" cy="{eye_y}" r="14" fill="none" stroke="#000" stroke-width="1" opacity="0.3"/>')
                p.append(f'<circle cx="{cx+30}" cy="{eye_y}" r="14" fill="none" stroke="#000" stroke-width="1" opacity="0.3"/>')

        # ── Nose ──
        nose_y = cy + 20
        p.append(f'<path d="M{cx-12} {nose_y} Q{cx} {nose_y-8} {cx+12} {nose_y} L{cx} {nose_y+12} Z" fill="#3E2723"/>')

        # ── Mouth / expression ──
        mouth_y = nose_y + 18
        if expr == "happy" or expr == "excited":
            # Big smile
            p.append(f'<path d="M{cx-22} {mouth_y} Q{cx} {mouth_y+18} {cx+22} {mouth_y}" stroke="#3E2723" stroke-width="2.5" fill="none" stroke-linecap="round"/>')
        elif expr == "angry" or expr == "fierce":
            # Frown / snarl
            p.append(f'<path d="M{cx-22} {mouth_y+8} Q{cx} {mouth_y-8} {cx+22} {mouth_y+8}" stroke="#3E2723" stroke-width="2.5" fill="none" stroke-linecap="round"/>')
            if expr == "fierce":
                # Fangs
                p.append(f'<polygon points="{cx-12},{mouth_y} {cx-9},{mouth_y+10} {cx-6},{mouth_y}" fill="white" stroke="#3E2723" stroke-width="0.5"/>')
                p.append(f'<polygon points="{cx+6},{mouth_y} {cx+9},{mouth_y+10} {cx+12},{mouth_y}" fill="white" stroke="#3E2723" stroke-width="0.5"/>')
        elif expr == "surprised":
            # O mouth
            p.append(f'<ellipse cx="{cx}" cy="{mouth_y+5}" rx="10" ry="12" fill="#3E2723"/>')
        elif expr == "sleepy":
            # Small open mouth (yawn-ish)
            p.append(f'<ellipse cx="{cx}" cy="{mouth_y+2}" rx="8" ry="6" fill="#3E2723" opacity="0.6"/>')
        elif expr == "laughing":
            # Big open smile
            p.append(f'<path d="M{cx-25} {mouth_y-2} Q{cx} {mouth_y+25} {cx+25} {mouth_y-2}" stroke="#3E2723" stroke-width="2" fill="#3E2723" opacity="0.5"/>')
        elif expr == "mischievous":
            # Smirk
            p.append(f'<path d="M{cx-15} {mouth_y+2} Q{cx+5} {mouth_y+10} {cx+22} {mouth_y-4}" stroke="#3E2723" stroke-width="2.5" fill="none" stroke-linecap="round"/>')
        elif expr == "cool":
            # Slight confident smirk
            p.append(f'<path d="M{cx-18} {mouth_y+2} Q{cx} {mouth_y+10} {cx+18} {mouth_y}" stroke="#3E2723" stroke-width="2" fill="none" stroke-linecap="round"/>')
        elif expr in ("zen", "enlightened", "cosmic", "divine", "legendary"):
            # Serene slight smile
            p.append(f'<path d="M{cx-15} {mouth_y} Q{cx} {mouth_y+8} {cx+15} {mouth_y}" stroke="#3E2723" stroke-width="2" fill="none" stroke-linecap="round"/>')
        elif expr == "winking":
            # Cheeky smile
            p.append(f'<path d="M{cx-20} {mouth_y} Q{cx} {mouth_y+14} {cx+20} {mouth_y}" stroke="#3E2723" stroke-width="2.5" fill="none" stroke-linecap="round"/>')
            # Tongue
            p.append(f'<ellipse cx="{cx+5}" cy="{mouth_y+8}" rx="5" ry="4" fill="#E88090"/>')
        else:
            # Neutral
            p.append(f'<line x1="{cx-15}" y1="{mouth_y}" x2="{cx+15}" y2="{mouth_y}" stroke="#3E2723" stroke-width="2" stroke-linecap="round"/>')

        # Whiskers (always)
        for side in [-1, 1]:
            for wy in [-5, 5]:
                wx1 = cx + side * 30
                wx2 = cx + side * 70
                p.append(f'<line x1="{wx1}" y1="{nose_y + wy}" x2="{wx2}" y2="{nose_y + wy + side*3}" stroke="#3E2723" stroke-width="1" opacity="0.3"/>')

        return "\n".join(p)

    # ── accessory ─────────────────────────────────────────────────
    @classmethod
    def _accessory(cls, acc: str, cx: int, cy: int, colors: dict) -> str:
        if acc == "none":
            return ""
        p = []

        if acc == "crown" or acc == "golden_crown":
            color = "#FFD700" if acc == "crown" else "#FFC800"
            stroke = "#B8860B" if acc == "crown" else "#DAA520"
            y = cy - 95
            p.append(f'<polygon points="{cx-30},{y+20} {cx-30},{y} {cx-18},{y+12} {cx-6},{y-5} {cx},{y+8} {cx+6},{y-5} {cx+18},{y+12} {cx+30},{y} {cx+30},{y+20}" fill="{color}" stroke="{stroke}" stroke-width="1.5"/>')
            if acc == "golden_crown":
                # Jewels
                for jx in [-15, 0, 15]:
                    p.append(f'<circle cx="{cx+jx}" cy="{y+8}" r="3" fill="#FF0040"/>')

        elif acc == "sunglasses":
            y = cy - 14
            p.append(f'<rect x="{cx-46}" y="{y-10}" width="28" height="18" rx="4" fill="#111" opacity="0.85"/>')
            p.append(f'<rect x="{cx+18}" y="{y-10}" width="28" height="18" rx="4" fill="#111" opacity="0.85"/>')
            p.append(f'<line x1="{cx-18}" y1="{y}" x2="{cx+18}" y2="{y}" stroke="#333" stroke-width="2"/>')
            p.append(f'<line x1="{cx-46}" y1="{y-4}" x2="{cx-60}" y2="{y-10}" stroke="#333" stroke-width="2"/>')
            p.append(f'<line x1="{cx+46}" y1="{y-4}" x2="{cx+60}" y2="{y-10}" stroke="#333" stroke-width="2"/>')

        elif acc == "monocle":
            y = cy - 12
            p.append(f'<circle cx="{cx+30}" cy="{y}" r="16" fill="none" stroke="#B8860B" stroke-width="2"/>')
            p.append(f'<line x1="{cx+30}" y1="{y+16}" x2="{cx+25}" y2="{cy+60}" stroke="#B8860B" stroke-width="1"/>')
            # Glass shine
            p.append(f'<path d="M{cx+24} {y-8} Q{cx+28} {y-12} {cx+34} {y-8}" stroke="white" stroke-width="1" fill="none" opacity="0.5"/>')

        elif acc == "bow":
            y = cy - 85
            p.append(f'<path d="M{cx+35} {y} Q{cx+55} {y-15} {cx+55} {y+15} Z" fill="#FF69B4"/>')
            p.append(f'<path d="M{cx+35} {y} Q{cx+15} {y-15} {cx+15} {y+15} Z" fill="#FF69B4"/>')
            p.append(f'<circle cx="{cx+35}" cy="{y}" r="4" fill="#FF1493"/>')

        elif acc == "simple_hat":
            y = cy - 95
            p.append(f'<ellipse cx="{cx}" cy="{y+20}" rx="55" ry="10" fill="#8B4513"/>')
            p.append(f'<rect x="{cx-30}" y="{y-10}" width="60" height="30" rx="5" fill="#A0522D"/>')

        elif acc == "bandana":
            y = cy - 80
            p.append(f'<path d="M{cx-60} {y} Q{cx} {y+15} {cx+60} {y}" stroke="#D32F2F" stroke-width="8" fill="none"/>')
            p.append(f'<path d="M{cx+50} {y+2} L{cx+65} {y+20} L{cx+55} {y+22}" fill="#D32F2F"/>')

        elif acc == "headphones":
            y = cy - 20
            p.append(f'<path d="M{cx-65} {y} Q{cx-65} {cy-85} {cx} {cy-90} Q{cx+65} {cy-85} {cx+65} {y}" stroke="#333" stroke-width="5" fill="none"/>')
            p.append(f'<ellipse cx="{cx-68}" cy="{y+5}" rx="12" ry="16" fill="#444"/>')
            p.append(f'<ellipse cx="{cx+68}" cy="{y+5}" rx="12" ry="16" fill="#444"/>')

        elif acc == "scarf":
            y = cy + 70
            p.append(f'<path d="M{cx-50} {y} Q{cx} {y+15} {cx+50} {y}" stroke="#E74C3C" stroke-width="12" fill="none" stroke-linecap="round"/>')
            p.append(f'<path d="M{cx+40} {y+5} L{cx+35} {y+35} L{cx+50} {y+30}" fill="#C0392B"/>')

        elif acc == "earring":
            p.append(f'<circle cx="{cx+72}" cy="{cy-55}" r="5" fill="#FFD700" stroke="#B8860B" stroke-width="1"/>')
            p.append(f'<circle cx="{cx+72}" cy="{cy-45}" r="3" fill="#FFD700"/>')

        elif acc == "laser_eyes":
            y = cy - 12
            p.append(f'<line x1="{cx-30}" y1="{y}" x2="{cx-120}" y2="{y+40}" stroke="#FF0000" stroke-width="3" opacity="0.7"/>')
            p.append(f'<line x1="{cx+30}" y1="{y}" x2="{cx+120}" y2="{y+40}" stroke="#FF0000" stroke-width="3" opacity="0.7"/>')
            p.append(f'<circle cx="{cx-30}" cy="{y}" r="6" fill="#FF0000" opacity="0.5"/>')
            p.append(f'<circle cx="{cx+30}" cy="{y}" r="6" fill="#FF0000" opacity="0.5"/>')

        elif acc == "halo":
            y = cy - 105
            p.append(f'<ellipse cx="{cx}" cy="{y}" rx="45" ry="12" fill="none" stroke="#FFD700" stroke-width="3" opacity="0.8"/>')
            p.append(f'<ellipse cx="{cx}" cy="{y}" rx="45" ry="12" fill="#FFD700" opacity="0.1"/>')

        elif acc == "horns":
            for side in [-1, 1]:
                hx = cx + side * 55
                p.append(f'<path d="M{hx} {cy-75} Q{hx+side*25} {cy-120} {hx+side*15} {cy-130}" stroke="#4A2800" stroke-width="8" fill="none" stroke-linecap="round"/>')

        elif acc == "wizard_hat":
            y = cy - 90
            p.append(f'<polygon points="{cx},{y-80} {cx-45},{y+10} {cx+45},{y+10}" fill="#2C3E80"/>')
            p.append(f'<ellipse cx="{cx}" cy="{y+10}" rx="55" ry="10" fill="#1A2550"/>')
            # Stars on hat
            p.append(cls._star_shape(cx - 10, y - 30, 5, 2.5, "#FFD700"))
            p.append(cls._star_shape(cx + 15, y - 50, 4, 2, "#FFD700"))

        elif acc == "diamond_chain":
            y = cy + 65
            for i in range(7):
                dx = cx - 42 + i * 14
                s = 5
                p.append(f'<polygon points="{dx},{y-s} {dx+s},{y} {dx},{y+s} {dx-s},{y}" fill="#87CEEB" stroke="#4A90D9" stroke-width="0.5"/>')
            p.append(f'<line x1="{cx-48}" y1="{y}" x2="{cx+48}" y2="{y}" stroke="#B8B8B8" stroke-width="1.5"/>')

        elif acc == "jetpack":
            for side in [-1, 1]:
                jx = cx + side * 85
                p.append(f'<rect x="{jx-8}" y="{cy-20}" width="16" height="40" rx="4" fill="#666"/>')
                p.append(f'<rect x="{jx-5}" y="{cy+20}" width="10" height="8" rx="2" fill="#FF4500"/>')
                p.append(f'<path d="M{jx-4} {cy+28} L{jx} {cy+50} L{jx+4} {cy+28}" fill="#FF6B00" opacity="0.6"/>')

        elif acc == "wings":
            for side in [-1, 1]:
                wx = cx + side * 80
                p.append(f'<path d="M{cx+side*60} {cy-10} Q{wx+side*40} {cy-60} {wx+side*30} {cy-80} Q{wx+side*20} {cy-40} {cx+side*60} {cy+20}" fill="white" stroke="#D0D0D0" stroke-width="1" opacity="0.7"/>')

        return "\n".join(p)

    # ── special effects ───────────────────────────────────────────
    @classmethod
    def _special(cls, special: str, w: int, h: int, seed: int) -> str:
        if special == "none":
            return ""
        p = []
        cx, cy = w // 2, h // 2

        if special == "sparkles":
            for i in range(10):
                sx = (seed * (i+1) * 19) % w
                sy = (seed * (i+1) * 23) % h
                size = 4 + i % 5
                p.append(cls._star_shape(sx, sy, size, size * 0.4, "#FFD700"))

        elif special == "glow":
            p.append(f'<circle cx="{cx}" cy="{cy}" r="100" fill="{cls.BODY_COLORS.get("golden", cls.BODY_COLORS["brown"])["highlight"]}" opacity="0.15" filter="url(#glow)"/>')

        elif special == "shadow":
            p.append(f'<ellipse cx="{cx}" cy="{cy+100}" rx="90" ry="20" fill="#000" opacity="0.2"/>')

        elif special == "aura":
            colors = ["#FF6B6B", "#FFD93D", "#6BCB77"]
            for i, c in enumerate(colors):
                r = 130 + i * 15
                p.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{c}" stroke-width="2" opacity="0.2"/>')

        elif special == "particles":
            for i in range(15):
                px = (seed * (i+1) * 29) % w
                py = (seed * (i+1) * 31) % h
                p.append(f'<circle cx="{px}" cy="{py}" r="{2+i%3}" fill="#88CCFF" opacity="0.4"/>')

        elif special == "energy":
            for i in range(6):
                angle = i * 60
                x2 = cx + int(140 * math.cos(math.radians(angle)))
                y2 = cy + int(140 * math.sin(math.radians(angle)))
                mx = cx + int(80 * math.cos(math.radians(angle + 15)))
                my = cy + int(80 * math.sin(math.radians(angle + 15)))
                p.append(f'<path d="M{cx} {cy} Q{mx} {my} {x2} {y2}" stroke="#00FFFF" stroke-width="1.5" fill="none" opacity="0.3"/>')

        elif special in ("transcendent", "godlike", "mythical"):
            # Intense multi-layer glow
            glow_colors = {
                "transcendent": "#FFFFFF",
                "godlike": "#FFD700",
                "mythical": "#9B59B6",
            }
            gc = glow_colors[special]
            p.append(f'<circle cx="{cx}" cy="{cy}" r="140" fill="{gc}" opacity="0.06"/>')
            p.append(f'<circle cx="{cx}" cy="{cy}" r="120" fill="{gc}" opacity="0.08"/>')
            p.append(f'<circle cx="{cx}" cy="{cy}" r="100" fill="{gc}" opacity="0.06"/>')
            # Sparkle ring
            for i in range(12):
                angle = i * 30
                sx = cx + int(135 * math.cos(math.radians(angle)))
                sy = cy + int(135 * math.sin(math.radians(angle)))
                p.append(cls._star_shape(sx, sy, 5, 2, gc))

        return "\n".join(p)

    # ── helpers ───────────────────────────────────────────────────
    @staticmethod
    def _star_shape(cx: int, cy: int, outer: float, inner: float, color: str) -> str:
        pts = []
        for i in range(10):
            angle = math.radians(i * 36 - 90)
            r = outer if i % 2 == 0 else inner
            pts.append(f"{cx + r * math.cos(angle):.1f},{cy + r * math.sin(angle):.1f}")
        return f'<polygon points="{" ".join(pts)}" fill="{color}"/>'

    @staticmethod
    def _heart_shape(cx: int, cy: int, size: float, color: str) -> str:
        s = size
        return (f'<path d="M{cx} {cy+s*0.6} '
                f'Q{cx-s} {cy-s*0.2} {cx-s*0.5} {cy-s*0.6} '
                f'Q{cx} {cy-s} {cx} {cy-s*0.2} '
                f'Q{cx} {cy-s} {cx+s*0.5} {cy-s*0.6} '
                f'Q{cx+s} {cy-s*0.2} {cx} {cy+s*0.6} Z" fill="{color}"/>')


def main():
    pass

if __name__ == "__main__":
    main()
