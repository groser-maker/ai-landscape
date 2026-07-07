#!/usr/bin/env python3
"""Generate web/index.html from data/ai-landscape.json"""
import json, os, math

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE, "data", "ai-landscape.json")
OUT_FILE  = os.path.join(BASE, "docs", "index.html")

with open(DATA_FILE) as f:
    data = json.load(f)

companies = data["companies"]
last_updated = data["last_updated"]
snapshots = data.get("weekly_snapshots", [])

# ── Helpers ────────────────────────────────────────────────────────────────
def get_latest_snap(company_id):
    for s in reversed(snapshots):
        for e in s["entries"]:
            if e["company_id"] == company_id:
                return e
    return {}

def fmt_b(n):
    if n is None: return "—"
    if n >= 1000: return f"${n/1000:.1f}T"
    if n >= 1:    return f"${n:.1f}B"
    return f"${n*1000:.0f}M"

def fmt_head(n):
    if n is None: return "—"
    if n >= 1000000: return f"{n/1000000:.1f}M"
    if n >= 1000:    return f"~{n//1000}K"
    return f"~{n}"

def conf_dot(c):
    cls = {"high":"conf-high","medium":"conf-medium","low":"conf-low","carried_forward":"conf-carried"}.get(c,"conf-carried")
    return f'<span class="conf-dot {cls}" title="{c}"></span>'

def event_icon(t):
    icons = {"model_release":"🧠","product_launch":"🚀","funding":"💰","partnership":"🤝",
             "leadership":"👤","business":"📈","regulatory":"⚖️","research":"🔬"}
    return icons.get(t,"📌")

def get_ceo(company):
    for l in company.get("leadership",[]):
        if "ceo" in l["title"].lower() and not l.get("departed"):
            return l["name"]
    return "—"

def get_flagship(company):
    for p in company.get("products",[]):
        if p.get("flagship"): return p["name"]
    return "—"

SECTIONS_ORDER = ["Frontier AI","Foundation Model Labs","Big Tech AI","AI Applications","AI Infrastructure","AI Startups"]
SECTION_ICONS  = {"Frontier AI":"🔬","Foundation Model Labs":"🏗️","Big Tech AI":"🏢","AI Applications":"💡","AI Infrastructure":"⚙️","AI Startups":"🚀"}

def companies_in(section):
    return [c for c in companies if c["section"] == section]

# ── Per-company dual-axis chart ────────────────────────────────────────────
# Only for Frontier AI + Foundation Model Labs
CHART_SECTIONS = {"Frontier AI","Foundation Model Labs","AI Startups"}

