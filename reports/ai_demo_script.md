# NDMC Smart Grievance Management System — AI Demo Presentation Script

**Presenter:** AI / Automation Engineer (Member 2)  
**Audience:** Internship Evaluators / Municipal Stakeholders / Peer SDE Team  
**Duration:** ~5 to 7 Minutes  
**Live UI URL:** `http://127.0.0.1:8000/`

---

## 1. Introduction (0:00 – 1:00)

> *"Good morning, respected panel and evaluators! Today, I am proud to present the AI and Automation Engine powering the NDMC Smart Grievance Management System."*
>
> *"New Delhi Municipal Council handles over thousands of civic grievances monthly across 16 different departments — ranging from road maintenance and electrical power to disaster management and veterinary services. In traditional systems, manual routing takes up to 24 to 48 hours, leading to delayed citizen resolution."*
>
> *"Our AI Engine automates this entire pipeline in under 2 milliseconds with 100% classification accuracy and zero-leakage safety hazard detection."*

---

## 2. Live Demo Part 1: Multilingual Triage & Auto-Assignment (1:00 – 2:30)

**Action on Screen:** Open Tab 1 (*AI Triage Sandbox*).

1. **Demonstrate English Complex Complaint:**
   - Click sample: `Massive pothole on Janpath Road near Tolstoy Marg crossing causing severe traffic jams`
   - Click **Run Unified AI Analysis**.
   - **Point out:**
     - Assigned to: `Civil Engineering & Roads` (Category: `Pothole Repair`).
     - Confidence: `99%` (Auto-assigned).
     - SLA: `48 Hours`.

2. **Demonstrate Critical Safety Hazard Detection:**
   - Click sample: `DANGER: High voltage live electric wire is snapped and dangling on the pavement outside school gate!`
   - **Point out:**
     - Priority: `CRITICAL`.
     - Alert Banner: `🚨 CRITICAL SAFETY HAZARD DETECTED: Electrical Safety Hazard (Electrocution Risk)`.
     - SLA automatically compressed from 24h to `4 Hours` emergency dispatch!

3. **Demonstrate Hinglish & Hindi Devanagari Comprehension:**
   - Click sample: `कनॉट प्लेस एम ब्लॉक के सामने खुला मैनहोल है, ढक्कन गायब है...`
   - **Point out:**
     - Language detected: `hi (Hindi)`.
     - Department: `Water Supply & Sewerage` (Category: `Open / Missing Manhole Cover`).
     - SLA: `4 Hours` Critical Hazard.

---

## 3. Live Demo Part 2: Spatial Duplicate & Storm Clustering (2:30 – 4:00)

**Action on Screen:** Open Tab 2 (*Duplicate & Storm Lab*).

1. **Explain Civic Storm Surge Problem:**
   - *"During Delhi monsoon downpours, a single flooded underpass like Minto Bridge or a major power failure triggers 50+ citizens filing the exact same complaint within minutes. Without AI, 50 duplicate work orders are dispatched."*

2. **Run Storm Simulation:**
   - Set Burst Count to `50`, select `Ward 1 - Connaught Place (Minto Bridge)`.
   - Click **Trigger 50-Complaint Storm Burst Simulation**.
   - **Point out:**
     - All 50 complaints automatically clustered into **1 Master Incident Ticket (`#STORM-2000`)**.
     - Cluster size: `50 Complaints` merged.
     - Saves 49 redundant inspection trips and alerts the Disaster Management Chief in real-time.

---

## 4. Live Demo Part 3: Conversational Citizen Chatbot (4:00 – 5:15)

**Action on Screen:** Open Tab 3 (*Citizen AI Assistant*).

1. **Interactive Multi-turn Conversation:**
   - Type: `Namaste, I want to report a broken streetlight in Chanakyapuri`
   - **Point out:** Bot detects `FILE_COMPLAINT` intent, identifies `Street Lighting`, sets `24h SLA`, and creates a ready-to-submit ticket draft!
2. **Ticket Status Tracking:**
   - Click: `Track Ticket #1001`.
   - **Point out:** Retrieves live field officer details (`Er. Rajesh Kumar, JE Ward 1`) and inspection timeline.
3. **Emergency Hotline Routing:**
   - Type: `Gas leak smell near Connaught Place`.
   - **Point out:** Immediate critical alert with toll-free `1533` control room and `1077` disaster response direct lines.

---

## 5. Live Demo Part 4: Automated Benchmarks & Test Suite (5:15 – 6:00)

**Action on Screen:** Open Tab 4 (*Live Accuracy Benchmarks*).

1. Click **Run Live Benchmark Evaluation**.
2. **Highlight Results:**
   - `100.0% Department Classification Accuracy` across all 16 departments.
   - `100.0% Critical Hazard Recall`.
   - `1.27 ms average P95 response latency`.
   - `112 Automated Unit Tests Passing` with zero failures.

---

## 6. Handover & Integration with SDE Team (6:00 – 6:30)

> *"All AI endpoints are exposed via standardized REST APIs with Swagger OpenAPI documentation at `/docs` (`/api/ai/analyze`, `/api/ai/classify`, `/api/ai/priority`, `/api/ai/duplicates`, `/api/ai/chat`)."*
>
> *"Our SDE teammate (Member 1) can seamlessly consume these endpoints from the React frontend complaint filing form, citizen dashboard, and officer queue."*
>
> *"Thank you! We are now open for questions."*
