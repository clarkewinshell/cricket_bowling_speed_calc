
# 🏏 Cricket Bowling Speed Calculator  

A simple **Windows Application** written in python & tkinter to measure cricket bowling speeds using video frame analysis.

---
## Features
- Input bowler details (name, type).
- Adjustable **pitching length** (default: 20.12 m for standard cricket pitch).
- Configurable **FPS** (frames per second) depending on video source.
- Calculates speed in **km/h** and **mph**.
- Save results to a **CSV file** for record-keeping.
- User-friendly **GUI** with reset & error handling.
---
## How It Works
1. Record a delivery with a fixed-frame-rate camera.
2. Identify the **frame number when the ball leaves the bowler’s hand** (start-frame).
3. Identify the **frame when the ball bounces on the pitch** (end-frame).
4. Enter the FPS (frames per second) of the recording.
5. The app computes:

$$
\Delta \text{frames} = \text{End-frame} - \text{Start-frame}
$$

$$
t \; (s) = \frac{\Delta \text{frames}}{\text{FPS}}
$$

$$
v \; (m/s) = \frac{\text{Pitch length (m)}}{t \; (s)}
$$

$$
v_{km/h} = v \times 3.6, \quad v_{mph} = v_{km/h} \times 0.621371
$$


6. Converted to **km/h** and **mph** for display.

## Usage
2.  Run the script:  `main.py` 
3.  Fill in the inputs and click **Calc** to compute speed.
4.  Click **Save** to export results as CSV.

## Example Output (CSV)

`Date,Time,Bowler's Name,Bowler Type,Pitching length (m),Start-frame,End-frame,FPS,Δ-frame,Time (s),Speed (mph),Speed (km/h)
2025-09-14,10:32:15 AM,James,Fast,20.12,45,95,30,50,1.667,54.00,86.87` 

## Requirements
- Python 3.6 or higher
- Tkinter (usually included with Python)

## Notes
-   Ensure accurate **frame selection** for best results. _(Kinovea could be a good option)_
-   Made only for **Individual testing purpose**, Highly inconvenient and inaccurate for professional-grade speed tracking.