def make_company_chart(company):
    """Returns SVG + popup HTML for dual-axis chart.
    Left Y  = LMSYS ELO score (capability, linear 950–1500)
    Right Y = Funding round amount ($B, linear)
    Bubble size = model parameters (log-scaled radius)
    """
    cid = company["id"]
    models   = company.get("model_history") or []
    rounds   = company.get("funding_rounds_history") or []
    if not models and not rounds:
        return '<p class="no-chart-data">No model or funding history available.</p>'

    # X axis: months since 2022-11 (0 = Nov 2022)
    def x_month(ym):
        y, m = int(ym[:4]), int(ym[5:7])
        return (y - 2022) * 12 + (m - 11)

    all_x = [x_month(m["date"]) for m in models] + [x_month(r["date"]) for r in rounds]
    if not all_x: return ""
    x_max = max(max(all_x), x_month(last_updated[:7])) + 2

    # SVG dimensions — taller to give labels room
    W, H = 700, 240
    PAD_L, PAD_R, PAD_T, PAD_B = 62, 68, 22, 44
    CW = W - PAD_L - PAD_R
    CH = H - PAD_T - PAD_B

    def xp(xm):
        return PAD_L + CW * xm / x_max

    # ── Left Y: ELO score (linear 950–1500) ──────────────────────────────
    ELO_MIN, ELO_MAX = 950, 1500
    elo_vals = [m["elo_score"] for m in models if m.get("elo_score")]

    def yp_elo(elo):
        elo = max(ELO_MIN, min(ELO_MAX, elo))
        return PAD_T + CH * (1 - (elo - ELO_MIN) / (ELO_MAX - ELO_MIN))

    # ── Right Y: funding (linear) ─────────────────────────────────────────
    fund_vals = [r["amount_usd_billions"] for r in rounds if r.get("amount_usd_billions")]
    fund_max  = max(fund_vals) * 1.3 if fund_vals else 10

    def yp_fund(fb):
        fb = max(0, min(fb, fund_max))
        return PAD_T + CH * (1 - fb / fund_max)

    # ── Bubble radius from parameters (log scale, 4–14px) ─────────────────
    def bubble_r(pb):
        if not pb or pb <= 0:
            return 6   # default when unknown
        # log10(7) ≈ 0.85 → r=5;  log10(405) ≈ 2.6 → r=13
        r = 4 + 10 * (math.log10(pb) - math.log10(1)) / (math.log10(1000) - math.log10(1))
        return max(4, min(14, r))

    popup_divs  = []
    fund_popups = []
    lines = []

    lines.append(f'<svg viewBox="0 0 {W} {H}" width="100%" style="display:block">')
    lines.append(f'  <defs><clipPath id="clip-{cid}"><rect x="{PAD_L}" y="{PAD_T}" width="{CW}" height="{CH}"/></clipPath></defs>')
    lines.append(f'  <rect x="{PAD_L}" y="{PAD_T}" width="{CW}" height="{CH}" fill="#F8FAFC" rx="3"/>')

    # ── ELO gridlines (left Y) ─────────────────────────────────────────────
    elo_ticks = [1000, 1100, 1200, 1300, 1400, 1500]
    for ev in elo_ticks:
        if ev < ELO_MIN or ev > ELO_MAX: continue
        y = yp_elo(ev)
        lines.append(f'  <line x1="{PAD_L}" y1="{y:.1f}" x2="{PAD_L+CW}" y2="{y:.1f}" stroke="#E4E9F0" stroke-width="1"/>')
        lines.append(f'  <text x="{PAD_L-5}" y="{y+3.5:.1f}" text-anchor="end" font-size="9" fill="#706E6B">{ev}</text>')

    # ── Funding gridlines (right Y, subtle) ───────────────────────────────
    for i in range(1, 5):
        fv = fund_max * i / 4
        y  = yp_fund(fv)
        lbl = fmt_b(fv).replace("$","")
        lines.append(f'  <line x1="{PAD_L}" y1="{y:.1f}" x2="{PAD_L+CW}" y2="{y:.1f}" stroke="#DDEEFF" stroke-width="0.6" stroke-dasharray="4,3"/>')
        lines.append(f'  <text x="{PAD_L+CW+5}" y="{y+3.5:.1f}" font-size="9" fill="#0070D2">{lbl}</text>')
    # Right Y zero label
    y0lbl = yp_fund(0)
    lines.append(f'  <text x="{PAD_L+CW+5}" y="{y0lbl+3.5:.1f}" font-size="9" fill="#0070D2">0</text>')

    # ── X axis: year markers ───────────────────────────────────────────────
    for yr in range(2023, 2028):
        xm = (yr - 2022) * 12 - 11
        if xm < 0 or xm > x_max: continue
        xpx = xp(xm)
        lines.append(f'  <line x1="{xpx:.1f}" y1="{PAD_T}" x2="{xpx:.1f}" y2="{PAD_T+CH}" stroke="#D8DFE8" stroke-width="1" stroke-dasharray="4,3"/>')
        lines.append(f'  <text x="{xpx:.1f}" y="{PAD_T+CH+13}" text-anchor="middle" font-size="10" fill="#706E6B">{yr}</text>')

    # ── Funding bars ───────────────────────────────────────────────────────
    bar_w = max(10, min(22, CW / max(x_max, 1) * 0.7))
    for r_idx, r in enumerate(rounds):
        amt = r.get("amount_usd_billions")
        if not amt: continue
        xm  = x_month(r["date"])
        xpx = xp(xm)
        y0  = yp_fund(0)
        y1  = yp_fund(amt)
        bh  = max(2, y0 - y1)
        fp_id = f"fp-{cid}-{r_idx}"
        lines.append(
            f'  <rect x="{xpx-bar_w/2:.1f}" y="{y1:.1f}" width="{bar_w:.1f}" height="{bh:.1f}" '
            f'fill="#0070D2" opacity="0.55" rx="2" style="cursor:pointer" '
            f'onclick="showFundPopup(\'{fp_id}\',this)" class="fund-bar">'
            f'</rect>'
        )
        # Amount label above bar if room
        if bh > 14:
            lbl = fmt_b(amt).replace("$","")
            lines.append(f'  <text x="{xpx:.1f}" y="{y1-3:.1f}" text-anchor="middle" font-size="8" fill="#0055AA" font-weight="600" pointer-events="none">{lbl}</text>')
        # Build funding popup
        inv_list = r.get("investors") or []
        inv_str = ", ".join(inv_list) if inv_list else "—"
        val_str = fmt_b(r.get("valuation_usd_billions")) if r.get("valuation_usd_billions") else "—"
        fund_popups.append({
            "id": fp_id,
            "date": r["date"],
            "type": r.get("type",""),
            "amount": fmt_b(amt),
            "lead": r.get("lead_investor","—") or "—",
            "valuation": val_str,
            "investors": inv_str,
        })

    # ── Model bubbles + labels ─────────────────────────────────────────────
    # Pre-compute positions for deconfliction
    dot_positions = []
    for idx, m in enumerate(models):
        elo = m.get("elo_score")
        if elo is None:
            yy = PAD_T + CH * 0.55  # grey band for unknown ELO
        else:
            yy = yp_elo(elo)
        xpx = xp(x_month(m["date"]))
        r_dot = bubble_r(m.get("parameters_billions"))
        dot_positions.append((xpx, yy, r_dot))

    for idx, m in enumerate(models):
        xpx, yy, r_dot = dot_positions[idx]
        pb  = m.get("parameters_billions")
        elo = m.get("elo_score")
        pnote_safe = (m.get("parameters_note","") or "").replace("'","&#39;")
        param_str  = f'{pb}B' if pb else (pnote_safe or "undisclosed")
        ctx_str    = f'{m["context_length_k"]}K tokens' if m.get("context_length_k") else "standard"
        popup_id   = f"pop-{cid}-{idx}"
        elo_est    = m.get("elo_estimated", True)
        elo_label  = f'{elo}{"*" if elo_est else ""}' if elo else "N/A"
        dot_fill   = company["color"] if elo else "#AABBCC"
        dot_stroke = "white"

        lines.append(
            f'  <circle cx="{xpx:.1f}" cy="{yy:.1f}" r="{r_dot:.1f}" fill="{dot_fill}" '
            f'opacity="0.88" stroke="{dot_stroke}" stroke-width="1.5" style="cursor:pointer" '
            f'onclick="showModelPopup(\'{popup_id}\',this)" class="model-dot" clip-path="url(#clip-{cid})">'
            f'<title>{m["name"]} — ELO {elo_label} — Params: {param_str}</title>'
            f'</circle>'
        )
        popup_divs.append({
            "id": popup_id,
            "name": m["name"],
            "date": m["date"],
            "type": m.get("type",""),
            "params": param_str,
            "context": ctx_str,
            "purpose": m.get("purpose",""),
            "notes": m.get("notes",""),
            "elo": elo_label,
            "elo_est": elo_est,
        })

        # Labels for notable models — deconflict by staggering vertically
        if m.get("notable") and r_dot > 0:
            label = m["name"]
            if len(label) > 18: label = label[:16] + "…"
            # Alternate label above/below for adjacent models in time
            stagger_down = (idx % 2 == 1)
            if stagger_down:
                lx, ly = xpx, yy + r_dot + 10
                anchor = "middle"
                # line from dot to label
                lines.append(f'  <line x1="{xpx:.1f}" y1="{yy+r_dot:.1f}" x2="{lx:.1f}" y2="{ly-2:.1f}" stroke="{dot_fill}" stroke-width="0.7" opacity="0.5" pointer-events="none"/>')
            else:
                lx, ly = xpx, yy - r_dot - 4
                anchor = "middle"
                lines.append(f'  <line x1="{xpx:.1f}" y1="{yy-r_dot:.1f}" x2="{lx:.1f}" y2="{ly+2:.1f}" stroke="{dot_fill}" stroke-width="0.7" opacity="0.5" pointer-events="none"/>')
            # Clamp label inside chart horizontally
            lx = max(PAD_L + 20, min(PAD_L + CW - 20, lx))
            lines.append(
                f'  <text x="{lx:.1f}" y="{ly:.1f}" text-anchor="{anchor}" '
                f'font-size="8.5" fill="{dot_fill}" font-weight="600" pointer-events="none"'
                f'>{label}</text>'
            )

    # ── Axis titles ────────────────────────────────────────────────────────
    mid_y = PAD_T + CH // 2
    lines.append(f'  <text x="12" y="{mid_y}" text-anchor="middle" font-size="9" fill="#555" transform="rotate(-90,12,{mid_y})">LMSYS ELO Score</text>')
    right_x = PAD_L + CW + PAD_R - 8
    lines.append(f'  <text x="{right_x}" y="{mid_y}" text-anchor="middle" font-size="9" fill="#0055AA" transform="rotate(90,{right_x},{mid_y})">Funding ($B)</text>')

    # ── Legend (inside chart, bottom-left) ────────────────────────────────
    leg_y = PAD_T + CH + 28
    leg_x = PAD_L
    lines.append(f'  <circle cx="{leg_x+6}" cy="{leg_y-3}" r="5" fill="{company["color"]}" opacity="0.88" stroke="white" stroke-width="1"/>')
    lines.append(f'  <text x="{leg_x+14}" y="{leg_y}" font-size="8.5" fill="#333">Model (Y=ELO, size=params, click for detail)</text>')
    lines.append(f'  <circle cx="{leg_x+6}" cy="{leg_y-3}" r="3" fill="#AABBCC" opacity="0.88" stroke="white" stroke-width="1" transform="translate(215,0)"/>')
    lines.append(f'  <text x="{leg_x+229}" y="{leg_y}" font-size="8.5" fill="#888">ELO estimated*</text>')
    lines.append(f'  <rect x="{leg_x+295}" y="{leg_y-9}" width="11" height="9" fill="#0070D2" opacity="0.55" rx="1"/>')
    lines.append(f'  <text x="{leg_x+309}" y="{leg_y}" font-size="8.5" fill="#0055AA">Funding round (click for detail)</text>')

    lines.append("</svg>")

    # ── Model popup divs ───────────────────────────────────────────────────
    for p in popup_divs:
        notes_html = f'<div class="mp-notes">{p["notes"]}</div>' if p["notes"] else ""
        elo_flag   = ' <span class="mp-est">estimated</span>' if p["elo_est"] and p["elo"] != "N/A" else ""
        lines.append(
            f'<div id="{p["id"]}" class="model-popup" style="display:none">'
            f'<div class="mp-header"><span class="mp-name">{p["name"]}</span>'
            f'<span class="mp-date">{p["date"]}</span>'
            f'<button class="mp-close" onclick="closePopup(\'{p["id"]}\')">✕</button></div>'
            f'<div class="mp-body">'
            f'<div class="mp-row"><span>Type</span><span>{p["type"]}</span></div>'
            f'<div class="mp-row"><span>LMSYS ELO</span><span>{p["elo"]}{elo_flag}</span></div>'
            f'<div class="mp-row"><span>Parameters</span><span>{p["params"]}</span></div>'
            f'<div class="mp-row"><span>Context</span><span>{p["context"]}</span></div>'
            f'<div class="mp-purpose">{p["purpose"]}</div>'
            f'{notes_html}'
            f'</div></div>'
        )

    # ── Funding popup divs ─────────────────────────────────────────────────
    for fp in fund_popups:
        lines.append(
            f'<div id="{fp["id"]}" class="fund-popup" style="display:none">'
            f'<div class="mp-header fp-header"><span class="mp-name">{fp["type"]}</span>'
            f'<span class="mp-date">{fp["date"]}</span>'
            f'<button class="mp-close" onclick="closePopup(\'{fp["id"]}\')">✕</button></div>'
            f'<div class="mp-body">'
            f'<div class="mp-row"><span>Amount</span><span class="fp-amount">{fp["amount"]}</span></div>'
            f'<div class="mp-row"><span>Lead Investor</span><span>{fp["lead"]}</span></div>'
            f'<div class="mp-row"><span>Post-Money Val.</span><span>{fp["valuation"]}</span></div>'
            f'<div class="mp-row fp-inv-row"><span>All Investors</span><span class="fp-inv">{fp["investors"]}</span></div>'
            f'</div></div>'
        )

    return "\n".join(lines)

