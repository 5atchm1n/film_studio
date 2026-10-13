"""Film data: on-screen text (English source + FR), the business example, layout and map coordinates.

Figures are illustrative orders of magnitude (no real Indigo numbers).
"""

import numpy as np
from manim import *

from studio.kit import primitives as kit
from studio.kit.actors import (Badge, Band, Chat, Chip, CodeFile, Module, data_block, harness_clamps, harness_frame,
                               packet, panel_frame)
from studio.kit.i18n import Translator, current_lang
from studio.kit.layout import (ANS_IN, BAND_Y, BUS_Y, CHAT_C, CHAT_H, CHAT_W, CHIP_POS, DATA_Y, IN_X,
                               OUT_Y, USER_POS)
from studio.kit.motions import dim, morph, send, words_from_blocks
from studio.kit.primitives import (BODY, CYAN, DIMC, GREEN, ICE, LABEL, MONO, NEON_OPS, ORANGE, RED, TITLE, flash_along,
                                   globe, icon_check, icon_doc, icon_format, icon_list, icon_lock, icon_log, icon_mail,
                                   icon_scope, icon_sheet, icon_tool_card, icon_user, neon, rack, rail, square_dot)

FW = config.frame_width

# --- Language: FILM_LANG=en (default) or fr. On-screen text is written in English; FR holds the French. --
LANG = current_lang()
FR = {  # English source text → French
    "CHAT · AI": "CHAT · IA",
    "AI - Retrieving dynamic data": "IA - Récupérer des données dynamiques", "01 · THE AI": "01 · L'IA",
    "02 · OUR REALITY": "02 · NOTRE RÉALITÉ", "03 · THE PROBLEM": "03 · LE PROBLÈME",
    "04 · WHAT DOES OUR DATA MEAN?": "04 · QUE VEULENT DIRE NOS DONNÉES ?",
    "What does our data mean?": "Que veulent dire nos données ?",
    "05 · HARNESS → TRUST": "05 · HARNESS → LA CONFIANCE", "06 · TOGETHER": "06 · ENSEMBLE",
    "General AI": "L'IA générale", "Our reality": "Notre réalité", "The problem": "Le problème",
    "Harness: trust": "Harness : la confiance", "Together": "Ensemble", "AI": "IA", "BOOKS": "LIVRES",
    "PUBLIC DATA": "DONNÉES PUBLIQUES", "WRITE A CLIENT EMAIL": "RÉDIGE UN MAIL CLIENT", "EMAIL READY": "E-MAIL PRÊT",
    "SUMMARISE A CONTRACT": "RÉSUME UN CONTRAT", "5 KEY POINTS": "5 POINTS CLÉS",
    "WRITE AN EXCEL FORMULA": "ÉCRIS UNE FORMULE EXCEL", "FORMULA": "FORMULE", "GENERAL AI": "IA GÉNÉRALE",
    "FAST · VERSATILE": "RAPIDE · POLYVALENTE", "OUR CAR PARKS · PARIS?": "NOS PARKINGS · PARIS ?",
    "MEMORY": "MÉMOIRE", "SOURCE: WEB": "SOURCE : WEB", "WORLD": "MONDE", "TENS": "DES DIZAINES",
    "HUNDREDS": "DES CENTAINES", "THOUSANDS": "DES MILLIERS", "OF CAR PARKS": "DE PARKINGS",
    "MILLIONS": "DES MILLIONS", "TENS OF MILLIONS": "DES DIZAINES DE MILLIONS",
    "OF EVENTS / DAY": "D'ÉVÉNEMENTS / JOUR", "TERABYTES": "DES To", "HUNDREDS OF TB": "DES CENTAINES DE To",
    "PETABYTES": "DES Po", "STORED": "STOCKÉS", "DATABASES": "BASES DE DONNÉES", "SENSORS": "CAPTEURS",
    "TICKETING": "BILLETTERIE", "SUBSCRIPTIONS": "ABONNEMENTS", "MASTER DATA": "RÉFÉRENTIEL",
    "DOZENS OF SYSTEMS · HUNDREDS OF TABLES": "DES DIZAINES DE SYSTÈMES · DES CENTAINES DE TABLES",
    "PRIVATE": "PRIVÉ", "PARKING SESSIONS · PARIS · SEPT.?": "STATIONNEMENTS · PARIS · SEPT. ?",
    "DIRECT ACCESS TO TABLES": "ACCÈS DIRECT AUX TABLES", "AMBIGUOUS": "AMBIGUË",
    "4 DEFINITIONS → 4 ANSWERS": "4 DÉFINITIONS → 4 RÉPONSES", "CAR PARKS": "PARKINGS", "+ STREET": "+ VOIRIE",
    "NO DUPLICATES": "SANS DOUBLONS", "WITH DUPLICATES": "AVEC DOUBLONS", "1.12 M": "1,12 M", "1.48 M": "1,48 M",
    "1.86 M": "1,86 M", "2.41 M": "2,41 M", "SEMANTIC LAYER": "COUCHE SÉMANTIQUE", "TOOL CALL": "APPEL D'OUTIL",
    "TABLES": "TABLEAUX", "CHARTS": "GRAPHIQUES", "REPORTS": "RAPPORTS",
    "RETRIEVING DYNAMIC DATA": "RÉCUPÉRER DES DONNÉES DYNAMIQUES", "UNDERSTANDING": "COMPRÉHENSION",
    "DATA": "DONNÉES", "DIRECTOR": "DIRECTEUR", "USER": "UTILISATEUR",
    "PARKING SESSIONS · SEPT.?": "STATIONNEMENTS · SEPT. ?", "WEST ZONE": "ZONE OUEST", "0.31 M": "0,31 M",
    "OFF-STREET · WEST ZONE · 09/26": "HORS VOIRIE · ZONE OUEST · 09/26",
    "09:14 sessions · west OK": "09:14 sessions · ouest OK", "TOOLS": "OUTILS", "0.74 M": "0,74 M",
    "DEFAULT · CAR PARKS": "PAR DÉFAUT · PARKINGS", "NO MAP": "SANS CARTE", "DIRECT QUERY": "REQUÊTE DIRECTE",
    "SENT TO MCP": "ENVOYÉ AU MCP", "TRUST": "CONFIANCE",
    "WHAT DOES OUR DATA MEAN?": "QUE VEULENT DIRE NOS DONNÉES ?", "ON-STREET SESSIONS": "SESSIONS VOIRIE",
    "OFF-STREET SESSIONS": "SESSIONS HORS VOIRIE",
    "CAR PARKS · NO DUPLICATES · 09/26": "PARKINGS · SANS DOUBLONS · 09/26", "occupancy()": "occupation()",
    "capacity()": "capacite()", "contracts()": "contrats()", "customers()": "clients()", "scope()": "perimetre()",
    "pricing()": "tarifs()", "SCOPE": "PÉRIMÈTRE", "RIGHTS": "DROITS", "audit.log": "journal.log",
}


