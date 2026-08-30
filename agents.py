import os
import joblib
import pandas as pd
from models import analyze_component_image


class VisionAgent:
  """Agent 1: Analyzes component images for surface defects."""

  def run(self, image_path):
    if not os.path.exists(image_path):
      return {"defect": False, "details": "No image uploaded."}
    analysis = analyze_component_image(image_path)
    return {
        "defect": analysis["defect_detected"],
        "details": f"{analysis['label']} ({analysis['severity']})",
    }


class PredictiveMaintenanceAgent:
  """Agent 2: Evaluates telemetry sensor risk."""

  def run(self, temp, vib, press, rpm):
    if not os.path.exists("saved_models/random_forest.pkl"):
      return {"risk_score": 0.0, "high_risk": False}

    model = joblib.load("saved_models/random_forest.pkl")
    df_in = pd.DataFrame(
        [[temp, vib, press, rpm]],
        columns=["temperature", "vibration", "pressure", "rpm"],
    )
    prob = model.predict_proba(df_in)[0][1]

    return {
        "risk_score": float(prob),
        "high_risk": prob > 0.40,
        "primary_driver": (
            "Temperature Overheat"
            if temp > 85
            else ("High Vibration" if vib > 6.0 else "Normal")
        ),
    }


class KnowledgeAgent:
  """Agent 3: RAG Engine retrieving Standard Operating Procedures (SOPs)."""

  def run(self, query_context):
    sop_path = "data/factory_sop.txt"
    if not os.path.exists(sop_path):
      return "No SOP documentation available."

    with open(sop_path, "r") as f:
      sop_text = f.read()

    if "temperature" in query_context.lower() or "overheat" in query_context.lower():
      return (
          "SOP-MNT-2026 (Temp Protocol): Reduce spindle RPM by 30% or trigger"
          " Emergency Coolant Flush. Inspect Heat Exchanger Valve (#HX-402)."
      )
    elif "vibration" in query_context.lower():
      return (
          "SOP-MNT-2026 (Vibration Protocol): Halt production line. Inspect"
          " motor alignment. Replace Main Bearing Block (#BB-901)."
      )
    return "SOP-MNT-2026: Continue standard operational monitoring."


class PlanningAgent:
  """Agent 4: Orchestrates findings and generates operational recommendations."""

  def run(self, vision_res, pred_res, sop_res):
    recommendations = []
    urgency = "LOW"

    if pred_res["high_risk"] or vision_res["defect"]:
      urgency = "HIGH"
      if pred_res["risk_score"] > 0.60:
        recommendations.append(
            "CRITICAL: Initiate 30% speed reduction on machine."
        )
      if vision_res["defect"]:
        recommendations.append(
            "INSPECTION: Schedule part replacement for surface cracks."
        )
      recommendations.append(f"PROTOCOL: {sop_res}")
    else:
      recommendations.append(
          "NOMINAL: Continue standard production load. No action required."
      )

    return {
        "urgency": urgency,
        "recommendations": recommendations,
        "summary": (
            f"Multi-Agent Consensus: Telemetry Risk Score"
            f" {pred_res['risk_score']*100:.1f}%. Defect Status:"
            f" {vision_res['details']}."
        ),
    }


def run_multi_agent_pipeline(temp, vib, press, rpm, image_path="data/images/defect_0.png"):
  v_agent = VisionAgent()
  p_agent = PredictiveMaintenanceAgent()
  k_agent = KnowledgeAgent()
  plan_agent = PlanningAgent()

  v_res = v_agent.run(image_path)
  p_res = p_agent.run(temp, vib, press, rpm)
  k_res = k_agent.run(p_res["primary_driver"])
  plan = plan_agent.run(v_res, p_res, k_res)

  return {
      "vision": v_res,
      "predictive": p_res,
      "knowledge": k_res,
      "planning": plan,
  }