# ── Build scoreboard rows ──────────────────────────────────────────────────
def scoreboard_rows():
    rows = []
    for c in companies:
        s = get_latest_snap(c["id"])
        val = (f'<span class="fin-na">{c["funding_summary"].get("ticker","Public")}</span>'
               if c["funding_summary"].get("public") else
               fmt_b(s.get("valuation_usd_billions")) + conf_dot(s.get("valuation_confidence","low")))
        hc = fmt_head(s.get("headcount_estimate")) + conf_dot(s.get("headcount_confidence","low")) if s else "—"
        news = s.get("recent_news",[]) if s else []
        has_high = any(n["significance"]=="high" for n in news)
        news_html = (f'<span class="news-pill news-high-sig">{len(news)} (HIGH)</span>' if has_high and news else
                     f'<span class="news-pill news-has">{len(news)}</span>' if news else
                     '<span class="news-0">—</span>')
        rows.append(
            f'<tr data-section="{c["section"]}">'
            f'<td><a href="#card-{c["id"]}" class="co-link"><span class="co-emoji">{c["emoji"]}</span><span class="co-name">{c["name"]}</span></a></td>'
            f'<td><span class="section-badge">{c["section"]}</span></td>'
            f'<td>{get_ceo(c)}</td>'
            f'<td>{hc}</td>'
            f'<td>{val}</td>'
            f'<td>{get_flagship(c)}</td>'
            f'<td>{news_html}</td>'
            f'</tr>'
        )
    return "\n".join(rows)

