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
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500;700&family=Outfit:wght@600;700;800&display=swap');

    :root {
        --blue: #2563eb;
        --blue-hover: #1d4ed8;
        --purple: #7c3aed;
        --green: #059669;
        --gold: #d97706;
        --red: #dc2626;
        
        /* Clean white light theme */
        --bg-primary: #ffffff;
        --bg-card: #f8fafc;
        --bg-card-hover: #f1f5f9;
        --border: #e2e8f0;
        --border-active: #cbd5e1;
        
        --text-primary: #0f172a;
        --text-secondary: #475569;
        --text-dim: #64748b;
        
        --r-sm: 8px; --r-md: 12px; --r-lg: 16px; --r-xl: 24px;
    }

    /* ── RESET & BASE ── */
    * { font-family: 'Inter', sans-serif !important; box-sizing: border-box; }

    /* ── FIX: supprime l'espace du header Streamlit caché ── */
    #MainMenu, footer, header { visibility: hidden !important; height: 0 !important; }
    .stApp > header { display: none !important; }
    [data-testid="stToolbar"] { display: none !important; }
    [data-testid="stDecoration"] { display: none !important; }

    .stApp {
        background: var(--bg-primary);
        min-height: 100vh;
    }

    /* ── FIX PRINCIPAL : retire le padding-top du container ── */
    .block-container {
        max-width: 960px;
        padding: 0 1.5rem 4rem !important;
        margin: 0 auto;
    }

    /* ── NAVBAR ── */
    .navbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 1rem 0;
        border-bottom: 1px solid var(--border);
        margin-bottom: 2rem;
    }
    .nav-brand {
        display: flex;
        align-items: center;
        gap: 10px;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 800;
        font-size: 1.2rem;
        color: var(--text-primary);
    }
    .nav-ball {
        font-size: 1.3rem;
    }
    .nav-brand .acc {
        color: var(--blue);
    }
    .nav-badge {
        font-size: 0.65rem; font-weight: 700; letter-spacing: 1px; text-transform: uppercase;
        color: var(--text-secondary); background: var(--bg-card); border: 1px solid var(--border);
        border-radius: 99px; padding: 4px 12px;
    }

    /* ── HERO ── */
    .hero { text-align: center; padding: 2.5rem 1rem 2rem; }
    .hero-tag {
        display: inline-flex; align-items: center; gap: 6px;
        background: var(--bg-card); border: 1px solid var(--border);
        border-radius: 99px; padding: 5px 14px;
        font-size: 0.75rem; font-weight: 600; letter-spacing: 1px; text-transform: uppercase;
        color: var(--text-secondary); margin-bottom: 1.2rem;
    }
    .hero-tag::before { content: '●'; font-size: 0.5rem; color: var(--blue); }
    
    .hero-title {
        font-family: 'Outfit', sans-serif !important;
        font-size: clamp(1.8rem, 4vw, 2.8rem); font-weight: 800;
        letter-spacing: -0.5px; color: var(--text-primary); margin: 0 0 1rem; 
        line-height: 1.6 !important; padding-bottom: 0.5rem; display: block;
    }
    .hero-title .acc {
        color: var(--blue);
    }
    .hero-sub {
        font-size: 1.05rem; color: var(--text-secondary);
        font-weight: 400; max-width: 550px; margin: 0 auto; 
        line-height: 1.6; text-align: center;
    }

    /* ── SOLID CARD ── */
    .glass {
        background: var(--bg-card); 
        border: 1px solid var(--border);
        border-radius: var(--r-lg); 
        padding: 24px;
        transition: border-color .2s;
    }

    /* ── SECTION TITLES ── */
    .sec {
        display: flex; align-items: center; gap: 10px;
        margin: 2.5rem 0 1rem; font-size: 1.05rem; font-weight: 700;
        color: var(--text-primary);
    }
    .sec-dot {
        width: 8px; height: 8px; border-radius: 50%; background: var(--blue);
        flex-shrink: 0;
    }

    /* ── TEAM TAG ── */
    .team-tag {
        font-size: 0.75rem; font-weight: 600; letter-spacing: 1px; text-transform: uppercase;
        color: var(--text-secondary); margin-bottom: 8px;
        display: flex; align-items: center; gap: 6px;
    }

    /* ── SELECTBOX ── */
    div[data-testid="stSelectbox"] > div > div {
        background: var(--bg-primary) !important; 
        border: 1px solid var(--border) !important;
        border-radius: var(--r-sm) !important; 
        color: var(--text-primary) !important;
        font-weight: 500 !important; font-size: 1rem !important; padding: 6px 12px !important;
    }
    div[data-testid="stSelectbox"] > div > div:hover,
    div[data-testid="stSelectbox"] > div > div:focus-within {
        border-color: var(--blue) !important;
    }
    div[data-baseweb="select"] { background: transparent !important; }
    div[data-baseweb="popover"] { z-index: 9999 !important; background: var(--bg-card) !important; }

    /* ── VS ── */
    .vs-center {
        display: flex; align-items: center; justify-content: center;
        padding-top: 28px;
    }
    .vs-pill {
        background: var(--bg-card);
        border: 1px solid var(--border); border-radius: var(--r-sm);
        padding: 6px 14px; font-family: 'JetBrains Mono', monospace !important;
        font-size: .85rem; font-weight: 700; color: var(--text-dim);
    }

    /* ── CHECKBOX ── */
    div[data-testid="stCheckbox"] label p { color: var(--text-secondary) !important; font-size: .9rem !important; }

    /* ── BUTTON ── */
    .stButton > button {
        background: var(--blue) !important;
        color: white !important; font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important; font-size: 1rem !important;
        border: none !important; border-radius: var(--r-md) !important;
        padding: .75rem 1.5rem !important;
        transition: background .2s !important;
    }
    .stButton > button:hover {
        background: var(--blue-hover) !important;
    }

    /* ── PREDICTION BOX ── */
    .pred-box {
        background: var(--bg-card);
        border: 1px solid var(--border); border-radius: var(--r-xl);
        padding: 2.5rem 2rem; text-align: center;
        margin: 1.5rem 0 1rem;
    }
    .pred-label {
        font-size: .75rem; font-weight: 600; letter-spacing: 2px; text-transform: uppercase;
        color: var(--text-dim); margin-bottom: 12px;
    }
    .pred-result {
        font-family: 'Outfit', sans-serif !important;
        font-size: clamp(2rem,4vw,2.5rem); font-weight: 800; margin: 0;
    }
    .confidence-wrap { margin: 1.5rem auto 0; max-width: 300px; }
    .confidence-row {
        display: flex; justify-content: space-between;
        font-size: .85rem; color: var(--text-secondary); margin-bottom: 6px;
    }
    .confidence-track { height: 8px; background: var(--bg-primary); border-radius: 99px; overflow: hidden; }
    .confidence-fill {
        height: 100%; border-radius: 99px;
        background: var(--blue);
    }
    .pred-home { color: var(--blue); }
    .pred-draw { color: var(--gold); }
    .pred-away { color: var(--green); }

    /* ── PROB BAR ── */
    .prob-bar {
        display: flex; border-radius: var(--r-md); overflow: hidden;
        height: 56px; margin: 1.5rem 0; gap: 2px;
    }
    .prob-seg {
        display: flex; align-items: center; justify-content: center; flex-direction: column;
        font-weight: 700; color: white; font-size: 1.05rem;
        font-family: 'JetBrains Mono', monospace !important;
        padding: 0 4px; overflow: hidden; gap: 2px;
    }
    .prob-seg small {
        font-size: .65rem; font-weight: 500; opacity: .9;
        font-family: 'Inter', sans-serif !important; white-space: nowrap;
        overflow: hidden; text-overflow: ellipsis; max-width: 90%;
    }
    .prob-home { background: var(--blue); border-radius: var(--r-sm) 0 0 var(--r-sm); }
    .prob-draw { background: var(--gold); color: #1e293b; }
    .prob-away { background: var(--green); border-radius: 0 var(--r-sm) var(--r-sm) 0; }

    /* ── STAT CARDS ── */
    .stat-grid {
        display: grid; grid-template-columns: repeat(3,1fr); gap: 16px; margin: 1.5rem 0;
    }
    .stat-card {
        background: var(--bg-card); border: 1px solid var(--border);
        border-radius: var(--r-md); padding: 20px 16px;
        text-align: center;
    }
    .stat-icon { font-size: 1.5rem; margin-bottom: 8px; display: block; }
    .stat-card .label {
        font-size: .65rem; font-weight: 600; letter-spacing: 1px;
        text-transform: uppercase; color: var(--text-dim); margin-bottom: 8px;
    }
    .stat-card .value {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 1.5rem; font-weight: 700; color: var(--text-primary); line-height: 1;
    }
    .stat-card .sub { font-size: .8rem; color: var(--text-secondary); margin-top: 8px; }
    .stat-home .value { color: var(--blue); }
    .stat-away .value { color: var(--green); }

    /* ── COMPARISON TABLE ── */
    .table-wrapper { width: 100%; overflow-x: auto; border-radius: var(--r-md); }
    .cmp-table { width: 100%; border-collapse: collapse; min-width: 400px; }
    .cmp-table th {
        font-size: .75rem; font-weight: 600; text-transform: uppercase;
        color: var(--text-dim); padding: 16px; text-align: center; border-bottom: 2px solid var(--border);
    }
    .cmp-table th:first-child { text-align: left; }
    .cmp-table td { padding: 16px; font-size: .95rem; border-bottom: 1px solid var(--border); text-align: center; }
    .cmp-table td:first-child { text-align: left; color: var(--text-secondary); }
    .cmp-table tr:last-child td { border-bottom: none; }
    .cmp-home-val { color: var(--blue); font-weight: 600; font-family: 'JetBrains Mono', monospace !important; }
    .cmp-away-val { color: var(--green); font-weight: 600; font-family: 'JetBrains Mono', monospace !important; }
    .cmp-winner::after { content: '★'; font-size: .7rem; margin-left: 6px; opacity: .8; }

    /* ── MATCH ROW ── */
    .match-row {
        display: flex; align-items: center; gap: 12px; padding: 12px 16px;
        border-radius: var(--r-sm); margin-bottom: 8px;
        background: var(--bg-card); border: 1px solid var(--border);
        font-size: .9rem;
    }
    .match-badge {
        width: 32px; height: 32px; border-radius: 6px;
        display: flex; align-items: center; justify-content: center;
        font-weight: 700; font-size: .75rem; flex-shrink: 0;
    }
    .mb-w { background: rgba(16, 185, 129, 0.15); color: var(--green); }
    .mb-d { background: rgba(245, 158, 11, 0.15); color: var(--gold); }
    .mb-l { background: rgba(239, 68, 68, 0.15); color: var(--red); }
    .match-teams { color: var(--text-primary); flex: 1; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    .match-date { color: var(--text-dim); font-size: .8rem; }
    .match-score { font-family: 'JetBrains Mono', monospace !important; font-weight: 600; color: var(--text-primary); }

    /* ── FORM HEADER ── */
    .form-header {
        display: flex; align-items: center; gap: 10px; margin-bottom: 16px;
        font-weight: 600; color: var(--text-primary); font-size: 1rem;
        padding-bottom: 12px; border-bottom: 1px solid var(--border);
    }
    .form-header .dot { width: 10px; height: 10px; border-radius: 50%; }
    .dot-home { background: var(--blue); }
    .dot-away { background: var(--green); }

    /* ── FOOTER ── */
    .footer {
        text-align: center; padding: 3rem 0 2rem;
        color: var(--text-dim); font-size: .85rem;
        border-top: 1px solid var(--border); margin-top: 4rem;
    }

    /* ── RESPONSIVE ── */
    @media (max-width: 768px) {
        .block-container { padding: 0 1rem 3rem !important; }
        .hero { padding: 1.5rem 0.5rem; }
        .stat-grid { grid-template-columns: repeat(2,1fr); }
    }
    @media (max-width: 480px) {
        .stat-grid { grid-template-columns: 1fr; }
        .nav-badge { display: none; }
    }
</style>
""", unsafe_allow_html=True)


# ═══ API HELPERS ═══════════════════════════════════════
def api_get(endpoint):
    try:
        resp = requests.get(f"{API_URL}{endpoint}", timeout=120)
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
        resp = requests.post(f"{API_URL}{endpoint}", json=data, timeout=120)
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
    <p class="hero-title">Prédisez le <span class="acc">résultat</span> avant le coup de sifflet</p>
</div>
""", unsafe_allow_html=True)

with st.spinner("Le serveur IA se réveille... (Cela peut prendre jusqu'à 2 minutes au premier lancement)"):
    data = api_get("/teams")
teams = data["teams"]

# ═══ MATCH SETUP ═══════════════════════════════════════
# Removed HTML div wrappers that caused the empty box
st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

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

st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

# ═══ RESULTS ═══════════════════════════════════════════
if predict:
    with st.spinner("Analyse en cours... (Le premier chargement peut prendre jusqu'à 2 minutes)"):
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
            radialaxis=dict(visible=True, range=[0, 10], gridcolor="rgba(0,0,0,0.06)", tickfont=dict(color="#64748b", size=9), linecolor="rgba(0,0,0,0.06)"),
            angularaxis=dict(gridcolor="rgba(0,0,0,0.06)", tickfont=dict(color="#475569", size=12), linecolor="rgba(0,0,0,0.06)"),
        ),
        showlegend=True,
        legend=dict(font=dict(color="#0f172a", size=12), x=0.5, xanchor="center", y=-0.12, orientation="h", bgcolor="rgba(0,0,0,0)"),
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
        xaxis=dict(gridcolor="rgba(0,0,0,0.04)", showgrid=False, zeroline=False, tickfont=dict(color="#64748b", size=10)),
        yaxis=dict(gridcolor="rgba(0,0,0,0.05)", zeroline=False, tickfont=dict(color="#64748b", size=10), title=dict(text="Buts marqués", font=dict(color="#475569", size=11))),
        legend=dict(font=dict(color="#0f172a", size=11), orientation="h", y=1.12, x=0.5, xanchor="center", bgcolor="rgba(0,0,0,0)"),
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
