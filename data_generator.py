import os
import cv2
import numpy as np
import pandas as pd


def generate_factory_datasets():
  os.makedirs("data", exist_ok=True)
  os.makedirs("data/images", exist_ok=True)

  np.random.seed(42)
  n_samples = 500

  machine_ids = np.random.choice(
      ["MCH-101", "MCH-102", "MCH-103", "MCH-104"], n_samples
  )
  temperature = np.random.normal(loc=75.0, scale=12.0, size=n_samples)
  vibration = np.random.normal(loc=4.5, scale=1.5, size=n_samples)
  pressure = np.random.normal(loc=100.0, scale=15.0, size=n_samples)
  rpm = np.random.normal(loc=1800, scale=200, size=n_samples)

  failure = []
  maintenance_notes = []

  for idx in range(n_samples):
    temp = temperature[idx]
    vib = vibration[idx]
    press = pressure[idx]

    if temp > 92.0 or vib > 7.2 or press < 75.0:
      failure.append(1)
      maintenance_notes.append(
          "Critical anomaly detected! Maintenance needed."
      )
    elif temp > 83.0 or vib > 5.8:
      failure.append(0)
      maintenance_notes.append("Elevated sensor readings observed.")
    else:
      failure.append(0)
      maintenance_notes.append("Routine check completed. Parameters normal.")

  df = pd.DataFrame({
      "timestamp": pd.date_range(
          start="2026-08-01", periods=n_samples, freq="15min"
      ),
      "machine_id": machine_ids,
      "temperature": np.round(temperature, 2),
      "vibration": np.round(vibration, 2),
      "pressure": np.round(pressure, 2),
      "rpm": np.round(rpm, 2),
      "maintenance_notes": maintenance_notes,
      "failure_label": failure,
  })

  df.to_csv("data/factory_telemetry.csv", index=False)

  # Generate sample defect images
  for i in range(10):
    img = np.full((128, 128, 3), 200, dtype=np.uint8)
    cv2.circle(img, (64, 64), 40, (100, 100, 100), -1)
    cv2.imwrite(f"data/images/normal_{i}.png", img)

    img_def = np.full((128, 128, 3), 200, dtype=np.uint8)
    cv2.circle(img_def, (64, 64), 40, (100, 100, 100), -1)
    cv2.line(img_def, (40, 40), (88, 88), (20, 20, 20), 4)
    cv2.imwrite(f"data/images/defect_{i}.png", img_def)

  # Write SOP file
  sop_content = """FACTORY STANDARD OPERATING PROCEDURE (SOP) - AI FACTORY 2.0
Document ID: SOP-MNT-2026

1. TEMPERATURE OVERHEAT PROTOCOL (Temp > 90°C):
- Action: Reduce spindle RPM by 30% immediately or trigger Emergency Coolant Flush.
- Recommended Parts: Check Heat Exchanger Valve (Part #HX-402).

2. HIGH VIBRATION PROTOCOL (Vibration > 7.0 mm/s):
- Action: Halt production line. Inspect motor alignment and mounting bolts.
- Recommended Parts: Replace Main Bearing Block (Part #BB-901).
"""
  with open("data/factory_sop.txt", "w") as f:
    f.write(sop_content)


if __name__ == "__main__":
  generate_factory_datasets()
  print("✅ Datasets generated successfully!")