import os
import streamlit as st
import requests
import plotly.graph_objects as go

API_URL = os.environ.get("API_URL", "http://localhost:8000")

st.set_page_config(
    page_title="ISO Predict · Football IA",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;700&family=Outfit:wght@400;600;700;800;900&display=swap');

    :root {
        --blue: #4f8cff;
        --blue-light: #7aaeff;
        --blue-glow: rgba(79,140,255,0.4);
        --purple: #a78bfa;
        --green: #22c55e;
        --green-glow: rgba(34,197,94,0.35);
        --gold: #facc15;
        --red: #ef4444;
        --bg-primary: #050813;
        --bg-card: rgba(255,255,255,0.033);
        --bg-card-hover: rgba(255,255,255,0.06);
        --border: rgba(255,255,255,0.07);
        --border-active: rgba(79,140,255,0.45);
        --border-glow: rgba(79,140,255,0.18);
        --text-primary: #eef2ff;
        --text-secondary: #7b8bb2;
        --text-dim: #3d4a6a;
        --r-sm: 12px; --r-md: 18px; --r-lg: 24px; --r-xl: 32px;
    }

    /* ── RESET & BASE ── */
    * { font-family: 'Inter', sans-serif !important; box-sizing: border-box; }

    /* ── FIX: supprime l'espace du header Streamlit caché ── */
    #MainMenu, footer, header { visibility: hidden !important; height: 0 !important; }
    .stApp > header { display: none !important; }
    [data-testid="stToolbar"] { display: none !important; }
    [data-testid="stDecoration"] { display: none !important; }
    [data-testid="stStatusWidget"] { display: none !important; }

    .stApp {
        background: var(--bg-primary);
        background-image:
            radial-gradient(ellipse 100% 60% at 50% -10%, rgba(79,140,255,0.10), transparent),
            radial-gradient(ellipse 70% 50% at 90% 110%, rgba(34,197,94,0.05), transparent),
            radial-gradient(ellipse 50% 30% at 10% 80%, rgba(167,139,250,0.04), transparent);
        min-height: 100vh;
    }

    /* ── FIX PRINCIPAL : retire le padding-top du container ── */
    .block-container {
        max-width: 1020px;
        padding: 0 1.5rem 4rem !important;
        margin: 0 auto;
    }

    /* ── NAVBAR ── */
    .navbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 1rem 0 1rem;
        border-bottom: 1px solid var(--border);
        margin-bottom: 2.5rem;
    }
    .nav-brand {
        display: flex;
        align-items: center;
        gap: 10px;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 800;
        font-size: 1.15rem;
        color: var(--text-primary);
        letter-spacing: -0.3px;
    }
    .nav-ball {
        font-size: 1.3rem;
        filter: drop-shadow(0 0 12px rgba(79,140,255,0.5));
        animation: spin-slow 10s linear infinite;
    }
    @keyframes spin-slow { from{transform:rotate(0deg)} to{transform:rotate(360deg)} }
    .nav-brand .acc {
        background: linear-gradient(135deg, var(--blue), var(--purple));
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    }
    .nav-badge {
        font-size: 0.62rem; font-weight: 700; letter-spacing: 2px; text-transform: uppercase;
        color: var(--blue); background: rgba(79,140,255,0.1); border: 1px solid rgba(79,140,255,0.2);
        border-radius: 99px; padding: 3px 10px;
    }

    /* ── HERO ── */
    .hero { text-align: center; padding: 3rem 1rem 2.2rem; }
    .hero-tag {
        display: inline-flex; align-items: center; gap: 6px;
        background: rgba(79,140,255,0.08); border: 1px solid rgba(79,140,255,0.18);
        border-radius: 99px; padding: 5px 14px;
        font-size: 0.7rem; font-weight: 600; letter-spacing: 1.5px; text-transform: uppercase;
        color: var(--blue-light); margin-bottom: 1.2rem;
    }
    .hero-tag::before { content: '●'; font-size: 0.5rem; animation: pulse-dot 2s ease-in-out infinite; }
    @keyframes pulse-dot { 0%,100%{opacity:.4} 50%{opacity:1} }
    .hero-title {
        font-family: 'Outfit', sans-serif !important;
        font-size: clamp(2.2rem, 6vw, 3.6rem); font-weight: 900;
        letter-spacing: -1.5px; color: var(--text-primary); margin: 0 0 0.6rem; line-height: 1.05;
    }
    .hero-title .acc {
        background: linear-gradient(135deg, var(--blue), var(--purple));
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    }
    .hero-sub {
        font-size: clamp(0.9rem, 2.5vw, 1.05rem); color: var(--text-secondary);
        font-weight: 400; max-width: 480px; margin: 0 auto; line-height: 1.6;
    }

    /* ── GLASS CARD ── */
    .glass {
        background: var(--bg-card); border: 1px solid var(--border);
        border-radius: var(--r-lg); padding: 28px;
        backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
        transition: border-color .25s, background .25s, box-shadow .25s;
    }
    .glass:hover {
        background: var(--bg-card-hover); border-color: var(--border-glow);
        box-shadow: 0 8px 40px rgba(0,0,0,.3), 0 0 0 1px var(--border-glow);
    }
    .glass-elevated {
        background: rgba(255,255,255,.04);
        border: 1px solid rgba(79,140,255,.15);
        box-shadow: 0 4px 32px rgba(0,0,0,.4), 0 0 0 1px rgba(79,140,255,.08);
    }

    /* ── SECTION TITLES ── */
    .sec {
        display: flex; align-items: center; gap: 10px;
        margin: 2.8rem 0 1.2rem; font-size: 1rem; font-weight: 700;
        color: var(--text-primary); letter-spacing: -0.3px;
    }
    .sec-dot {
        width: 8px; height: 8px; border-radius: 50%; background: var(--blue);
        box-shadow: 0 0 10px var(--blue-glow); flex-shrink: 0;
        animation: glow-pulse 3s ease-in-out infinite;
    }
    @keyframes glow-pulse {
        0%,100%{box-shadow:0 0 8px var(--blue-glow)}
        50%{box-shadow:0 0 18px var(--blue-glow),0 0 30px rgba(79,140,255,.2)}
    }

    /* ── TEAM TAG ── */
    .team-tag {
        font-size: 0.65rem; font-weight: 700; letter-spacing: 2px; text-transform: uppercase;
        color: var(--text-dim); margin-bottom: 10px;
        display: flex; align-items: center; gap: 6px;
    }
    .team-tag::after { content:''; flex:1; height:1px; background: var(--border); }

    /* ── SELECTBOX ── */
    div[data-testid="stSelectbox"] > div > div {
        background: rgba(255,255,255,.035) !important; border: 1.5px solid var(--border) !important;
        border-radius: var(--r-sm) !important; color: var(--text-primary) !important;
        font-weight: 600 !important; font-size: .95rem !important; padding: 6px 14px !important;
        transition: border-color .2s, box-shadow .2s !important;
    }
    div[data-testid="stSelectbox"] > div > div:hover,
    div[data-testid="stSelectbox"] > div > div:focus-within {
        border-color: var(--border-active) !important;
        box-shadow: 0 0 0 3px rgba(79,140,255,.08) !important;
    }
    div[data-baseweb="select"] { background: transparent !important; }
    div[data-baseweb="popover"] { z-index: 9999 !important; }

    /* ── VS ── */
    .vs-center {
        display: flex; align-items: center; justify-content: center;
        padding-top: 30px; flex-direction: column; gap: 6px;
    }
    .vs-pill {
        background: linear-gradient(135deg, rgba(79,140,255,.15), rgba(167,139,250,.15));
        border: 1px solid rgba(79,140,255,.25); border-radius: var(--r-sm);
        padding: 8px 18px; font-family: 'JetBrains Mono', monospace !important;
        font-size: .88rem; font-weight: 700; color: var(--blue-light);
        letter-spacing: 3px; box-shadow: 0 0 20px rgba(79,140,255,.1);
    }

    /* ── CHECKBOX ── */
    div[data-testid="stCheckbox"] label p { color: var(--text-secondary) !important; font-size: .88rem !important; font-weight: 500 !important; }

    /* ── BUTTON ── */
    .stButton > button {
        background: linear-gradient(135deg, var(--blue), #7c5cff) !important;
        color: white !important; font-family: 'Outfit', sans-serif !important;
        font-weight: 800 !important; font-size: 1rem !important;
        border: none !important; border-radius: var(--r-md) !important;
        padding: .85rem 2rem !important;
        box-shadow: 0 4px 24px var(--blue-glow), inset 0 1px 0 rgba(255,255,255,.15) !important;
        transition: all .22s cubic-bezier(.4,0,.2,1) !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) scale(1.01) !important;
        box-shadow: 0 10px 40px rgba(79,140,255,.55), inset 0 1px 0 rgba(255,255,255,.2) !important;
    }
    .stButton > button:active { transform: translateY(0) scale(.99) !important; }

    /* ── PREDICTION BOX ── */
    .pred-box {
        background: linear-gradient(135deg, rgba(79,140,255,.07), rgba(167,139,250,.07));
        border: 1px solid rgba(79,140,255,.18); border-radius: var(--r-xl);
        padding: 2.8rem 2rem 2.2rem; text-align: center;
        margin: 1.8rem 0 1rem; position: relative; overflow: hidden;
        animation: fadeUp .5s ease forwards;
    }
    .pred-box::before {
        content: ''; position: absolute; top: -1px; left: 15%; right: 15%;
        height: 2px; background: linear-gradient(90deg, transparent, var(--blue), var(--purple), transparent);
    }
    .pred-label {
        font-size: .65rem; font-weight: 700; letter-spacing: 3px; text-transform: uppercase;
        color: var(--text-dim); margin-bottom: 12px;
        display: flex; align-items: center; justify-content: center; gap: 8px;
    }
    .pred-label::before,.pred-label::after { content:'—'; opacity:.3; }
    .pred-result {
        font-family: 'Outfit', sans-serif !important;
        font-size: clamp(1.8rem,5vw,2.8rem); font-weight: 900; letter-spacing: -1px; margin: 0;
    }
    .confidence-wrap { margin: 1.2rem auto 0; max-width: 260px; }
    .confidence-row {
        display: flex; justify-content: space-between;
        font-size: .75rem; color: var(--text-dim); margin-bottom: 6px; font-weight: 500;
    }
    .confidence-track { height: 6px; background: rgba(255,255,255,.06); border-radius: 99px; overflow: hidden; }
    .confidence-fill {
        height: 100%; border-radius: 99px;
        background: linear-gradient(90deg, var(--blue), var(--purple));
        box-shadow: 0 0 10px var(--blue-glow);
    }
    .pred-home { background: linear-gradient(135deg,var(--blue),var(--purple)); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; }
    .pred-draw { background: linear-gradient(135deg,var(--gold),#f59e0b); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; }
    .pred-away { background: linear-gradient(135deg,var(--green),#10b981); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; }

    /* ── PROB BAR ── */
    .prob-bar {
        display: flex; border-radius: var(--r-md); overflow: hidden;
        height: 62px; margin: 1.4rem 0;
        box-shadow: 0 4px 24px rgba(0,0,0,.35); gap: 2px;
        animation: fadeUp .6s .1s ease both;
    }
    .prob-seg {
        display: flex; align-items: center; justify-content: center; flex-direction: column;
        font-weight: 800; color: white; font-size: 1.1rem;
        font-family: 'JetBrains Mono', monospace !important;
        transition: flex .5s cubic-bezier(.4,0,.2,1); padding: 0 4px; overflow: hidden; gap: 2px;
    }
    .prob-seg:hover { filter: brightness(1.15); }
    .prob-seg small {
        font-size: .58rem; font-weight: 600; opacity: .75; letter-spacing: .5px;
        font-family: 'Inter', sans-serif !important; white-space: nowrap;
        overflow: hidden; text-overflow: ellipsis; max-width: 90%; text-transform: uppercase;
    }
    .prob-home { background: linear-gradient(180deg,#5b9aff,#3b7dff); border-radius: var(--r-sm) 0 0 var(--r-sm); }
    .prob-draw { background: linear-gradient(180deg,rgba(250,204,21,.92),rgba(234,179,8,.92)); color: #1a1a00; }
    .prob-away { background: linear-gradient(180deg,#28d866,#16a34a); border-radius: 0 var(--r-sm) var(--r-sm) 0; }

    /* ── STAT CARDS ── */
    .stat-grid {
        display: grid; grid-template-columns: repeat(3,1fr); gap: 14px; margin: 1.2rem 0;
        animation: fadeUp .6s .15s ease both;
    }
    .stat-card {
        background: var(--bg-card); border: 1px solid var(--border);
        border-radius: var(--r-md); padding: 18px 16px 14px;
        text-align: center; transition: border-color .22s, transform .22s, box-shadow .22s;
        position: relative; overflow: hidden;
    }
    .stat-card::before {
        content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
        background: linear-gradient(90deg, transparent, var(--blue), transparent);
        opacity: 0; transition: opacity .25s;
    }
    .stat-card:hover { border-color: var(--border-active); transform: translateY(-3px); box-shadow: 0 8px 30px rgba(0,0,0,.3); }
    .stat-card:hover::before { opacity: 1; }
    .stat-icon { font-size: 1.2rem; margin-bottom: 6px; display: block; }
    .stat-card .label {
        font-size: .6rem; font-weight: 700; letter-spacing: 1.5px;
        text-transform: uppercase; color: var(--text-dim); margin-bottom: 7px;
    }
    .stat-card .value {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 1.45rem; font-weight: 700; color: var(--text-primary); line-height: 1;
    }
    .stat-card .sub { font-size: .7rem; color: var(--text-secondary); margin-top: 6px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; font-weight: 500; }
    .stat-home .value { color: var(--blue-light); }
    .stat-away .value { color: var(--green); }

    /* ── COMPARISON TABLE ── */
    .table-wrapper { width: 100%; overflow-x: auto; -webkit-overflow-scrolling: touch; border-radius: var(--r-lg); }
    .cmp-table { width: 100%; border-collapse: separate; border-spacing: 0; min-width: 380px; }
    .cmp-table thead tr { background: rgba(255,255,255,.025); }
    .cmp-table th {
        font-size: .62rem; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase;
        color: var(--text-dim); padding: 14px 16px; text-align: center; border-bottom: 1px solid var(--border);
    }
    .cmp-table th:first-child { text-align: left; }
    .cmp-table th:nth-child(2) { color: var(--blue-light); }
    .cmp-table th:nth-child(3) { color: var(--green); }
    .cmp-table td { padding: 13px 16px; font-size: .9rem; border-bottom: 1px solid rgba(255,255,255,.035); text-align: center; transition: background .15s; }
    .cmp-table tbody tr:hover td { background: rgba(255,255,255,.025); }
    .cmp-table td:first-child { text-align: left; color: var(--text-secondary); font-size: .85rem; font-weight: 500; }
    .cmp-table tr:last-child td { border-bottom: none; }
    .cmp-home-val { color: var(--blue-light); font-weight: 700; font-family: 'JetBrains Mono', monospace !important; }
    .cmp-away-val { color: var(--green); font-weight: 700; font-family: 'JetBrains Mono', monospace !important; }
    .cmp-winner::after { content: '▲'; font-size: .55rem; margin-left: 5px; opacity: .7; vertical-align: middle; }

    /* ── MATCH ROW ── */
    .match-row {
        display: flex; align-items: center; gap: 10px; padding: 11px 14px;
        border-radius: var(--r-sm); margin-bottom: 6px;
        background: rgba(255,255,255,.02); border: 1px solid rgba(255,255,255,.04);
        font-size: .85rem; transition: background .15s, border-color .15s, transform .15s;
    }
    .match-row:hover { background: rgba(255,255,255,.05); transform: translateX(3px); }
    .match-badge {
        width: 28px; height: 28px; border-radius: 8px;
        display: flex; align-items: center; justify-content: center;
        font-weight: 800; font-size: .7rem; flex-shrink: 0;
    }
    .mb-w { background: rgba(34,197,94,.15); color: var(--green); border: 1px solid rgba(34,197,94,.2); }
    .mb-d { background: rgba(250,204,21,.1); color: var(--gold); border: 1px solid rgba(250,204,21,.2); }
    .mb-l { background: rgba(239,68,68,.1); color: var(--red); border: 1px solid rgba(239,68,68,.15); }
    .match-teams { color: var(--text-secondary); font-size: .78rem; flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
    .match-date { color: var(--text-dim); font-size: .72rem; flex-shrink: 0; }
    .match-score { font-family: 'JetBrains Mono', monospace !important; font-weight: 700; color: var(--text-primary); font-size: .9rem; flex-shrink: 0; }

    /* ── FORM HEADER ── */
    .form-header {
        display: flex; align-items: center; gap: 9px; margin-bottom: 14px;
        font-weight: 700; color: var(--text-primary); font-size: .92rem;
        font-family: 'Outfit', sans-serif !important;
        padding-bottom: 12px; border-bottom: 1px solid var(--border);
    }
    .form-header .dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
    .dot-home { background: var(--blue); box-shadow: 0 0 8px var(--blue-glow); }
    .dot-away { background: var(--green); box-shadow: 0 0 8px var(--green-glow); }

    /* ── FOOTER ── */
    .footer {
        text-align: center; padding: 3.5rem 0 1rem;
        color: var(--text-dim); font-size: .72rem;
        border-top: 1px solid var(--border); margin-top: 3rem;
    }
    .footer strong { color: var(--text-secondary); font-weight: 600; }

    /* ── ANIMATIONS ── */
    @keyframes fadeUp { from{opacity:0;transform:translateY(14px)} to{opacity:1;transform:translateY(0)} }
    .animate-in { animation: fadeUp .5s ease forwards; }

    /* ── RESPONSIVE ── */
    @media (max-width: 768px) {
        .block-container { padding: 0 1rem 3rem !important; }
        .hero { padding: 2rem 0.5rem 1.5rem; }
        .glass { padding: 18px; border-radius: var(--r-md); }
        .pred-box { padding: 2rem 1.2rem 1.6rem; }
        .prob-bar { height: 52px; }
        .prob-seg { font-size: .95rem; }
        .stat-grid { grid-template-columns: repeat(2,1fr); gap: 10px; }
        .stat-card .value { font-size: 1.2rem; }
    }
    @media (max-width: 480px) {
        .prob-bar { height: 46px; gap: 1px; }
        .prob-seg { font-size: .82rem; }
        .stat-grid { grid-template-columns: repeat(2,1fr); gap: 8px; }
        .stat-card { padding: 14px 12px 10px; }
        .stat-card .value { font-size: 1.1rem; }
        .cmp-table th, .cmp-table td { padding: 10px; font-size: .82rem; }
        .nav-badge { display: none; }
    }
</style>
""", unsafe_allow_html=True)


# ═══ API HELPERS ═══════════════════════════════════════
def api_get(endpoint):
    try:
        resp = requests.get(f"{API_URL}{endpoint}", timeout=15)
        resp.raise_for_status()
        return resp.json()
    except requests.ConnectionError:
        st.error("⚠️ Backend non disponible. Réessayez plus tard.")
        st.stop()
    except Exception as e:
        st.error(f"⚠️ Erreur API : {e}")
        st.stop()


def api_post(endpoint, data):
    try:
        resp = requests.post(f"{API_URL}{endpoint}", json=data, timeout=15)
        resp.raise_for_status()
        return resp.json()
    except requests.ConnectionError:
        st.error("⚠️ Backend non disponible. Réessayez plus tard.")
        st.stop()
    except requests.HTTPError as e:
        detail = e.response.json().get("detail", str(e)) if e.response else str(e)
        st.error(f"⚠️ Erreur : {detail}")
        st.stop()


# ═══ NAVBAR ════════════════════════════════════════════
st.markdown("""
<div class="navbar">
    <div class="nav-brand">
        <span class="nav-ball">⚽</span>
        <span><span class="acc">ISO</span>Predict</span>
    </div>
    <div class="nav-badge">IA Football</div>
</div>
""", unsafe_allow_html=True)

# ═══ HERO ══════════════════════════════════════════════
st.markdown("""
<div class="hero animate-in">
    <div class="hero-tag">Prédiction par Intelligence Artificielle</div>
    <p class="hero-title">Prédisez le <span class="acc">résultat</span><br>avant le coup de sifflet</p>
    <p class="hero-sub">Analyse basée sur les classements FIFA, la forme récente et les statistiques historiques.</p>
</div>
""", unsafe_allow_html=True)

data = api_get("/teams")
teams = data["teams"]

# ═══ MATCH SETUP ═══════════════════════════════════════
st.markdown('<div class="glass glass-elevated">', unsafe_allow_html=True)

c1, c_vs, c2 = st.columns([5, 1.2, 5])

with c1:
    st.markdown('<div class="team-tag">🏠 Équipe Domicile</div>', unsafe_allow_html=True)
    home_team = st.selectbox(
        "Domicile", teams,
        index=teams.index("France") if "France" in teams else 0,
        key="home", label_visibility="collapsed",
    )

with c_vs:
    st.markdown('<div class="vs-center"><span class="vs-pill">VS</span></div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="team-tag">✈️ Équipe Extérieur</div>', unsafe_allow_html=True)
    away_team = st.selectbox(
        "Extérieur", teams,
        index=teams.index("Brazil") if "Brazil" in teams else 1,
        key="away", label_visibility="collapsed",
    )

st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
neutral = st.checkbox("🏟️ Match sur terrain neutre")
st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

_, btn_c, _ = st.columns([1, 2.2, 1])
with btn_c:
    predict = st.button("🔮  Lancer la Prédiction", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# ═══ RESULTS ═══════════════════════════════════════════
if predict:
    with st.spinner("Analyse en cours…"):
        result = api_post("/predict", {
            "home_team": home_team,
            "away_team": away_team,
            "neutral": neutral,
        })

    prob = result["probabilities"]
    p_home = prob.get("Domicile", 0)
    p_draw = prob.get("Nul", 0)
    p_away = prob.get("Extérieur", 0)

    pred = result["prediction"]
    pred_cls = "pred-home" if "Domicile" in pred else ("pred-draw" if "Nul" in pred else "pred-away")
    confidence = max(p_home, p_draw, p_away)

    # ── Prediction box
    st.markdown(f"""
    <div class="pred-box">
        <p class="pred-label">Résultat prédit</p>
        <p class="pred-result {pred_cls}">{pred}</p>
        <div class="confidence-wrap">
            <div class="confidence-row">
                <span>Confiance du modèle</span>
                <span style="color:var(--text-primary);font-weight:700">{confidence}%</span>
            </div>
            <div class="confidence-track">
                <div class="confidence-fill" style="width:{confidence}%"></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Probability bar
    st.markdown(f"""
    <div class="prob-bar">
        <div class="prob-seg prob-home" style="flex:{p_home}">
            <span>{p_home}%</span><small>{home_team}</small>
        </div>
        <div class="prob-seg prob-draw" style="flex:{p_draw}">
            <span>{p_draw}%</span><small>Nul</small>
        </div>
        <div class="prob-seg prob-away" style="flex:{p_away}">
            <span>{p_away}%</span><small>{away_team}</small>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Team stats
    with st.spinner("Chargement des statistiques…"):
        home_stats = api_get(f"/team_stats/{home_team}")
        away_stats = api_get(f"/team_stats/{away_team}")

    st.markdown(f"""
    <div class="stat-grid">
        <div class="stat-card stat-home">
            <span class="stat-icon">🏆</span>
            <div class="label">Classement FIFA</div>
            <div class="value">{home_stats['rank'] or '—'}</div>
            <div class="sub">🏠 {home_team}</div>
        </div>
        <div class="stat-card stat-home">
            <span class="stat-icon">⭐</span>
            <div class="label">Points FIFA</div>
            <div class="value">{home_stats['total_points'] or '—'}</div>
            <div class="sub">🏠 {home_team}</div>
        </div>
        <div class="stat-card stat-home">
            <span class="stat-icon">📈</span>
            <div class="label">Forme récente</div>
            <div class="value">{home_stats['avg_outcome'] or '—'}</div>
            <div class="sub">🏠 {home_team}</div>
        </div>
        <div class="stat-card stat-away">
            <span class="stat-icon">🏆</span>
            <div class="label">Classement FIFA</div>
            <div class="value">{away_stats['rank'] or '—'}</div>
            <div class="sub">✈️ {away_team}</div>
        </div>
        <div class="stat-card stat-away">
            <span class="stat-icon">⭐</span>
            <div class="label">Points FIFA</div>
            <div class="value">{away_stats['total_points'] or '—'}</div>
            <div class="sub">✈️ {away_team}</div>
        </div>
        <div class="stat-card stat-away">
            <span class="stat-icon">📈</span>
            <div class="label">Forme récente</div>
            <div class="value">{away_stats['avg_outcome'] or '—'}</div>
            <div class="sub">✈️ {away_team}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Comparison table
    st.markdown('<div class="sec"><span class="sec-dot"></span> Comparaison directe</div>', unsafe_allow_html=True)

    def cmp_val(a, b):
        try:
            return float(a) > float(b)
        except (TypeError, ValueError):
            return False

    rows = [
        ("🏅 Classement FIFA", home_stats['rank'] or 'N/A', away_stats['rank'] or 'N/A',
         cmp_val(away_stats['rank'], home_stats['rank'])),
        ("⭐ Points FIFA", home_stats['total_points'] or 'N/A', away_stats['total_points'] or 'N/A',
         cmp_val(home_stats['total_points'], away_stats['total_points'])),
        ("⚽ Buts marqués (moy.)", home_stats['avg_goals_scored'], away_stats['avg_goals_scored'],
         cmp_val(home_stats['avg_goals_scored'], away_stats['avg_goals_scored'])),
        ("🛡️ Buts encaissés (moy.)", home_stats['avg_goals_conceded'], away_stats['avg_goals_conceded'],
         cmp_val(away_stats['avg_goals_conceded'], home_stats['avg_goals_conceded'])),
        ("📊 Diff. de buts", home_stats['avg_goal_diff'], away_stats['avg_goal_diff'],
         cmp_val(home_stats['avg_goal_diff'], away_stats['avg_goal_diff'])),
        ("📈 Forme récente", home_stats['avg_outcome'], away_stats['avg_outcome'],
         cmp_val(home_stats['avg_outcome'], away_stats['avg_outcome'])),
    ]

    table_html = f'''<div class="glass" style="padding:0;overflow:hidden">
      <div class="table-wrapper"><table class="cmp-table">
        <thead><tr><th>Statistique</th><th>🏠 {home_team}</th><th>✈️ {away_team}</th></tr></thead>
        <tbody>'''
    for label, hv, av, h_wins in rows:
        hc = "cmp-home-val cmp-winner" if h_wins else "cmp-home-val"
        ac = "cmp-away-val cmp-winner" if not h_wins else "cmp-away-val"
        table_html += f'<tr><td>{label}</td><td class="{hc}">{hv}</td><td class="{ac}">{av}</td></tr>'
    table_html += '</tbody></table></div></div>'
    st.markdown(table_html, unsafe_allow_html=True)

    # ── Radar
    st.markdown('<div class="sec"><span class="sec-dot"></span> Profil comparatif</div>', unsafe_allow_html=True)

    categories = ["Attaque", "Défense", "Forme", "Classement", "Points"]

    def norm(val, mx):
        return min(val / mx * 10, 10) if mx else 0

    mx_s = max(home_stats["avg_goals_scored"], away_stats["avg_goals_scored"], 1)
    mx_c = max(home_stats["avg_goals_conceded"], away_stats["avg_goals_conceded"], 1)
    mx_r = max(home_stats["rank"] or 100, away_stats["rank"] or 100, 1)
    mx_p = max(home_stats["total_points"] or 1, away_stats["total_points"] or 1, 1)

    h_radar = [
        norm(home_stats["avg_goals_scored"], mx_s),
        10 - norm(home_stats["avg_goals_conceded"], mx_c),
        norm(home_stats["avg_outcome"] + 1, 2),
        10 - norm(home_stats["rank"] or 100, mx_r),
        norm(home_stats["total_points"] or 0, mx_p),
    ]
    a_radar = [
        norm(away_stats["avg_goals_scored"], mx_s),
        10 - norm(away_stats["avg_goals_conceded"], mx_c),
        norm(away_stats["avg_outcome"] + 1, 2),
        10 - norm(away_stats["rank"] or 100, mx_r),
        norm(away_stats["total_points"] or 0, mx_p),
    ]

    fig_r = go.Figure()
    fig_r.add_trace(go.Scatterpolar(
        r=h_radar + [h_radar[0]], theta=categories + [categories[0]],
        fill="toself", name=home_team,
        line=dict(color="#4f8cff", width=2.5), fillcolor="rgba(79,140,255,0.12)",
    ))
    fig_r.add_trace(go.Scatterpolar(
        r=a_radar + [a_radar[0]], theta=categories + [categories[0]],
        fill="toself", name=away_team,
        line=dict(color="#22c55e", width=2.5), fillcolor="rgba(34,197,94,0.12)",
    ))
    fig_r.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True, range=[0, 10], gridcolor="rgba(255,255,255,0.06)", tickfont=dict(color="#3d4a6a", size=9), linecolor="rgba(255,255,255,0.06)"),
            angularaxis=dict(gridcolor="rgba(255,255,255,0.06)", tickfont=dict(color="#7b8bb2", size=12), linecolor="rgba(255,255,255,0.06)"),
        ),
        showlegend=True,
        legend=dict(font=dict(color="#eef2ff", size=12), x=0.5, xanchor="center", y=-0.12, orientation="h", bgcolor="rgba(0,0,0,0)"),
        paper_bgcolor="rgba(0,0,0,0)", height=420,
        margin=dict(l=50, r=50, t=30, b=60),
    )
    st.markdown('<div class="glass" style="padding:10px">', unsafe_allow_html=True)
    st.plotly_chart(fig_r, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Recent form
    st.markdown('<div class="sec"><span class="sec-dot"></span> Forme récente (5 derniers matchs)</div>', unsafe_allow_html=True)

    h_matches = home_stats.get("recent_matches", [])[-5:]
    a_matches = away_stats.get("recent_matches", [])[-5:]

    def render_matches(team_name, matches, dot_cls):
        html = f'<div class="glass" style="padding:18px"><div class="form-header"><span class="dot {dot_cls}"></span>{team_name}</div>'
        if not matches:
            html += '<div style="color:var(--text-dim);font-size:.85rem;text-align:center;padding:1rem 0">Aucun match disponible</div>'
        for m in matches:
            badge_cls = f"mb-{m['outcome'].lower()}"
            html += f'''<div class="match-row">
                <span class="match-badge {badge_cls}">{m['outcome']}</span>
                <span class="match-teams">{m.get('opponent', '')}</span>
                <span class="match-date">{m['date']}</span>
                <span class="match-score">{m['goals_for']:.0f} – {m['goals_against']:.0f}</span>
            </div>'''
        html += '</div>'
        return html

    mc1, mc2 = st.columns(2)
    with mc1:
        st.markdown(render_matches(home_team, h_matches, "dot-home"), unsafe_allow_html=True)
    with mc2:
        st.markdown(render_matches(away_team, a_matches, "dot-away"), unsafe_allow_html=True)

    # ── Goals evolution
    st.markdown('<div class="sec"><span class="sec-dot"></span> Évolution des buts (10 derniers matchs)</div>', unsafe_allow_html=True)

    h_goals = [m.get("goals_for", 0) for m in home_stats.get("recent_matches", [])[-10:]]
    a_goals = [m.get("goals_for", 0) for m in away_stats.get("recent_matches", [])[-10:]]

    fig_g = go.Figure()
    fig_g.add_trace(go.Scatter(
        y=h_goals, mode="lines+markers", name=home_team,
        line=dict(color="#4f8cff", width=3, shape="spline"),
        marker=dict(size=9, color="#4f8cff", line=dict(color="#050813", width=2)),
        fill="tozeroy", fillcolor="rgba(79,140,255,0.07)",
    ))
    fig_g.add_trace(go.Scatter(
        y=a_goals, mode="lines+markers", name=away_team,
        line=dict(color="#22c55e", width=3, shape="spline"),
        marker=dict(size=9, color="#22c55e", line=dict(color="#050813", width=2)),
        fill="tozeroy", fillcolor="rgba(34,197,94,0.07)",
    ))
    fig_g.update_layout(
        height=300, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(gridcolor="rgba(255,255,255,0.04)", showgrid=False, zeroline=False, tickfont=dict(color="#3d4a6a", size=10)),
        yaxis=dict(gridcolor="rgba(255,255,255,0.05)", zeroline=False, tickfont=dict(color="#3d4a6a", size=10), title=dict(text="Buts marqués", font=dict(color="#4a5578", size=11))),
        legend=dict(font=dict(color="#eef2ff", size=11), orientation="h", y=1.12, x=0.5, xanchor="center", bgcolor="rgba(0,0,0,0)"),
        margin=dict(l=10, r=10, t=20, b=10), hovermode="x unified",
    )
    st.markdown('<div class="glass" style="padding:10px">', unsafe_allow_html=True)
    st.plotly_chart(fig_g, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

# ═══ FOOTER ════════════════════════════════════════════
st.markdown("""
<div class="footer">
    <p><strong>ISO Predict</strong> · Prédiction de matches internationaux par IA</p>
    <p style="margin-top:4px;opacity:.5">Données FIFA · Modèle Machine Learning</p>
</div>
""", unsafe_allow_html=True)
