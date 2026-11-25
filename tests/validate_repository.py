"""Validate packaging without network access or a running HA instance."""

import ast
import json
from pathlib import Path
import struct

root = Path(__file__).resolve().parents[1]
integration = root / "custom_components" / "lea_noe"
manifest = json.loads((integration / "manifest.json").read_text(encoding="utf-8"))
hacs = json.loads((root / "hacs.json").read_text(encoding="utf-8"))
assert [p.name for p in (root / "custom_components").iterdir() if p.is_dir() and p.name != "__pycache__"] == ["lea_noe"]
for key in ("domain", "documentation", "issue_tracker", "codeowners", "name", "version"):
    assert manifest.get(key), f"Missing required HACS manifest field: {key}"
assert manifest["domain"] == integration.name
assert hacs["homeassistant"] == "2026.11.0"
assert hacs.get("content_in_root") is False
for path in root.rglob("*.json"):
    json.loads(path.read_text(encoding="utf-8"))
for path in integration.glob("*.py"):
    ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
icon = (integration / "brand" / "icon.png").read_bytes()
assert icon[:8] == b"\x89PNG\r\n\x1a\n"
width,height=struct.unpack(">II", icon[16:24])
assert width == height and width >= 256
assert (integration / "frontend" / "lea-logo.svg").is_file()
assert (integration / "frontend" / "lea-card.js").is_file()
print("JSON, Python syntax, HACS manifest, integration layout and PNG icon: OK")

