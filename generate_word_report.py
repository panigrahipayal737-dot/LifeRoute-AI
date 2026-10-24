import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

doc = Document()
for s in doc.sections:
    s.top_margin = s.bottom_margin = s.left_margin = s.right_margin = Inches(1)

# Page 1: Title
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('VEER NARMAD SOUTH GUJARAT UNIVERSITY, SURAT\n')
r.font.bold = True
r.font.size = Pt(14)
r.font.color.rgb = RGBColor(15, 23, 42)

r_col = p.add_run('VIMAL TORMAL PODDAR BCA COLLEGE\n')
r_col.font.bold = True
r_col.font.size = Pt(13)
r_col.font.color.rgb = RGBColor(5, 150, 105)

r_yr = p.add_run('TYBCA (SEMESTER-5) • 2026-27\n\n')
r_yr.font.bold = True
r_yr.font.size = Pt(11)

p_t = doc.add_paragraph()
p_t.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_t = p_t.add_run('SHRI MAHAVIR VIDYAMANDIR TRUST\nसा विद्या या विमुक्तये\n\n\n')
r_t.font.bold = True
r_t.font.size = Pt(11)
r_t.font.color.rgb = RGBColor(6, 95, 70)

p_title = doc.add_paragraph()
p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_p1 = p_title.add_run('PROJECT REPORT ON\n')
r_p1.font.bold = True
r_p1.font.size = Pt(14)

r_p2 = p_title.add_run('LIFEROUTE AI\n')
r_p2.font.bold = True
r_p2.font.size = Pt(26)
r_p2.font.color.rgb = RGBColor(5, 150, 105)

r_sub = p_title.add_run('\n\n\n\n')
r_sub.font.italic = True
r_sub.font.size = Pt(11.5)

t = doc.add_table(rows=1, cols=2)
t.alignment = WD_TABLE_ALIGNMENT.CENTER
t.rows[0].cells[0].width = Inches(3.2)
t.rows[0].cells[1].width = Inches(3.2)
t.rows[0].cells[0].text = 'GUIDED BY:\n\nMS. PINAL SOLANKI\nAssistant Professor,\nDepartment of Computer Science'
t.rows[0].cells[1].text = 'SUBMITTED BY:\n\nPAYAL PANIGRAHI\nDAMINI SURYAVANSHI\nAcademic Year: 2026-2027'
t.rows[0].cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT

doc.add_page_break()

# Page 2: Acknowledgement
h_ack = doc.add_heading('ACKNOWLEDGEMENT', level=1)
h_ack.runs[0].font.color.rgb = RGBColor(5, 150, 105)
doc.add_paragraph(
    'We take this opportunity to express our sincere gratitude to all those who supported and guided us during the conceptualization, system architecture, development, and successful completion of this project titled "".\n\n'
    'We are thankful to all the professors and staff members of Vimal Tormal Poddar BCA College for their cooperation, guidance, and encouragement throughout our course of study.\n\n'
    'We express our special thanks to Dr. Chetan Rathod, I/C Principal of Vimal Tormal Poddar BCA College, for granting us the opportunity and resources to undertake this project.\n\n'
    'Finally, we convey our sincere appreciation to our project guide, Ms. Pinal Solanki, for her valuable guidance, constructive suggestions, and continuous support.'
)
p_s = doc.add_paragraph('\n\nPayal Panigrahi\nDamini Suryavanshi\nTYBCA (Semester-5)')
p_s.alignment = WD_ALIGN_PARAGRAPH.RIGHT

doc.add_page_break()

