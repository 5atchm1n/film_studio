"""The Stage: everything the beats hand to each other, in one place (see film.py)."""

from dataclasses import dataclass


@dataclass(slots=True)
class Stage:
    """Everything the beats hand to each other, in one place. Created once (Film.build_stage); slots=True makes a
    typo or an attribute invented inside a beat fail immediately. Grouped by the act that first sets it."""
    # 01 · the AI
    chip: object = None
    in_rail: object = None
    intro_bits: object = None
    out_rail: object = None
    public: object = None
    sources: object = None
    traces: object = None
    user: object = None
    # 02 · our reality
    badge: object = None
    count: object = None
    count_lbl: object = None
    ev_count: object = None
    ev_lbl: object = None
    frontier: object = None
    level_lbl: object = None
    paris: object = None
    parks: object = None
    pushed: object = None
    rack_lbl: object = None
    racks: object = None
    racks_on: object = 0
    st_count: object = None
    st_lbl: object = None
    unfold: object = None
    # 02 · zoom out
    tables: object = None
    vault: object = None
    # 03 · the problem
    p3: object = None
    p3_call: object = None
    p3_grid: object = None
    p3_rail: object = None
    question: object = None
    reply: object = None
    # 03 · wiring (build_wiring)
    chaos: object = None
    cut_pts: object = None
    j1_pos: object = None
    j2_pos: object = None
    joints: object = None
    seg1: object = None
    seg2: object = None
    seg3: object = None
    # 03 · NO MAP panel (table_panel)
    p3_box: object = None
    # 03 · guesses
    amb_sub: object = None
    doubts: object = None
    tree: object = None
    # 03 · semantic layer
    band_ph: object = None
    band_shape: object = None
    box_shape: object = None
    mcp: object = None
    sens_lbl: object = None
    sens_sub: object = None
    # 04 · MCP
    band: object = None
    band_label: object = None
    bus: object = None
    bus_pts: object = None
    chat_extra: object = None
    data_box: object = None
    lit: object = None
    lit_ok: object = None
    mini: object = None
    nodes: object = None
    p4_alt: object = None
    roots: object = None
    trunk: object = None
    trunk_pts: object = None
    # 05 · harness
    background: object = None
    clamps: object = None
    code: object = None
    frame: object = None
    frame_label: object = None
    gates: object = None
    log_top: object = None
    logs: object = None
    strip: object = None
    tag: object = None
    tests: object = None
    # 05 · scoped question
    ok: object = None
    # 05 · scope lookup
    scope_pill: object = None
    # 05 · condense
    condensed: object = False
    tools_icon: object = None
    # hand-offs between beats of the same act (beats are cut where the viewer reads)
    use_cases: object = None      # 01: tasks, results, tag, rails — morph into the chat
    u_bub: object = None          # 01: the first question bubble
    world: object = None          # 02: globe + its data dots
    count_txt: object = None      # 03: "4 DEFINITIONS → 4 ANSWERS"
    guess_rng: object = None      # 03: the random picks of both attempts
    sens_mid: object = None       # 03: SEMANTIC LAYER, centred, before it rises
    tool_steps: object = None     # 04: [domain grid, (call, sent)] of the TOOL CALL panel
    used_table: object = None     # 04: the table read by the first call
    second: object = None         # 04: second attempt — lit path, its table, its call, the wrong answer
    descs: object = None          # 05: tool descriptions + the scan around the picked one
    outs: object = None           # 06: tables · charts · reports
    words: object = None          # 06: TRUST · SEMANTIC LAYER · RETRIEVING DYNAMIC DATA
