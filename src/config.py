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
FONT_PATH = BASE_DIR / "assets" / "fonts" / "Gaegu-Regular.ttf"
SUN_ICON_PATH = BASE_DIR / "assets" / "brand" / "sun.svg"

POSTS_PER_CHAPTER = 30
CARD_WIDTH = 1080
CARD_HEIGHT = 1350

PALETTES = [
    {"name": "Obsidian Chrome", "canvas": "#121316", "ink": "#D8DCE0"},
    {"name": "Forest Tablet", "canvas": "#0D382A", "ink": "#A3E5C2"},
    {"name": "Terracotta Sunset", "canvas": "#1F1412", "ink": "#FAD4C0"},
    {"name": "Colonial Cobalt", "canvas": "#0D1B2A", "ink": "#F4EBD9"},
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
