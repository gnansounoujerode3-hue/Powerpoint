# 🎨 PACK 1500 — 1 500 templates PowerPoint premium

> **1 500 modèles uniques · 10 diapositives chacun · 15 000 slides · 30 univers graphiques · 50 palettes.**
> Des designs originaux générés par code, 100 % modifiables, avec une galerie web pour les explorer et les télécharger.

Ce dépôt n'est pas une collection de fichiers téléchargés : c'est un **système de design complet**. Chaque modèle est la combinaison déterministe d'une famille de mise en page et d'une palette, rendue en **formes PowerPoint natives** (textes, rectangles, ellipses, dégradés, graphiques, notes de présentation). Aucune image aplatie, aucune police exotique, aucun élément verrouillé.

---

## ✨ Ce que contient le pack

| | |
|---|---|
| **1 500** | modèles `.pptx` uniques, nommés `T0001` → `T1500` |
| **10 slides** | couverture, sommaire, transition, vision, chiffres clés, données, processus, équipe, citation, clôture |
| **30 familles** | Suisse Minimal, Néon Startup, Noir & Or, Éditorial Bold, Data Room, Terre Organique, Béton Brut… |
| **50 palettes** | 25 histoires chromatiques × 2 ambiances (clair / nuit) |
| **10 univers** | Business, Tech, Finance, Créatif, Éducation, Santé, Luxe, Marketing, Écologie, Architecture |
| **Format** | 16:9 (13,33 × 7,5 pouces), polices Office standard, notes de présentation incluses |
| **Animations** | Transitions natives + fondus séquencés sur titres, cartes et images |
| **Images** | 4 vraies images remplaçables par modèle (visuel principal + 3 portraits) |

Chaque fichier est **entièrement éditable** dans PowerPoint, Keynote, Google Slides et LibreOffice Impress.

---

## 🎬 Animations professionnelles

Chaque diapositive reçoit deux niveaux d'animation **nativement PowerPoint** (XML OOXML, aucune macro, aucun plugin) :