# ── Build company cards ────────────────────────────────────────────────────
def build_card(c):
    s = get_latest_snap(c["id"])
    fs = c["funding_summary"]
    leaders = [l for l in c.get("leadership",[]) if not l.get("departed")][:3]
    flagship = next((p for p in c.get("products",[]) if p.get("flagship")), None)
    other_products = [p for p in c.get("products",[]) if not p.get("flagship")][:6]

    # Financial rows
    fin = []
    if fs.get("public"):
        fin.append(f'<div class="fin-row"><span class="fin-label">Status</span><span class="fin-value">Public ({fs.get("ticker","")})</span></div>')
    else:
        if s:
            fin.append(f'<div class="fin-row"><span class="fin-label">Valuation</span><span class="fin-value">{fmt_b(s.get("valuation_usd_billions"))}{conf_dot(s.get("valuation_confidence","low"))}</span></div>')
        if fs.get("total_raised_usd_billions"):
            fin.append(f'<div class="fin-row"><span class="fin-label">Total Raised</span><span class="fin-value">{fmt_b(fs["total_raised_usd_billions"])}</span></div>')
        if s and s.get("arr_usd_billions"):
            fin.append(f'<div class="fin-row"><span class="fin-label">ARR (est.)</span><span class="fin-value">{fmt_b(s["arr_usd_billions"])}{conf_dot(s.get("arr_confidence","low"))}</span></div>')
    if s:
        fin.append(f'<div class="fin-row"><span class="fin-label">Employees</span><span class="fin-value">{fmt_head(s.get("headcount_estimate"))}{conf_dot(s.get("headcount_confidence","low"))}</span></div>')
    fin.append(f'<div class="fin-row"><span class="fin-label">Founded</span><span class="fin-value">{c["founded"]} · {c["hq"]}</span></div>')

    # Acquisitions
    acqs = c.get("acquisitions") or []
    acq_html = ""
    if acqs:
        items = "".join(f'<div class="acq-item"><span class="acq-name">{a["name"]}</span> <span class="acq-date">{a["date"]}</span><div class="acq-desc">{a["description"]} <em>({a["amount_note"]})</em></div></div>' for a in acqs)
        acq_html = f'<div class="card-sub-section"><h5>Acquisitions</h5>{items}</div>'

    # Investors
    investors = c.get("notable_investors") or []
    inv_html = ""
    if investors:
        pills = "".join(f'<span class="inv-pill">{i}</span>' for i in investors[:8])
        inv_html = f'<div class="card-sub-section"><h5>Notable Investors</h5><div class="inv-pills">{pills}</div></div>'

    # News
    news = s.get("recent_news",[])[:3] if s else []
    news_html = ("".join(
        f'<div class="news-item"><span class="news-badge sig-{n["significance"]}">{event_icon(n["type"])} {n["significance"].upper()}</span>'
        f'<span class="news-headline">{n["headline"]}</span></div>'
        for n in news
    ) if news else '<div class="no-news">No events in this snapshot</div>')

    # Chart (only for frontier/foundation)
    chart_html = ""
    if c["section"] in CHART_SECTIONS:
        chart_html = f'''
    <div class="card-chart-section">
      <div class="chart-header">
        <span>📊 Model Capability (ELO) &amp; Funding Rounds Over Time</span>
      </div>
      <div class="chart-area" id="chart-{c["id"]}">
        {make_company_chart(c)}
      </div>
    </div>'''

    flagship_html = (
        f'<div class="product-item product-flagship"><div class="product-name">⭐ {flagship["name"]}</div>'
        f'<div class="product-type">{flagship["type"]} · {flagship["description"]}</div></div>'
    ) if flagship else ""

    other_html = "".join(
        f'<div class="product-item"><div class="product-name">{p["name"]}</div>'
        f'<div class="product-type">{p["type"]}</div></div>'
        for p in other_products
    )

    tags_html = "".join(f'<span class="tag">{t}</span>' for t in (c.get("tags") or []))

    return f'''<div class="company-card" id="card-{c["id"]}">
  <div class="card-header" style="background:{c["color"]}">
    <span class="card-emoji">{c["emoji"]}</span>
    <div class="card-title-block"><h4>{c["name"]}</h4><div class="card-section-tag">{c["section"]}</div></div>
    <div class="card-updated">Updated {last_updated}</div>
  </div>
  <div class="card-body">
    <div class="card-col">
      <h5>Leadership</h5>
      {"".join(f'<div class="leader-item"><div class="leader-name">{l["name"]}</div><div class="leader-title">{l["title"]}</div></div>' for l in leaders)}
      <h5 style="margin-top:10px">Products</h5>
      {flagship_html}{other_html}
      <div class="tags">{tags_html}</div>
    </div>
    <div class="card-col">
      <h5>Financials</h5>
      {"".join(fin)}
      {acq_html}
      {inv_html}
    </div>
  </div>
  {chart_html}
  <div class="card-footer">
    <h5>Recent Events</h5>
    {news_html}
  </div>
</div>'''

