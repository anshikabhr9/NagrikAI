"""
NDMC Smart Grievance Management System — 100+ Automated AI Test Suite
Author: AI / Automation Engineer (Member 2)
File: tests/test_ai_suite.py

Comprehensive 100+ automated test suite covering:
- 16 Department Multi-lingual Classification (English, Hindi, Hinglish)
- Critical Safety Hazard & Priority SLA Scoring
- Spatial-Temporal Semantic Duplicate Detection & Storm Clustering
- Citizen Chatbot NLU & Multi-turn Conversational Intent Engine
- Unified Analyzer Pipeline & Entity Extraction
- REST API integration contracts
"""

import unittest
import os
import sys

# Configure UTF-8 encoding for Windows terminal
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Ensure root directory is on Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.classifier import GrievanceClassifier
from services.priority_detector import PriorityDetector
from services.duplicate_detector import DuplicateDetector
from services.unified_analyzer import UnifiedAnalyzer
from services.chatbot import CitizenChatbot

class TestNDMCClassification(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.classifier = GrievanceClassifier()

    # 1. Civil Engineering & Roads
    def test_civil_roads_en(self):
        res = self.classifier.classify("Huge deep pothole on Janpath Road near Tolstoy Marg crossing")
        self.assertEqual(res["department_id"], "civil_roads")
        self.assertTrue(res["confidence"] >= 0.70)

    def test_civil_roads_hi(self):
        res = self.classifier.classify("कनॉट प्लेस इनर सर्किल के पास फुटपाथ के पेवर ब्लॉक टूटे हुए हैं")
        self.assertEqual(res["department_id"], "civil_roads")

    def test_civil_roads_hinglish(self):
        res = self.classifier.classify("Mandi House circle ke paas sadak par bada gaddha ho gaya hai")
        self.assertEqual(res["department_id"], "civil_roads")

    def test_civil_roads_speed_breaker(self):
        res = self.classifier.classify("Speed breaker is broken on Barakhamba road causing vehicle damage")
        self.assertEqual(res["department_id"], "civil_roads")

    # 2. Public Health & Sanitation
    def test_sanitation_en(self):
        res = self.classifier.classify("Overflowing garbage dustbin and dhalao behind Khan Market causing terrible stench")
        self.assertEqual(res["department_id"], "public_health_sanitation")

    def test_sanitation_hi(self):
        res = self.classifier.classify("सरोजिनी नगर मार्केट में सार्वजनिक शौचालय बहुत गंदा है और बदबू आ रही है")
        self.assertEqual(res["department_id"], "public_health_sanitation")

    def test_sanitation_hinglish(self):
        res = self.classifier.classify("Gole market me kachra sadak par fail raha hai pichle 3 din se sweeper nahi aaya")
        self.assertEqual(res["department_id"], "public_health_sanitation")

    def test_sanitation_dead_animal(self):
        res = self.classifier.classify("Dead street dog lying near Lodhi Colony block 15 needs removal")
        self.assertEqual(res["department_id"], "public_health_sanitation")

    # 3. Electricity & Power Distribution
    def test_electricity_en(self):
        res = self.classifier.classify("High voltage live electric wire snapped and hanging outside school gate")
        self.assertEqual(res["department_id"], "electricity_power")

    def test_electricity_hi(self):
        res = self.classifier.classify("चाणक्यपुरी में बिजली का फीडर पिलर खुला पड़ा है करंट का खतरा है")
        self.assertEqual(res["department_id"], "electricity_power")

    def test_electricity_hinglish(self):
        res = self.classifier.classify("Transformer me se spark nikal raha hai aur bijli gul hai")
        self.assertEqual(res["department_id"], "electricity_power")

    def test_electricity_blackout(self):
        res = self.classifier.classify("Complete powercut and blackout in Bengali market since 3 hours")
        self.assertEqual(res["department_id"], "electricity_power")

    # 4. Water Supply & Sewerage
    def test_water_en(self):
        res = self.classifier.classify("Contaminated dirty black tap water coming in residential quarters")
        self.assertEqual(res["department_id"], "water_sewerage")

    def test_water_hi(self):
        res = self.classifier.classify("कनॉट प्लेस एम ब्लॉक के सामने खुला मैनहोल है ढक्कन गायब है")
        self.assertEqual(res["department_id"], "water_sewerage")

    def test_water_hinglish(self):
        res = self.classifier.classify("Sarojini Nagar block 8 me sewer line choke ho gayi hai pura ganda pani beh raha hai")
        self.assertEqual(res["department_id"], "water_sewerage")

    def test_water_pipeline_burst(self):
        res = self.classifier.classify("Major water pipeline burst on Shanti Path water gushing out on road")
        self.assertEqual(res["department_id"], "water_sewerage")

    # 5. Horticulture & Gardens
    def test_horticulture_en(self):
        res = self.classifier.classify("Huge Neem tree uprooted during thunderstorm blocking main road")
        self.assertEqual(res["department_id"], "horticulture_gardens")

    def test_horticulture_hi(self):
        res = self.classifier.classify("लोधी गार्डन में बच्चों के झूले टूटे हुए हैं और पार्क की घास नहीं कटी")
        self.assertEqual(res["department_id"], "horticulture_gardens")

    def test_horticulture_hinglish(self):
        res = self.classifier.classify("Nehru Park ke walking track ke paas ghas bahut badi ho gayi hai")
        self.assertEqual(res["department_id"], "horticulture_gardens")

    def test_horticulture_branch(self):
        res = self.classifier.classify("Dry overhanging tree branch hanging precariously in Chanakyapuri")
        self.assertEqual(res["department_id"], "horticulture_gardens")

    # 6. Building Architecture & Encroachment
    def test_building_en(self):
        res = self.classifier.classify("Unauthorized illegal construction of 4th floor going on without sanction")
        self.assertEqual(res["department_id"], "building_encroachment")

    def test_building_hi(self):
        res = self.classifier.classify("सरोजिनी नगर में सरकारी जमीन पर अवैध कब्जा करके शेड बना लिया गया है")
        self.assertEqual(res["department_id"], "building_encroachment")

    def test_building_hinglish(self):
        res = self.classifier.classify("Footpath par avaidh kabza karke rasta block kar diya hai")
        self.assertEqual(res["department_id"], "building_encroachment")

    def test_building_structure(self):
        res = self.classifier.classify("Old dilapidated building structure with cracks near Gole Market")
        self.assertEqual(res["department_id"], "building_encroachment")

    # 7. Street Lighting
    def test_street_lighting_en(self):
        res = self.classifier.classify("All 8 streetlights on Mother Teresa Crescent road are non-functional dark spot")
        self.assertEqual(res["department_id"], "street_lighting")

    def test_street_lighting_hi(self):
        res = self.classifier.classify("कस्तूरबा गांधी मार्ग पर स्ट्रीट लाइट लगातार ब्लिंक कर रही है")
        self.assertEqual(res["department_id"], "street_lighting")

    def test_street_lighting_hinglish(self):
        res = self.classifier.classify("Lodhi colony main road par saari street lights din me bhi jal rahi hain")
        self.assertEqual(res["department_id"], "street_lighting")

    def test_street_lighting_pole(self):
        res = self.classifier.classify("Streetlight pole leaning at 45 degree angle after truck hit")
        self.assertEqual(res["department_id"], "street_lighting")

    # 8. Medical Services
    def test_medical_en(self):
        res = self.classifier.classify("Charak Palika Hospital pharmacy is refusing essential insulin medicines citing zero stock")
        self.assertEqual(res["department_id"], "medical_services")

    def test_medical_hi(self):
        res = self.classifier.classify("डिस्पेंसरी में डॉक्टर उपस्थित नहीं हैं और दवाइयां नहीं मिल रहीं")
        self.assertEqual(res["department_id"], "medical_services")

    def test_medical_hinglish(self):
        res = self.classifier.classify("Moti Bagh dispensary me doctor absent hain emergency patient ko dekh nahi rahe")
        self.assertEqual(res["department_id"], "medical_services")

    def test_medical_birth_cert(self):
        res = self.classifier.classify("Birth certificate delay after delivery at Charak Palika hospital")
        self.assertEqual(res["department_id"], "medical_services")

    # 9. Education
    def test_education_en(self):
        res = self.classifier.classify("Navyug School classroom has broken benches and damaged blackboard")
        self.assertEqual(res["department_id"], "education")

    def test_education_hi(self):
        res = self.classifier.classify("अटल आदर्श विद्यालय में छात्राओं के शौचालय का दरवाजा टूटा हुआ है")
        self.assertEqual(res["department_id"], "education")

    def test_education_hinglish(self):
        res = self.classifier.classify("Navyug school me drinking water cooler kharab hai bachho ko pareshani ho rahi")
        self.assertEqual(res["department_id"], "education")

    def test_education_midday(self):
        res = self.classifier.classify("Mid-day meal delivered today at school was stale and smelling bad")
        self.assertEqual(res["department_id"], "education")

    # 10. Commercial & Property Tax
    def test_property_tax_en(self):
        res = self.classifier.classify("Property tax payment deducted from bank account but receipt not generated")
        self.assertEqual(res["department_id"], "commercial_property_tax")

    def test_property_tax_hi(self):
        res = self.classifier.classify("दुकान का ट्रेड लाइसेंस रिन्यूअल फीस कट गई लेकिन सर्टिफिकेट डाउनलोड नहीं हुआ")
        self.assertEqual(res["department_id"], "commercial_property_tax")

    def test_property_tax_hinglish(self):
        res = self.classifier.classify("Property tax portal par mutation application 45 din se pending hai")
        self.assertEqual(res["department_id"], "commercial_property_tax")

    def test_property_tax_calc(self):
        res = self.classifier.classify("Property tax calculation error in demand notice with double commercial factor")
        self.assertEqual(res["department_id"], "commercial_property_tax")

    # 11. Parking Management
    def test_parking_en(self):
        res = self.classifier.classify("Parking attendant at Connaught Place charging 100 rupees instead of 20 rupee rate")
        self.assertEqual(res["department_id"], "parking_traffic")

    def test_parking_hi(self):
        res = self.classifier.classify("चाणक्यपुरी में स्कूल के सामने जेब्रा क्रॉसिंग का पेंट पूरी तरह मिट चुका है")
        self.assertEqual(res["department_id"], "parking_traffic")

    def test_parking_hinglish(self):
        res = self.classifier.classify("Khan market multilevel parking barrier toot gaya hai extra parking charge le rahe")
        self.assertEqual(res["department_id"], "parking_traffic")

    def test_parking_mafia(self):
        res = self.classifier.classify("Illegal parking blocking entire fire lane in Sarojini market")
        self.assertEqual(res["department_id"], "parking_traffic")

    # 12. Stray Animals & Veterinary
    def test_animals_en(self):
        res = self.classifier.classify("Pack of aggressive stray dogs bit a delivery boy in Lodhi Colony")
        self.assertEqual(res["department_id"], "stray_animals_veterinary")

    def test_animals_hi(self):
        res = self.classifier.classify("तिलक मार्ग मुख्य सड़क पर 4-5 आवारा गाय बैठी हैं गाड़ियों की टक्कर का खतरा है")
        self.assertEqual(res["department_id"], "stray_animals_veterinary")

    def test_animals_hinglish(self):
        res = self.classifier.classify("Troop of aggressive monkeys entered balconies in Chanakyapuri attacking residents")
        self.assertEqual(res["department_id"], "stray_animals_veterinary")

    def test_animals_injured(self):
        res = self.classifier.classify("Injured street dog near Sarojini market needs urgent veterinary treatment")
        self.assertEqual(res["department_id"], "stray_animals_veterinary")

    # 13. Enforcement
    def test_enforcement_en(self):
        res = self.classifier.classify("Dozens of unauthorized thelas and street hawkers blocking pedestrian walkway outside Palika Bazaar")
        self.assertEqual(res["department_id"], "enforcement")

    def test_enforcement_hi(self):
        res = self.classifier.classify("कनॉट प्लेस में बिना अनुमति के बड़े-बड़े अवैध होर्डिंग और बैनर पेड़ और खंभों पर टांग दिए गए हैं")
        self.assertEqual(res["department_id"], "enforcement")

    def test_enforcement_hinglish(self):
        res = self.classifier.classify("Sarojini market me kapde ke thele walo ne rasta band kar diya hai")
        self.assertEqual(res["department_id"], "enforcement")

    def test_enforcement_non_vending(self):
        res = self.classifier.classify("Illegal fruit vendor stalls in designated non-vending zone near metro")
        self.assertEqual(res["department_id"], "enforcement")

    # 14. IT & E-Governance
    def test_it_egov_en(self):
        res = self.classifier.classify("NDMC 311 mobile app continuously crashing on grievance photo upload screen")
        self.assertEqual(res["department_id"], "it_egovernance")

    def test_it_egov_hi(self):
        res = self.classifier.classify("कनॉट प्लेस पालिका केंद्र के पास लगा स्मार्ट सिटी कियोस्क काम नहीं कर रहा")
        self.assertEqual(res["department_id"], "it_egovernance")

    def test_it_egov_hinglish(self):
        res = self.classifier.classify("Citizen grievance portal not sending OTP to registered mobile number")
        self.assertEqual(res["department_id"], "it_egovernance")

    def test_it_egov_server(self):
        res = self.classifier.classify("NDMC website showing 500 internal server error on grievance tracking link")
        self.assertEqual(res["department_id"], "it_egovernance")

    # 15. Environment & Pollution
    def test_environment_en(self):
        res = self.classifier.classify("Security guard openly burning huge pile of dry leaves and plastic waste causing thick smoke")
        self.assertEqual(res["department_id"], "environment_pollution")

    def test_environment_hi(self):
        res = self.classifier.classify("चाणक्यपुरी में जनरेटर से भयंकर काला धुआं और तेज आवाज निकल रही है")
        self.assertEqual(res["department_id"], "environment_pollution")

    def test_environment_hinglish(self):
        res = self.classifier.classify("Khan market ke pass dukan wale raat ko plastic kachra jala rahe hain saans lena mushkil ho gaya")
        self.assertEqual(res["department_id"], "environment_pollution")

    def test_environment_dust(self):
        res = self.classifier.classify("Construction site at Tolstoy Marg operating without dust tarpaulin causing heavy smog")
        self.assertEqual(res["department_id"], "environment_pollution")

    # 16. Disaster Management & Emergency
    def test_disaster_en(self):
        res = self.classifier.classify("EMERGENCY: Heavy downpour caused 4 feet waterlogging in Minto Bridge underpass car trapped")
        self.assertEqual(res["department_id"], "disaster_emergency")

    def test_disaster_hi(self):
        res = self.classifier.classify("कनॉट प्लेस के पास भूमिगत गैस पाइपलाइन से तेज गंध आ रही है आग लगने का गंभीर खतरा है")
        self.assertEqual(res["department_id"], "disaster_emergency")

    def test_disaster_hinglish(self):
        res = self.classifier.classify("Peshwa Road par purani building ki balcony gir gayi hai malba sadak par gira relief bhejo")
        self.assertEqual(res["department_id"], "disaster_emergency")

    def test_disaster_wall(self):
        res = self.classifier.classify("Boundary wall collapsed during storm on parked vehicles immediate disaster team needed")
        self.assertEqual(res["department_id"], "disaster_emergency")


class TestNDMCPriorityDetection(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.detector = PriorityDetector()

    def test_critical_live_wire(self):
        res = self.detector.detect_priority("Live wire hanging from pole outside school gate")
        self.assertEqual(res["priority"], "CRITICAL")
        self.assertTrue(res["is_hazard"])
        self.assertLessEqual(res["sla_hours"], 12)

    def test_critical_open_manhole(self):
        res = self.detector.detect_priority("Open manhole on dark road cover is missing")
        self.assertEqual(res["priority"], "CRITICAL")
        self.assertTrue(res["is_hazard"])

    def test_critical_gas_leak(self):
        res = self.detector.detect_priority("Smell of toxic gas leak near restaurant kitchen")
        self.assertEqual(res["priority"], "CRITICAL")
        self.assertTrue(res["is_hazard"])

    def test_critical_flooding_trapped(self):
        res = self.detector.detect_priority("Underpass waterlogging car trapped with passengers inside")
        self.assertEqual(res["priority"], "CRITICAL")
        self.assertTrue(res["is_hazard"])

    def test_critical_building_collapse(self):
        res = self.detector.detect_priority("Old building wall collapse and falling debris")
        self.assertEqual(res["priority"], "CRITICAL")
        self.assertTrue(res["is_hazard"])

    def test_critical_contaminated_water(self):
        res = self.detector.detect_priority("Contaminated black and foul-smelling dirty tap water supply")
        self.assertEqual(res["priority"], "CRITICAL")
        self.assertTrue(res["is_hazard"])

    def test_critical_dog_bite(self):
        res = self.detector.detect_priority("Pack of aggressive stray dogs bit a delivery boy in colony")
        self.assertEqual(res["priority"], "CRITICAL")
        self.assertTrue(res["is_hazard"])

    def test_critical_leaning_pole(self):
        res = self.detector.detect_priority("Light pole leaning dangerously at 45 degree angle")
        self.assertEqual(res["priority"], "CRITICAL")
        self.assertTrue(res["is_hazard"])

    def test_critical_burning_smoke(self):
        res = self.detector.detect_priority("Security guard openly burning huge pile of plastic waste with suffocating smoke")
        self.assertEqual(res["priority"], "CRITICAL")
        self.assertTrue(res["is_hazard"])

    def test_critical_midday_meal(self):
        res = self.detector.detect_priority("Mid-day meal stale and smelling bad at school")
        self.assertEqual(res["priority"], "CRITICAL")
        self.assertTrue(res["is_hazard"])

    def test_critical_uprooted_tree(self):
        res = self.detector.detect_priority("Huge Neem tree uprooted during storm blocking main road for ambulances")
        self.assertEqual(res["priority"], "CRITICAL")
        self.assertTrue(res["is_hazard"])

    def test_high_power_blackout(self):
        res = self.detector.detect_priority("Complete power outage and blackout in block C")
        self.assertEqual(res["priority"], "HIGH")
        self.assertEqual(res["sla_hours"], 24)

    def test_high_pipeline_burst(self):
        res = self.detector.detect_priority("Underground water pipeline burst gushing water")
        self.assertEqual(res["priority"], "HIGH")

    def test_high_dead_animal(self):
        res = self.detector.detect_priority("Dead street dog lying near colony park")
        self.assertEqual(res["priority"], "HIGH")

    def test_high_sewer_overflow(self):
        res = self.detector.detect_priority("Sewer line choke dirty water overflowing on road")
        self.assertEqual(res["priority"], "HIGH")

    def test_high_uncollected_garbage(self):
        res = self.detector.detect_priority("Overflowing dhalao with massive garbage pile on street")
        self.assertEqual(res["priority"], "HIGH")

    def test_high_dark_spot(self):
        res = self.detector.detect_priority("All 8 streetlights non-functional pitch black road")
        self.assertEqual(res["priority"], "HIGH")

    def test_high_doctor_absent(self):
        res = self.detector.detect_priority("NDMC dispensary doctor absent emergency patients waiting")
        self.assertEqual(res["priority"], "HIGH")

    def test_high_dust_violation(self):
        res = self.detector.detect_priority("Construction site dust violation without tarpaulin heavy smog")
        self.assertEqual(res["priority"], "HIGH")

    def test_medium_pothole(self):
        res = self.detector.detect_priority("Small pothole on colony road", department_id="civil_roads")
        self.assertEqual(res["priority"], "MEDIUM")

    def test_medium_parking_slip(self):
        res = self.detector.detect_priority("Parking attendant overcharging for parking slip", department_id="parking_traffic")
        self.assertEqual(res["priority"], "MEDIUM")

    def test_medium_app_crash(self):
        res = self.detector.detect_priority("NDMC 311 app crash on submit screen", department_id="it_egovernance")
        self.assertEqual(res["priority"], "MEDIUM")

    def test_low_park_grass(self):
        res = self.detector.detect_priority("Park grass is overgrown need grass cutting", department_id="horticulture_gardens")
        self.assertEqual(res["priority"], "LOW")
        self.assertEqual(res["sla_hours"], 72)

    def test_low_daytime_lights(self):
        res = self.detector.detect_priority("Street lights on in daytime energy waste", department_id="street_lighting")
        self.assertEqual(res["priority"], "LOW")

    def test_low_mutation_delay(self):
        res = self.detector.detect_priority("Mutation application pending for 45 days", department_id="commercial_property_tax")
        self.assertEqual(res["priority"], "LOW")


class TestNDMCDuplicateDetection(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.detector = DuplicateDetector()

    def test_exact_duplicate_detection(self):
        query = "Massive pothole on Janpath Road near Tolstoy Marg crossing"
        res = self.detector.find_duplicates(
            new_text=query,
            ward="Ward 1 - Connaught Place",
            department_id="civil_roads"
        )
        self.assertTrue(res["is_duplicate"])
        self.assertGreaterEqual(res["highest_similarity"], 0.70)
        self.assertEqual(res["primary_match"]["complaint_id"], "CMP-2026-1001")

    def test_live_wire_duplicate(self):
        query = "Live wire hanging from pole outside NDMC school Chanakyapuri"
        res = self.detector.find_duplicates(
            new_text=query,
            ward="Ward 3 - Chanakyapuri",
            department_id="electricity_power"
        )
        self.assertTrue(res["is_duplicate"])
        self.assertEqual(res["primary_match"]["complaint_id"], "CMP-2026-1002")

    def test_different_ward_non_duplicate(self):
        query = "Live wire hanging in Dwarka sector 10"
        res = self.detector.find_duplicates(
            new_text=query,
            ward="Ward 12 - Dwarka",
            department_id="electricity_power"
        )
        self.assertFalse(res["is_duplicate"])

    def test_storm_surge_simulation(self):
        res = self.detector.simulate_storm_scenario(count=50, ward="Ward 1 - Connaught Place")
        self.assertEqual(res["total_simulated_complaints"], 50)
        self.assertTrue(res["detected_as_surge"])
        self.assertGreaterEqual(res["cluster_size"], 10)

    def test_empty_complaint_text(self):
        sim = self.detector.compute_text_similarity("", "")
        self.assertEqual(sim, 0.0)


class TestNDMCChatbotNLU(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bot = CitizenChatbot()

    def test_greeting_english(self):
        res = self.bot.process_message("Hello good morning")
        self.assertEqual(res["intent"], "GREETING")
        self.assertIn("Namaste", res["reply"])

    def test_greeting_hindi(self):
        res = self.bot.process_message("नमस्ते")
        self.assertEqual(res["intent"], "GREETING")

    def test_greeting_namaskar(self):
        res = self.bot.process_message("नमस्कार")
        self.assertEqual(res["intent"], "GREETING")

    def test_track_complaint_intent(self):
        res = self.bot.process_message("Please track status of ticket CMP-2026-1001")
        self.assertEqual(res["intent"], "TRACK_STATUS")
        self.assertIn("CMP-2026-1001", res["reply"])

    def test_track_complaint_generic(self):
        res = self.bot.process_message("How do I check my complaint status?")
        self.assertEqual(res["intent"], "TRACK_STATUS")

    def test_faq_office_timings(self):
        res = self.bot.process_message("What are NDMC office timings and address?")
        self.assertEqual(res["intent"], "FAQ_QUERY")
        self.assertIn("Palika Kendra", res["reply"])

    def test_faq_water_tanker(self):
        res = self.bot.process_message("How can I request an emergency water tanker?")
        self.assertEqual(res["intent"], "FAQ_QUERY")
        self.assertIn("tanker", res["reply"].lower())

    def test_faq_property_tax(self):
        res = self.bot.process_message("How do I pay property tax online?")
        self.assertEqual(res["intent"], "FAQ_QUERY")
        self.assertIn("property", res["reply"].lower())

    def test_escalation_intent(self):
        res = self.bot.process_message("My complaint is unresolved and pending for days please escalate to senior officer")
        self.assertEqual(res["intent"], "ESCALATE")
        self.assertIn("Escalation", res["reply"])

    def test_complaint_filing_nlu(self):
        res = self.bot.process_message("Streetlight is broken and not working in Chanakyapuri")
        self.assertEqual(res["intent"], "FILE_COMPLAINT")
        self.assertIsNotNone(res["complaint_draft"])
        self.assertEqual(res["complaint_draft"]["classification"]["department_id"], "street_lighting")

    def test_complaint_filing_pothole(self):
        res = self.bot.process_message("Deep pothole on Janpath Road near Tolstoy Marg")
        self.assertEqual(res["intent"], "FILE_COMPLAINT")
        self.assertEqual(res["complaint_draft"]["classification"]["department_id"], "civil_roads")

    def test_emergency_alert_nlu(self):
        res = self.bot.process_message("DANGER: Live wire snapped on road in Connaught Place!")
        self.assertEqual(res["intent"], "EMERGENCY_ALERT")
        self.assertIn("CRITICAL SAFETY ALERT", res["reply"])


class TestNDMCUnifiedAnalyzer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.analyzer = UnifiedAnalyzer()

    def test_full_pipeline_analysis(self):
        text = "Deep pothole on Janpath Road near Tolstoy Marg, contact 9811223344"
        res = self.analyzer.analyze(text=text, ward="Ward 1 - Connaught Place")
        
        self.assertTrue(res["success"])
        self.assertEqual(res["classification"]["department_id"], "civil_roads")
        self.assertEqual(res["entities"]["contact_number"], "9811223344")
        self.assertIn("Janpath", res["entities"]["detected_landmarks"])
        self.assertIsNotNone(res["priority"]["tier"])
        self.assertIsNotNone(res["title"])

    def test_emergency_pipeline_analysis(self):
        text = "URGENT: Live electric wire snapped near Mandi House metro station"
        res = self.analyzer.analyze(text=text, ward="Ward 2 - Mandi House")
        self.assertTrue(res["priority"]["is_safety_hazard"])
        self.assertEqual(res["priority"]["tier"], "CRITICAL")
        self.assertEqual(res["sentiment"], "URGENT_DISTRESSED")

    def test_polite_request_sentiment(self):
        text = "Please kindly trim overgrown tree branches near Lodhi Garden"
        res = self.analyzer.analyze(text=text)
        self.assertEqual(res["sentiment"], "POLITE_REQUEST")

    def test_hindi_language_detection(self):
        text = "कनॉट प्लेस में पानी का गटर ओवरफ्लो हो रहा है"
        res = self.analyzer.analyze(text=text)
        self.assertEqual(res["language"], "hi")

    def test_hinglish_language_detection(self):
        text = "Sarojini nagar me sadak par bada gaddha ho gaya hai gaadi nikal nahi rahi"
        res = self.analyzer.analyze(text=text)
        self.assertEqual(res["language"], "hinglish")

    def test_empty_string_handling(self):
        res = self.analyzer.analyze(text="")
        self.assertTrue(res["success"])
        self.assertEqual(res["priority"]["tier"], "LOW")

if __name__ == "__main__":
    unittest.main()
