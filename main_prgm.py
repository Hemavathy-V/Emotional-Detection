from transformers import pipeline
import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="Emotion Detector AI",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="expanded",
)

EMOTIONS = {
    "anger":    {"emoji": "😠", "color": "#FF4757"},
    "disgust":  {"emoji": "🤢", "color": "#2ED573"},
    "fear":     {"emoji": "😨", "color": "#A29BFE"},
    "joy":      {"emoji": "😄", "color": "#FFA502"},
    "neutral":  {"emoji": "😐", "color": "#B2BEC3"},
    "sadness":  {"emoji": "😢", "color": "#74B9FF"},
    "surprise": {"emoji": "😲", "color": "#FD9644"},
}

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
* { font-family: 'Inter', sans-serif !important; }
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0d0d1a 0%, #1a1a2e 40%, #0f3460 100%);
    min-height: 100vh;
}
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.04) !important;
    border-right: 1px solid rgba(255,255,255,0.08);
}
[data-testid="stSidebar"] * { color: white !important; }
[data-testid="stSidebar"] .stButton > button {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    color: rgba(255,255,255,0.7) !important;
    border-radius: 12px !important;
    font-size: 14px !important;
    padding: 10px 20px !important;
    box-shadow: none !important;
}
h1, h2, h3, p, label, div { color: white; }
.main-title {
    font-size: 3rem;
    font-weight: 800;
    text-align: center;
    background: linear-gradient(90deg, #FF6B6B, #FFA502, #4ECDC4, #74B9FF);
    background-size: 300% 300%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: gradientShift 4s ease infinite;
    margin-bottom: 4px;
    line-height: 1.2;
}
@keyframes gradientShift {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
.subtitle {
    text-align: center;
    color: rgba(255,255,255,0.5) !important;
    font-size: 1rem;
    margin-bottom: 2rem;
    letter-spacing: 0.5px;
}
.emotion-card {
    background: rgba(255,255,255,0.07);
    backdrop-filter: blur(20px);
    border-radius: 24px;
    padding: 36px 24px;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.12);
    animation: slideUp 0.5s ease-out;
}
@keyframes slideUp {
    from { opacity: 0; transform: translateY(24px); }
    to   { opacity: 1; transform: translateY(0); }
}
.emotion-emoji {
    font-size: 88px;
    line-height: 1;
    margin-bottom: 14px;
    display: block;
    animation: float 2.4s ease-in-out infinite alternate;
}
@keyframes float {
    from { transform: translateY(0px); }
    to   { transform: translateY(-12px); }
}
.emotion-name {
    font-size: 2rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 5px;
    margin-bottom: 6px;
}
.emotion-conf { font-size: 1rem; color: rgba(255,255,255,0.65) !important; }
.scores-wrap { padding: 8px 0; }
.score-row { display: flex; align-items: center; margin: 9px 0; gap: 10px; }
.score-label { width: 100px; color: rgba(255,255,255,0.85); font-size: 0.88rem; font-weight: 500; flex-shrink: 0; }
.bar-track { flex: 1; background: rgba(255,255,255,0.08); border-radius: 20px; height: 10px; overflow: hidden; }
.bar-fill { height: 100%; border-radius: 20px; }
.score-pct { width: 46px; text-align: right; color: rgba(255,255,255,0.7); font-size: 0.82rem; font-weight: 600; flex-shrink: 0; }
.section-label {
    font-size: 0.78rem; font-weight: 700; letter-spacing: 2px; text-transform: uppercase;
    color: rgba(255,255,255,0.4) !important; margin-bottom: 12px;
}
.divider { border: none; border-top: 1px solid rgba(255,255,255,0.08); margin: 28px 0; }
.history-row {
    display: flex; align-items: center; background: rgba(255,255,255,0.04);
    border-radius: 12px; padding: 12px 16px; margin: 8px 0; border-left: 4px solid; gap: 10px;
}
.history-text { flex: 1; color: rgba(255,255,255,0.75); font-size: 0.88rem; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.history-badge { font-size: 0.82rem; font-weight: 700; white-space: nowrap; }
.history-time { font-size: 0.74rem; color: rgba(255,255,255,0.3); white-space: nowrap; }
.stat-box {
    background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px; padding: 20px 16px; text-align: center; margin-bottom: 14px;
}
.stat-num { font-size: 2.2rem; font-weight: 800; color: white; }
.stat-desc { font-size: 0.78rem; color: rgba(255,255,255,0.45) !important; margin-top: 4px; text-transform: uppercase; letter-spacing: 1px; }
.stTextArea > div > div > textarea {
    background: rgba(255,255,255,0.06) !important; border: 2px solid rgba(255,255,255,0.15) !important;
    border-radius: 16px !important; color: white !important; font-size: 15px !important;
    padding: 14px !important; resize: none !important; transition: border-color 0.25s !important;
}
.stTextArea > div > div > textarea:focus {
    border-color: rgba(78,205,196,0.6) !important;
    box-shadow: 0 0 0 3px rgba(78,205,196,0.12) !important;
}
.stTextArea > div > div > textarea::placeholder { color: rgba(255,255,255,0.28) !important; }
.stTextArea label { display: none !important; }
.stButton > button {
    background: linear-gradient(135deg, #FF6B6B, #4ECDC4) !important;
    color: white !important; border: none !important; border-radius: 14px !important;
    padding: 14px 28px !important; font-size: 16px !important; font-weight: 700 !important;
    width: 100% !important; letter-spacing: 0.5px !important; transition: all 0.25s ease !important;
    box-shadow: 0 6px 28px rgba(255,107,107,0.28) !important;
}
.stButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 10px 36px rgba(255,107,107,0.45) !important; }
.warning-box {
    background: rgba(255,170,0,0.12); border: 1px solid rgba(255,170,0,0.3);
    border-radius: 12px; padding: 12px 16px; color: #FFA502 !important; font-size: 0.9rem; text-align: center;
}
#MainMenu, footer, [data-testid="stDecoration"] { display: none !important; }
</style>
"""

@st.cache_resource(show_spinner=False)
def load_model():
    return pipeline(
        "text-classification",
        model="j-hartmann/emotion-english-distilroberta-base",
        top_k=None,
    )

def parse_scores(raw) -> dict:
    items = raw[0] if isinstance(raw[0], list) else raw
    return {r["label"].lower(): r["score"] for r in items}

def score_bars_html(scores: dict, highlight: str) -> str:
    rows = []
    for emotion, score in sorted(scores.items(), key=lambda x: x[1], reverse=True):
        meta = EMOTIONS.get(emotion, {"emoji": "❓", "color": "#95A5A6"})
        pct = score * 100
        opacity = "1" if emotion == highlight else "0.5"
        rows.append(f"""
        <div class="score-row" style="opacity:{opacity}">
          <div class="score-label">{meta['emoji']} {emotion.capitalize()}</div>
          <div class="bar-track"><div class="bar-fill" style="width:{pct:.1f}%;background:{meta['color']};"></div></div>
          <div class="score-pct">{pct:.1f}%</div>
        </div>""")
    return f'<div class="scores-wrap">{"".join(rows)}</div>'

def emotion_card_html(emotion: str, confidence: float) -> str:
    meta = EMOTIONS.get(emotion, {"emoji": "❓", "color": "#95A5A6"})
    return f"""
    <div class="emotion-card" style="border:2px solid {meta['color']}33;">
      <span class="emotion-emoji">{meta['emoji']}</span>
      <div class="emotion-name" style="color:{meta['color']};">{emotion.upper()}</div>
      <div class="emotion-conf">Confidence: <strong>{confidence*100:.1f}%</strong></div>
    </div>"""

if "history" not in st.session_state:
    st.session_state.history = []
if "total" not in st.session_state:
    st.session_state.total = 0
if "last" not in st.session_state:
    st.session_state.last = None

st.markdown(CSS, unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 📊 Dashboard")
    st.markdown(f"""
    <div class="stat-box">
      <div class="stat-num">{st.session_state.total}</div>
      <div class="stat-desc">Total Analyses</div>
    </div>""", unsafe_allow_html=True)

    if st.session_state.history:
        counts: dict = {}
        for h in st.session_state.history:
            counts[h["emotion"]] = counts.get(h["emotion"], 0) + 1
        top = max(counts, key=counts.get)
        top_meta = EMOTIONS.get(top, {"emoji": "❓"})
        st.markdown(f"""
        <div class="stat-box">
          <div class="stat-num">{top_meta['emoji']}</div>
          <div class="stat-desc">Most detected<br>{top.capitalize()}</div>
        </div>""", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("**Emotion Breakdown**")
        for emotion, cnt in sorted(counts.items(), key=lambda x: x[1], reverse=True):
            meta = EMOTIONS.get(emotion, {"emoji": "❓", "color": "#95A5A6"})
            pct = cnt / st.session_state.total * 100
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:8px;margin:6px 0;">
              <span>{meta['emoji']}</span>
              <div style="flex:1;background:rgba(255,255,255,0.08);border-radius:20px;height:8px;overflow:hidden;">
                <div style="width:{pct:.0f}%;height:100%;background:{meta['color']};border-radius:20px;"></div>
              </div>
              <span style="font-size:0.8rem;color:rgba(255,255,255,0.5);width:28px;text-align:right;">{cnt}</span>
            </div>""", unsafe_allow_html=True)

    st.markdown("---")
    if st.button("🗑️  Clear History"):
        st.session_state.history = []
        st.session_state.total = 0
        st.session_state.last = None
        st.rerun()

st.markdown('<h1 class="main-title">🎭 Emotion Detector AI</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle">Powered by DistilRoBERTa &nbsp;·&nbsp; Detects 7 Emotions in Real-Time</p>',
    unsafe_allow_html=True,
)

with st.spinner("⚡ Loading AI model…"):
    model = load_model()

user_input = st.text_area(
    "input",
    placeholder="Type or paste your text here…\ne.g. 'I can't believe how amazing today turned out!'",
    height=130,
    key="user_input",
    label_visibility="collapsed",
)

_, btn_col, _ = st.columns([1, 2, 1])
with btn_col:
    run = st.button("✨  Analyze Emotion")

if run:
    if not user_input.strip():
        st.markdown('<div class="warning-box">⚠️ Please enter some text before analyzing.</div>', unsafe_allow_html=True)
        st.session_state.last = None
    else:
        with st.spinner("Analyzing…"):
            raw = model(user_input)
        scores = parse_scores(raw)
        top = max(scores, key=scores.get)
        conf = scores[top]
        st.session_state.last = {"emotion": top, "confidence": conf, "scores": scores}
        st.session_state.history.insert(0, {
            "text": user_input,
            "emotion": top,
            "score": conf,
            "time": datetime.now().strftime("%H:%M"),
        })
        st.session_state.total += 1

if st.session_state.last:
    r = st.session_state.last
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    left, right = st.columns([1, 1], gap="large")
    with left:
        st.markdown('<p class="section-label">Detected Emotion</p>', unsafe_allow_html=True)
        st.markdown(emotion_card_html(r["emotion"], r["confidence"]), unsafe_allow_html=True)
    with right:
        st.markdown('<p class="section-label">All Emotion Scores</p>', unsafe_allow_html=True)
        st.markdown(score_bars_html(r["scores"], r["emotion"]), unsafe_allow_html=True)

if st.session_state.history:
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<p class="section-label">Recent Analyses</p>', unsafe_allow_html=True)
    for item in st.session_state.history[:6]:
        meta = EMOTIONS.get(item["emotion"], {"emoji": "❓", "color": "#95A5A6"})
        snippet = (item["text"][:65] + "…") if len(item["text"]) > 65 else item["text"]
        st.markdown(f"""
        <div class="history-row" style="border-left-color:{meta['color']};">
          <div class="history-text">"{snippet}"</div>
          <div class="history-badge" style="color:{meta['color']};">{meta['emoji']} {item['emotion'].capitalize()}</div>
          <div class="history-time">{item['time']}</div>
        </div>""", unsafe_allow_html=True)
