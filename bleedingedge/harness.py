"""The harness: hard checks every change must pass before the improver opens a pull request.

    uv run python -m bleedingedge.harness            # all checks; exit 1 if any fails
    uv run python -m bleedingedge.harness --offline  # skip the checks that need the network

Each check returns (passed, detail). The report goes to stdout and site/harness.json.
The checks, and why each exists:
  tests          the test suite passes                      (nothing that worked breaks)
  page_scripts   the page's scripts parse, one-writer line  (the site loads at all)
  site_data      the site's data builds, every topic charts (no empty panels)
  caveat         the backtest record shows on page and email (never hide that flags are long shots)
  no_hype        reader-facing text avoids overselling words (hook people without overclaiming)
  explainers     each explainer is short, plain, cited, with no made-up numbers, and its arXiv
                 sources exist                               (nothing made up passes as fact)
  reading_level  explainers and page help text read at grade 10 or below (friends, family, students)
  private        no dashboard link or email address in tracked files (the repo is public)
"""
import argparse
import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

from . import brief as br

ROOT = br.ROOT
PAGE = ROOT / "web" / "radar.html"
EXPLAINERS = ROOT / "data" / "Explainers.json"
REPORT = ROOT / "site" / "harness.json"

# Words that sell rather than inform. Matched as whole words, case-insensitive.
HYPE = ["revolutionary", "revolutionize", "groundbreaking", "game-changer", "game-changing", "breakthrough",
        "guaranteed", "the next big thing", "explosive", "skyrocketing", "unstoppable", "mind-blowing",
        "huge opportunity", "don't miss", "must-learn", "will dominate", "certain to"]
MAX_GRADE = 10.0
WORDS = (25, 90)        # each explainer part: at least, at most


def _text_of_page(html: str) -> str:
    """The words a reader sees in the page's own HTML (not data), scripts and styles removed."""
    html = re.sub(r"<(script|style)\b.*?</\1>", " ", html, flags=re.S)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html)).strip()


def _sentences(text: str) -> list[str]:
    return [s for s in re.split(r"(?<=[.!?])\s+", text.strip()) if re.search(r"[A-Za-z]", s)]


def _syllables(word: str) -> int:
    w = re.sub(r"[^a-z]", "", word.lower())
    if not w:
        return 0
    groups = re.findall(r"[aeiouy]+", w)
    n = len(groups) - (1 if w.endswith("e") and not w.endswith(("le", "ee")) and len(groups) > 1 else 0)
    return max(1, n)


def grade(text: str) -> float:
    """Flesch-Kincaid grade level: 0.39 (words/sentence) + 11.8 (syllables/word) - 15.59."""
    sents = _sentences(text)
    words = re.findall(r"[A-Za-z][A-Za-z'-]*", text)
    if not sents or not words:
        return 0.0
    syl = sum(_syllables(w) for w in words)
    return 0.39 * len(words) / len(sents) + 11.8 * syl / len(words) - 15.59


def explainers() -> dict:
    return json.loads(EXPLAINERS.read_text()) if EXPLAINERS.exists() else {}


# ---- checks -------------------------------------------------------------------------------------

def check_tests(offline: bool) -> tuple[bool, str]:
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider"], cwd=ROOT,
                       capture_output=True, text=True)
    last = (r.stdout.strip().splitlines() or ["no output"])[-1]
    return r.returncode == 0, last


def check_page_scripts(offline: bool) -> tuple[bool, str]:
    html = PAGE.read_text()
    if not html.startswith('<meta name="dash-one-writer">'):
        return False, "web/radar.html must start with the one-writer line"
    bad = []
    for i, js in enumerate(re.findall(r"<script>(.*?)</script>", html, re.S)):
        r = subprocess.run(["node", "--check", "-"], input=js, capture_output=True, text=True)
        if r.returncode:
            bad.append(f"script {i + 1}: {(r.stderr.strip().splitlines() or ['?'])[-1]}")
    if re.search(r"\son[a-z]+=", re.sub(r"<script>.*?</script>", "", html, flags=re.S)):
        bad.append("an on…= attribute (the page type drops these)")
    return not bad, "; ".join(bad) or "all scripts parse"


def check_site_data(offline: bool) -> tuple[bool, str]:
    from . import site
    d = site.build()
    topics = {r["topic"] for r in d["topics"]}
    charted = {r["topic"] for r in d["series"]}
    missing = sorted(topics - charted)
    if not topics:
        return False, "no topics"
    if missing:
        return False, f"no series for: {', '.join(missing)}"
    return True, f"{len(topics)} topics, {len(d['picks'])} picks"


def check_caveat(offline: bool) -> tuple[bool, str]:
    from . import daily, site
    rec = site.record()[0]
    problems = []
    if 'data-draw="rec-hit"' not in PAGE.read_text() or "long shot" not in PAGE.read_text():
        problems.append("page lost the track-record line")
    empty = '<feed xmlns="http://www.w3.org/2005/Atom"></feed>'
    out = daily.OUT
    try:
        daily.OUT = ROOT / "site" / "harness-email.json"
        e = daily.compose(date.today(), "https://example.invalid", lambda url: empty)
    finally:
        daily.OUT = out
    if f"{rec['took_off']} of {rec['flagged']}" not in e["text"]:
        problems.append("email lost the track-record line")
    return not problems, "; ".join(problems) or f"{rec['took_off']} of {rec['flagged']} shown on page and email"


