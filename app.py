import os
import streamlit as st
from datetime import datetime
from langchain_core.messages import HumanMessage
from main import app

# ── Page Configuration ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Travel Booking System",
    page_icon="✈️",
    layout="wide"
)

# ── Session State for Inputs ──────────────────────────────────────────────────
if "user_query_val" not in st.session_state:
    st.session_state.user_query_val = ""

def set_query_text(text):
    st.session_state.user_query_val = text

# ── Custom CSS: Dark Violet & Aurora Gradient Theme ────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

html, body, .stApp {
    font-family: 'Plus Jakarta Sans', sans-serif;
    background-color: #09070f !important;
    color: #f3f4f6;
}

/* ── Dynamic Ambient Glows ── */
.bg-glow-1 {
    position: fixed;
    top: -10%;
    left: -10%;
    width: 50vw;
    height: 50vw;
    background: radial-gradient(circle, rgba(168, 85, 247, 0.18) 0%, rgba(0,0,0,0) 70%);
    border-radius: 50%;
    z-index: 0;
    pointer-events: none;
}
.bg-glow-2 {
    position: fixed;
    bottom: -10%;
    right: -10%;
    width: 55vw;
    height: 55vw;
    background: radial-gradient(circle, rgba(236, 72, 153, 0.15) 0%, rgba(0,0,0,0) 70%);
    border-radius: 50%;
    z-index: 0;
    pointer-events: none;
}

/* ── Hero Banner ── */
.hero-wrapper {
    position: relative;
    border-radius: 24px;
    overflow: hidden;
    margin-bottom: 2rem;
    height: 260px;
    border: 1px solid rgba(168, 85, 247, 0.25);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
}
.hero-bg {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
    filter: brightness(0.35) saturate(1.2);
    position: absolute;
    top: 0; left: 0;
}
.hero-content {
    position: relative;
    z-index: 2;
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 2rem;
    background: linear-gradient(180deg, rgba(9, 7, 15, 0.1) 0%, rgba(9, 7, 15, 0.85) 100%);
}
.hero-badge {
    background: rgba(168, 85, 247, 0.2);
    border: 1px solid rgba(168, 85, 247, 0.5);
    color: #d8b4fe !important;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 0.35rem 1rem;
    border-radius: 20px;
    margin-bottom: 0.8rem;
    display: inline-block;
}
.hero-title {
    font-size: 2.5rem;
    font-weight: 800;
    color: #ffffff;
    margin: 0 0 0.5rem;
    line-height: 1.2;
}
.hero-sub {
    color: #9ca3af;
    font-size: 0.95rem;
    max-width: 600px;
}

