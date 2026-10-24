import cv2
import numpy as np

# Canvas Setup (1280x720 High-Definition Junction Canvas)
W, H = 1280, 720
img = np.zeros((H, W, 3), dtype=np.uint8)

# 1. Ground / Buildings / Terrain
img[:] = (35, 45, 40) # Urban ground/sidewalk

# 2. Road Network (Char Rasta Crossroads)
road_color = (60, 60, 65)
road_w = 240
cx, cy = W // 2, H // 2

# Horizontal Road (West to East)
cv2.rectangle(img, (0, cy - road_w // 2), (W, cy + road_w // 2), road_color, -1)
# Vertical Road (North to South)
cv2.rectangle(img, (cx - road_w // 2, 0), (cx + road_w // 2, H), road_color, -1)

# Yellow Junction Box (Yellow Criss-Cross Keep Clear Box)
box_x1, box_y1 = cx - road_w // 2, cy - road_w // 2
box_x2, box_y2 = cx + road_w // 2, cy + road_w // 2
cv2.rectangle(img, (box_x1, box_y1), (box_x2, box_y2), (40, 180, 240), 2)
for i in range(-road_w, road_w, 40):
    cv2.line(img, (box_x1 + max(0, i), box_y1), (min(box_x2, box_x1 + road_w + i), box_y2), (30, 160, 220), 1)

# Lane Dividers (Dashed White Lines)
for x in range(0, box_x1, 50):
    cv2.line(img, (x, cy), (x + 30, cy), (240, 240, 240), 2)
for x in range(box_x2, W, 50):
    cv2.line(img, (x, cy), (x + 30, cy), (240, 240, 240), 2)
for y in range(0, box_y1, 50):
    cv2.line(img, (cx, y), (cx, y + 30), (240, 240, 240), 2)
for y in range(box_y2, H, 50):
    cv2.line(img, (cx, y), (cx, y + 30), (240, 240, 240), 2)

# Helper function to draw cars
def draw_car(canvas, x, y, w, h, color, roof_color=(40, 40, 40)):
    cv2.rectangle(canvas, (x, y), (x + w, y + h), color, -1)
    cv2.rectangle(canvas, (x, y), (x + w, y + h), (20, 20, 20), 2)
    # Windshield/Roof
    pad_w = int(w * 0.2)
    pad_h = int(h * 0.2)
    cv2.rectangle(canvas, (x + pad_w, y + pad_h), (x + w - pad_w, y + h - pad_h), roof_color, -1)

# 3. Civilian Vehicles (Trapped at Intersection)
# North Lane Queues (Stopped facing South)
draw_car(img, cx - 80, box_y1 - 90, 60, 75, (180, 50, 50))   # Red Car
draw_car(img, cx - 80, box_y1 - 180, 60, 75, (220, 220, 220)) # White Sedan
draw_car(img, cx - 90, box_y1 - 290, 75, 95, (40, 150, 200))  # Auto/Bus

# South Lane Queues (Stopped facing North)
draw_car(img, cx + 20, box_y2 + 20, 60, 75, (200, 200, 200))  # Silver Car
draw_car(img, cx + 20, box_y2 + 110, 60, 75, (60, 140, 60))   # Green Hatchback

# East Lane Queues (Stopped facing West)
draw_car(img, box_x2 + 25, cy - 80, 75, 55, (220, 160, 30))   # Taxi Yellow
draw_car(img, box_x2 + 120, cy - 80, 75, 55, (190, 190, 190)) # White Car

# 4. Approaching 108 Emergency Ambulance (Far on West Road ~920m away)
amb_x, amb_y = 60, cy + 15
amb_w, amb_h = 130, 85

# Ambulance White Chassis
cv2.rectangle(img, (amb_x, amb_y), (amb_x + amb_w, amb_y + amb_h), (250, 250, 250), -1)
cv2.rectangle(img, (amb_x, amb_y), (amb_x + amb_w, amb_y + amb_h), (30, 30, 30), 2)

# Red Stripe on Side
cv2.rectangle(img, (amb_x, amb_y + 35), (amb_x + amb_w, amb_y + 50), (20, 20, 220), -1)

# Red Cross (+) Marking
cross_cx, cross_cy = amb_x + 50, amb_y + 42
cv2.rectangle(img, (cross_cx - 6, cross_cy - 16), (cross_cx + 6, cross_cy + 16), (20, 20, 220), -1)
cv2.rectangle(img, (cross_cx - 16, cross_cy - 6), (cross_cx + 16, cross_cy + 6), (20, 20, 220), -1)

# Blue/Red Emergency Flashing Beacons
cv2.circle(img, (amb_x + 25, amb_y + 12), 9, (230, 30, 30), -1)  # Red Flasher
cv2.circle(img, (amb_x + 105, amb_y + 12), 9, (30, 140, 240), -1) # Blue Flasher
cv2.putText(img, "108 ALS", (amb_x + 32, amb_y + 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (10, 10, 10), 2)

# 5. AI Vision Detection Bounding Box & HUD
cv2.rectangle(img, (amb_x - 10, amb_y - 15), (amb_x + amb_w + 15, amb_y + amb_h + 15), (0, 255, 0), 3)
cv2.putText(img, "AI LOCKED: 108 AMBULANCE [920.0m]", (amb_x - 10, amb_y - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 0), 2)

# 6. Char Rasta Traffic Signals (3 ALL-RED, 1 GREEN-WAVE)
# North Signal (RED)
cv2.rectangle(img, (cx + 130, box_y1 - 60), (cx + 210, box_y1 - 10), (15, 23, 42), -1)
cv2.circle(img, (cx + 150, box_y1 - 35), 14, (0, 0, 255), -1)
cv2.putText(img, "RED", (cx + 170, box_y1 - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 255), 2)

# South Signal (RED)
cv2.rectangle(img, (cx - 210, box_y2 + 10), (cx - 130, box_y2 + 60), (15, 23, 42), -1)
cv2.circle(img, (cx - 190, box_y2 + 35), 14, (0, 0, 255), -1)
cv2.putText(img, "RED", (cx - 170, box_y2 + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 255), 2)

# East Signal (RED)
cv2.rectangle(img, (box_x2 + 10, cy + 130), (box_x2 + 90, cy + 180), (15, 23, 42), -1)
cv2.circle(img, (box_x2 + 30, cy + 155), 14, (0, 0, 255), -1)
cv2.putText(img, "RED", (box_x2 + 50, cy + 160), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 255), 2)

# West Ambulance Signal (GREEN-WAVE HOLD LOCKED)
cv2.rectangle(img, (box_x1 - 190, cy - 160), (box_x1 - 10, cy - 100), (6, 78, 59), -1)
cv2.rectangle(img, (box_x1 - 190, cy - 160), (box_x1 - 10, cy - 100), (16, 185, 129), 2)
cv2.circle(img, (box_x1 - 160, cy - 130), 16, (0, 255, 0), -1)
cv2.putText(img, "GREEN WAVE", (box_x1 - 135, cy - 125), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 2)

# 7. System Top Banner Overlay
cv2.rectangle(img, (0, 0), (W, 55), (10, 15, 25), -1)
cv2.putText(img, "LIFEROUTE AI: CHAR RASTA AUTONOMOUS PREEMPTION OVERLAY", (25, 36), cv2.FONT_HERSHEY_SIMPLEX, 0.85, (56, 189, 248), 2)
cv2.putText(img, "STATE: 100% EMERGENCY LOCK (WEST APPROACH)", (780, 36), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (74, 222, 128), 2)

# Save Image
output_filename = "char_rasta_ambulance_preemption.jpg"
cv2.imwrite(output_filename, img)
print(f"Char Rasta Preemption Scene generated -> {output_filename}")

