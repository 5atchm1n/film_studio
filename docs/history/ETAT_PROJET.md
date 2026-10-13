# État du projet — film « Yes, you can control AI » / « Oui, on peut contrôler l'IA »

> Copied verbatim (French) from `visuels_mcp_harness/ETAT_PROJET.md` @ 6fb3c32: the project state file before film_studio. Successor: `films/<name>/STATUS.md`.

*Mis à jour : 11 oct. 2026 · Sert à reprendre le travail sans l'historique de la conversation.*

## Le film
Vidéo autonome (sans orateur), style TRON minimaliste, Manim. Explique que l'IA générale ne connaît pas nos données,
que le **MCP** apporte le **sens** (couche sémantique) et que le **Harness** (du code, versionné et testé) apporte la
**confiance** en encadrant la puce et ses tool calls.

| Acte | Contenu actuel |
|---|---|
| 01 · L'IA | Sources publiques → particules fines qui forment la puce (dissolve) + « TRAINED ON THE WORLD » · 3 cas d'usage (mail, contrat, Excel) apparus ensemble (morphing) · utilisateur → fiche → « OUR CAR PARKS · PARIS? » · la puce consulte INTERNET + MÉMOIRE → « ~40? · SOURCE: WEB » |
| 02 · Notre réalité | Plongée dans « ~40? » → carte de Paris → France → monde (ordres de grandeur vagues, baies « DATABASES ») → 6 systèmes → 10 tables confuses · frontière en pointillé PUBLIC / PRIVATE |
| 03 · Le problème | Le câblage EST l'arbre (PARKINGS / + VOIRIE × SANS / AVEC DOUBLONS → tables différentes) · « AMBIGUOUS » · 2 essais (1.48 M, 2.41 M) · diagnostic SENS / CONFIANCE (morphing) |
| 04 · MCP | Câbles coupés · concepts (fiche de définition) · tables écartées · bonne réponse 1.12 M + mini-arbre |
| 05 · Harness | harness.py s'écrit → se compile en cadre autour de la puce · modules SCOPE/RIGHTS sur le tool call, FORMAT/TRACE sur la réponse · refus « plates » + DATA PROTECTED · audit.log |
| 06 · Ensemble | Circuit complet · modèle remplaçable · légende AI · REPLACEABLE / MCP · MEANING / HARNESS · TRUST |

## Fichiers
- `film.py` — la scène (acte par acte, `a_*`), textes FR + dictionnaire `EN`.
- `film_kit.py` (couleurs, néon, pistes, icônes, puce). Ancien trio `tron.py`/`story.py`/`presentation.py` archivé dans `_archives/gen2_code/`.
- `dev.sh`, `planche.py`, `build_auto_html.py`, `requirements.txt` (Manim 0.21 figé pour manim-slides).
- `_archives/` — versions précédentes (v6 dissolve, v7 arbre câblé, anciennes générations).
- `../Discours_Histoire_MCP_Harness.md` — ancien discours (plus aligné sur le film actuel).

## Commandes
```bash
./dev.sh dev13            # actes 1-3, 480p, page DEV13_Actes_1-3.html en boucle (~20 s)
./dev.sh dev              # film complet 480p + DEV_AI_Retrieving_dynamic_data.html (~30 s)
./dev.sh <acte> --planche # un acte : ia realite probleme mcp harness ensemble
FILM_LANG=fr ./dev.sh dev # version française (anglais par défaut)
./dev.sh final            # 1080p + MP4 + HTML — UNIQUEMENT après validation
```
Boutons PyCharm équivalents dans `.run/` (dossier « Film »).

## Règles de travail (validées)
- Toujours poser des questions QCM avant de modifier.
- Ne jamais lancer le rendu final sans validation ; itérer avec les versions dev (HTML).
- Archiver la version courante dans `_archives/` avant d'en commencer une nouvelle.
- Pas de chiffres précis (ordres de grandeur seulement) tant que les vrais chiffres Indigo ne sont pas fournis.

## En cours / prochaines étapes
- Focus actuel : actes 1-3 (≈1:18), optimisation du rythme et des transitions (morphing simultané élément par élément, FadeTransform).
- Points d'audit non traités : incohérence du refus (outil `plates` non exposé par le MCP), textes trop petits,
  « MONDE » à double sens, durée totale (~2:40).
- Le tilde de « ~40? » en Futura est haut — option « ≈ 40? ».

## Mise à jour 12 oct. 2026 (titre : « AI - Retrieving dynamic data »)
- 03 : panneau NO MAP (tables piochées au hasard), réponses dans le chat, « AMBIGUOUS » sous le titre.
- 04 : titre = « What does our data mean? », 5 domaines (voirie / hors voirie / parkings / abonnements / zones), panneau TOOL CALL,
  question reposée → ON-STREET (≠), tables condensées en DATA.
- 05 : harness = TOOLS (au-dessus de la puce) + FORMAT + SCOPE + RIGHTS + audit.log ; harness.py à droite (tests en « matrice »),
  question du directeur sans zone → SCOPE récupère WEST ZONE → 0.31 M ; fin condensée (harness / MCP / DATA).
- 06 : harness vide, CONFIANCE / COUCHE SÉMANTIQUE flashent, réponse → tableaux / graphiques / rapports renvoyés au chat.
- Badge utilisateur sous le chat dès l'acte 02 (INDIGO · USER → DIRECTOR · WEST ZONE).
- Commandes ajoutées : ./dev.sh dev4, ./dev.sh dev5. Archives : _archives/v9_final_en_2026-10-12/.
- Reste : renommer les fichiers de sortie, version FR, rendu final après validation.
- Nettoyage (13 oct.) : étape 1 code mort supprimé ; étape 2 actes renommés (a1_general_ai … a6_together),
  sorties renommées `AI_Retrieving_dynamic_data.(mp4|html)` / `DEV_AI_Retrieving_dynamic_data.html`. Voir `docs/AUDIT.md`.
  Étape 3 : `film_kit.py` remplace tron.py ; manim-slides retiré des dépendances (Manim reste à 0.21).