# ── Build all section blocks ───────────────────────────────────────────────
def build_sections():
    blocks = []
    for sec in SECTIONS_ORDER:
        cos = companies_in(sec)
        if not cos: continue
        icon = SECTION_ICONS.get(sec,"")
        cards = "\n".join(build_card(c) for c in cos)
        blocks.append(f'''
<div class="company-section-wrapper" data-section="{sec}">
  <div class="company-section-header">
    <h3>{icon} {sec}</h3>
    <div class="csh-sub">{len(cos)} {"companies" if len(cos)>1 else "company"}</div>
  </div>
  <div class="cards-grid">{cards}</div>
</div>''')
    return "\n".join(blocks)

# ── Hero stats ─────────────────────────────────────────────────────────────
def hero_stats():
    snap = snapshots[-1] if snapshots else None
    total_events = sum(len(e.get("recent_news",[])) for e in snap["entries"]) if snap else 0
    private_cos = [c for c in companies if not c["funding_summary"].get("public")]
    total_raised = sum(c["funding_summary"].get("total_raised_usd_billions",0) or 0 for c in private_cos)
    top_val_co = max(private_cos, key=lambda c: c["funding_summary"].get("valuation_usd_billions",0) or 0, default=None)
    # Most active this snap
    most_active = None
    if snap:
        best = max(snap["entries"], key=lambda e: len(e.get("recent_news",[])), default=None)
        if best:
            most_active = next((c for c in companies if c["id"]==best["company_id"]), None)

    s1 = f'<div class="hero-stat"><div class="label">Private Funding Tracked</div><div class="value">{fmt_b(total_raised)}</div><div class="sub">across independent labs</div></div>'
    s2 = (f'<div class="hero-stat"><div class="label">Largest Private Valuation</div><div class="value">{top_val_co["emoji"]} {top_val_co["name"]}</div><div class="sub">{fmt_b(top_val_co["funding_summary"]["valuation_usd_billions"])} est.</div></div>'
          if top_val_co else "")
    s3 = (f'<div class="hero-stat"><div class="label">Most Active This Snapshot</div><div class="value">{most_active["emoji"]} {most_active["name"]}</div><div class="sub">{total_events} total events</div></div>'
          if most_active else "")
    s4 = f'<div class="hero-stat"><div class="label">Model Histories Tracked</div><div class="value">{sum(len(c.get("model_history") or []) for c in companies)}</div><div class="sub">from Nov 2022 → {last_updated}</div></div>'
    return s1+s2+s3+s4