/* ── Section Headers ── */
.sec-head {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    margin: 2rem 0 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}
.sec-head span { font-size: 1.15rem; font-weight: 700; color: #f3f4f6; }

/* ── Input Card ── */
.input-label {
    color: #a855f7;
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 0.75rem;
}

/* ── Primary Violet/Pink Gradient Button ── */
div[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #a855f7 0%, #ec4899 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.85rem 2rem !important;
    font-size: 1.05rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.02em !important;
    width: 100% !important;
    box-shadow: 0 4px 20px rgba(168, 85, 247, 0.35) !important;
    transition: all 0.3s ease !important;
}
div[data-testid="stButton"] > button:hover {
    box-shadow: 0 6px 28px rgba(236, 72, 153, 0.5) !important;
    transform: translateY(-2px) !important;
    filter: brightness(1.1) !important;
}
div[data-testid="stButton"] > button:active {
    transform: translateY(0px) !important;
}

/* ── Agent Status Expanders ── */
[data-testid="stStatusWidget"] {
    background: rgba(22, 17, 35, 0.8) !important;
    border: 1px solid rgba(168, 85, 247, 0.2) !important;
    border-radius: 14px !important;
    backdrop-filter: blur(12px) !important;
}
[data-testid="stStatusWidget"] > div:first-child {
    background: rgba(22, 17, 35, 0.9) !important;
    border-radius: 14px 14px 0 0 !important;
}
[data-testid="stStatusWidget"] details,
[data-testid="stStatusWidget"] details > div,
[data-testid="stStatusWidget"] [data-testid="stVerticalBlock"] {
    background: rgba(14, 10, 24, 0.95) !important;
    color: #e5e7eb !important;
    padding: 0.5rem 0.75rem !important;
}
[data-testid="stStatusWidget"] * { color: #f3f4f6 !important; }
[data-testid="stStatusWidget"] a { color: #ec4899 !important; }
[data-testid="stStatusWidget"] hr { border-color: rgba(168, 85, 247, 0.2) !important; }

/* ── Metric Bar ── */
.metric-row {
    display: flex;
    gap: 1rem;
    margin: 1.5rem 0;
}
.metric-box {
    flex: 1;
    background: rgba(22, 17, 35, 0.75);
    border: 1px solid rgba(168, 85, 247, 0.2);
    border-radius: 14px;
    padding: 1.2rem;
    text-align: center;
    backdrop-filter: blur(12px);
}
.metric-val { 
    font-size: 1.8rem; 
    font-weight: 800; 
    background: linear-gradient(135deg, #a855f7, #ec4899);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.metric-lbl { 
    font-size: 0.75rem; 
    color: #9ca3af !important; 
    margin-top: 0.25rem; 
    text-transform: uppercase; 
    letter-spacing: 0.08em; 
    font-weight: 600;
}

/* ── Final Plan Card ── */
.final-card {
    background: linear-gradient(165deg, rgba(26, 18, 48, 0.85) 0%, rgba(14, 10, 24, 0.95) 100%);
    border: 1px solid rgba(168, 85, 247, 0.3);
    border-left: 4px solid #ec4899;
    border-radius: 16px;
    padding: 1.8rem;
    line-height: 1.8;
    color: #e5e7eb;
    font-size: 0.95rem;
    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
}

/* ── Save / Info Bar ── */
.save-bar {
    background: rgba(22, 17, 35, 0.75);
    border: 1px solid rgba(168, 85, 247, 0.2);
    border-radius: 12px;
    padding: 0.85rem 1.2rem;
    color: #9ca3af;
    font-size: 0.88rem;
    margin-top: 0.5rem;
}
.save-bar code { color: #ec4899 !important; background: rgba(255, 255, 255, 0.06) !important; }

/* ── Sidebar Styling ── */
section[data-testid="stSidebar"] {
    background: rgba(14, 10, 24, 0.9) !important;
    border-right: 1px solid rgba(168, 85, 247, 0.18) !important;
    backdrop-filter: blur(16px);
}
.sidebar-chip {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-radius: 8px;
    padding: 0.5rem 0.75rem;
    margin-bottom: 0.4rem;
    font-size: 0.82rem;
    color: #9ca3af;
}
.sidebar-title { 
    color: #f3f4f6; 
    font-size: 0.75rem; 
    text-transform: uppercase;
    letter-spacing: 0.1em;
    font-weight: 700; 
    margin: 1.2rem 0 0.6rem; 
}

/* ── Streamlit Form Input Styling ── */
.stTextArea textarea {
    background: rgba(10, 7, 18, 0.6) !important;
    border: 1px solid rgba(168, 85, 247, 0.25) !important;
    border-radius: 12px !important;
    color: #f3f4f6 !important;
    font-size: 0.95rem !important;
    resize: none !important;
}
.stTextArea textarea:focus {
    border-color: #ec4899 !important;
    box-shadow: 0 0 0 3px rgba(236, 72, 153, 0.18) !important;
}
.stTextArea textarea::placeholder { color: #6b7280 !important; }

input[type="text"], .stTextInput input {
    background: rgba(14, 10, 24, 0.7) !important;
    border: 1px solid rgba(168, 85, 247, 0.25) !important;
    border-radius: 8px !important;
    color: #f3f4f6 !important;
}
input[type="text"]:focus, .stTextInput input:focus {
    border-color: #ec4899 !important;
    box-shadow: 0 0 0 2px rgba(236, 72, 153, 0.2) !important;
}

.stTextInput label, .stTextArea label {
    color: #a855f7 !important;
    font-size: 0.82rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.08em !important;
}

.stMarkdown p, .stMarkdown li, .stMarkdown td, .stMarkdown th { color: #d1d5db !important; }
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3 { color: #f3f4f6 !important; }

/* Download Button */
div[data-testid="stDownloadButton"] > button {
    background: rgba(168, 85, 247, 0.18) !important;
    color: #ffffff !important;
    border: 1px solid #a855f7 !important;
    border-radius: 10px !important;
}
div[data-testid="stDownloadButton"] > button:hover {
    background: #a855f7 !important;
    box-shadow: 0 0 15px rgba(168, 85, 247, 0.4) !important;
}

/* Hide branding */
#MainMenu, footer, header { visibility: hidden; }
</style>

<!-- Ambient Glow Divs -->
<div class="bg-glow-1"></div>
<div class="bg-glow-2"></div>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="font-size: 1.25rem; font-weight: 800; background: linear-gradient(135deg, #ffffff, #a855f7, #ec4899); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
        ✈️ AI Travel Planner
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    thread_id = st.text_input("👤 Session User ID", value="ankush_user",
                              help="Session ID keeps travel history across your queries")

    st.markdown("<div class='sidebar-title'>Powered by</div>", unsafe_allow_html=True)
    for tech in ["🔗 LangGraph", "🧠 Groq · LLaMA 3.3 70B", "🐘 PostgreSQL", "🔍 Tavily Search", "✈️ AviationStack"]:
        st.markdown(f"<div class='sidebar-chip'>{tech}</div>", unsafe_allow_html=True)

    st.markdown("<div class='sidebar-title'>Agent Pipeline</div>", unsafe_allow_html=True)
    for step in ["① Flight Agent", "② Hotel Agent", "③ Itinerary Agent", "④ Final Agent"]:
        st.markdown(f"<div class='sidebar-chip'>{step}</div>", unsafe_allow_html=True)

# ── Hero Section ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrapper">
    <img class="hero-bg"
         src="https://images.unsplash.com/photo-1436491865332-7a61a109cc05?w=1400&q=80"
         alt="airplane above clouds"/>
    <div class="hero-content">
        <div class="hero-badge">✦ Multi-Agent AI System</div>
        <div class="hero-title">✈️ AI Travel Booking System</div>
        <div class="hero-sub">Four autonomous AI agents work together — searching flights, finding hotels, building an itinerary, and delivering your personalized trip plan.</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Destination Visual Picker Strip ───────────────────────────────────────────
DESTINATIONS = [
    ("🇯🇵 Tokyo",   "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=300&q=70", "Plan a 7-day trip to Tokyo including flights, hotels and sightseeing under ₹2 Lakhs"),
    ("🇫🇷 Paris",   "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=300&q=70", "Paris trip for 5 days with luxury stay and central attractions"),
    ("🇹🇭 Bangkok", "https://images.unsplash.com/photo-1508009603885-50cf7c579365?w=300&q=70", "5-day Bangkok trip under budget with street food and temple tours"),
    ("🇮🇹 Rome",    "https://images.unsplash.com/photo-1552832230-c0197dd311b5?w=300&q=70", "4 days in Rome exploring historical monuments, flights and stays"),
    ("🇦🇪 Dubai",   "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=300&q=70", "Dubai weekend getaway 3 days luxury experience"),
]

cols = st.columns(5)
for col, (name, img_url, prompt_preset) in zip(cols, DESTINATIONS):
    with col:
        st.markdown(f"""
        <div style="border-radius:12px;overflow:hidden;position:relative;height:85px;margin-bottom:6px;border:1px solid rgba(168,85,247,0.25);">
            <img src="{img_url}" style="width:100%;height:100%;object-fit:cover;filter:brightness(0.65);" />
            <div style="position:absolute;bottom:6px;left:0;right:0;text-align:center;
                        color:#fff;font-size:0.8rem;font-weight:700;">{name}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"Select {name.split()[1]}", key=f"dest_{name}"):
            set_query_text(prompt_preset)

st.markdown("<br>", unsafe_allow_html=True)

# ── User Input & Presets ──────────────────────────────────────────────────────
st.markdown("<div class='input-label'>🗺️ Describe your trip</div>", unsafe_allow_html=True)

QUICK = [
    "7-day Japan under ₹2L",
    "Paris trip for 5 days",
    "Dubai weekend trip",
    "Bali backpacking 10 days"
]

qcols = st.columns(len(QUICK))
for qc, label in zip(qcols, QUICK):
    with qc:
        if st.button(label, key=f"q_{label}"):
            set_query_text(f"Plan a complete {label} including flights, hotels and sightseeing")

user_query = st.text_area(
    "",
    value=st.session_state.user_query_val,
    placeholder="e.g. Plan a complete 7-day Japan trip including flights, hotels and sightseeing under ₹2 lakhs...",
    height=100,
    label_visibility="collapsed",
)

generate = st.button("🚀 Generate My Travel Plan", use_container_width=True)

# ── Agent Execution Pipeline ──────────────────────────────────────────────────
AGENT_META = {
    "flight_agent":    ("✈️", "Flight Agent"),
    "hotel_agent":     ("🏨", "Hotel Agent"),
    "itinerary_agent": ("🗓️", "Itinerary Agent"),
    "final_agent":     ("🧠", "Final Synthesis Agent"),
}

if generate:
    if not user_query.strip():
        st.warning("Please describe your trip first.")
    else:
        config = {"configurable": {"thread_id": thread_id}}
        collected = {
            "flight_results": "",
            "hotel_results": "",
            "itinerary": "",
            "final_response": "",
            "llm_calls": 0
        }

        st.markdown("---")
        st.markdown("<div class='sec-head'><span>🤖 Agent Pipeline — Live Status</span></div>", unsafe_allow_html=True)

        # Stream execution through LangGraph
        for chunk in app.stream(
            {
                "messages": [HumanMessage(content=user_query)],
                "user_query": user_query,
                "flight_results": "",
                "hotel_results": "",
                "itinerary": "",
                "llm_calls": 0,
            },
            config=config,
            stream_mode="updates",
        ):
            for node_name, state_update in chunk.items():
                icon, label = AGENT_META.get(node_name, ("🔧", node_name))

                with st.status(f"{icon}  {label}", state="complete", expanded=True):
                    if node_name == "flight_agent":
                        text = state_update.get("flight_results", "")
                        collected["flight_results"] = text
                        st.markdown(text or "_No flight data returned._")

                    elif node_name == "hotel_agent":
                        text = state_update.get("hotel_results", "")
                        collected["hotel_results"] = text
                        st.markdown(text or "_No hotel data returned._")

                    elif node_name == "itinerary_agent":
                        text = state_update.get("itinerary", "")
                        collected["itinerary"] = text
                        st.markdown(text or "_No itinerary generated._")

                    elif node_name == "final_agent":
                        msgs = state_update.get("messages", [])
                        text = msgs[-1].content if msgs else ""
                        collected["final_response"] = text
                        st.markdown(text or "_No final response._")

                    collected["llm_calls"] = state_update.get("llm_calls", collected["llm_calls"])

        # ── Execution Metrics ─────────────────────────────────────────────────
        st.markdown(f"""
        <div class="metric-row">
            <div class="metric-box"><div class="metric-val">4</div><div class="metric-lbl">Agents Executed</div></div>
            <div class="metric-box"><div class="metric-val">{collected['llm_calls']}</div><div class="metric-lbl">LLM Calls Made</div></div>
            <div class="metric-box"><div class="metric-val">✅</div><div class="metric-lbl">Status</div></div>
        </div>
        """, unsafe_allow_html=True)

        # ── Final Plan Card ───────────────────────────────────────────────────
        if collected["final_response"]:
            st.markdown("<div class='sec-head'><span>🧠 Final Travel Plan</span></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='final-card'>{collected['final_response']}</div>", unsafe_allow_html=True)

        # ── Auto-Save to File System ──────────────────────────────────────────
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"travel_plan_{timestamp}.md"
        save_dir = os.path.join(os.path.dirname(__file__), "travel_plans")
        os.makedirs(save_dir, exist_ok=True)

        file_content = f"""# Travel Plan
**Query:** {user_query}
**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**User Session ID:** {thread_id}

---

## ✈️ Flight Information
{collected['flight_results'] or 'N/A'}

---

## 🏨 Hotel Information
{collected['hotel_results'] or 'N/A'}

---

## 🗓️ Itinerary
{collected['itinerary'] or 'N/A'}

---

## 🧠 Final Travel Plan
{collected['final_response'] or 'N/A'}

---
*LLM Calls Executed: {collected['llm_calls']}*
"""
        with open(os.path.join(save_dir, filename), "w", encoding="utf-8") as f:
            f.write(file_content)

        # Download & Save Bar
        dl_col, info_col = st.columns([1, 3])
        with dl_col:
            st.download_button(
                "⬇️ Download Markdown Plan",
                data=file_content,
                file_name=filename,
                mime="text/markdown",
                use_container_width=True
            )
        with info_col:
            st.markdown(f"<div class='save-bar'>📁 Auto-saved session → <code>travel_plans/{filename}</code></div>", unsafe_allow_html=True)