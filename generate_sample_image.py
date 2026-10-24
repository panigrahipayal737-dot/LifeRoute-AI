from PIL import Image, ImageDraw, ImageFont
import os

def create_ambulance_traffic_scene(output_path="sample_ambulance_traffic.jpg"):
    W, H = 1000, 650
    img = Image.new("RGB", (W, H), color=(20, 26, 38))
    draw = ImageDraw.Draw(img)

    # 1. 3-Lane Asphalt Road (Perspective View)
    road_poly = [(120, 650), (320, 100), (680, 100), (880, 650)]
    draw.polygon(road_poly, fill=(35, 42, 54), outline=(71, 85, 105), width=2)

    # Footpaths / Curbs
    draw.polygon([(0, 650), (120, 650), (320, 100), (0, 100)], fill=(24, 30, 42))
    draw.polygon([(880, 650), (1000, 650), (1000, 100), (680, 100)], fill=(24, 30, 42))

    # Lane Dividers (Dashed White Lines)
    for i in range(12):
        y1 = 120 + i * 42
        y2 = y1 + 24
        # Left Divider
        x1_l = int(320 + (120 - 320) * (y1 - 100) / 550 + 80)
        x2_l = int(320 + (120 - 320) * (y2 - 100) / 550 + 80)
        draw.line([(x1_l, y1), (x2_l, y2)], fill=(255, 255, 255), width=3)

        # Right Divider
        x1_r = int(680 + (880 - 680) * (y1 - 100) / 550 - 80)
        x2_r = int(680 + (880 - 680) * (y2 - 100) / 550 - 80)
        draw.line([(x1_r, y1), (x2_r, y2)], fill=(255, 255, 255), width=3)

    # Stop Line & Traffic Junction in Background
    draw.line([(310, 130), (690, 130)], fill=(239, 68, 68), width=3)

    # -------------------------------------------------------------
    # 2. AAGE KI GADIYAN (FRONT VEHICLES IN TRAFFIC)
    # -------------------------------------------------------------
    
    # A) Front-Left: Auto-Rickshaw (Yellow & Green)
    draw.rectangle([(250, 160), (330, 230)], fill=(234, 179, 8), outline=(255, 255, 255), width=2)
    draw.rectangle([(260, 170), (320, 210)], fill=(22, 101, 52)) # Roof
    draw.text((255, 235), "AUTO-RICKSHAW", fill=(250, 204, 21))

    # B) Front-Center: White Sedan Car
    draw.rectangle([(440, 150), (550, 240)], fill=(241, 245, 249), outline=(148, 163, 184), width=2)
    draw.rectangle([(455, 165), (535, 200)], fill=(30, 41, 59)) # Rear Glass
    draw.rectangle([(470, 215), (520, 230)], fill=(250, 204, 21)) # Number Plate
    draw.text((475, 217), "GJ-01", fill=(0, 0, 0))
    draw.text((455, 245), "SEDAN CAR", fill=(203, 213, 225))

    # C) Front-Right: Red/Orange Two-Wheeler Motorcycle
    draw.ellipse([(670, 180), (705, 235)], fill=(234, 88, 12), outline=(251, 146, 60), width=2)
    draw.text((660, 240), "2-WHEELER", fill=(251, 146, 60))

    # D) Mid-Right: Blue SUV Car
    draw.rectangle([(620, 280), (760, 400)], fill=(29, 78, 216), outline=(96, 165, 250), width=2)
    draw.rectangle([(640, 300), (740, 350)], fill=(15, 23, 42)) # Windshield
    draw.rectangle([(665, 365), (735, 385)], fill=(250, 204, 21)) # Number Plate
    draw.text((672, 368), "GJ-05-AB", fill=(0, 0, 0))
    draw.text((660, 405), "PRIVATE SUV", fill=(96, 165, 250))

    # E) Mid-Left: City Auto #2
    draw.rectangle([(180, 290), (280, 390)], fill=(234, 179, 8), outline=(255, 255, 255), width=2)
    draw.rectangle([(195, 305), (265, 365)], fill=(22, 101, 52))
    draw.text((190, 395), "AUTO #02", fill=(250, 204, 21))

    # -------------------------------------------------------------
    # 3. PICHE AMBULANCE (EMERGENCY AMBULANCE 108 IN REAR LANE)
    # -------------------------------------------------------------
    # Large high-detail Ambulance approaching from behind in the center corridor lane
    amb_x1, amb_y1 = 360, 380
    amb_x2, amb_y2 = 580, 590

    # Ambulance Body (White + Bright Red Emergency Markings)
    draw.rectangle([(amb_x1, amb_y1), (amb_x2, amb_y2)], fill=(255, 255, 255), outline=(220, 38, 38), width=4)
    # Red Side Stripe
    draw.rectangle([(amb_x1 + 10, amb_y1 + 90), (amb_x2 - 10, amb_y1 + 130)], fill=(220, 38, 38))
    # Emergency Red Cross
    cross_cx, cross_cy = (amb_x1 + amb_x2) // 2, amb_y1 + 110
    draw.rectangle([(cross_cx - 8, cross_cy - 22), (cross_cx + 8, cross_cy + 22)], fill=(255, 255, 255))
    draw.rectangle([(cross_cx - 22, cross_cy - 8), (cross_cx + 22, cross_cy + 8)], fill=(255, 255, 255))

    # Rear Windshield
    draw.rectangle([(amb_x1 + 25, amb_y1 + 20), (amb_x2 - 25, amb_y1 + 80)], fill=(15, 23, 42), outline=(148, 163, 184), width=2)

    # Flashing Dual Siren Light Bar on Roof
    draw.rectangle([(amb_x1 + 40, amb_y1 - 25), (amb_x1 + 90, amb_y1)], fill=(239, 68, 68), outline=(255, 255, 255), width=2) # Red Strobe
    draw.rectangle([(amb_x2 - 90, amb_y1 - 25), (amb_x2 - 40, amb_y1)], fill=(59, 130, 246), outline=(255, 255, 255), width=2) # Blue Strobe
    draw.rectangle([(amb_x1 + 95, amb_y1 - 20), (amb_x2 - 95, amb_y1 - 5)], fill=(250, 204, 21)) # Yellow Beacon

    # Number Plate & Text
    draw.rectangle([(amb_x1 + 60, amb_y2 - 40), (amb_x2 - 60, amb_y2 - 15)], fill=(250, 204, 21), outline=(0, 0, 0), width=2)
    draw.text((amb_x1 + 75, amb_y2 - 34), "GJ-01-EA-108", fill=(0, 0, 0))
    draw.text((amb_x1 + 35, amb_y2 + 8), "🚨 108 EMERGENCY AMBULANCE (ALS)", fill=(239, 68, 68))

    # CCTV HUD Overlays
    draw.text((25, 20), "🔴 CCTV JUNCTION CAM-04 (HIGHWAY INLET)", fill=(248, 113, 113))
    draw.text((25, 40), "AI VEHICLE DETECTION FEED • REAL-TIME 4K", fill=(56, 189, 248))

    img.save(output_path, quality=95)
    print(f"Sample image successfully generated: {os.path.abspath(output_path)}")

if __name__ == "__main__":
    create_ambulance_traffic_scene()

