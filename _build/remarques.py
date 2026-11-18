"""Rassemble les fichiers remarques-*.json renvoyés par les frères (déposés dans _retours/) en _retours/synthese.md."""
import json, glob, os, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR = os.path.join(ROOT, "_retours")
ICON = {"like": "👍", "dislike": "👎", "note": "💬"}


def main():
    os.makedirs(DIR, exist_ok=True)
    items, seen, files = [], set(), sorted(glob.glob(os.path.join(DIR, "*.json")))
    for f in files:
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception as e:
            print("illisible :", os.path.basename(f), e); continue
        for c in d.get("remarques", []):
            if c.get("id") in seen: continue
            seen.add(c.get("id")); c["auteur"] = c.get("auteur") or d.get("auteur") or "?"; items.append(c)
    if not items:
        print("Aucune remarque dans", DIR); return

    out = [f"# Remarques des frères — synthèse", "",
           f"{len(items)} remarques, {len({c['auteur'] for c in items})} frère(s) : "
           + ", ".join(sorted({c['auteur'] for c in items})) + f" — {len(files)} fichier(s).", ""]

    # tableau par version
    out += ["## Bilan par version", "", "| Version | 👍 | 👎 | 💬 | Frères |", "|---|---|---|---|---|"]
    by_v = collections.defaultdict(list)
    for c in items: by_v[c["version"]].append(c)
    for v in sorted(by_v):
        L = by_v[v]; n = collections.Counter(c["verdict"] for c in L)
        out.append(f"| {v} | {n['like']} | {n['dislike']} | {n['note']} | {', '.join(sorted({c['auteur'] for c in L}))} |")
    out.append("")

    # détail par version > page > élément
    for v in sorted(by_v):
        out += [f"## {v}", ""]
        by_p = collections.defaultdict(list)
        for c in by_v[v]: by_p[c["page"]].append(c)
        for p in sorted(by_p, key=lambda x: (x != "index.html", x)):
            out += [f"### {p}", ""]
            by_e = collections.OrderedDict()
            for c in sorted(by_p[p], key=lambda c: c["date"]):
                by_e.setdefault(c["selecteur"], []).append(c)
            for sel, L in by_e.items():
                c0 = L[0]
                ext = f" — « {c0['extrait']} »" if c0.get("extrait") else ""
                out.append(f"- **{c0['element']}**{ext}  \n  `{sel}`")
                for c in L:
                    t = f" : {c['texte']}" if c.get("texte") else ""
                    out.append(f"  - {ICON.get(c['verdict'], '?')} {c['auteur']} ({c.get('ecran', '')}){t}")
            out.append("")

    path = os.path.join(DIR, "synthese.md")
    open(path, "w", encoding="utf-8").write("\n".join(out))
    print(f"{len(items)} remarques -> {path}")


if __name__ == "__main__":
    main()
