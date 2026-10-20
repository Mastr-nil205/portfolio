"""Read-only public content repository, independent of Flask and Jinja."""

import json
import re
from pathlib import Path
from urllib.parse import urlsplit

SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def https_url(value):
    parsed = urlsplit(value)
    return parsed.scheme == "https" and bool(parsed.netloc) and not parsed.username


class PortfolioRepository:
    def __init__(self, directory):
        self.directory = Path(directory)
        self.profile = self._read("profile.json")
        self.experience = self._read("experience.json")
        self.skills = self._read("skills.json")
        self._projects = self._read("projects.json")
        self._validate()

    def _read(self, filename):
        return json.loads((self.directory / filename).read_text(encoding="utf-8"))

    def _validate(self):
        for name in ("github", "linkedin"):
            if not https_url(self.profile[name]):
                raise ValueError(f"Invalid public {name} URL")
        seen = set()
        for project in self._projects:
            if not SLUG.fullmatch(project["slug"]) or project["slug"] in seen:
                raise ValueError("Project slugs must be unique URL-safe identifiers")
            seen.add(project["slug"])
            for key in ("title", "summary", "category", "status", "contribution"):
                if not isinstance(project.get(key), str) or not project[key].strip():
                    raise ValueError(f"Missing project field: {key}")
            if not https_url(project["repository_url"]):
                raise ValueError("Projects require an HTTPS evidence link")
            if not isinstance(project.get("public"), bool):
                raise ValueError("Project publication flag must be explicit")
        for item in self.experience:
            for key in ("employer", "title", "period", "source_kind"):
                if not item.get(key):
                    raise ValueError(f"Missing experience field: {key}")
            if item.get("source_path") != "/resume/download/" and not https_url(item.get("source_url", "")):
                raise ValueError("Experience requires a public resume or HTTPS source")

    def projects(self, query="", category=""):
        results = [item for item in self._projects if item["public"]]
        if category:
            results = [item for item in results if item["category"] == category]
        if query:
            needle = query.casefold()
            results = [
                item for item in results
                if needle in " ".join(
                    [item["title"], item["summary"], item["category"], *item["technologies"]]
                ).casefold()
            ]
        return results

    def categories(self):
        return sorted({item["category"] for item in self.projects()})

    def project(self, slug):
        return next((item for item in self.projects() if item["slug"] == slug), None)
