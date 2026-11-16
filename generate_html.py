#!/usr/bin/env python3
"""
Génère une page HTML statique pour chaque workflow n8n (fichier .json)
présent dans le sous-dossier « workflows ». Les pages sont écrites dans
le sous-dossier « html » avec le même nom (extension .json -> .html).
"""

import html
import re
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
WF_DIRNAME = BASE_DIR / "workflows"
HTML_DIRNAME = BASE_DIR / "html"

# Même contrainte que le script PHP d'origine sur les noms de workflow
VALID_NAME = re.compile(r"^[a-zA-Z0-9_-]+$")

TEMPLATE = """<html>
	<head>
		<meta charset="utf-8">
		<title>{title}</title>
	</head>
	<body>
		<script src="https://cdn.jsdelivr.net/npm/@webcomponents/webcomponentsjs@2.0.0/webcomponents-loader.js"></script>
		<script src="https://www.unpkg.com/lit@2.0.0-rc.2/polyfill-support.js"></script>
		<script type="module" src="https://cdn.jsdelivr.net/npm/@n8n_io/n8n-demo-component/n8n-demo.bundled.js"></script>

		<n8n-demo workflow="{workflow}" ></n8n-demo>
	</body>
</html>
"""


def main() -> int:
    if not WF_DIRNAME.is_dir():
        print(f"Dossier introuvable : {WF_DIRNAME}", file=sys.stderr)
        return 1

    HTML_DIRNAME.mkdir(exist_ok=True)

    generated, skipped = 0, 0
    for wf_path in sorted(WF_DIRNAME.glob("*.json")):
        wf_name = wf_path.stem

        if not VALID_NAME.match(wf_name):
            print(f"Ignoré (nom invalide) : {wf_path.name}", file=sys.stderr)
            skipped += 1
            continue

        wf_json = wf_path.read_text(encoding="utf-8")
        # Équivalent de htmlentities() : échappe & < > " '
        wf_json_escaped = html.escape(wf_json, quote=True)

        page = TEMPLATE.format(
            title=html.escape(wf_name),
            workflow=wf_json_escaped,
        )

        out_path = HTML_DIRNAME / f"{wf_name}.html"
        out_path.write_text(page, encoding="utf-8")
        print(f"Généré : {out_path.relative_to(BASE_DIR)}")
        generated += 1

    print(f"\n{generated} page(s) générée(s), {skipped} fichier(s) ignoré(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
