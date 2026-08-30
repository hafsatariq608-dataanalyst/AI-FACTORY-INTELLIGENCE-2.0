# 🏭 AI Factory 2.0: Autonomous Manufacturing Intelligence & Command Center

An end-to-end industrial command center integrating real-time multimodal telemetry, computer vision defect inspection, multi-agent AI consensus workflows, dynamic digital twin simulations, and automated executive PDF audit generation.

---

## 📌 System Architecture & High-Level Execution Flow

```text
+-----------------------------------------------------------------------------------+
|                            1. MULTIMODAL DATA INGESTION                           |
|  [ Sensor Telemetry: Temp, Vibration, Pressure, RPM ]   [ Optical Inspection Cam ]|
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                        2. PREDICTIVE & VISION INFERENCE ENGINE                    |
|  • Machine Learning: Random Forest & ANN Deep Learning models (Failure Risk %)    |
|  • Computer Vision: OpenCV surface defect detection & visual severity scoring    |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                          3. MULTI-AGENT RAG CONSENSUS                             |
|   👁️ Vision Agent   |  📈 Predictive Agent  |  📚 Knowledge Agent (SOP RAG)        |
|   +-----------------+-----------+-----------+-------------------------------------+
|                                 |
|                                 v
|                       🧠 Planning Agent Synthesis                                 |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                      4. DIGITAL TWIN OPERATIONAL SIMULATION                       |
|   Evaluates: Maintain Load | Emergency Stop | Speed Throttle (-30%) | Reroute      |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                     5. HUMAN-IN-THE-LOOP (HITL) & PDF AUDITING                    |
|   • Plant Supervisor Decision Validation / Manual Override                        |
|   • Automated ReportLab Executive Compliance PDF Export                           |
+-----------------------------------------------------------------------------------+


## 🚀 Key Features

* 📊 **Real-Time Telemetry Dashboard:** Live monitoring of temperature, vibration RMS, hydraulic pressure, and spindle speeds across industrial machinery with interactive dual-axis trend visualizations.
* 👁️ **Multimodal Computer Vision Inspection:** Automated surface defect classification with severity grading and confidence metrics.
* 🤖 **Multi-Agent RAG Orchestration:** 
  * **Vision Agent:** Analyzes visual component evidence.
  * **Predictive Maintenance Agent:** Evaluates sensor values using ML/ANN models to assess failure probabilities.
  * **Knowledge Agent:** Retrieves grounded Standard Operating Procedures (SOPs) from documentation.
  * **Planning Agent:** Formulates actionable operational consensus and recommendations.
* 🌐 **Digital Twin Operational Simulation:** Runs dynamic "What-If" scenarios comparing operational risk against estimated financial impact and downtime.
* 🧑‍💼 **Human-in-the-Loop Governance & PDF Auditing:** Enables supervisor override/approval with instant automated generation of structured executive PDF incident audit reports.

---

## 🛠️ Tech Stack

* **Frontend & UI:** Streamlit (Custom CSS, responsive dark UI, animated badges)
* **Data & Machine Learning:** Python, Pandas, NumPy, Scikit-Learn (Random Forest), PyTorch/TensorFlow (ANN), Matplotlib
* **Document Generation & Reporting:** ReportLab / PyPDF (Automated executive report layout engine)
* **Orchestration:** Multi-Agent consensus pipelines & RAG retrieval mechanisms

---

## ⚙️ Project Structure

```text
├── app.py                   # Main Streamlit application runner
├── report_generator.py      # PDF audit report generator
├── models.py                # Telemetry ML models & vision classification logic
├── agents.py                # Multi-agent consensus pipeline implementation
├── data/                    # Telemetry CSV, sample defect images & SOP text files
└── output/                  # Generated PDF audit reports
---

## 🚀 How to Run the Application

Follow these steps to launch the **AI Factory 2.0** command center locally using VS Code or your system terminal.

### 1. Set Up & Activate Virtual Environment
Open your terminal (or press `Ctrl + ~` in VS Code) and run:

* **Windows (PowerShell):**
  ```powershell
  python -m venv venv
  .\venv\Scripts\activate
