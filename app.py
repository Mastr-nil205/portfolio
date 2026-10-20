"""Personal portfolio. No request-time writes, accounts, or database."""

import os
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

from flask import Flask, abort, render_template, request, send_from_directory, url_for
from portfolio_data import PortfolioRepository

ROOT = Path(__file__).resolve().parent


def create_app(test_config=None):
    app = Flask(__name__, static_folder=None)
    app.config.from_mapping(
        DATA_DIR=ROOT / "data",
        PUBLIC_DIR=ROOT / "public",
        SITE_URL=os.environ.get("SITE_URL", "").rstrip("/"),
        DEPLOYMENT_ENV=os.environ.get("VERCEL_ENV", "development"),
        LOCAL_ASSETS=not bool(os.environ.get("VERCEL")),
        MAX_CONTENT_LENGTH=16 * 1024,
        DEBUG=False,
    )
    if test_config:
        app.config.update(test_config)
    if app.config["SITE_URL"]:
        parsed = urlsplit(app.config["SITE_URL"])
        if parsed.scheme != "https" or not parsed.netloc or parsed.path or parsed.query or parsed.fragment or parsed.username:
            raise ValueError("SITE_URL must be an HTTPS origin without a path")
    repository = PortfolioRepository(app.config["DATA_DIR"])
    app.extensions["portfolio_repository"] = repository

    def asset_url(filename):
        return f"{request.script_root}/{filename.lstrip('/')}"

    def resume_available():
        return bool(repository.profile.get("resume_approved")) and (
            Path(app.config["PUBLIC_DIR"]) / "resume.pdf"
        ).is_file()

    @app.context_processor
    def shared_context():
        canonical = ""
        if app.config["SITE_URL"]:
            canonical = app.config["SITE_URL"] + request.script_root + request.path
        return {
            "profile": repository.profile,
            "year": datetime.now(timezone.utc).year,
            "asset_url": asset_url,
            "canonical": canonical,
            "site_url": app.config["SITE_URL"],
            "noindex": app.config["DEPLOYMENT_ENV"] != "production" or not app.config["SITE_URL"],
            "resume_available": resume_available(),
        }

    @app.after_request
    def response_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; script-src 'self'; style-src 'self'; "
            "font-src 'self'; img-src 'self' data:; object-src 'none'; "
            "base-uri 'self'; form-action 'self'; frame-ancestors 'none'"
        )
        if app.config["DEPLOYMENT_ENV"] != "production" or not app.config["SITE_URL"] or response.status_code >= 400 or request.query_string:
            response.headers["X-Robots-Tag"] = "noindex, nofollow"
        return response

    @app.get("/")
    def home():
        return render_template("home.html", title="IT professional & technical builder",
                               description=repository.profile["summary"],
                               featured=repository.projects()[:1], experience=repository.experience[:2])

    @app.get("/about/")
    def about():
        return render_template("about.html", title="About",
                               description="Luigi Josue’s background, technical interests, and professional journey.")

    @app.get("/experience/")
    def experience():
        return render_template("experience.html", title="Experience",
                               description="Luigi Josue’s desktop support, systems configuration, and enterprise IT experience.",
                               experience=repository.experience, skills=repository.skills)

    @app.get("/projects/")
    def projects():
        if set(request.args) - {"q", "category"} or any(len(request.args.getlist(key)) != 1 for key in request.args):
            abort(400, description="Use one search term and one category.")
        query = request.args.get("q", "").strip()
        category = request.args.get("category", "").strip()
        if len(query) > 100 or len(category) > 60 or any(ord(char) < 32 for char in query):
            abort(400, description="Please use a search term of 100 characters or fewer.")
        if category and category not in repository.categories():
            abort(400, description="Choose a category from the project list.")
        return render_template("projects.html", title="Projects",
                               description="Documented technical projects, implementation decisions, and learning notes.",
                               projects=repository.projects(query, category),
                               categories=repository.categories(), query=query, category=category,
                               noindex=bool(query or category) or app.config["DEPLOYMENT_ENV"] != "production" or not app.config["SITE_URL"])

    @app.get("/projects/<slug>/")
    def project_detail(slug):
        project = repository.project(slug)
        if project is None:
            abort(404)
        return render_template("project_detail.html", title=project["title"],
                               description=project["summary"], project=project)

    @app.get("/resume/")
    def resume():
        return render_template("resume.html", title="Resume",
                               description="Luigi Josue’s professional profile and public resume.")

    @app.get("/resume/download/")
    def resume_download():
        if not resume_available():
            abort(404)
        return send_from_directory(app.config["PUBLIC_DIR"], "resume.pdf",
                                   as_attachment=True, download_name="Luigi-Josue-Resume.pdf")

    @app.get("/contact/")
    def contact():
        return render_template("contact.html", title="Contact",
                               description="Connect with Luigi Josue on LinkedIn and GitHub.")

    @app.get("/robots.txt")
    def robots():
        allow = app.config["DEPLOYMENT_ENV"] == "production" and app.config["SITE_URL"]
        return ("User-agent: *\n" + ("Allow: /\n" if allow else "Disallow: /\n"),
                200, {"Content-Type": "text/plain; charset=utf-8"})

    if app.config["LOCAL_ASSETS"]:
        @app.get("/<asset_group>/<path:filename>")
        def local_asset(asset_group, filename):
            if asset_group not in {"css", "js", "fonts", "vendor", "images"}:
                abort(404)
            return send_from_directory(Path(app.config["PUBLIC_DIR"]) / asset_group, filename)

        @app.get("/favicon.svg")
        def favicon():
            return send_from_directory(app.config["PUBLIC_DIR"], "favicon.svg")

    @app.errorhandler(404)
    def not_found(_error):
        return render_template("error.html", title="Page not found", description="Return to Luigi Josue’s portfolio.",
                               code=404, message="This page isn’t here.", detail="The address may have changed. Let’s get you back to the work.", noindex=True), 404

    @app.errorhandler(400)
    def bad_request(error):
        return render_template("error.html", title="Check your search", description="Please adjust your project search.",
                               code=400, message="Let’s try that again.", detail=error.description, noindex=True), 400

    @app.errorhandler(500)
    def server_error(_error):
        return render_template("error.html", title="Something went wrong", description="Please try again later.",
                               code=500, message="A temporary interruption.", detail="Please try again in a moment.", noindex=True), 500

    return app


app = create_app()
