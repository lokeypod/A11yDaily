from pathlib import Path

APP_DIR = Path(__file__).resolve().parent
API_ROOT = APP_DIR.parent.parent
CONFIG_DIR = API_ROOT / "config"

CONTENT_SOURCES_PATH = CONFIG_DIR / "content_sources.yaml"
