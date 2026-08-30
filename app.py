import os
import joblib
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import importlib

# Force dynamic module reloading for report generator
import report_generator
importlib.reload(report_generator)
from report_generator import generate_pdf_report

from models import train_telemetry_models, analyze_component_image
from agents import run_multi_agent_pipeline

# Page Config
st.set_page_config(
    page_title="AI Factory 2.0: Command Center",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (Dark UI, Custom Badges, Blue Metrics, and Animations)
st.markdown("""
<style>
    .stApp { background-color: #0B0F19; color: #F8FAFC; }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 1px solid #1F2937;
    }
    
    /* Animated Pulsing Status Badges */
    @keyframes pulse-green {
        0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.5); }
        70% { box-shadow: 0 0 0 12px rgba(16, 185, 129, 0); }
        100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
    }
    @keyframes pulse-blue {
        0% { box-shadow: 0 0 0 0 rgba(59, 130, 246, 0.5); }
        70% { box-shadow: 0 0 0 12px rgba(59, 130, 246, 0); }
        100% { box-shadow: 0 0 0 0 rgba(59, 130, 246, 0); }
    }
    @keyframes pulse-yellow {
        0% { box-shadow: 0 0 0 0 rgba(245, 158, 11, 0.5); }
        70% { box-shadow: 0 0 0 12px rgba(245, 158, 11, 0); }
        100% { box-shadow: 0 0 0 0 rgba(245, 158, 11, 0); }
    }

    /* Badges */
    .status-badge-green {
        background-color: rgba(16, 185, 129, 0.15);
        color: #10B981;
        border: 1px solid #10B981;
        border-radius: 8px;
        padding: 12px;
        font-weight: 600;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 8px;
        animation: pulse-green 2s infinite;
    }
    .status-badge-blue {
        background-color: rgba(59, 130, 246, 0.15);
        color: #60A5FA;
        border: 1px solid #3B82F6;
        border-radius: 8px;
        padding: 12px;
        font-weight: 600;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 8px;
        animation: pulse-blue 2s infinite;
    }
    .status-badge-yellow {
        background-color: rgba(245, 158, 11, 0.15);
        color: #FBBF24;
        border: 1px solid #F59E0B;
        border-radius: 8px;
        padding: 12px;
        font-weight: 600;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 8px;
        animation: pulse-yellow 2.5s infinite;
    }

    /* Agent Cards - Interactive 3D Lift & Glow */
    .agent-card {
        background-color: #1E293B;
        border-radius: 8px;
        padding: 15px;
        border-left: 4px solid #38BDF8;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        margin-bottom: 10px;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    }
    .agent-card:hover {
        transform: translateY(-6px) scale(1.02);
        box-shadow: 0 12px 24px rgba(56, 189, 248, 0.3);
        border-left-color: #60A5FA;
    }

    /* Smooth Metric Cards Hover */
    div[data-testid="stMetric"] {
        background: rgba(30, 41, 59, 0.4);
        padding: 10px;
        border-radius: 8px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        transition: all 0.3s ease;
    }
    div[data-testid="stMetric"]:hover {
        transform: scale(1.04);
        background: rgba(30, 41, 59, 0.8);
        border-color: #38BDF8;
    }
</style>
""", unsafe_allow_html=True)

# Train/Verify Models
if not os.path.exists("saved_models/random_forest.pkl"):
    rf_metrics, ann_metrics = train_telemetry_models()
else:
    rf_metrics, ann_metrics = train_telemetry_models()

# SIDEBAR: Branding & System Status Badges
st.sidebar.markdown("## 🏭 AI Factory 2.0 Control")
st.sidebar.caption("Autonomous Manufacturing Intelligence")

selected_machine = st.sidebar.selectbox(
    "Active Machine Focus:",
    ["MCH-01 CNC Mill", "MCH-02 Robotic Arm", "MCH-03 Hydraulic Press", "MCH-04 Lathe"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### System Status")
st.sidebar.markdown('<div class="status-badge-green">🟢 Multimodal Pipeline Active</div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="status-badge-blue">🌐 Multi-Agent Consensus Ready</div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="status-badge-yellow">⚡ Digital Twin Engine Operational</div>', unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🕹️ Telemetry Controls")
temp_in = st.sidebar.slider("Temperature (°C)", 40.0, 110.0, 58.2)
vib_in = st.sidebar.slider("Vibration RMS (mm/s)", 1.0, 10.0, 2.55)
press_in = st.sidebar.slider("Hydraulic Pressure (bar)", 10.0, 150.0, 25.2)
rpm_in = st.sidebar.slider("Spindle Speed (RPM)", 1000, 2400, 1850)

# HEADER SECTION
header_col1, header_col2 = st.columns([3, 1])
with header_col1:
    st.title("🏭 AI FACTORY 2.0: COMMAND CENTER")
    st.caption("Autonomous Manufacturing Intelligence, Multi-Agent Decisioning & Digital Twin Simulation")

with header_col2:
    st.metric(label="System Operational Time", value="99.8%", delta="+0.4%")

st.divider()

# TABBED NAVIGATION
tabs = st.tabs([
    "📊 Live Dashboard", 
    "📈 Multimodal Ingestion & EDA", 
    "🧠 Models & MLOps", 
    "👁️ Vision & NLP Inspection", 
    "🤖 Multi-Agent RAG System"
])

# TAB 1: LIVE DASHBOARD
with tabs[0]:
    st.subheader(f"Real-Time Telemetry & Machine Health: {selected_machine}")
    
    # Run Agent Inference
    agent_data = run_multi_agent_pipeline(temp_in, vib_in, press_in, rpm_in, "data/images/defect_0.png")
    risk_score_pct = agent_data["predictive"]["risk_score"] * 100

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric(label="Temperature", value=f"{temp_in} °C", delta="Normal" if temp_in < 80 else "Overheat", delta_color="normal" if temp_in < 80 else "inverse")
    with m2:
        st.metric(label="Vibration RMS", value=f"{vib_in} mm/s", delta="Normal" if vib_in < 5.0 else "High", delta_color="normal" if vib_in < 5.0 else "inverse")
    with m3:
        st.metric(label="Hydraulic Pressure", value=f"{press_in} bar", delta="-5.0", delta_color="normal")
    with m4:
        st.metric(label="AI Failure Probability", value=f"{risk_score_pct:.1f}%", delta="STABLE" if risk_score_pct < 40 else "CRITICAL", delta_color="normal" if risk_score_pct < 40 else "inverse")

    st.divider()

    # SENSOR TELEMETRY TIME-SERIES DUAL-AXIS CHART
    st.subheader("Sensor Telemetry Time-Series (Last 50 Hours)")
    
    # Generate Synthetic Time-Series Plot
    dates = pd.date_range(start="2026-04-07", periods=50, freq="12h")
    np.random.seed(42)
    temp_series = 65 + np.random.randn(50) * 5
    vib_series = 2.5 + np.random.randn(50) * 0.8
    
    # Introduce spike
    temp_series[10:13] = [88, 93, 85]
    vib_series[10:13] = [5.5, 6.2, 5.1]

    fig, ax1 = plt.subplots(figsize=(10, 3.5), facecolor="#0B0F19")
    ax1.set_facecolor("#FFFFFF")
    
    ax1.set_xlabel('Timestamp', color='black', fontsize=9)
    ax1.set_ylabel('Temperature (°C)', color='brown', fontsize=9)
    ax1.plot(dates, temp_series, color='brown', linewidth=1.5, label='Temperature')
    ax1.tick_params(axis='y', labelcolor='brown')
    ax1.tick_params(axis='x', rotation=45, labelsize=8)
    ax1.axhline(y=80, color='brown', linestyle='--', alpha=0.6)

    ax2 = ax1.twinx()
    ax2.set_ylabel('Vibration (mm/s)', color='steelblue', fontsize=9)
    ax2.plot(dates, vib_series, color='steelblue', linewidth=1.5, label='Vibration')
    ax2.tick_params(axis='y', labelcolor='steelblue')
    ax2.axhline(y=4.0, color='steelblue', linestyle='--', alpha=0.6)

    plt.title(f"Telemetry Trends - {selected_machine}", color='black', fontsize=10, pad=10)
    plt.tight_layout()
    st.pyplot(fig)

    st.divider()

    # DIGITAL TWIN "WHAT-IF" SIMULATION
    st.subheader("🌐 Digital Twin: Operational 'What-If' Simulation")
    sim1, sim2, sim3 = st.columns(3)
    with sim1:
        st.markdown("### Option A: Maintain Load")
        st.write("• Expected Downtime: **4.5 Hours**")
        st.write("• Repair Cost: **$12,500**")
        st.error(f"Failure Risk: {min(100.0, risk_score_pct * 1.2):.1f}%")
    with sim2:
        st.markdown("### Option B: Full Emergency Stop")
        st.write("• Downtime: **1.0 Hour**")
        st.write("• Repair Cost: **$1,200**")
        st.success("Failure Risk: 0.0%")
    with sim3:
        st.markdown("### Option C: Throttle Speed (30%)")
        st.write("• Output Capacity: **70%**")
        st.write("• Repair Cost: **$400**")
        st.warning(f"Failure Risk: {max(5.0, risk_score_pct * 0.25):.1f}%")

# TAB 2: MULTIMODAL INGESTION & EDA
with tabs[1]:
    st.subheader("📋 Raw Telemetry Ingestion Log")
    if os.path.exists("data/factory_telemetry.csv"):
        df_log = pd.read_csv("data/factory_telemetry.csv")
        st.dataframe(df_log.head(15), use_container_width=True)

# TAB 3: MODELS & MLOPS
with tabs[2]:
    st.subheader("🧠 Model Performance & Benchmarking")
    comp_df = pd.DataFrame([rf_metrics, ann_metrics], index=["Baseline (Random Forest)", "Deep Learning (ANN)"])
    st.table(comp_df)

# TAB 4: VISION & NLP INSPECTION
with tabs[3]:
    st.subheader("👁️ Surface Defect Detection & SOP Extraction")
    vcol1, vcol2 = st.columns(2)
    with vcol1:
        st.write("**Defect Image Analysis**")
        if os.path.exists("data/images/defect_0.png"):
            st.image("data/images/defect_0.png", width=220)
            res_d = analyze_component_image("data/images/defect_0.png")
            st.caption(f"Classification: {res_d['label']} | Severity: {res_d['severity']}")
    with vcol2:
        st.write("**SOP Document Retrieval**")
        if os.path.exists("data/factory_sop.txt"):
            with open("data/factory_sop.txt", "r") as f:
                st.text(f.read())

# TAB 5: MULTI-AGENT RAG SYSTEM & HUMAN-IN-THE-LOOP
with tabs[4]:
    st.subheader("🤖 Multi-Agent Consensus Cards")
    ca1, ca2, ca3, ca4 = st.columns(4)
    with ca1:
        st.markdown(f'<div class="agent-card"><b>👁️ Vision Agent</b><br><small>{agent_data["vision"]["details"]}</small></div>', unsafe_allow_html=True)
    with ca2:
        st.markdown(f'<div class="agent-card"><b>📈 Predictive Agent</b><br><small>Failure Risk: {risk_score_pct:.1f}%</small></div>', unsafe_allow_html=True)
    with ca3:
        st.markdown(f'<div class="agent-card"><b>📚 Knowledge Agent</b><br><small>{agent_data["knowledge"][:45]}...</small></div>', unsafe_allow_html=True)
    with ca4:
        st.markdown(f'<div class="agent-card"><b>🧠 Planning Agent</b><br><small>Urgency: <b>{agent_data["planning"]["urgency"]}</b></small></div>', unsafe_allow_html=True)

    st.divider()

    st.subheader("🧑‍💼 Human-in-the-Loop Audit & Executive PDF Export")
    hcol1, hcol2 = st.columns(2)
    with hcol1:
        decision = st.radio("Supervisor Protocol:", ["Approve Recommended Action", "Modify Parameters", "Reject System Alert"])
    with hcol2:
        if st.button("📄 Generate PDF Audit Report", type="primary"):
            pdf_path = generate_pdf_report(
                machine_id=selected_machine,
                status_decision=decision,
                risk_score=risk_score_pct,
                temp=temp_in,
                vib=vib_in,
                recommendations=agent_data["planning"]["recommendations"]
            )
            with open(pdf_path, "rb") as file:
                st.download_button(
                    label="⬇️ Download Executive Audit PDF",
                    data=file,
                    file_name=f"Incident_Report_{selected_machine.replace(' ', '_')}.pdf",
                    mime="application/pdf"
                )