import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

CANON_PATH = BASE_DIR / "database" / "canon.json"
TEMPLATE_PATH = BASE_DIR / "templates" / "card_template.html"
RENDERED_DIR = BASE_DIR / "assets" / "rendered"
DOODLES_DIR = BASE_DIR / "assets" / "doodles"
MANIFEST_PATH = DOODLES_DIR / "manifest.json"
SUN_ICON_PATH = BASE_DIR / "assets" / "brand" / "sun.svg"

POSTS_PER_CHAPTER = 30
CARD_WIDTH = 1080
CARD_HEIGHT = 1350

# Three-stop gradients, picked at random per post (not rotated) -- see
# GRADIENT_ANGLE below for the fixed direction they're all rendered at.
PALETTES = [
    {"name": "Obsidian Chrome", "stops": ["#0B0B0D", "#3B4652", "#D8DCE0"], "ink": "#F4F5F6"},
    {"name": "Terracotta Sunset", "stops": ["#2E1A14", "#C96A4B", "#FAD4C0"], "ink": "#FBEAE0"},
    {"name": "Amethyst Geode", "stops": ["#1A1030", "#6C4AB6", "#D8CCF0"], "ink": "#F3EEFC"},
    {"name": "Violet Tempest", "stops": ["#0D1B3E", "#4B2E83", "#6FE7DD"], "ink": "#F2FFFC"},
    {"name": "Vintage Hearth", "stops": ["#3A0F1B", "#8C8680", "#F1E7DA"], "ink": "#FBF5EC"},
    {"name": "Colonial Cobalt", "stops": ["#1B3F8B", "#C9A67A", "#F4EBD9"], "ink": "#FCF8F1"},
]
GRADIENT_ANGLE = 0

# Rendered via a live Google Fonts CDN link (generation already needs internet
# for the Gemini call, so this isn't an extra offline dependency) -- picked at
# random per post. Only fonts confirmed free for commercial use belong here.
FONTS = [
    {"name": "Nunito", "family": "'Nunito', sans-serif", "google_param": "Nunito:wght@400;700"},
    {"name": "Poppins", "family": "'Poppins', sans-serif", "google_param": "Poppins:wght@400;700"},
]

CAPTION_TEMPLATE = (
    "nim. {chapter}.{verse}\n"
    ".\n"
    ".\n"
    "#nim #stoic #primalwisdom #cavemanmindset #mindfulness #innerpeace"
)

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
# Verify this against the currently available models for your google-genai
# SDK version before relying on it — model names/availability shift over time.
GEMINI_MODEL = "gemini-2.5-flash"
