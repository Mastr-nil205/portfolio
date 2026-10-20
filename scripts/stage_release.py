"""Create a new, allowlisted local release directory; never upload or deploy."""

import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = ("app.py", "portfolio_data.py", "requirements.txt", "pyproject.toml",
         ".python-version", "vercel.json", ".vercelignore")
DIRECTORIES = ("templates", "data", "public")


def stage(root=ROOT):
    projects = json.loads((root / "data/projects.json").read_text(encoding="utf-8"))
    if any(not project.get("public") for project in projects):
        raise ValueError("Unpublished project data must not enter a deployment artifact")
    profile = json.loads((root / "data/profile.json").read_text(encoding="utf-8"))
    if (root / "public/resume.pdf").exists() and not profile.get("resume_approved"):
        raise ValueError("Remove unapproved resume from public assets before staging")
    output = root / ".release" / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    output.mkdir(parents=True, exist_ok=False)
    for name in FILES:
        shutil.copy2(root / name, output / name)
    for name in DIRECTORIES:
        shutil.copytree(root / name, output / name)
    manifest = {
        str(path.relative_to(output)).replace("\\", "/"): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(output.rglob("*")) if path.is_file()
    }
    # Keep the review manifest beside the upload directory, outside its contents.
    output.with_suffix(".manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return output


if __name__ == "__main__":
    print(stage())