- **Transition** adaptée à la famille graphique : `fade`, `push`, `wipe`, `dissolve`, `split`, `cover`, `checker` — les slides de transition utilisent `dissolve`, la clôture un fondu.
- **Séquence d'apparitions en fondu** : les titres, cartes, KPI et images apparaissent les uns après les autres. **Un clic lance la séquence**, puis les éléments s'enchaînent automatiquement (190 ms d'écart, fondu de 550 ms). Maximum 7 effets par slide pour rester lisible.

Tout est modifiable dans PowerPoint : onglet **Transitions** et onglet **Animations** → *Volet Animation* (durées, ordre, déclencheurs). Le moteur est dans `core/animation.py`.

## 🖼️ Images prêtes à remplacer

Ce ne sont pas des rectangles colorés : ce sont de **vrais objets image** (`p:pic`) intégrés au `.pptx`.

- **300 visuels uniques** générés par code (`core/media.py` + Pillow) : 50 palettes × 3 visuels principaux + 50 × 3 portraits. Dégradés, halos et géométrie assortis à chaque palette, sans copyright ni téléchargement.
- **4 images par modèle** : visuel principal (couverture des familles split / éditorial / asymétrique, slide *Vision*, slide de transition) + 3 portraits circulaires sur le slide *Équipe*.
- **Pour mettre vos images** : clic droit sur l'image → **« Modifier l'image » → « À partir d'un fichier »**. Le cadrage est conservé automatiquement (recadrage sans déformation, masque circulaire pour les portraits).
- Les consignes sont rappelées sur les slides et dans les **notes de présentation**.
- Les mêmes images sont **intégrées en data-URI dans les aperçus SVG** de la galerie : ce que vous voyez est exactement ce que vous téléchargez.

---

## 🚀 Démarrage rapide

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt

# 1. Générer le catalogue (JSON + CSV)
.venv/bin/python scripts/export.py --catalogue

# 2. Lancer la galerie web  →  http://localhost:8000
.venv/bin/python web/server.py

# 3. Construire l'archive ZIP complète (1 500 .pptx + INDEX.csv + LISEZ-MOI.txt)
.venv/bin/python scripts/export.py --all --zip
```

La galerie démarre la génération de l'archive automatiquement si elle n'existe pas encore et affiche sa progression. L'archive est écrite dans `dist/Pack-1500-Templates-PowerPoint.zip` (~80 Mio, 1 502 fichiers).

> `dist/` et `.venv/` sont ignorés par Git : seuls le code, le catalogue et la documentation sont versionnés. Le pack se régénère en ~2 minutes sur 2 cœurs.

---

## 🖥️ La galerie

```
http://localhost:8000
```

- **Recherche** plein texte (nom, n°, univers, couleur, motif, typo) — raccourci `/`
- **Filtres** : univers, ambiance clair/sombre, motif décoratif, typographie, couleur dominante
- **Tris** : popularité, numéro, nom, famille
- **Favoris** sauvegardés dans le navigateur
- **Aperçu fidèle** : la vignette SVG est générée à partir de la même scène vectorielle que le `.pptx`
- **Modale de détail** : les 10 diapositives, les couleurs de la palette, les métadonnées, le téléchargement
- **Pack complet** : bouton avec barre de progression, téléchargement dès que l'archive est prête

### API

| Route | Description |
|---|---|
| `GET /api/catalog` | les 1 500 modèles + métadonnées (JSON) |
| `GET /api/thumb/T0042.svg?slide=0` | aperçu vectoriel d'une diapositive (0 → 9) |
| `GET /api/download/T0042.pptx` | génère et télécharge un modèle |
| `GET /api/pack/status` | avancement de l'archive |
| `GET /api/pack` | l'archive ZIP des 1 500 modèles |
| `GET /api/pack/start` | lance la génération en arrière-plan |
| `GET /api/health` | état du serveur |

Le serveur n'utilise que la bibliothèque standard Python (`http.server`) pour l'API et `python-pptx` pour la génération.

---

## 🧩 Architecture

```
Powerpoint/
├── core/
│   ├── design_system.py    30 familles × 50 palettes = 1 500 modèles + catalogue
│   ├── scene.py            scène vectorielle neutre (Rect, Ellipse, Line, Text…)
│   ├── layouts.py          10 mises en page premium, déclinées par famille
│   ├── media.py            300 visuels JPEG/PNG générés par palette
│   ├── animation.py        transitions + séquences de fondus (OOXML)
│   ├── render_svg.py       rendu SVG (aperçus du site, images en data-URI)
│   ├── render_pptx.py      rendu PowerPoint natif et éditable
│   └── pack.py             construction du ZIP, cache, statut
├── catalog/
│   ├── templates.json      catalogue complet (1 500 entrées)
│   └── templates.csv       même catalogue pour Excel
├── scripts/export.py       CLI : catalogue, un modèle, aperçu, pack complet
├── web/
│   ├── server.py           serveur HTTP + API
│   ├── index.html          galerie
│   ├── styles.css          interface sombre premium
│   └── app.js              filtres, favoris, modale, progression
└── dist/                   (ignoré) archive ZIP, cache, statut
```

**Principe clé :** une scène est une liste de primitives. Elle est rendue deux fois — en SVG pour l'aperçu web, en formes PowerPoint pour le fichier `.pptx`. L'aperçu est donc exactement ce que l'on obtient dans PowerPoint.

---

## 🛠️ Ligne de commande

```bash
# Un seul modèle
.venv/bin/python scripts/export.py --id T0042 --out ~/Bureau/mon-template.pptx

# Aperçu SVG d'une diapositive (contrôle qualité)
.venv/bin/python scripts/export.py --apercu T0042 0

# Tout régénérer après modification du design system
.venv/bin/python scripts/export.py --catalogue --all --zip --force

# Nombre de processus
.venv/bin/python scripts/export.py --all --zip --workers 4

# Contrôle qualité (catalogue, ZIP, .pptx, aperçus SVG)
.venv/bin/python scripts/validate.py
```

---

## 🎨 Personnaliser les designs

Tout se passe dans `core/design_system.py` :

- **`STORIES`** — les 25 histoires chromatiques (accent, accent secondaire, fonds clair/nuit). Ajoutez-en une → +2 modèles par famille.
- **`FAMILIES` / `_FAMILY_ROWS`** — nom, univers, `archetype` de couverture, `motif` décoratif, `typo`, rayon des cartes, densité.
- **`FONTS`** — 8 appariements typographiques utilisant des polices présentes dans Office.
- **`HEADLINES` / `SUBTITLES`** — les textes d'exemple des couvertures.

`core/layouts.py` contient les 10 mises en page. Chaque fonction reçoit le modèle et retourne une `Scene` ; ajoutez-y vos propres primitives (`Rect`, `Ellipse`, `Line`, `Text`, `Triangle`) pour créer de nouveaux slides. Les dégradés sont décrits par `gradient(c1, c2, angle)` et fonctionnent dans les deux moteurs de rendu.

Exemple minimal :

```python
from design_system import get_template
from render_pptx import render_deck

t = get_template("T0042")
render_deck(t, "mon-template.pptx")
```

---

## ✅ Qualité et compatibilité

- Les fichiers sont validés (archive ZIP testée, `.pptx` relus avec `python-pptx`).
- Chaque slide contient une **note de présentation** avec une astuce d'édition.
- Dégradés, transparence, coins arrondis et rotations sont de vraies propriétés de forme PowerPoint.
- Polices utilisées : Arial, Calibri, Georgia, Cambria, Trebuchet MS, Consolas, Aptos, Arial Black.
- `scripts/validate.py` vérifie aussi la présence des **transitions**, du **volet d'animations** et des **images** dans les `.pptx`.
- Aucun appel réseau, aucune dépendance externe au-delà de `python-pptx` et `Pillow`.

> ⚠️ Les animations et transitions s'affichent dans **PowerPoint** (Windows, macOS, web). Keynote, Google Slides et LibreOffice importent le `.pptx` mais peuvent ignorer tout ou partie du volet d'animations ; le design statique reste intact.

## 📄 Licence

Code et designs originaux sous licence MIT : usage personnel et commercial libre, sans attribution obligatoire. Voir [LICENSE](LICENSE).

---

**Bonnes présentations !** 🚀