def check_no_hype(offline: bool) -> tuple[bool, str]:
    texts = {"page": _text_of_page(PAGE.read_text())}
    for topic, e in explainers().items():
        texts[f"explainer: {topic}"] = f"{e.get('what', '')} {e.get('why', '')}"
    found = []
    for where, t in texts.items():
        for w in HYPE:
            if re.search(rf"(?<![\w-]){re.escape(w)}(?![\w-])", t, re.I):
                found.append(f"{where}: '{w}'")
    return not found, "; ".join(found) or f"{len(texts)} texts clean"


def _arxiv_ids_exist(ids: list[str]) -> list[str]:
    """The ids arXiv doesn't know (cached query, one call for all)."""
    from .http import get_text
    from .sources.arxiv import API, NS
    import xml.etree.ElementTree as ET
    if not ids:
        return []
    feed = get_text(f"{API}?id_list={','.join(sorted(ids))}&max_results={len(ids)}")
    found = {e.findtext("a:id", "", NS).rsplit("/", 1)[-1].split("v")[0]
             for e in ET.fromstring(feed).findall("a:entry", NS) if e.findtext("a:title", "", NS).strip() != "Error"}
    return sorted(set(ids) - found)


def check_explainers(offline: bool) -> tuple[bool, str]:
    ex = explainers()
    if not ex:
        return True, "none written yet"
    problems, ids = [], []
    for topic, e in ex.items():
        for part in ("what", "why"):
            text = e.get(part, "")
            n = len(text.split())
            if not WORDS[0] <= n <= WORDS[1]:
                problems.append(f"{topic}/{part}: {n} words (want {WORDS[0]}–{WORDS[1]})")
            digits = re.findall(r"\d+", re.sub(re.escape(topic), "", text, flags=re.I))
            if digits:
                problems.append(f"{topic}/{part}: numbers {digits} (numbers come from data, not prose)")
        srcs = e.get("sources", [])
        if not srcs:
            problems.append(f"{topic}: no sources")
        for s in srcs:
            url = s.get("url", "")
            if not url.startswith("https://"):
                problems.append(f"{topic}: source not https: {url}")
            m = re.fullmatch(r"https://arxiv\.org/abs/(\d{4}\.\d{4,5})", url)
            if m:
                ids.append(m[1])
    if ids and not offline:
        try:
            unknown = _arxiv_ids_exist(ids)
            problems += [f"arXiv has no paper {i}" for i in unknown]
        except Exception as err:          # network trouble is reported, not passed
            problems.append(f"couldn't check arXiv ids: {err}")
    return not problems, "; ".join(problems) or f"{len(ex)} explainers, {len(ids)} arXiv sources checked"


def check_reading_level(offline: bool) -> tuple[bool, str]:
    html = PAGE.read_text()
    help_text = " ".join(_text_of_page(m) for m in re.findall(r'<p class="br-(?:help|lede|caveat)[^"]*"[^>]*>(.*?)</p>', html, re.S))
    texts = {"page help text": help_text}
    for topic, e in explainers().items():
        texts[f"explainer: {topic}"] = f"{e.get('what', '')} {e.get('why', '')}"
    over = [f"{k}: grade {grade(t):.1f}" for k, t in texts.items() if t.strip() and grade(t) > MAX_GRADE]
    worst = max((grade(t) for t in texts.values() if t.strip()), default=0)
    return not over, "; ".join(over) or f"highest grade {worst:.1f} (limit {MAX_GRADE:.0f})"


def check_private(offline: bool) -> tuple[bool, str]:
    files = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True).stdout.split()
    pats = [re.compile(r"claude\.ai/artifact/[A-Za-z0-9]{10,}"), re.compile(r"[\w.+-]+@gmail\.com")]
    hits = []
    for f in files:
        p = ROOT / f
        if p.suffix in {".png", ".gz", ".jpg"} or not p.is_file() or p.stat().st_size > 5_000_000:
            continue
        try:
            t = p.read_text()
        except UnicodeDecodeError:
            continue
        if any(x.search(t) for x in pats):
            hits.append(f)
    return not hits, ", ".join(hits) or "no private links or addresses"


CHECKS = {"tests": check_tests, "page_scripts": check_page_scripts, "site_data": check_site_data,
          "caveat": check_caveat, "no_hype": check_no_hype, "explainers": check_explainers,
          "reading_level": check_reading_level, "private": check_private}


def run(offline: bool = False, only: list[str] | None = None) -> dict:
    results = {}
    for name, fn in CHECKS.items():
        if only and name not in only:
            continue
        try:
            ok, detail = fn(offline)
        except Exception as err:
            ok, detail = False, f"crashed: {err}"
        results[name] = {"passed": ok, "detail": detail}
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(results, indent=1))
    return results


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Run the BleedingEdge harness.")
    ap.add_argument("--offline", action="store_true")
    ap.add_argument("--only", nargs="*")
    a = ap.parse_args()
    res = run(a.offline, a.only)
    for name, r in res.items():
        print(f"{'PASS' if r['passed'] else 'FAIL'}  {name:14} {r['detail']}")
    sys.exit(0 if all(r["passed"] for r in res.values()) else 1)
