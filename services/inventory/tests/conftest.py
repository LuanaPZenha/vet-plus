import os
import sys
from pathlib import Path

import django

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
_shared_dir = BASE_DIR / "shared"
if not _shared_dir.exists():
    _shared_dir = BASE_DIR.parent.parent / "shared"
sys.path.insert(0, str(_shared_dir))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()