tr = Translator(FR, LANG)


def L(text, *a, **k):
    return kit.label(tr(text), *a, **k)


def T_(text, **k):
    """Translated Text()."""
    return Text(tr(text), **k)


# --- Business example (illustrative figures, to be replaced by real ones) -----------------------------
QUESTION = tr("PARKING SESSIONS · PARIS · SEPT.?")
CALL_OK = tr('stationnements("PARIS", "09/26")')
# tree of possibilities: 2 definitions × 2 ways of counting = 4 answers
TREE_L1 = [tr(x) for x in ["CAR PARKS", "+ STREET"]]
TREE_L2 = [tr(x) for x in ["NO DUPLICATES", "WITH DUPLICATES"]]
TREE_LEAVES = [tr(x) for x in ["1.12 M", "1.48 M", "1.86 M", "2.41 M"]]   # (P,no dup) (P,dup) (P+S,no dup) (P+S,dup)
TRIES = [1, 3]                                         # leaf picked at each attempt (never the right one)
GUESSES = [TREE_LEAVES[i] for i in TRIES]
GOOD = (tr("1.12 M"), tr("CAR PARKS · NO DUPLICATES · 09/26"))
QUESTION_ME = tr("PARKING SESSIONS · SEPT.?")            # no zone: the harness derives it from the user's rights
# the user's context grows act by act: 02 · 04 (with the MCP) · 05 (when SCOPE asks for it)
USER_CTX = [["INDIGO", "USER"], ["INDIGO", "DIRECTOR"], ["INDIGO", "DIRECTOR", "WEST ZONE"]]  # [1] unused
# Deliberately vague orders of magnitude (no precise figures until validated)
LEVELS = ["PARIS", "FRANCE", "WORLD"]
PARKS_MAG = ["TENS", "HUNDREDS", "THOUSANDS"]
EVENTS_MAG = ["THOUSANDS", "MILLIONS", "TENS OF MILLIONS"]
STORAGE_MAG = ["TERABYTES", "HUNDREDS OF TB", "PETABYTES"]
RACKS = [1, 5, 12]                         # databases lit per level
SYSTEMS = ["SENSORS", "TICKETING", "SUBSCRIPTIONS", "CRM", "FINANCE", "MASTER DATA"]
# deliberately confusing tables: duplicates, versions, temp tables, overlapping notions
TABLES = ["stn_evt_raw", "stn_evt_v2", "stn_v2_bkp", "stat_park_tmp", "pk_site_ref", "tkt_pass_24",
          "voirie_horod", "abo_ctr_24", "zone_idf_map", "cpt_old_2019"]
