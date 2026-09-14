"""Rebuild the portfolio and push the new version to the live site.

    python publish.py

The source of truth is this folder — D:\\Don_Portfolio\\_portfolio_source.
The git repo at _site_repo keeps a mirror of it purely as a backup, and this
script overwrites that mirror every time, so there is only ever one folder to
edit and no way to publish a stale copy by mistake.
"""
import os, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
REPO = os.path.join(ROOT, "_site_repo")
BUILT = os.path.join(ROOT, "Vittorio_Zumpano_Portfolio.html")
DECK = os.path.join(ROOT, "TalentDesk_Presentation.html")
SKIP = {"__pycache__", ".git"}


def run(cmd, cwd=None):
    r = subprocess.run(cmd, cwd=cwd, shell=isinstance(cmd, str))
    if r.returncode:
        sys.exit("failed: %s" % (cmd,))


def mirror(src, dst):
    """Copy src over dst, removing anything in dst that is no longer in src."""
    if os.path.isdir(dst):
        shutil.rmtree(dst)
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns(*SKIP))


if not os.path.isdir(os.path.join(REPO, ".git")):
    sys.exit("no git repo at %s — nothing to publish to" % REPO)

print("1/4  building")
run([sys.executable, os.path.join(HERE, "build_portfolio.py")], cwd=HERE)

print("2/4  staging")
shutil.copy(BUILT, os.path.join(REPO, "docs", "index.html"))
if os.path.exists(DECK):
    shutil.copy(DECK, os.path.join(REPO, "docs", "TalentDesk_Presentation.html"))
mirror(HERE, os.path.join(REPO, "_portfolio_source"))

print("3/4  committing")
run("git add -A", cwd=REPO)
if subprocess.run("git diff --cached --quiet", cwd=REPO, shell=True).returncode == 0:
    print("     nothing changed — already published")
    sys.exit(0)
run('git -c user.name="Don-BP" -c user.email="samusxaran@hotmail.com" '
    'commit -q -m "Update portfolio"', cwd=REPO)

print("4/4  pushing")
run("git push -q origin main", cwd=REPO)
print("\nlive in a minute or two at:")
print("  https://don-bp.github.io/vittorio_zumpano_portfolio/")
