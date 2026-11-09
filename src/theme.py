"""
Design tokens : palettes, typographie, espacements.
Tout le pack est piloté par ces tokens (style "Infografity" : fond profond,
accents néon, cartes arrondies, micro-dégradés, grille généreuse).
"""

FONT_TITLE = "Poppins"
FONT_BODY = "Poppins"

# ---------------------------------------------------------------- palettes
# Chaque palette : fond principal, fond secondaire (cartes), accents x3,
# couleur de texte principale, texte secondaire.
PALETTES = {
    "midnight": {
        "label": "Midnight Violet",
        "bg": "#0C0A1D",
        "bg2": "#141130",
        "card": "#1B1740",
        "accent": "#7C5CFF",
        "accent2": "#22D3EE",
        "accent3": "#FF5C93",
        "text": "#FFFFFF",
        "muted": "#A9A5C9",
        "line": "#2C2760",
        "glow": "#7C5CFF",
    },
    "aurora": {
        "label": "Aurora Teal",
        "bg": "#05161A",
        "bg2": "#07242B",
        "card": "#0B3038",
        "accent": "#2DD4BF",
        "accent2": "#7DD3FC",
        "accent3": "#FDE68A",
        "text": "#F2FFFE",
        "muted": "#8FB6BB",
        "line": "#12454F",
        "glow": "#2DD4BF",
    },
    "sunset": {
        "label": "Sunset Coral",
        "bg": "#1A0B12",
        "bg2": "#2A121C",
        "card": "#361725",
        "accent": "#FF7A59",
        "accent2": "#FFC46B",
        "accent3": "#8B7CFF",
        "text": "#FFF5F0",
        "muted": "#C9A2A6",
        "line": "#4A2033",
        "glow": "#FF7A59",
    },
    "graphite": {
        "label": "Graphite Lime",
        "bg": "#101214",
        "bg2": "#171B1F",
        "card": "#1F252A",
        "accent": "#B6F25B",
        "accent2": "#5BD1F2",
        "accent3": "#FF8A5B",
        "text": "#F5F7F8",
        "muted": "#98A2A8",
        "line": "#2C343A",
        "glow": "#B6F25B",
    },
    "royal": {
        "label": "Royal Blue",
        "bg": "#060D26",
        "bg2": "#0A1638",
        "card": "#101F4D",
        "accent": "#4C8DFF",
        "accent2": "#4CE0B3",
        "accent3": "#FFD166",
        "text": "#FFFFFF",
        "muted": "#93A3C9",
        "line": "#1B2E63",
        "glow": "#4C8DFF",
    },
    "blush": {
        "label": "Blush Neomorphic",
        "bg": "#F4EFF7",
        "bg2": "#EDE6F2",
        "card": "#FBF8FD",
        "accent": "#8B5CF6",
        "accent2": "#EC4899",
        "accent3": "#0EA5E9",
        "text": "#231934",
        "muted": "#6F6483",
        "line": "#DED3E8",
        "glow": "#8B5CF6",
    },
    "light": {
        "label": "Clean Light",
        "bg": "#FFFFFF",
        "bg2": "#F5F7FB",
        "card": "#FFFFFF",
        "accent": "#2563EB",
        "accent2": "#0EA5E9",
        "accent3": "#F97316",
        "text": "#0F172A",
        "muted": "#64748B",
        "line": "#E2E8F0",
        "glow": "#2563EB",
    },
    "medical": {
        "label": "Medical Mint",
        "bg": "#F3FBF9",
        "bg2": "#E7F6F2",
        "card": "#FFFFFF",
        "accent": "#0FA37F",
        "accent2": "#22B8CF",
        "accent3": "#F59F00",
        "text": "#0B2B26",
        "muted": "#5C7C77",
        "line": "#D3E9E4",
        "glow": "#0FA37F",
    },
    "finance": {
        "label": "Finance Navy",
        "bg": "#08121F",
        "bg2": "#0D1C2E",
        "card": "#12263D",
        "accent": "#E9B949",
        "accent2": "#4ECDC4",
        "accent3": "#FF6B6B",
        "text": "#F4F7FA",
        "muted": "#8AA0B8",
        "line": "#1B3450",
        "glow": "#E9B949",
    },
    "sport": {
        "label": "Sport Energy",
        "bg": "#12100C",
        "bg2": "#1C1811",
        "card": "#26211A",
        "accent": "#FFD400",
        "accent2": "#FF4D4D",
        "accent3": "#38E1A6",
        "text": "#FFFDF7",
        "muted": "#B4A992",
        "line": "#332C22",
        "glow": "#FFD400",
    },
    "tech": {
        "label": "Tech Grid",
        "bg": "#070B14",
        "bg2": "#0C1322",
        "card": "#121B2E",
        "accent": "#00E5A0",
        "accent2": "#5B8DFF",
        "accent3": "#FF6BD6",
        "text": "#F0F6FF",
        "muted": "#8494AE",
        "line": "#1A2740",
        "glow": "#00E5A0",
    },
    "creative": {
        "label": "Creative Pop",
        "bg": "#150E2E",
        "bg2": "#1F1445",
        "card": "#2B1D5C",
        "accent": "#FF4D8D",
        "accent2": "#FFD166",
        "accent3": "#4CC9F0",
        "text": "#FFFFFF",
        "muted": "#B7A9E0",
        "line": "#372672",
        "glow": "#FF4D8D",
    },
    "isometric": {
        "label": "Isometric Sky",
        "bg": "#0B2545",
        "bg2": "#12335C",
        "card": "#1A4275",
        "accent": "#62D0FF",
        "accent2": "#FFB84C",
        "accent3": "#FF6F91",
        "text": "#F2F9FF",
        "muted": "#9DBBDA",
        "line": "#1F4C86",
        "glow": "#62D0FF",
    },
    "earth": {
        "label": "Earth Maps",
        "bg": "#0A1F16",
        "bg2": "#102C20",
        "card": "#163B2C",
        "accent": "#7BE495",
        "accent2": "#FFD97D",
        "accent3": "#6FC3FF",
        "text": "#F3FFF8",
        "muted": "#97B8A6",
        "line": "#1E4A38",
        "glow": "#7BE495",
    },
}

DEFAULT_PALETTE = "midnight"

# ---------------------------------------------------------------- grille
SLIDE_W_IN = 13.333333
SLIDE_H_IN = 7.5
PX_PER_IN = 144.0          # resolution de rendu du fond
W = int(SLIDE_W_IN * PX_PER_IN)   # 1920
H = int(SLIDE_H_IN * PX_PER_IN)   # 1080

MARGIN = 96
CONTENT_W = W - 2 * MARGIN

# Tailles de police en PX de la grille 1920x1080 (2 px = 1 pt PowerPoint).
# ex. 72 px -> 36 pt
T_HERO = 116
T_TITLE = 68
T_SUB = 34
T_KICKER = 23
T_BODY = 28
T_SMALL = 23
T_STAT = 120
T_LEAD = 30
T_CARD = 26
