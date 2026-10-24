#!/usr/bin/env python3
"""Comprueba que cada lección solo usa formas verbales ya enseñadas.

Lee curriculum.json (qué formas introduce cada lección y qué expresiones se
adelantan como frase hecha) y revisa el euskera de los ejemplos, diálogos y
ejercicios de lessons/*.json. Uso:  python3 tools/check_progression.py
"""
import json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
cur = json.loads((ROOT / "curriculum.json").read_text(encoding="utf-8"))
order = {c["id"]: i for i, c in enumerate(cur)}
intro = {}                       # forma -> lección donde se enseña
for c in cur:
    for f in c["forms"]:
        intro.setdefault(f, c["id"])
# homógrafos que no son formas verbales en su uso habitual
HOMOGRAPHS = {"zuen"}            # zuen = «vuestro» (posesivo, A1-09)

def basque_texts(d):
    for eu, _ in d["examples"]:
        yield "ejemplo", eu
    for line in d["dialog"]["lines"]:
        yield "diálogo", line[1]
    for i, e in enumerate(d["exercises"], 1):
        if e["type"] == "gap":
            yield f"ejercicio {i}", e["q"].replace("___", e["a"][0])
        elif e["type"] == "order":
            for a in e["a"]:
                yield f"ejercicio {i}", a
        elif e["type"] == "match":
            for a, _ in e["pairs"]:
                yield f"ejercicio {i}", a

def tokens(text):
    return re.findall(r"[a-zñ]+", text.lower())

problems, checked = [], 0
lessons = sorted((ROOT / "lessons").glob("*.json"))
for p in lessons:
    d = json.loads(p.read_text(encoding="utf-8"))
    me = order[d["id"]]
    allowed = set()
    for c in cur[: me + 1]:
        allowed.update(c["chunks"])
    for where, text in basque_texts(d):
        for t in tokens(text):
            form = t[2:] if t.startswith("ba") and t[2:] in intro and t not in intro else t
            if form in intro and form not in HOMOGRAPHS and form not in allowed and order[intro[form]] > me:
                problems.append(f"{d['id']} · {where}: «{t}» se enseña en {intro[form]} → «{text}»")
            checked += 1
print(f"{len(lessons)} lecciones revisadas, {checked} palabras en euskera analizadas.")
if problems:
    print(f"{len(problems)} usos adelantados:")
    print("\n".join("  " + x for x in problems))
    sys.exit(1)
print("Progresión correcta: ninguna lección usa formas verbales que aún no se han enseñado.")
