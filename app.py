import os
import streamlit as st
from agents import run_multi_agent_pipeline
from report_generator import generate_pdf_report

# Page Configuration
st.set_page_config(
    page_title="AI Factory 2.0 Command Center",
    page_icon="🏭",
    layout="wide"
)

# Custom Styling / UI Overrides
st.markdown("""
    <style>
    .main {
        background-color: #0b0f19;
    }
    .stMetric {
        background-color: #1e293b;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #334155;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🏭 AI Factory 2.0: Industrial Command Center")
st.caption("Real-Time Telemetry, Visual Inspection, Multi-Agent RAG & Executive Auditing")

st.divider()

# Sidebar Control Options
st.sidebar.header("⚙️ Control Panel")
machine_id = st.sidebar.selectbox("Select Machine Unit", ["MCH-01 CNC Mill", "MCH-02 Hydraulic Press", "MCH-03 Robotic Arm"])
inspection_frame = st.sidebar.radio("Optical Frame Stream", ["Defect Anomaly Frame", "Nominal Frame"])

# Determine Image Frame Path
if inspection_frame == "Defect Anomaly Frame":
    image_path = "data/images/defect_0.png"
else:
    image_path = "data/images/normal_0.png"

# Section 1: Interactive Telemetry Controls
st.subheader(f"📡 Real-Time Telemetry & Machine Health: {machine_id}")

col_s1, col_s2, col_s3, col_s4 = st.columns(4)

with col_s1:
    temp_in = st.slider("Temperature (°C)", 40.0, 130.0, 88.5, step=0.5)
with col_s2:
    vib_in = st.slider("Vibration RMS (g)", 0.01, 0.12, 0.065, step=0.005)
with col_s3:
    press_in = st.slider("Hydraulic Pressure (kPa)", 80.0, 130.0, 94.0, step=0.5)
with col_s4:
    rpm_in = st.slider("Spindle Speed (RPM)", 800, 3000, 1950, step=50)

st.divider()

# Section 2: Visual Inspection & Agent Pipeline Execution
col_v1, col_v2 = st.columns([1, 1.5])

with col_v1:
    st.subheader("👁️ Live Visual Stream")
    if os.path.exists(image_path):
        st.image(image_path, caption=f"Active Stream: {inspection_frame}", use_container_width=True)
    else:
        st.warning("Visual frame stream offline or file missing.")

with col_v2:
    st.subheader("🤖 Multi-Agent Pipeline Analysis")
    
    # Execute Multi-Agent Workflow
    agent_data = run_multi_agent_pipeline(temp_in, vib_in, press_in, rpm_in, image_path)
    
    # Extract Safety Metrics safely
    risk_score_pct = agent_data["predictive"].get("failure_probability", agent_data["predictive"].get("risk_score", 0.0) * 100)
    vision_severity = agent_data["vision"].get("severity", 0.0)
    primary_action = agent_data["consensus"].get("recommended_action", "N/A")
    priority_level = agent_data["consensus"].get("priority", "LOW")
    
    # Display Key Performance Metrics
    m1, m2, m3 = st.columns(3)
    m1.metric("Predicted Failure Risk", f"{risk_score_pct}%")
    m2.metric("Vision Defect Severity", f"{vision_severity}%")
    m3.metric("Action Priority", priority_level)
    
    st.markdown(f"**Recommended Strategy:** `{primary_action}`")
    st.info(f"**Grounded SOP Directive:**\n{agent_data['knowledge']}")

st.divider()

# Section 3: Executive Reporting & Documentation
st.subheader("📄 Automated Compliance & Grounding Audit")

col_r1, col_r2 = st.columns([1, 1])

with col_r1:
    st.markdown("### Export Executive Audit Report")
    st.write("Generate a formal PDF report containing multi-agent diagnostics, telemetry snapshots, and digital signature lines.")
    
    if st.button("🔨 Build Executive PDF Audit", type="primary"):
        pdf_path = generate_pdf_report(machine_id, {
            "temperature": temp_in,
            "vibration": vib_in,
            "pressure": press_in,
            "rpm": rpm_in
        }, agent_data["consensus"])
        
        if os.path.exists(pdf_path):
            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="⬇️ Download Audit PDF",
                    data=f,
                    file_name=f"Audit_Report_{machine_id.replace(' ', '_')}.pdf",
                    mime="application/pdf"
                )

with col_r2:
    st.markdown("### Grounding Documentation (SOP)")
    sop_file = "data/factory_sop.txt"
    if os.path.exists(sop_file):
        # FIX FOR LINE 275: Explicit UTF-8 decoding with error suppression
        with open(sop_file, "r", encoding="utf-8", errors="ignore") as f:
            st.text_area("Reference SOP Text File", f.read(), height=160)
    else:
        st.caption("Standard Operating Procedure document not found at `data/factory_sop.txt`.")
