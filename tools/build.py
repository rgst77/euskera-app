#!/usr/bin/env python3
"""Genera index.html insertando todas las lecciones de lessons/*.json en src/app.html.

Uso:  python3 tools/build.py
"""
import json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
REQUIRED = ["id", "lvl", "n", "title", "es", "goal", "explain", "examples", "dialog", "exercises", "create", "links"]

def validate(d, path):
    for k in REQUIRED:
        if k not in d:
            sys.exit(f"{path.name}: falta el campo «{k}»")
    for i, e in enumerate(d["exercises"], 1):
        t = e.get("type")
        if t == "choice" and not (0 <= e["a"] < len(e["options"])):
            sys.exit(f"{path.name}: ejercicio {i}, índice de respuesta fuera de rango")
        if t == "gap" and "___" not in e["q"]:
            sys.exit(f"{path.name}: ejercicio {i}, el hueco necesita ___")
        if t == "order":
            words = sorted(w.lower() for w in e["words"])
            for a in e["a"]:
                if sorted(a.lower().split()) != words:
                    sys.exit(f"{path.name}: ejercicio {i}, «{a}» no usa exactamente las palabras dadas")
        if t not in ("choice", "gap", "order", "match"):
            sys.exit(f"{path.name}: ejercicio {i}, tipo desconocido «{t}»")

lessons = {}
for p in sorted((ROOT / "lessons").glob("*.json")):
    d = json.loads(p.read_text(encoding="utf-8"))
    validate(d, p)
    lessons[d["id"]] = d

tpl = (ROOT / "src" / "app.html").read_text(encoding="utf-8")
marker = "/*__LESSONS__*/{}"
if marker not in tpl:
    sys.exit("No se encuentra el marcador /*__LESSONS__*/ en src/app.html")
data = json.dumps(lessons, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
cur = json.loads((ROOT / "curriculum.json").read_text(encoding="utf-8"))
cur_data = json.dumps([{k: c[k] for k in ("id", "lvl", "n", "title", "es", "introduce")} for c in cur], ensure_ascii=False, separators=(",", ":"))
if "/*__CURRICULUM__*/[]" not in tpl:
    sys.exit("No se encuentra el marcador /*__CURRICULUM__*/ en src/app.html")
for lid in lessons:
    if not any(c["id"] == lid for c in cur):
        sys.exit(f"La lección {lid} no está en curriculum.json")
html = tpl.replace(marker, data).replace("/*__CURRICULUM__*/[]", cur_data)
(ROOT / "index.html").write_text(html, encoding="utf-8")
print(f"index.html generado con {len(lessons)} lecciones")

# CURRICULUM.md: temario legible con el estado de cada lección
names = {"A1": "A1 · Inicial", "A2": "A2 · Básico", "B1": "B1 · Intermedio", "B2": "B2 · Intermedio alto", "C1": "C1 · Avanzado"}
out = ["# Temario de Euskara Lantegia", "",
       "Generado por `tools/build.py` desde `curriculum.json`. Cada lección se apoya solo en las anteriores;",
       "`tools/check_progression.py` comprueba que ninguna use formas verbales que aún no se han enseñado.", ""]
done = sum(1 for c in cur if c["id"] in lessons)
out.append(f"**Progreso: {done} de {len(cur)} lecciones escritas.**")
for lvl in names:
    out += ["", f"## {names[lvl]}", "", "| Nº | Lección | Qué introduce | Estado |", "|---|---|---|---|"]
    for c in (c for c in cur if c["lvl"] == lvl):
        st = "escrita" if c["id"] in lessons else "pendiente"
        out.append(f"| {c['n']} | **{c['title']}** · {c['es']} | {', '.join(c['introduce'])} | {st} |")
(ROOT / "CURRICULUM.md").write_text("\n".join(out) + "\n", encoding="utf-8")
print("CURRICULUM.md actualizado")