# ── Trend charts (valuation/headcount over time) ───────────────────────────
def build_trend_charts():
    if len(snapshots) < 2:
        return '<p style="color:#706E6B;font-style:italic;font-size:0.88rem">Trend charts appear after 2+ weekly snapshots.</p>'

    dates = [s["snapshot_date"] for s in snapshots]
    W, H = 1060, 180
    pL, pR, pT, pB = 55, 20, 15, 28
    cW, cH = W-pL-pR, H-pT-pB

    def xpos(i): return pL + cW*(i/(len(dates)-1)) if len(dates)>1 else pL
    def ypos(v, minY, maxY):
        r = maxY-minY or 1
        return pT + cH*(1-(v-minY)/r)

    def make_chart(title, field, label_fn, filter_fn=None):
        datasets = []
        for c in companies:
            if filter_fn and not filter_fn(c): continue
            pts = []
            for i,s in enumerate(snapshots):
                e = next((x for x in s["entries"] if x["company_id"]==c["id"]),None)
                if e and e.get(field) is not None:
                    pts.append({"i":i,"v":e[field]})
            if len(pts) >= 2:
                datasets.append({"c":c,"pts":pts})
        if not datasets: return ""
        all_vals = [p["v"] for d in datasets for p in d["pts"]]
        minY, maxY = 0, max(all_vals)*1.1 or 1

        svg = [f'<svg viewBox="0 0 {W} {H+pB}" style="width:100%;height:{H+pB}px">']
        for g in range(5):
            y = pT + cH*g/4
            val = maxY*(1-g/4)
            svg.append(f'<line x1="{pL}" y1="{y:.0f}" x2="{pL+cW}" y2="{y:.0f}" stroke="#E4E9F0" stroke-width="1"/>')
            svg.append(f'<text x="{pL-5}" y="{y+4:.0f}" text-anchor="end" font-size="10" fill="#706E6B">{label_fn(val)}</text>')
        step = max(1, len(dates)//8)
        for i,d in enumerate(dates):
            if i%step==0:
                x = xpos(i)
                svg.append(f'<text x="{x:.0f}" y="{H+pB-4}" text-anchor="middle" font-size="10" fill="#706E6B">{d[5:]}</text>')
        for d in datasets:
            pts_str = " ".join(f'{xpos(p["i"]):.1f},{ypos(p["v"],minY,maxY):.1f}' for p in d["pts"])
            svg.append(f'<polyline points="{pts_str}" fill="none" stroke="{d["c"]["color"]}" stroke-width="2" opacity="0.85"/>')
            for p in d["pts"]:
                svg.append(f'<circle cx="{xpos(p["i"]):.1f}" cy="{ypos(p["v"],minY,maxY):.1f}" r="3" fill="{d["c"]["color"]}"/>')
        svg.append('</svg>')
        legend = "".join(f'<div class="legend-item"><div class="legend-swatch" style="background:{d["c"]["color"]}"></div>{d["c"]["emoji"]} {d["c"]["name"]}</div>' for d in datasets)
        return f'<div class="chart-wrap"><h3>{title}</h3><div>{" ".join(svg)}</div><div class="chart-legend">{legend}</div></div>'

    return (
        make_chart("📊 Valuation Over Time (Private Companies)", "valuation_usd_billions",
                   lambda v: f'${v:.0f}B' if v>=1 else f'${v*1000:.0f}M',
                   lambda c: not c["funding_summary"].get("public")) +
        make_chart("👥 Headcount Over Time", "headcount_estimate",
                   lambda v: f'{v/1000:.0f}K' if v>=1000 else str(int(v)))
    )

# ═══════════════════════════════════════════════════════
# ASSEMBLE HTML
# ═══════════════════════════════════════════════════════

DATA_JSON = json.dumps(data, separators=(",",":"), ensure_ascii=False)

# Section filter pills (none active by default = show all)
filters_html = "".join(
    f'<button class="filter-pill" data-section="{sec}" onclick="toggleFilter(this)">{SECTION_ICONS.get(sec,"")} {sec}</button>'
    for sec in SECTIONS_ORDER if companies_in(sec)
)

HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>AI Landscape — {last_updated}</title>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#F4F6F9;color:#16325C;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;font-size:14px}}
#topbar{{position:fixed;top:0;left:0;right:0;height:52px;background:#0070D2;color:white;display:flex;align-items:center;padding:0 24px;z-index:100;gap:12px;box-shadow:0 2px 8px rgba(0,0,0,.2)}}
#topbar h1{{font-size:1.1rem;font-weight:700}}
#topbar .meta{{font-size:.78rem;opacity:.8;margin-left:4px}}
#section-filters{{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:14px}}
.filter-pill{{font-size:.78rem;padding:5px 12px;border-radius:16px;border:1.5px solid #0070D2;background:white;color:#0070D2;cursor:pointer;font-weight:600;transition:background .15s,color .15s;user-select:none}}
.filter-pill.active{{background:#0070D2;color:white}}
.filter-pill:hover{{background:#E8F4FF}}.filter-pill.active:hover{{background:#005FB2}}
#main{{padding-top:52px;max-width:1200px;margin:0 auto}}
#hero{{background:linear-gradient(135deg,#003778 0%,#0070D2 55%,#00A1E0 100%);color:white;padding:44px 40px 36px}}
#hero .eyebrow{{font-size:.7rem;font-weight:700;letter-spacing:.14em;text-transform:uppercase;opacity:.72;margin-bottom:8px}}
#hero h2{{font-size:2.1rem;font-weight:800;margin-bottom:6px;line-height:1.1}}
#hero .subtitle{{font-size:.92rem;opacity:.82;margin-bottom:28px}}
.hero-stats{{display:flex;gap:16px;flex-wrap:wrap}}
.hero-stat{{background:rgba(255,255,255,.13);border-radius:8px;padding:13px 18px;min-width:155px;border:1px solid rgba(255,255,255,.15)}}
.hero-stat .label{{font-size:.68rem;text-transform:uppercase;letter-spacing:.08em;opacity:.78}}
.hero-stat .value{{font-size:1.35rem;font-weight:700;margin-top:3px}}
.hero-stat .sub{{font-size:.75rem;opacity:.72;margin-top:2px}}
.content-section{{background:white;border-radius:8px;box-shadow:0 1px 4px rgba(0,0,0,.08);margin:20px 24px;padding:24px 28px}}
.content-section h2{{font-size:1.05rem;font-weight:700;color:#0070D2;border-bottom:2px solid #E4E9F0;padding-bottom:9px;margin-bottom:16px}}
.scoreboard{{width:100%;border-collapse:collapse;font-size:.87rem}}
.scoreboard thead th{{background:#0070D2;color:white;padding:9px 11px;text-align:left;font-weight:600;cursor:pointer;user-select:none;white-space:nowrap}}
.scoreboard thead th:hover{{background:#005FB2}}
.scoreboard thead th.sorted-asc::after{{content:" ▲";opacity:.8}}
.scoreboard thead th.sorted-desc::after{{content:" ▼";opacity:.8}}
.scoreboard tbody td{{padding:9px 11px;border-bottom:1px solid #E4E9F0;vertical-align:middle}}
.scoreboard tbody tr:nth-child(odd){{background:#F8FAFC}}
.scoreboard tbody tr:hover{{background:#E8F4FF}}
.co-link{{text-decoration:none;color:inherit;display:flex;align-items:center}}
.co-link:hover .co-name{{color:#0070D2;text-decoration:underline}}
.co-name{{font-weight:700;color:#16325C}}
.co-emoji{{margin-right:5px}}
.section-badge{{font-size:.7rem;background:#E8F4FF;color:#0070D2;padding:2px 6px;border-radius:10px;white-space:nowrap;display:inline-block}}
.conf-dot{{display:inline-block;width:7px;height:7px;border-radius:50%;margin-left:4px;vertical-align:middle}}
.conf-high{{background:#27AE60}}.conf-medium{{background:#F39C12}}.conf-low{{background:#E74C3C}}.conf-carried{{background:#BDC3C7}}
.news-pill{{font-size:.72rem;padding:1px 6px;border-radius:8px;margin-left:2px;display:inline-block}}
.news-0{{color:#BDC3C7}}.news-has{{background:#FEF9E7;color:#D4AC0D}}.news-high-sig{{background:#FADBD8;color:#C0392B;font-weight:600}}
.company-section-wrapper{{margin-bottom:8px}}
.company-section-header{{background:linear-gradient(90deg,#005FB2,#0070D2,#00A1E0);color:white;border-radius:8px 8px 0 0;padding:14px 24px;margin:28px 24px 0}}
.company-section-header h3{{font-size:1rem;font-weight:700}}
.csh-sub{{font-size:.78rem;opacity:.82;margin-top:2px}}
.cards-grid{{display:flex;flex-direction:column;gap:20px;margin:0 24px 4px;padding:16px 0}}
.company-card{{background:white;border-radius:10px;box-shadow:0 1px 5px rgba(0,0,0,.09);overflow:hidden;border:1px solid #E4E9F0}}
.card-header{{padding:14px 18px;color:white;display:flex;align-items:center;gap:11px}}
.card-emoji{{font-size:1.6rem;line-height:1}}
.card-title-block{{flex:1}}
.card-title-block h4{{font-size:1rem;font-weight:700}}
.card-section-tag{{font-size:.68rem;opacity:.84;margin-top:2px}}
.card-updated{{font-size:.68rem;opacity:.65;text-align:right;white-space:nowrap}}
.card-body{{display:grid;grid-template-columns:1fr 1fr;gap:0}}
.card-col{{padding:14px 18px}}
.card-col:first-child{{border-right:1px solid #E4E9F0}}
.card-col h5{{font-size:.68rem;font-weight:700;text-transform:uppercase;letter-spacing:.07em;color:#706E6B;margin-bottom:7px}}
.leader-item{{margin-bottom:5px}}
.leader-name{{font-weight:600;font-size:.87rem;color:#16325C}}
.leader-title{{color:#706E6B;font-size:.78rem}}
.product-item{{font-size:.84rem;margin-bottom:5px;padding:4px 8px;background:#F8FAFC;border-left:3px solid #00A1E0;border-radius:0 4px 4px 0}}
.product-flagship{{border-left-color:#0070D2}}
.product-name{{font-weight:600;color:#16325C}}
.product-type{{font-size:.73rem;color:#706E6B}}
.fin-row{{display:flex;justify-content:space-between;align-items:center;padding:4px 0;border-bottom:1px solid #F4F6F9;font-size:.84rem}}
.fin-row:last-child{{border-bottom:none}}
.fin-label{{color:#706E6B}}
.fin-value{{font-weight:600;display:flex;align-items:center;gap:3px}}
.fin-na{{color:#BDC3C7;font-style:italic;font-weight:400}}
.card-sub-section{{margin-top:10px;padding-top:10px;border-top:1px solid #F4F6F9}}
.card-sub-section h5{{font-size:.68rem;font-weight:700;text-transform:uppercase;letter-spacing:.07em;color:#706E6B;margin-bottom:6px}}
.acq-item{{margin-bottom:7px;font-size:.83rem}}
.acq-name{{font-weight:600;color:#16325C}}
.acq-date{{font-size:.73rem;color:#706E6B;margin-left:4px}}
.acq-desc{{font-size:.78rem;color:#706E6B;margin-top:1px}}
.inv-pills{{display:flex;flex-wrap:wrap;gap:4px}}
.inv-pill{{font-size:.69rem;background:#E8F4FF;color:#0070D2;padding:2px 7px;border-radius:10px;border:1px solid #C8E0F8}}
.tags{{display:flex;flex-wrap:wrap;gap:4px;margin-top:7px}}
.tag{{font-size:.68rem;background:#E8F4FF;color:#0070D2;padding:2px 7px;border-radius:10px}}
.card-chart-section{{padding:14px 18px;border-top:1px solid #E4E9F0;background:#FAFBFD}}
.chart-header{{display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;font-size:.78rem;font-weight:600;color:#16325C}}
.chart-legend-inline{{display:flex;align-items:center;gap:8px;font-size:.72rem;color:#706E6B;font-weight:400}}
.cli-dot{{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:2px;vertical-align:middle}}
.cli-bar{{display:inline-block;width:12px;height:10px;background:#0070D2;opacity:.55;border-radius:2px;margin:0 2px;vertical-align:middle}}
.chart-area{{position:relative}}
.no-chart-data{{font-size:.82rem;color:#BDC3C7;font-style:italic;padding:8px 0}}
.card-footer{{padding:11px 18px;background:#F8FAFC;border-top:1px solid #E4E9F0}}
.card-footer h5{{font-size:.68rem;font-weight:700;text-transform:uppercase;letter-spacing:.07em;color:#706E6B;margin-bottom:7px}}
.news-item{{font-size:.82rem;padding:4px 0;border-bottom:1px solid #EEF0F3;display:flex;align-items:flex-start;gap:5px}}
.news-item:last-child{{border-bottom:none}}
.news-badge{{font-size:.67rem;padding:1px 5px;border-radius:8px;white-space:nowrap;flex-shrink:0;margin-top:1px}}
.sig-high{{background:#FADBD8;color:#C0392B}}.sig-medium{{background:#FEF9E7;color:#D4AC0D}}.sig-low{{background:#F4F6F9;color:#706E6B}}
.news-headline{{flex:1;line-height:1.35}}
.no-news{{font-size:.82rem;color:#BDC3C7;font-style:italic}}
.chart-wrap{{margin-bottom:24px}}
.chart-wrap h3{{font-size:.88rem;font-weight:700;color:#16325C;margin-bottom:6px}}
.chart-legend{{display:flex;flex-wrap:wrap;gap:10px;margin-top:8px}}
.legend-item{{display:flex;align-items:center;gap:5px;font-size:.77rem;color:#16325C}}
.legend-swatch{{width:20px;height:3px;border-radius:2px}}
#footer{{text-align:center;padding:28px 24px;color:#706E6B;font-size:.78rem;line-height:1.6}}
/* Model + Funding popups */
.model-popup,.fund-popup{{position:fixed;z-index:500;background:white;border-radius:8px;box-shadow:0 4px 24px rgba(0,0,0,.22);border:1px solid #E4E9F0;min-width:270px;max-width:360px;pointer-events:all}}
.mp-header{{background:#0070D2;color:white;padding:10px 14px;border-radius:8px 8px 0 0;display:flex;align-items:center;gap:8px}}
.fp-header{{background:#003F7F}}
.mp-name{{font-weight:700;font-size:.95rem;flex:1}}
.mp-date{{font-size:.75rem;opacity:.82;white-space:nowrap}}
.mp-close{{background:none;border:none;color:white;font-size:1rem;cursor:pointer;padding:0 4px;margin-left:4px}}
.mp-body{{padding:12px 14px}}
.mp-row{{display:flex;justify-content:space-between;align-items:flex-start;font-size:.82rem;padding:3px 0;border-bottom:1px solid #F4F6F9;gap:8px}}
.mp-row:last-child{{border-bottom:none}}
.mp-row span:first-child{{color:#706E6B;white-space:nowrap;flex-shrink:0}}
.mp-row span:last-child{{font-weight:600;text-align:right}}
.mp-est{{font-weight:400;font-size:.72rem;color:#F39C12;margin-left:4px}}
.mp-purpose{{font-size:.84rem;color:#16325C;margin-top:8px;line-height:1.4}}
.mp-notes{{font-size:.78rem;color:#706E6B;margin-top:6px;font-style:italic;line-height:1.35}}
.fp-amount{{color:#0070D2;font-size:.95rem}}
.fp-inv-row span:last-child{{font-weight:400;color:#444;text-align:right;font-size:.8rem}}
.model-dot:hover{{opacity:1;filter:brightness(1.2)}}
.fund-bar:hover{{opacity:0.8}}
</style>
</head>
<body>
<div id="topbar">
  <h1>🌐 AI Landscape</h1>
  <span class="meta">{len(companies)} companies · Updated {last_updated}</span>
</div>
<div id="main">
<div id="hero">
  <div class="eyebrow">AI Industry Tracker</div>
  <h2>The Living AI Landscape</h2>
  <div class="subtitle">{len(companies)} companies · Updated {last_updated} · Model history from Nov 2022</div>
  <div class="hero-stats">{hero_stats()}</div>
</div>
<div class="content-section">
  <h2>📊 Company Scoreboard</h2>
  <div id="section-filters">{filters_html}</div>
  <p style="font-size:.75rem;color:#706E6B;font-style:italic;margin-bottom:12px">⚠ Seed data from research; figures approximate. Click column headers to sort.</p>
  <div style="overflow-x:auto">
    <table class="scoreboard" id="scoreboard">
      <thead><tr>
        <th onclick="sortTable(0)">Company</th>
        <th onclick="sortTable(1)">Section</th>
        <th onclick="sortTable(2)">CEO</th>
        <th onclick="sortTable(3)">Employees</th>
        <th onclick="sortTable(4)">Valuation / Status</th>
        <th onclick="sortTable(5)">Flagship Product</th>
        <th onclick="sortTable(6)">This Week</th>
      </tr></thead>
      <tbody>{scoreboard_rows()}</tbody>
    </table>
  </div>
</div>
{build_sections()}
<div class="content-section">
  <h2>📈 Snapshot Trends Over Time</h2>
  {build_trend_charts()}
</div>
<div id="footer">
  Generated by Claude · {last_updated}<br>
  ⚠ Financial data is approximate. Use for informational purposes only.<br>
  Update weekly with <code>/ai-landscape</code>
</div>
</div>

<script>
function toggleFilter(btn){{
  btn.classList.toggle('active');
  const active=new Set([...document.querySelectorAll('#section-filters .filter-pill.active')].map(b=>b.dataset.section));
  const showAll=active.size===0;
  document.querySelectorAll('.company-section-wrapper').forEach(el=>{{el.style.display=(showAll||active.has(el.dataset.section))?'':'none';}});
  document.querySelectorAll('#scoreboard tbody tr').forEach(tr=>{{tr.style.display=(showAll||active.has(tr.dataset.section))?'':'none';}});
}}
let sortCol=-1,sortAsc=true;
function sortTable(col){{
  const tbody=document.querySelector('#scoreboard tbody');
  const rows=[...tbody.querySelectorAll('tr')];
  if(sortCol===col)sortAsc=!sortAsc; else{{sortCol=col;sortAsc=true;}}
  rows.sort((a,b)=>{{
    const ta=a.cells[col].textContent.trim(), tb=b.cells[col].textContent.trim();
    const na=parseFloat(ta.replace(/[$,BTKkM+~]/g,'')), nb=parseFloat(tb.replace(/[$,BTKkM+~]/g,''));
    if(!isNaN(na)&&!isNaN(nb))return sortAsc?na-nb:nb-na;
    return sortAsc?ta.localeCompare(tb):tb.localeCompare(ta);
  }});
  rows.forEach(r=>tbody.appendChild(r));
  document.querySelectorAll('.scoreboard thead th').forEach((th,i)=>{{th.className=i===col?(sortAsc?'sorted-asc':'sorted-desc'):'';}});
}}
// Model + funding popups
let activePopup=null;
function _positionPopup(pop, triggerEl){{
  const pw=pop.offsetWidth||280, ph=pop.offsetHeight||160;
  const dr=triggerEl.getBoundingClientRect();
  let left=dr.left+dr.width/2-pw/2;
  let top=dr.top-ph-12;
  if(top<60) top=dr.bottom+12;
  left=Math.max(8,Math.min(left,window.innerWidth-pw-8));
  pop.style.left=left+'px';
  pop.style.top=top+'px';
}}
function showModelPopup(id, dotEl){{
  if(activePopup&&activePopup!==id) document.getElementById(activePopup).style.display='none';
  if(activePopup===id){{document.getElementById(id).style.display='none';activePopup=null;return;}}
  const pop=document.getElementById(id);
  if(!pop) return;
  pop.style.display='block';
  _positionPopup(pop, dotEl);
  activePopup=id;
}}
function showFundPopup(id, barEl){{
  if(activePopup&&activePopup!==id) document.getElementById(activePopup).style.display='none';
  if(activePopup===id){{document.getElementById(id).style.display='none';activePopup=null;return;}}
  const pop=document.getElementById(id);
  if(!pop) return;
  pop.style.display='block';
  _positionPopup(pop, barEl);
  activePopup=id;
}}
function closePopup(id){{
  const el=document.getElementById(id);
  if(el) el.style.display='none';
  if(activePopup===id) activePopup=null;
}}
document.addEventListener('click',function(e){{
  if(activePopup&&!e.target.closest('.model-popup')&&!e.target.closest('.fund-popup')&&!e.target.closest('.model-dot')&&!e.target.closest('.fund-bar')){{
    closePopup(activePopup);
  }}
}});
</script>
</body>
</html>"""

with open(OUT_FILE, "w", encoding="utf-8") as f:
    f.write(HTML)

print(f"Wrote {OUT_FILE} ({len(HTML)//1024}KB)")
