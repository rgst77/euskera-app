# Euskara Lantegia

> **In English:** a self-study Basque course for Spanish speakers, packaged as a single web page: 80 lessons from A1 to C1, verb and declension trainers and spaced repetition. The rest of this README is in Spanish, the course's language.

Un taller para aprender euskera (batua) de forma autónoma, pensado para hispanohablantes que empiezan de cero. Es una sola página web, sin servidor ni instalación.

## Qué incluye

- **Ikasgaiak (lecciones):** temario de 80 lecciones, 16 por nivel, de A1 a C1. Cada lección tiene cinco pasos: teoría (con introducción, paso a paso, errores típicos y resumen), diálogo, ejercicios con pistas, escritura y repaso.
- **Aditzak (verbos):** entrenador de auxiliares y verbos sintéticos (NOR, NOR-NORK, NOR-NORI, NOR-NORI-NORK), con unas 240 formas y fichas de teoría.
- **Deklinabidea (casos):** entrenador de 12 casos de declinación, generados por un motor de reglas.
- **Hiztegia (vocabulario):** unas 890 palabras en 28 temas, clasificadas de A1 a B1.
- **Repaso espaciado:** todo lo que practicas se programa para repasarlo en el momento justo.
- **Sesión guiada:** repasar, avanzar en el temario y practicar lo aprendido, en ese orden.

## Cómo usarlo

**Fuera de Claude:** abre `index.html` en el navegador, o publícalo con GitHub Pages. El progreso se guarda en el navegador. Las funciones de IA (corrección de textos, dudas y ejercicios extra) no aparecen en este modo.

**Dentro de Claude:** sube `index.html` a una conversación en claude.ai y pide que lo publique como artifact con las capacidades `db`, `user` y `sample`. El progreso se guarda en la cuenta de cada persona, y las funciones de IA se activan (cada consulta usa la cuenta de quien la hace).

## Estructura

```
index.html                  La app completa, generada (no editar a mano)
src/app.html                Código de la app, con los marcadores donde se insertan temario y lecciones
curriculum.json             Mapa del curso: qué introduce cada lección y qué formas verbales enseña
CURRICULUM.md               Temario legible con el estado de cada lección (generado)
lessons/*.json              Una lección por archivo
tools/build.py              Valida las lecciones y genera index.html y CURRICULUM.md
tools/check_progression.py  Comprueba que ninguna lección use formas verbales aún no enseñadas
```

## Añadir o corregir lecciones

1. Edita o crea `lessons/<nivel>-<número>.json` (por ejemplo `a2-03.json`) siguiendo el formato de las existentes.
2. Si la lección introduce formas verbales nuevas, añádelas a su entrada de `curriculum.json` (campo `forms`). Las expresiones que se adelantan como frase hecha van en `chunks`.
3. Ejecuta `python3 tools/check_progression.py` para comprobar el orden y `python3 tools/build.py` para generar la app. El script de construcción comprueba cada lección (campos obligatorios, respuestas coherentes, que los ejercicios de ordenar usen exactamente las palabras dadas) y regenera `index.html`.

Tipos de ejercicio: `choice` (elegir opción), `gap` (rellenar el hueco marcado con `___`), `order` (ordenar palabras, con varias respuestas aceptadas) y `match` (emparejar). Todos admiten un campo `hint` con una pista. En los textos, `**así**` se muestra en negrita y `{nor:…}`, `{nork:…}` y `{nori:…}` con el color de cada función gramatical.

## Notas

- El contenido (explicaciones, ejemplos, diálogos, ejercicios y vocabulario) es original. El orden del temario toma como referencia el curso gratuito de [euskera.net](https://euskera.net/curso/).
- Los paradigmas verbales y las declinaciones siguen el euskera batua estándar. Si encuentras un error, se agradece una *issue* o un *pull request*.

## Licencia

- **Código** (lógica de la app y `tools/`): [MIT](LICENSE).
- **Contenido** (lecciones, temario, explicaciones, ejercicios y vocabulario): [CC BY-SA 4.0](LICENSE-CONTENT.md).
