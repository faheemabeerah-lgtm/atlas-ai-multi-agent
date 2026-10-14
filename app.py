import streamlit as st
from crew import run_research

st.set_page_config(
    page_title="Atlas AI • Research Team",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');
:root { --ink:#eaf0ff; --muted:#a9b7d0; --panel:#101a2c; --line:rgba(180,198,230,.15); }
html, body, [class*="css"] { font-family:'DM Sans',sans-serif; }
.stApp { background: radial-gradient(ellipse at 15% 0%, #172b50 0%, #0a1020 42%, #080d18 100%); color:var(--ink); }
.block-container { max-width: 1200px; padding-top: 2rem; padding-bottom: 4rem; }
h1,h2,h3 { font-family:'Manrope',sans-serif !important; letter-spacing:-.035em; }
.hero { padding: 2.1rem 2.2rem; border:1px solid var(--line); border-radius:24px;
background:linear-gradient(120deg,rgba(29,52,91,.88),rgba(16,26,44,.92)); margin-bottom:1.25rem; }
.eyebrow { color:#8bb8ff; text-transform:uppercase; font-size:.76rem; font-weight:800; letter-spacing:.16em; }
.hero h1 { font-size:clamp(2.2rem,5vw,3.8rem); margin:.45rem 0 .7rem; color:#f6f8ff; }
.hero p { max-width:740px; color:#bdcbe3; font-size:1.05rem; line-height:1.7; }
.pill { display:inline-block; border:1px solid rgba(139,184,255,.32); color:#b9d4ff;
border-radius:999px; padding:.38rem .72rem; margin:.15rem .25rem .1rem 0; font-size:.78rem; }
.agent-card { background:rgba(16,26,44,.86); border:1px solid var(--line); border-radius:16px; padding:1rem; min-height:155px; }
.agent-number { color:#8bb8ff; font-weight:800; font-size:.78rem; letter-spacing:.12em; }
.agent-title { color:#f4f7ff; font-family:'Manrope',sans-serif; font-size:1.04rem; font-weight:800; margin:.45rem 0; }
.agent-desc { color:#a9b7d0; font-size:.87rem; line-height:1.5; }
div[data-testid="stTextArea"] textarea, div[data-testid="stTextInput"] input {
background:#0d1728 !important; color:#eef3ff !important; border:1px solid #293953 !important; border-radius:12px !important;
}
.stButton > button, .stDownloadButton > button { border-radius:12px; font-weight:800; min-height:2.8rem; }
.stButton > button[kind="primary"] { background:linear-gradient(90deg,#4c7df0,#8065f5); border:0; color:white; }
div[data-testid="stMetric"] { background:rgba(16,26,44,.8); border:1px solid var(--line); padding:1rem; border-radius:14px; }
div[data-testid="stExpander"] { border:1px solid var(--line); border-radius:12px; }
footer {visibility:hidden;}
</style>
""", unsafe_allow_html=True)

if "report" not in st.session_state:
    st.session_state.report = ""
if "sources" not in st.session_state:
    st.session_state.sources = []
if "topic" not in st.session_state:
    st.session_state.topic = ""

with st.sidebar:
    st.markdown("## 🔎 Atlas AI")
    st.caption("Multi-agent research workspace")
    st.markdown("---")
    st.markdown("**Your research team**")
    st.markdown("🧭 **01 · Researcher**")
    st.caption("Searches the live web")
    st.markdown("🧠 **02 · Analyst**")
    st.caption("Finds patterns and insights")
    st.markdown("🛡️ **03 · Fact-checker**")
    st.caption("Checks claims and uncertainty")
    st.markdown("✍️ **04 · Report writer**")
    st.caption("Builds the final report")
    st.markdown("---")
    st.caption("Model: Groq · GPT-OSS 120B")
    st.caption("Search: DuckDuckGo")
    st.caption("Research may contain errors; verify important claims against cited sources.")

st.markdown("""
<div class="hero">
  <div class="eyebrow">AI-powered research studio</div>
  <h1>From question to<br>evidence-backed insight.</h1>
  <p>Four specialized AI agents research, analyze, cross-check, and synthesize your topic into one clear report. Watch the team work, step by step.</p>
  <span class="pill">4 specialist agents</span><span class="pill">Live web search</span><span class="pill">Source-aware report</span>
</div>
""", unsafe_allow_html=True)

st.markdown("### Meet your research team")
cols = st.columns(4, gap="medium")
agents = [
    ("01", "Researcher", "Collects recent information and source URLs.", "🧭"),
    ("02", "Analyst", "Turns evidence into themes and useful insights.", "🧠"),
    ("03", "Fact-checker", "Looks for corroboration and flags weak claims.", "🛡️"),
    ("04", "Report writer", "Creates the final structured report.", "✍️"),
]
for col, (num, name, desc, emoji) in zip(cols, agents):
    with col:
        st.markdown(f"""<div class="agent-card"><div class="agent-number">AGENT {num}</div>
        <div class="agent-title">{emoji} {name}</div><div class="agent-desc">{desc}</div></div>""",
        unsafe_allow_html=True)

st.markdown("")
left, right = st.columns([1.45, 1], gap="large")
with left:
    st.markdown("### Start a research mission")
    topic = st.text_area(
        "What should the team investigate?",
        placeholder="Example: How is generative AI changing university education in 2026?",
        height=125,
        max_chars=600,
        help="Be specific for a more useful report.",
    )
    focus = st.selectbox(
        "Research angle",
        ["Balanced overview", "Latest developments", "Business opportunities", "Risks and limitations", "Academic / technical analysis"],
    )
    depth = st.select_slider("Report depth", options=["Brief", "Standard", "Detailed"], value="Standard")
    run = st.button("🚀  Run the research team", type="primary", use_container_width=True)
with right:
    st.markdown("### What you’ll receive")
    st.markdown("""
    - **Executive summary** of the key findings
    - **Main findings** organized into readable sections
    - **Evidence and source URLs** gathered by search tools
    - **Fact-check notes** for uncertainty or conflicting information
    - **Conclusion and next questions** for deeper research
    """)
    st.info("Tip: a focused question usually produces a stronger report than a broad topic such as “technology”.")

if run:
    if not topic.strip():
        st.warning("Enter a research topic first.")
    else:
        st.session_state.report = ""
        st.session_state.sources = []
        st.session_state.topic = topic.strip()
        status = st.status("Preparing the research team…", expanded=True)
        progress = st.empty()

        def on_agent_start(name, detail):
            progress.markdown(f"### ⚡ Currently working: **{name}**\n\n{detail}")
            status.write(f"▶️ {name} started")

        def on_agent_done(name):
            status.write(f"✅ {name} completed")

        try:
            with st.spinner("The team is working. Research can take a few minutes…"):
                report, sources = run_research(
                    topic=topic.strip(),
                    focus=focus,
                    depth=depth,
                    on_agent_start=on_agent_start,
                    on_agent_done=on_agent_done,
                )
            st.session_state.report = str(report)
            st.session_state.sources = sources
            status.update(label="Research mission completed", state="complete", expanded=False)
            progress.markdown("### ✅ All four agents have completed their work.")
        except Exception as exc:
            status.update(label="Research mission needs attention", state="error", expanded=True)
            st.error("The research run failed. Check the deployment logs and the troubleshooting section below.")
            st.code(str(exc))
            st.stop()

if st.session_state.report:
    st.markdown("---")
    st.markdown("## 📘 Research report")
    st.caption(f"Research topic: {st.session_state.topic}")
    st.download_button(
        "⬇️ Download report (.md)",
        data=st.session_state.report,
        file_name="atlas_research_report.md",
        mime="text/markdown",
    )
    st.markdown(st.session_state.report)
    if st.session_state.sources:
        with st.expander(f"🔗 Search sources ({len(st.session_state.sources)})", expanded=False):
            for source in st.session_state.sources:
                st.markdown(f"- [{source['title']}]({source['url']})")
                if source.get("snippet"):
                    st.caption(source["snippet"])

with st.expander("Troubleshooting"):
    st.markdown("""
    **Missing GROQ_API_KEY:** open Streamlit Cloud → your app → Settings → Secrets and add `GROQ_API_KEY = "your_key"`.

    **Model or API error:** confirm the key is active and the Groq account can access `openai/gpt-oss-120b`.

    **Search error:** DuckDuckGo is a free third-party search service and can temporarily rate-limit requests. Retry later if this happens.

    **Build error:** verify that `requirements.txt` is in the repository root and Python is set to 3.12. Read the first dependency error in Streamlit Cloud → Manage app → Logs.
    """)