# Page 3: Index
h_idx = doc.add_heading('INDEX', level=1)
h_idx.runs[0].font.color.rgb = RGBColor(5, 150, 105)
idx_data = [
    ('Ch.1', 'Introduction & Project Profile', '01'),
    ('', '1.1 Project Description', '01'),
    ('', '1.2 Literature Review / Existing System', '01'),
    ('', '1.3 Objectives & Proposed System', '02'),
    ('Ch.2', 'Environment Description & Tech Stack', '04'),
    ('', '2.1 Hardware and Software Requirements', '04'),
    ('', '2.2 Technology Used (Python, Streamlit, OpenCV, SQLite, PyTorch)', '05'),
    ('Ch.3', 'System Analysis', '07'),
    ('', '3.1 Existing System and Its Drawbacks', '07'),
    ('', '3.2 Mathematical Pinhole Optical Distance Formula', '09'),
    ('Ch.4', 'Proposed System & Modules', '10'),
    ('', '4.1 Scope (9 Medical Specialties & V2X Corridor)', '10'),
    ('', '4.2 Project Modules (Mission Control, Hospital Desk, Police CAD, GIS Map)', '13'),
    ('Ch.5', 'System Design & Planning', '17'),
    ('', '5.1 Use Case & Data Flow Diagram (DFD Level-0 & Level-1)', '17'),
    ('', '5.2 Data Dictionary (emergency_dispatches & challans Tables)', '18'),
    ('Ch.6', 'Screen Layout & Interface Design', '21'),
    ('', '6.1 Mission Control & AI Optical Radar Screen Layout', '21'),
    ('', '6.2 4-Way Traffic Preemption & Turning Simulation Layout', '24'),
    ('', '6.3 Hospital Emergency Intake & Clinical Handover Layout', '27'),
    ('', '6.4 Police CAD & AI Challan Engine Layout', '30'),
    ('', '6.5 Road-Snapped 3D GIS Multi-Junction Map Layout', '32'),
    ('Ch.7', 'References & Bibliography', '34'),
]
t_idx = doc.add_table(rows=1, cols=3)
t_idx.alignment = WD_TABLE_ALIGNMENT.CENTER
t_idx.rows[0].cells[0].text = 'Chapter'
t_idx.rows[0].cells[1].text = 'Particulars'
t_idx.rows[0].cells[2].text = 'Page No.'
for ch, part, pg in idx_data:
    row = t_idx.add_row()
    row.cells[0].text = ch
    row.cells[1].text = part
    row.cells[2].text = pg
    row.cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT

doc.add_page_break()

# Chapter 1
h1 = doc.add_heading('1. Introduction', level=1)
h1.runs[0].font.color.rgb = RGBColor(5, 150, 105)
doc.add_heading('1.1 Project Description: -', level=2)
doc.add_paragraph(
    '➤ In today\'s fast-moving urban life, emergency medical vehicles (108 Ambulances) face severe delays due to heavy traffic congestion at crossroads.\n'
    '➤ "LifeRoute AI" is an autonomous optical V2X emergency preemption and clinical staging platform designed to solve this problem.\n'
    '➤ It utilizes computer vision to recognize approaching ambulances from CCTV feeds, locks traffic signals to green, and alerts receiving hospitals in advance with live patient vitals and ICU bed availability.\n'
    '➤ The system provides an integrated Mission Control, Traffic Preemption Console, Hospital Clinical Intake Desk, Police CAD Escort, and automated Section 194E MVA Challan enforcement.'
)
doc.add_heading('1.2 Literature Review / Existing System: -', level=2)
doc.add_paragraph(
    'Limitations of Existing Systems:\n'
    '➤ Rigid Timer Cycles: Traffic lights run on fixed timers regardless of approaching ambulances.\n'
    '➤ Blind Hospital Ingestion: Emergency doctors receive zero advance telemetry regarding patient blood requirement or vitals.\n'
    '➤ High Deployment Cost: Specialized hardware transponders and roadside RFID scanners are expensive to deploy across every intersection.\n'
    '➤ Corridor Tailgating: Civilian vehicles follow ambulances through red lights without automated legal penalty enforcement.'
)

doc.add_heading('Project Profile: -', level=2)
table_prof = doc.add_table(rows=7, cols=2)
prof_data = [
    ('Project Title:', 'LifeRoute AI'),
    ('Frontend:', 'Streamlit, HTML5, CSS3, JavaScript Web Audio'),
    ('AI Vision & Deep Learning:', 'OpenCV (cv2), PyTorch ANN Multi-Class Classifier'),
    ('Backend:', 'Python 3.11, Dual-Bus JSON State Architecture'),
    ('Database:', 'SQLite 3 Database'),
    ('Mapping Engine:', 'Folium Leaflet & CartoDB Vector Tiles'),
    ('Internal Guide:', 'Ms. Pinal Solanki')
]
for i, (k, v) in enumerate(prof_data):
    table_prof.rows[i].cells[0].text = k
    table_prof.rows[i].cells[0].paragraphs[0].runs[0].font.bold = True
    table_prof.rows[i].cells[1].text = v

doc.add_heading('1.3 Objectives: -', level=2)
doc.add_paragraph(
    '• To develop an AI-powered optical radar to detect 108 ALS ambulances from live camera feeds.\n'
    '• To dynamically calculate physical distance in meters using monocular pinhole camera geometry.\n'
    '• To preempt 4-way traffic signals by switching the approaching corridor to GREEN WAVE and locking cross-traffic to ALL-RED.\n'
    '• To eliminate delays during the critical "Golden Hour" by reducing ambulance travel time from 14.5 minutes to 4.1 minutes.\n'
    '• To provide real-time hospital bed allocation across 9 clinical specialties with live ICU capacity verification.'
)

