"""Rebuild the portfolio and push the new version to the live site.

    python publish.py

Two things get built from the same source:

  * D:\\Don_Portfolio\\Vittorio_Zumpano_Portfolio.html
    one self-contained file, for emailing or handing over on a stick

  * _site_repo/docs/
    the same page split into a small HTML file plus an assets folder, so the
    live site opens straight away instead of downloading fifty megabytes first

The source of truth is this folder. The copy inside the repo is a backup and is
overwritten every time, so there is no way to publish a stale one by mistake.
"""
import os, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
REPO = os.path.join(ROOT, "_site_repo")
DOCS = os.path.join(REPO, "docs")
BUILT = os.path.join(ROOT, "Vittorio_Zumpano_Portfolio.html")
DECK = os.path.join(ROOT, "TalentDesk_Presentation.html")
SKIP = {"__pycache__", ".git"}
LIVE = "https://don-bp.github.io/vittorio_zumpano_portfolio/"


def run(cmd, cwd=None):
    r = subprocess.run(cmd, cwd=cwd, shell=isinstance(cmd, str))
    if r.returncode:
        sys.exit("failed: %s" % (cmd,))


if not os.path.isdir(os.path.join(REPO, ".git")):
    sys.exit("no git repo at %s - nothing to publish to" % REPO)

print("1/5  building the single file")
run([sys.executable, os.path.join(HERE, "build_portfolio.py")], cwd=HERE)

print("2/5  building the web version")
# start from a clean assets folder so images dropped from the page do not
# linger on the server for ever
shutil.rmtree(os.path.join(DOCS, "assets"), ignore_errors=True)
run([sys.executable, os.path.join(HERE, "build_portfolio.py"), "--web", DOCS], cwd=HERE)

print("3/5  staging")
if os.path.exists(DECK):
    shutil.copy(DECK, os.path.join(DOCS, "TalentDesk_Presentation.html"))
mirror = os.path.join(REPO, "_portfolio_source")
shutil.rmtree(mirror, ignore_errors=True)
shutil.copytree(HERE, mirror, ignore=shutil.ignore_patterns(*SKIP))

print("4/5  committing")
run("git add -A", cwd=REPO)
if subprocess.run("git diff --cached --quiet", cwd=REPO, shell=True).returncode == 0:
    print("     nothing changed - already published")
    sys.exit(0)
run('git -c user.name="Don-BP" -c user.email="samusxaran@hotmail.com" '
    'commit -q -m "Update portfolio"', cwd=REPO)

print("5/5  pushing")
run("git push -q origin main", cwd=REPO)
print("\nlive in a minute or two at:\n  " + LIVE)