CONCEPTS = [("ON-STREET SESSIONS", 6), ("OFF-STREET SESSIONS", 0), ("CAR PARKS", 4), ("SUBSCRIPTIONS", 7), ("ZONES", 8)]
CONCEPT_TABLES = [[6], [0, 5], [4], [7], [8]]   # tables read by each MCP domain
TEXT_DIM = 0.6                                  # act 03: tree labels stay readable when dimmed
BOTTOM_DIM = 0.25                               # act 03: wiring and tree dimmed while the panel is shown
CHIP_IN_HARNESS = 0.8                           # chip scale once inside the harness
RUN_LINES = ["check_format(question)", "tools = mcp.list_tools()", "scope = user.zone()",
             "assert user.can_read(tool)", "data = mcp.call(tool, scope)", "log.trace(request)"]
GATE_LINE = {0: 0, 1: 2, 2: 3, 3: 5}               # harness module → line of harness.py that runs
TOOLS_H = 1.2                                  # height of the TOOLS step, above the chip
SEL = 1                                         # domain picked for the question (off-street = car parks)
# each domain exposes 2 tools, each tool reads one table (almost every valid table is wired)
TOOLS = [[("sessions()", 0), ("occupancy()", 5)], [("sites()", 4), ("capacity()", 6)],
         [("contracts()", 7), ("customers()", 7)], [("scope()", 8), ("pricing()", 6)]]
LEAF_TABLES = [[0], [0, 2], [1, 6], [3, 6, 9]]   # tables read by each definition (tree leaf)

# --- Diagram layout (standard anchors in studio.kit.layout; film-specific positions here) ----------------
FRAME = (np.array([0.225, 0.575, 0]), 5.55, 3.65)          # the Harness surrounds the chip
GATES = [  # (name, icon, position, label side)  — in the order of the lines of harness.py
    ("FORMAT", icon_format, np.array([-2.55, OUT_Y, 0]), DOWN),   # on the way in, before the chip
    ("SCOPE", icon_scope, np.array([-1.2, -0.25, 0]), LEFT),
    ("RIGHTS", icon_lock, np.array([-1.2, -0.9, 0]), LEFT),
    ("TRACE", icon_log, np.array([1.6, OUT_Y, 0]), DOWN),
]
JOURNAL_C = np.array([1.85, OUT_Y, 0])   # the audit log lives in the harness, instead of the TRACE icon
TABLE_XS = list(np.linspace(-6.1, 6.1, 10))
J1_POS = [np.array([-3.6, -0.95, 0]), np.array([3.0, -0.95, 0])]   # branch CAR PARKS / + STREET
J2_DX, J2_Y = 1.3, -1.85                                            # branch NO / WITH DUPLICATES

# --- Map ------------------------------------------------------------------------------------------------
MAP_C = np.array([-18.0, 0.0, 0])
# Act 02 split screen: the map (built around MAP_C) is scaled down and placed below the boundary
SPLIT_Y = -0.02                                   # PUBLIC (top) / PRIVATE (bottom) boundary
TOP_Y = 2.45                                    # the boundary rises to here when our world unfolds
PV_K = 0.9                                      # scale of the private area
PV_REF = MAP_C + np.array([1.05, -0.075, 0])    # centre of the map content
PV_DEST = np.array([0.1, -0.85, 0])             # where that centre appears on screen
PUSH = dict(scale=0.45, to=np.array([-1.4, 3.25, 0]))  # the chip (and the user) pushed to the top
MC = MAP_C + UP * 0.3
COS = np.cos(np.radians(48))
FR_C, FR_K = (2.5, 46.6), 0.56
EU_C, EU_K = (10.0, 52.0), 0.19
FRANCE = [(2.5, 51.1), (4.2, 50.0), (8.2, 49.0), (7.5, 47.5), (6.8, 46.4), (7.6, 45.2), (7.0, 44.0), (7.5, 43.7),
          (4.8, 43.3), (3.1, 43.2), (3.2, 42.4), (1.5, 42.5), (-1.8, 43.4), (-1.2, 46.0), (-2.2, 47.2), (-4.7, 48.5),
          (-1.6, 48.7), (-1.5, 49.7), (0.2, 49.5), (1.6, 50.9), (2.5, 51.1)]
FR_CITIES = [(2.35, 48.85, 9), (4.85, 45.76, 4), (5.37, 43.3, 3), (3.06, 50.63, 3), (-0.58, 44.84, 3), (1.44, 43.6, 3),
             (-1.55, 47.2, 3), (7.75, 48.58, 2), (7.26, 43.7, 2), (-1.68, 48.11, 2), (3.88, 43.61, 2), (5.72, 45.19, 2)]
WORLD_DOTS = [(0.22, 0.55), (0.27, 0.5), (0.3, 0.58), (0.2, 0.47), (0.33, 0.52), (0.25, 0.6), (-0.55, 0.45),
              (-0.48, 0.38), (-0.62, 0.52), (-0.42, 0.5), (-0.3, -0.25), (-0.25, -0.38), (-0.33, -0.12), (0.62, 0.38),
              (0.7, 0.3)]


def ll(lon, lat, k, c, center=MC):
    return center + np.array([(lon - c[0]) * COS * k, (lat - c[1]) * k, 0])


TASK_ICONS = [icon_mail, icon_doc, icon_sheet]
