import json
import shutil
from pathlib import Path
from urllib.parse import urlsplit

import html5lib
import pytest
from bs4 import BeautifulSoup
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.test import Client
from werkzeug.wrappers import Response

from app import ROOT, create_app
from scripts.stage_release import stage

PAGES = ("/", "/about/", "/experience/", "/projects/",
         "/projects/personal-portfolio/", "/resume/", "/contact/")


@pytest.fixture
def app():
    return create_app({"TESTING": True, "LOCAL_ASSETS": True})


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.mark.parametrize("path", PAGES)
def test_pages_html_and_local_links(client, path):
    response = client.get(path)
    assert response.status_code == 200
    html5lib.HTMLParser(strict=True).parse(response.text)
    soup = BeautifulSoup(response.text, "html.parser")
    assert len(soup.select("h1")) == 1
    assert soup.html["lang"] == "en"
    assert soup.select_one("main#main")
    ids = [element["id"] for element in soup.select("[id]")]
    assert len(ids) == len(set(ids))
    for element in soup.select("a[href], link[href], script[src]"):
        url = element.get("href", element.get("src"))
        if url.startswith("#"):
            assert soup.find(id=url[1:])
        elif url.startswith("/"):
            assert client.get(url).status_code == 200, url
    for element in soup.select("input:not([type=hidden]), select"):
        assert soup.find("label", attrs={"for": element["id"]})
    assert "noindex" in response.headers["X-Robots-Tag"]
    assert "script-src 'self'" in response.headers["Content-Security-Policy"]


def test_search_filter_and_escape(client):
    assert "personal-portfolio" in client.get("/projects/?q=FLASK").text
    assert "personal-portfolio" in client.get("/projects/?category=Web%20development").text
    assert "personal-portfolio" not in client.get("/projects/?q=unfindable").text
    response = client.get("/projects/", query_string={"q": '<script>alert("x")</script>'})
    assert response.status_code == 200
    assert '<script>alert("x")</script>' not in response.text
    assert "&lt;script&gt;" in response.text


@pytest.mark.parametrize("query", [
    {"q": "x" * 101}, {"category": "invalid"}, {"q": "a\x00b"},
    {"unexpected": "yes"}, [("q", "a"), ("q", "b")],
])
def test_invalid_queries(client, query):
    assert client.get("/projects/", query_string=query).status_code == 400


@pytest.mark.parametrize("path", [
    "/missing/", "/projects/missing/", "/resume.pdf",
    "/data/profile.json", "/docs/portfolio-brief.md", "/app.py",
    "/css/../../app.py", "/ventures/",
])
def test_missing_and_private_paths(client, path):
    assert client.get(path).status_code == 404


def test_prefix(app):
    mounted = Client(DispatcherMiddleware(Response(status=404), {"/portfolio": app}), Response)
    for path in PAGES:
        response = mounted.get("/portfolio" + path)
        assert response.status_code == 200
        soup = BeautifulSoup(response.text, "html.parser")
        for element in soup.select("a[href], link[href], script[src]"):
            url = element.get("href", element.get("src"))
            if url.startswith("/"):
                assert url.startswith("/portfolio/")
                assert mounted.get(url).status_code == 200


def test_production_metadata():
    client = create_app({"TESTING": True, "SITE_URL": "https://example.vercel.app",
                         "DEPLOYMENT_ENV": "production"}).test_client()
    response = client.get("/", headers={"Host": "untrusted.example"})
    assert 'rel="canonical" href="https://example.vercel.app/"' in response.text
    assert "untrusted.example" not in response.text
    assert "X-Robots-Tag" not in response.headers
    assert "noindex" in client.get("/projects/?q=Flask").headers["X-Robots-Tag"]
    assert "Allow: /" in client.get("/robots.txt").text


def test_content_and_resume_boundaries(tmp_path):
    data = tmp_path / "data"
    public = tmp_path / "public"
    shutil.copytree(ROOT / "data", data)
    public.mkdir()
    projects = json.loads((data / "projects.json").read_text())
    draft = dict(projects[0], slug="unpublished-example", public=False, title="Unpublished example")
    (data / "projects.json").write_text(json.dumps([*projects, draft]))
    profile = json.loads((data / "profile.json").read_text())
    profile["resume_approved"] = False
    (data / "profile.json").write_text(json.dumps(profile))
    (public / "resume.pdf").write_bytes(b"%PDF-1.4\nTest fixture only")
    config = {"TESTING": True, "DATA_DIR": data, "PUBLIC_DIR": public}
    client = create_app(config).test_client()
    assert "Unpublished example" not in client.get("/projects/").text
    assert client.get("/projects/unpublished-example/").status_code == 404
    assert client.get("/resume/download/").status_code == 404
    profile["resume_approved"] = True
    (data / "profile.json").write_text(json.dumps(profile))
    response = create_app(config).test_client().get("/resume/download/")
    assert response.status_code == 200
    assert "attachment" in response.headers["Content-Disposition"]


def test_approved_resume_download(client):
    import hashlib
    response = client.get("/resume/download/")
    profile = json.loads((ROOT / "data/profile.json").read_text())
    assert response.status_code == 200
    assert response.mimetype == "application/pdf"
    assert "Luigi-Josue-Resume.pdf" in response.headers["Content-Disposition"]
    assert response.data == (ROOT / "public/resume.pdf").read_bytes()
    assert hashlib.sha256(response.data).hexdigest() == profile["resume_sha256"]
    assert "/resume/download/" in client.get("/resume/").text
    assert "mailto:" + profile["email"] in client.get("/contact/").text


def test_staging_allowlist(tmp_path):
    from scripts.stage_release import FILES, DIRECTORIES
    for name in FILES:
        shutil.copy2(ROOT / name, tmp_path / name)
    for name in DIRECTORIES:
        shutil.copytree(ROOT / name, tmp_path / name)
    (tmp_path / "private-note.txt").write_text("Must not ship")
    output = stage(tmp_path)
    assert not (output / "private-note.txt").exists()
    assert not (output / "docs").exists()
    assert (output / "app.py").is_file()
    projects_path = tmp_path / "data/projects.json"
    projects = json.loads(projects_path.read_text())
    projects[0]["public"] = False
    projects_path.write_text(json.dumps(projects))
    with pytest.raises(ValueError, match="Unpublished"):
        stage(tmp_path)
