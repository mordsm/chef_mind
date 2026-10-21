"""Chef Core: standalone knowledge and decision service."""

# The standalone engine is a sibling of backend, also used without the web app.
import sys
from pathlib import Path

project_root = str(Path(__file__).resolve().parents[2])
if project_root not in sys.path:
    sys.path.append(project_root)
