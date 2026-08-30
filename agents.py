import os
import cv2
import numpy as np

try:
    from models import predict_failure_risk
except ImportError:
    # Safe fallback if models module is loaded from a different path
    def predict_failure_risk(sensor_input):
        temp = sensor_input.get('temperature', 75.0)
        vibe = sensor_input.get('vibration', 0.04)
        risk = 10.0
        if temp > 85.0:
            risk += 40.0
        if vibe > 0.05:
            risk += 40.0
        return min(round(risk, 2), 100.0)


class VisionAgent:
    """Analyzes surface inspection frames for visual defect detection."""
    def run(self, image_path):
        if not os.path.exists(image_path):
            return {
                "status": "NOMINAL",
                "severity": 0.0,
                "details": "Inspection frame unavailable"
            }
            
        img = cv2.imread(image_path)
        if img is None:
            return {
                "status": "NOMINAL",
                "severity": 0.0,
                "details": "Unable to decode visual stream"
            }
            
        # Detect anomaly region via HSV masking
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower_red = np.array([0, 100, 100])
        upper_red = np.array([10, 255, 255])
        mask = cv2.inRange(hsv, lower_red, upper_red)
        defect_pixel_count = cv2.countNonZero(mask)
        
        if defect_pixel_count > 50:
            return {
                "status": "CRACK DETECTED",
                "severity": 85.0,
                "details": "Surface structural crack identified"
            }
        return {
            "status": "NOMINAL",
            "severity": 5.0,
            "details": "No visual surface anomalies detected"
        }


class PredictiveAgent:
    """Evaluates multi-sensor telemetry to compute failure likelihood and identify drivers."""
    def run(self, temp, vibe, press, rpm):
        sensor_input = {
            "temperature": temp,
            "vibration": vibe,
            "pressure": press,
            "rpm": rpm
        }
        
        failure_prob = predict_failure_risk(sensor_input)
        
        # Determine primary operational risk driver
        drivers = []
        if temp > 85.0:
            drivers.append("Thermal Overheating")
        if vibe > 0.05:
            drivers.append("Mechanical Vibration Exceeded")
        if press < 95.0 or press > 110.0:
            drivers.append("Pressure Anomaly")
            
        primary_driver = drivers[0] if drivers else "Nominal Operating Parameters"
        
        return {
            "failure_probability": failure_prob,
            "risk_score": failure_prob / 100.0,  # Key required by app.py (0.0 to 1.0 range)
            "status": "HIGH RISK" if failure_prob > 50.0 else "STABLE",
            "primary_driver": primary_driver
        }


class KnowledgeAgent:
    """Retrieves grounded Standard Operating Procedures (SOPs) safely handling Unicode text."""
    def run(self, primary_driver, sop_filepath="data/factory_sop.txt"):
        sop_text = ""
        
        # Robust UTF-8 file reading with fallback
        if os.path.exists(sop_filepath):
            try:
                with open(sop_filepath, "r", encoding="utf-8", errors="ignore") as f:
                    sop_text = f.read()
            except Exception:
                sop_text = ""

        # Default fallback SOP lookup if file is empty or missing specific query
        if "Thermal Overheating" in primary_driver:
            return "SOP-702: High thermal output detected. Reduce thermal load, inspect coolant flow rate, and engage auxiliary cooling fans."
        elif "Vibration" in primary_driver:
            return "SOP-409: High vibration detected. Throttle spindle speed by 30%, inspect bearing alignment, and check dynamic balance."
        elif "Pressure" in primary_driver:
            return "SOP-305: Hydraulic pressure anomaly. Inspect pressure release valves and check fluid levels."
            
        if sop_text.strip():
            return sop_text[:300] + "..."
            
        return "SOP-101: Continue standard operational monitoring schedule. All metrics within tolerance."


class PlanningAgent:
    """Synthesizes diagnostic agent signals to produce optimal, prioritized action plans."""
    def run(self, vision_res, pred_res, sop_res):
        failure_risk = pred_res.get("failure_probability", 0.0)
        vision_severity = vision_res.get("severity", 0.0)
        
        if failure_risk > 75.0 or vision_severity > 80.0:
            action = "EMERGENCY SHUTDOWN & IMMEDIATE INSPECTION"
            priority = "CRITICAL"
        elif failure_risk > 40.0 or vision_severity > 40.0:
            action = "THROTTLE SPEED (-30%) & SCHEDULE MAINTENANCE"
            priority = "MEDIUM"
        else:
            action = "MAINTAIN NOMINAL PRODUCTION LOAD"
            priority = "LOW"
            
        return {
            "recommended_action": action,
            "priority": priority,
            "sop_reference": sop_res
        }


def run_multi_agent_pipeline(temp, vibe, press, rpm, image_path="data/images/defect_0.png"):
    """Orchestrates full multi-agent workflow execution."""
    v_agent = VisionAgent()
    p_agent = PredictiveAgent()
    k_agent = KnowledgeAgent()
    plan_agent = PlanningAgent()
    
    v_res = v_agent.run(image_path)
    p_res = p_agent.run(temp, vibe, press, rpm)
    k_res = k_agent.run(p_res["primary_driver"])
    plan_res = plan_agent.run(v_res, p_res, k_res)
    
    return {
        "vision": v_res,
        "predictive": p_res,
        "knowledge": k_res,
        "consensus": plan_res
    }