doc.add_page_break()

# Chapter 2
h2 = doc.add_heading('2. Environment Description', level=1)
h2.runs[0].font.color.rgb = RGBColor(5, 150, 105)
doc.add_heading('2.1 Hardware and Software Requirements: -', level=2)
doc.add_paragraph(
    'Hardware Requirements:\n'
    '✓ Processor: Intel Core i3 / i5 or above (2.0 GHz+)\n'
    '✓ RAM: 4 GB DDR4 or above\n'
    '✓ Hard Disk: 250 GB SSD or above\n'
    '✓ Optical Camera: 720p HD Webcam / 1080p FHD CCTV Gantry Camera / Mobile IP Camera\n'
    '✓ Monitor: 15" Colour Display\n\n'
    'Software Requirements:\n'
    '1. Frontend: Streamlit Framework, HTML5, CSS3, JavaScript Web Audio API\n'
    '2. Backend & AI: Python 3.10 / 3.11, OpenCV 4.10+, PyTorch\n'
    '3. Database: SQLite 3 Database, active_emergency_bus.json\n'
    '4. Operating System: Windows 10 / 11 / Linux Ubuntu'
)

doc.add_page_break()

# Chapter 3 & 4
h3 = doc.add_heading('3. System Analysis & Mathematical Model', level=1)
h3.runs[0].font.color.rgb = RGBColor(5, 150, 105)
doc.add_paragraph(
    'LifeRoute AI calculates physical distance using monocular bounding box ratio:\n\n'
    '    Distance (Meters) = α / Max(ε, [ Bounding Box Width (px) / Total Frame Width (px) ])\n\n'
    'Where focal calibration constant α = 28.0 and stabilization clamp ε = 0.05 ensure precise range estimation from 12m to 850m.'
)

h4 = doc.add_heading('4. Proposed System & Modules', level=1)
h4.runs[0].font.color.rgb = RGBColor(5, 150, 105)
doc.add_paragraph(
    '1. Mission Control & AI Optical Radar Module\n'
    '2. Patient Dossier & ECG Telemetry Module (Pulse, SpO2, Lead-II ECG)\n'
    '3. 4-Way Traffic Preemption & Crossroads Turn Simulation\n'
    '4. Hospital Intake Desk & Downloadable Clinical Handover Slip\n'
    '5. Police CAD Escort & Section 194E MVA Automated ₹10,000 Challan Engine\n'
    '6. Road-Snapped 3D GIS Surat Multi-Junction Preemption Map'
)

doc.add_page_break()

# Chapter 5 & 7
h5 = doc.add_heading('5. System Design & Data Dictionary', level=1)
h5.runs[0].font.color.rgb = RGBColor(5, 150, 105)
doc.add_paragraph(
    'Master Dispatches Schema (emergency_dispatches Table):\n'
    '• incident_id (TEXT, Primary Key)\n'
    '• patient_name (TEXT) & patient_age (INTEGER)\n'
    '• patient_blood (TEXT) - Matched Blood Group\n'
    '• emergency_type (TEXT) - Clinical Diagnosis\n'
    '• target_hospital (TEXT) & assigned_doctor (TEXT)\n'
    '• corridor_lane (TEXT) - Preempted Lane (NORTH/WEST)\n'
    '• radar_distance_m (REAL) & eta_minutes (REAL)\n'
    '• patient_pulse (INT), patient_spo2 (INT), patient_bp (TEXT)\n'
    '• status (TEXT - ACTIVE / RESOLVED)'
)

h7 = doc.add_heading('7. References & Bibliography', level=1)
h7.runs[0].font.color.rgb = RGBColor(5, 150, 105)
doc.add_paragraph(
    '1. OpenCV Official Documentation. Available at: https://docs.opencv.org/\n'
    '2. Streamlit Framework Documentation. Available at: https://docs.streamlit.io/\n'
    '3. Motor Vehicles (Amendment) Act, Section 194E - Penalty for Failure to Yield Right-of-Way to Emergency Vehicles, MoRTH, Government of India.\n'
    '4. Surat Municipal Corporation (SMC) Smart City ICCC Traffic Signal Architecture.\n'
    '5. PyTorch Deep Learning Platform. Available at: https://pytorch.org/\n'
    '6. Folium Leaflet Geospatial Visualization in Python.\n\n\n'
    'End of Project Report • LifeRoute AI • Vimal Tormal Poddar BCA College (2026-27)'
)

doc.save('LIFEROUTE_AI_FINAL_REPORT.docx')
print('SUCCESS: Report file saved as LIFEROUTE_AI_FINAL_REPORT.docx!')

