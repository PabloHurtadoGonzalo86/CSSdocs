#!/usr/bin/env python3
"""Vigilante semanal de novedades en CSS.

Compara, sin usar ninguna API de pago ni claves propias, tres fuentes oficiales
frente al estado guardado en la ejecucion anterior:

1. MDN Web Docs (repo `mdn/content`): commits recientes que tocan la referencia de CSS.
2. CSSWG Drafts (repo `w3c/csswg-drafts`): commits recientes en las especificaciones.
3. caniuse-db: cambios de madurez (status) en un listado vigilado de features CSS modernas.

No redacta ni "adivina" nada: solo enlaza los cambios reales detectados para que
una persona decida si hay que actualizar la documentacion.
"""
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_PATH = os.path.join(SCRIPT_DIR, "state.json")
CHANGELOG_PATH = os.path.normpath(
    os.path.join(SCRIPT_DIR, "..", "..", "docs", "novedades", "changelog.md")
)
LAST_REPORT_PATH = os.path.join(SCRIPT_DIR, "last_report.md")

GITHUB_API = "https://api.github.com"
USER_AGENT = "CSSdocs-weekly-watcher (+https://github.com/PabloHurtadoGonzalo86/CSSdocs)"

# Features CSS modernas que interesa vigilar de cerca (id de caniuse -> etiqueta legible)
CANIUSE_WATCHLIST = {
    "css-nesting": "CSS Nesting nativo",
    "css-has": "Selector :has()",
    "css-container-queries": "Container queries (@container)",
    "css-cascade-layers": "Cascade layers (@layer)",
    "css-scroll-timeline": "Scroll-driven animations (animation-timeline)",
    "css-anchor-positioning": "Anchor positioning",
    "css-subgrid": "Subgrid",
    "css-color-function": "color() / relative color syntax",
    "css-cascade-scope": "@scope",
    "css-container-query-units": "Unidades de container queries (cqw, cqh...)",
    "css-media-range-syntax": "Sintaxis de rango en media queries",
    "css-view-transitions": "View Transitions API",
}


def gh_get(url):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/vnd.github+json"})
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())


def fetch_commits(repo, path, since_iso):
    url = f"{GITHUB_API}/repos/{repo}/commits?since={since_iso}&per_page=100"
    if path:
        url += f"&path={path}"
    try:
        return gh_get(url)
    except (urllib.error.HTTPError, urllib.error.URLError) as e:
        print(f"WARN: no se pudieron obtener commits de {repo}: {e}", file=sys.stderr)
        return []


def fetch_caniuse_data():
    url = "https://raw.githubusercontent.com/Fyrd/caniuse/main/fulldata-json/data-2.0.json"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode())


def load_state():
    if os.path.exists(STATE_PATH):
        with open(STATE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"last_run": None, "caniuse_status": {}}


def save_state(state):
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")


def main():
    now = datetime.now(timezone.utc).replace(microsecond=0)
    now_iso = now.isoformat().replace("+00:00", "Z")

    state = load_state()
    first_run = state.get("last_run") is None
    since_iso = state.get("last_run") or now_iso

    findings = []

    if not first_run:
        mdn_commits = fetch_commits("mdn/content", "files/en-us/web/css", since_iso)
        if mdn_commits:
            findings.append((
                "MDN Web Docs — cambios en la referencia de CSS",
                [
                    f"- [{c['commit']['message'].splitlines()[0]}]({c['html_url']}) "
                    f"({c['commit']['author']['date'][:10]})"
                    for c in mdn_commits[:25]
                ],
            ))

        csswg_commits = fetch_commits("w3c/csswg-drafts", None, since_iso)
        if csswg_commits:
            findings.append((
                "CSSWG Drafts — cambios en especificaciones",
                [
                    f"- [{c['commit']['message'].splitlines()[0]}]({c['html_url']}) "
                    f"({c['commit']['author']['date'][:10]})"
                    for c in csswg_commits[:25]
                ],
            ))

    try:
        caniuse = fetch_caniuse_data()
        data = caniuse.get("data", {})
        prev_status = state.get("caniuse_status", {})
        new_status = {}
        status_changes = []
        for feature_id, label in CANIUSE_WATCHLIST.items():
            feature = data.get(feature_id)
            if not feature:
                continue
            status = feature.get("status", "unknown")
            new_status[feature_id] = status
            if not first_run and prev_status.get(feature_id) not in (None, status):
                status_changes.append(
                    f"- **{label}** (`{feature_id}`): `{prev_status[feature_id]}` -> `{status}` "
                    f"— https://caniuse.com/{feature_id}"
                )
        if status_changes:
            findings.append(("caniuse — cambios de madurez en features CSS vigiladas", status_changes))
        state["caniuse_status"] = new_status
    except Exception as e:  # noqa: BLE001 - queremos que un fallo de red no rompa el job
        print(f"WARN: no se pudo consultar caniuse: {e}", file=sys.stderr)

    state["last_run"] = now_iso
    save_state(state)

    report_lines = [f"# Vigilancia semanal de CSS — {now.date().isoformat()}", ""]
    if first_run:
        report_lines.append(
            "Primera ejecucion: se ha guardado el estado inicial (commits de referencia y "
            "estados de madurez de caniuse). A partir de la proxima ejecucion semanal se "
            "compararan los cambios reales frente a este punto de partida."
        )
    elif not findings:
        report_lines.append("No se han detectado cambios relevantes esta semana en las fuentes vigiladas.")
    else:
        for title, lines in findings:
            report_lines.append(f"## {title}")
            report_lines.extend(lines)
            report_lines.append("")

    report = "\n".join(report_lines).strip() + "\n"
    has_findings = bool(findings) and not first_run

    gh_output = os.environ.get("GITHUB_OUTPUT")
    if gh_output:
        with open(gh_output, "a", encoding="utf-8") as f:
            f.write(f"has_findings={'true' if has_findings else 'false'}\n")

    os.makedirs(os.path.dirname(CHANGELOG_PATH), exist_ok=True)
    if os.path.exists(CHANGELOG_PATH):
        with open(CHANGELOG_PATH, "r", encoding="utf-8") as f:
            existing = f.read()
    else:
        existing = (
            "# Changelog automático de CSS\n\n"
            "Entradas generadas por el vigilante semanal "
            "(`.github/workflows/weekly-css-watch.yml`). Cada entrada enlaza cambios "
            "reales detectados en MDN, CSSWG Drafts y caniuse — nunca contenido inventado.\n"
        )

    with open(CHANGELOG_PATH, "w", encoding="utf-8") as f:
        f.write(existing.rstrip() + "\n\n---\n\n" + report)

    with open(LAST_REPORT_PATH, "w", encoding="utf-8") as f:
        f.write(report)


if __name__ == "__main__":
    main()
