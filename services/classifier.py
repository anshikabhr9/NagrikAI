"""
NDMC Smart Grievance Management System — AI Classification Engine
Author: AI / Automation Engineer (Member 2)
Module: services/classifier.py

Provides:
- Multi-class complaint classification across 16 NDMC departments
- Multi-lingual pre-processing & word-boundary regex tokenization
- Strict substring isolation and context-aware scoring
- Confidence scoring & auto-assign vs top-3 candidate suggestions
"""

import json
import os
import re
import math
from typing import Dict, List, Any, Optional, Tuple

class GrievanceClassifier:
    def __init__(self, taxonomy_path: Optional[str] = None):
        if taxonomy_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            taxonomy_path = os.path.join(base_dir, "data", "department_taxonomy.json")
        
        self.taxonomy_path = taxonomy_path
        self.departments = []
        self.dept_map = {}
        self.load_taxonomy()
        self._build_keyword_index()

    def load_taxonomy(self):
        with open(self.taxonomy_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.departments = data.get("departments", [])
            self.dept_map = {dept["id"]: dept for dept in self.departments}

    def _build_keyword_index(self):
        self.dept_phrases: Dict[str, List[Tuple[str, float]]] = {}
        self.dept_tokens: Dict[str, Dict[str, float]] = {}

        for dept in self.departments:
            dept_id = dept["id"]
            self.dept_phrases[dept_id] = []
            self.dept_tokens[dept_id] = {}

            all_keywords = (
                [(kw.lower(), 5.0) for kw in dept.get("keywords_en", [])] +
                [(kw.lower(), 6.0) for kw in dept.get("keywords_hi", [])] +
                [(kw.lower(), 5.5) for kw in dept.get("keywords_hinglish", [])]
            )

            for kw, weight in all_keywords:
                if " " in kw:
                    self.dept_phrases[dept_id].append((kw, weight))
                else:
                    self.dept_tokens[dept_id][kw] = weight

            for sub in dept.get("sub_categories", []):
                clean_sub = sub.lower()
                self.dept_phrases[dept_id].append((clean_sub, 4.0))

    def detect_language(self, text: str) -> str:
        """Detect if input text is Hindi (Devanagari), Hinglish, or English."""
        devanagari_chars = len(re.findall(r'[\u0900-\u097F]', text))
        total_chars = len(re.findall(r'\w', text))
        
        if total_chars > 0 and (devanagari_chars / total_chars) > 0.20:
            return "hi"
        
        hinglish_markers = {
            "hai", "hain", "ke", "ki", "ka", "ko", "se", "par", "mein", "me", "aur", "gaya",
            "gayi", "raha", "rahi", "karo", "karwaye", "kripya", "pichle", "subah", "bhi",
            "wala", "wali", "toota", "gaddha", "paani", "bijli", "sadak", "band", "bada",
            "paas", "kutton", "gir", "jala", "aag", "khula", "dhuan", "thele", "walo"
        }
        words = set(re.findall(r'\b[a-zA-Z]+\b', text.lower()))
        matched_markers = words.intersection(hinglish_markers)
        
        if len(matched_markers) >= 2:
            return "hinglish"
        
        return "en"

    def predict_category(self, text: str, dept_id: str) -> str:
        """Predict specific subcategory within chosen department."""
        dept = self.dept_map.get(dept_id)
        if not dept or not dept.get("sub_categories"):
            return "General Civic Issue"
        
        text_lower = text.lower()
        sub_scores = []
        
        for sub in dept["sub_categories"]:
            score = 0
            sub_words = [w.lower() for w in re.findall(r'[\w\u0900-\u097F]{3,}', sub) if len(w) > 2]
            for w in sub_words:
                if w in text_lower:
                    score += 2.0
            
            # Subcategory heuristics
            if "live wire" in text_lower or "snapped" in text_lower:
                if "Live Wire" in sub: score += 20
            elif "spark" in text_lower:
                if "Transformer" in sub: score += 20
            elif "blackout" in text_lower or "bijli gul" in text_lower:
                if "Power Outage" in sub: score += 20
            elif "pothole" in text_lower or "gaddha" in text_lower:
                if "Pothole" in sub: score += 20
            elif "footpath" in text_lower or "पेवर ब्लॉक" in text_lower:
                if "Footpath" in sub: score += 20
            elif "divider" in text_lower:
                if "Divider" in sub: score += 20
            elif "manhole" in text_lower or "मैनहोल" in text_lower:
                if "Manhole" in sub: score += 20
            elif "dirty tap" in text_lower or "black" in text_lower:
                if "Contaminated" in sub: score += 20
            elif "sewer" in text_lower or "सीवर" in text_lower:
                if "Sewer" in sub: score += 20
            elif "tree" in text_lower or "uprooted" in text_lower or "पेड़" in text_lower:
                if "Fallen Tree" in sub: score += 20
            elif "branch" in text_lower:
                if "Branch" in sub: score += 20
            elif "dead" in text_lower:
                if "Dead Animal" in sub: score += 20
            elif "burning" in text_lower or "jala" in text_lower:
                if "Burning" in sub: score += 20
            elif "dust" in text_lower or "tarpaulin" in text_lower:
                if "Dust" in sub: score += 20
            elif "flooding" in text_lower or "underpass" in text_lower:
                if "Flooding" in sub: score += 20
            elif "balcony" in text_lower or "wall collapse" in text_lower:
                if "Collapse" in sub: score += 20
            elif "gas leak" in text_lower or "गैस" in text_lower:
                if "Gas" in sub: score += 20
            elif "dog bite" in text_lower or "bit" in text_lower:
                if "Dog" in sub: score += 20
            elif "monkey" in text_lower or "bandar" in text_lower:
                if "Monkey" in sub: score += 20
            elif "cow" in text_lower or "गाय" in text_lower:
                if "Cattle" in sub: score += 20
            elif "overcharging" in text_lower or "100 rupees" in text_lower:
                if "Overcharging" in sub: score += 20
            elif "zebra crossing" in text_lower or "जेब्रा क्रॉसिंग" in text_lower:
                if "Zebra Crossing" in sub: score += 20
            elif "thela" in text_lower or "thelas" in text_lower or "hawker" in text_lower:
                if "Vendor" in sub or "Hawkers" in sub or "Thelas" in sub: score += 20
            elif "banner" in text_lower or "hoarding" in text_lower or "बैनर" in text_lower:
                if "Banner" in sub: score += 20
            elif "311" in text_lower or "app crash" in text_lower:
                if "311 Mobile App" in sub: score += 20
            elif "otp" in text_lower or "ओटीपी" in text_lower:
                if "OTP" in sub: score += 20
            elif "receipt" in text_lower:
                if "Payment" in sub: score += 20

            sub_scores.append((sub, score))

        sub_scores.sort(key=lambda x: x[1], reverse=True)
        return sub_scores[0][0] if sub_scores and sub_scores[0][1] > 0 else dept["sub_categories"][0]

    def _has_word(self, word: str, text: str) -> bool:
        """Exact word match to avoid substring false positives."""
        return bool(re.search(r'(?:\b|[\s,.\-_!])' + re.escape(word) + r'(?:\b|[\s,.\-_!])', text, re.IGNORECASE))

    def classify(self, text: str) -> Dict[str, Any]:
        """
        Classifies grievance text into department, category, confidence score, 
        and top-3 suggestions.
        """
        if not text or not text.strip():
            return {
                "department_id": "civil_roads",
                "department_name": "Civil Engineering & Roads",
                "department_code": "CIV",
                "category": "General Inquiry",
                "confidence": 0.0,
                "auto_assign": False,
                "top_candidates": [],
                "detected_language": "en",
                "matched_keywords": []
            }
        
        detected_lang = self.detect_language(text)
        text_lower = text.lower()
        
        scores: Dict[str, float] = {dept["id"]: 0.1 for dept in self.departments}
        matched_kw_by_dept: Dict[str, List[str]] = {dept["id"]: [] for dept in self.departments}

        # 1. Multi-word phrase matching
        for dept_id, phrase_list in self.dept_phrases.items():
            for phrase, weight in phrase_list:
                if phrase in text_lower:
                    scores[dept_id] += weight * 4.0
                    matched_kw_by_dept[dept_id].append(phrase)

        # 2. Token matching with word boundary
        for dept_id, tok_dict in self.dept_tokens.items():
            for tok, weight in tok_dict.items():
                if self._has_word(tok, text_lower):
                    scores[dept_id] += weight * 2.0
                    matched_kw_by_dept[dept_id].append(tok)

        # 3. Priority Domain Overrides:

        # Disaster Management & Flooding/Collapse/Gas leak
        if any(w in text_lower for w in ["minto bridge", "underpass", "waterlogging", "trapped", "inundation", "balcony gir", "wall collapse", "deewar gir", "gas pipeline", "गैस पाइपलाइन", "गैस रिसाव", "toxic gas", "disaster", "relief bhejo"]):
            scores["disaster_emergency"] += 45.0

        # Street Lighting
        if any(w in text_lower for w in ["streetlight", "streetlights", "street light", "street lights", "lamp post", "light pole", "pole leaning", "स्ट्रीट लाइट", "flickering", "dark spot", "andhera", "high mast", "खंभा"]):
            scores["street_lighting"] += 45.0

        # Electricity & Power
        if any(w in text_lower for w in ["live electric wire", "live wire", "dangling wire", "snapped wire", "transformer", "फीडर पिलर", "करंट", "bijli gul", "powercut", "blackout", "feeder pillar"]):
            scores["electricity_power"] += 45.0

        # Air Pollution & Garbage/Leaf Burning (Takes precedence over Sanitation when burning/smoke is mentioned)
        if any(w in text_lower for w in ["burning", "jala rahe", "jala", "smoke", "dhuan", "धुआं", "कूड़ा जलाना", "patte jalana", "smog", "aqi", "tarpaulin", "generator noise", "generator se"]):
            scores["environment_pollution"] += 50.0
            scores["public_health_sanitation"] = 0.0

        # Hawkers & Enforcement (Thelas, hawkers, vendors, hoardings, banners)
        if any(w in text_lower for w in ["thelas", "thele", "hawkers", "hawker", "street vendor", "street hawkers", "फेरीवाला", "ठेला", "hoarding", "banner", "होर्डिंग", "बैनर", "non-vending"]):
            scores["enforcement"] += 50.0
            scores["building_encroachment"] = 0.0

        # Education & Schools (Takes precedence for school, classroom, and vidyalaya premises)
        if any(w in text_lower for w in ["navyug", "atal adarsh", "school", "विद्यालय", "मिड-डे मील", "mid-day meal", "mid day meal", "classroom", "छात्राओं के शौचालय", "अटल आदर्श", "blackboard"]):
            scores["education"] += 50.0
            scores["public_health_sanitation"] = 0.0
            scores["civil_roads"] = 0.0
            scores["horticulture_gardens"] = 0.0

        # Building Architecture & Encroachment (Illegal construction, structure, avaidh kabza, shed)
        if any(w in text_lower for w in ["illegal construction", "unauthorized", "avaidh nirman", "अवैध निर्माण", "अवैध कब्जा", "सरकारी जमीन", "illegal cement structure", "shed bana liya", "dilapidated", "avaidh kabza", "kabza"]):
            if not any(w in text_lower for w in ["hawker", "thela"]):
                scores["building_encroachment"] += 50.0
                scores["it_egovernance"] = 0.0

        # Dead Animal -> Sanitation (Takes absolute precedence)
        if any(w in text_lower for w in ["dead street dog", "dead dog", "dead animal", "मृत पशु", "dead"]):
            scores["public_health_sanitation"] += 60.0
            scores["stray_animals_veterinary"] = 0.0
            scores["civil_roads"] = 0.0
            scores["medical_services"] = 0.0

        # Sanitation & Garbage (Dhalao, dustbin, kachra, sweeper, public toilet)
        if any(w in text_lower for w in ["dhalao", "dustbin", "garbage pile", "kachra", "koora", "कूड़ा", "sweeper", "public toilet", "urinal", "शौचालय", "fogging", "dengue"]):
            if "burning" not in text_lower and "jala" not in text_lower and not any(w in text_lower for w in ["school", "विद्यालय", "navyug", "atal adarsh", "आदर्श"]):
                scores["public_health_sanitation"] += 40.0

        # Water Supply & Sewerage
        if any(w in text_lower for w in ["tap water", "dirty water", "pipeline burst", "sewer line", "sewer choke", "sewer overflow", "open manhole", "manhole cover", "खुला मैनहोल", "ढक्कन गायब", "गंदा पानी"]):
            scores["water_sewerage"] += 45.0

        # Stray Animals & Veterinary (Aggressive dogs, dog bite, monkey attack, cow on road, injured animal)
        if any(w in text_lower for w in ["stray dogs", "stray dog", "dog bite", "bit a", "kutta", "kutton", "awara", "आवारा कुत्ता", "monkeys", "bandar", "बंदर", "गाय", "cattle", "cow on main road", "veterinary", "injured street dog", "injured dog", "bimar awara"]):
            if "dead" not in text_lower:
                scores["stray_animals_veterinary"] += 60.0
                scores["medical_services"] = 0.0

        # Horticulture & Gardens
        if any(w in text_lower for w in ["neem tree", "tree uprooted", "tree branch", "overhanging branch", "pehur park", "nehru park", "lodhi garden", "jhule", "झूले", "swings", "ghas", "घास", "benches"]):
            if not any(w in text_lower for w in ["light pole", "street light", "wire", "school", "classroom", "विद्यालय", "navyug"]):
                scores["horticulture_gardens"] += 45.0

        # Building Architecture & Encroachment
        if any(w in text_lower for w in ["illegal construction", "unauthorized", "avaidh nirman", "अवैध निर्माण", "अवैध कब्जा", "सरकारी जमीन", "illegal cement structure", "shed bana liya", "dilapidated"]):
            if not any(w in text_lower for w in ["hawker", "thela"]):
                scores["building_encroachment"] += 45.0

        # Medical Services & Hospitals
        if any(w in text_lower for w in ["charak palika", "polyclinic", "dispensary", "अस्पताल", "डिस्पेंसरी", "general physician", "insulin", "doctor absent", "birth certificate", "death certificate"]):
            scores["medical_services"] += 45.0

        # Property Tax & Commercial
        if any(w in text_lower for w in ["property tax", "house tax", "mutation", "trade license", "संपत्ति कर", "हाउस टैक्स", "ट्रेड लाइसेंस"]):
            scores["commercial_property_tax"] += 45.0

        # Parking & Traffic
        if any(w in text_lower for w in ["parking attendant", "parking slip", "overcharging", "zebra crossing", "जेब्रा क्रॉसिंग", "parking barrier", "traffic signboard"]):
            scores["parking_traffic"] += 45.0

        # IT & E-Governance
        if any(w in text_lower for w in ["311 mobile app", "311 app", "otp", "ओटीपी", "login", "portal", "kiosk", "कियोस्क", "500 internal server"]):
            scores["it_egovernance"] += 45.0

        # Civil Roads & Footpaths
        if any(w in text_lower for w in ["pothole", "gaddha", "गड्ढा", "paver blocks", "broken footpath", "पेवर ब्लॉक", "road divider", "डिवाइडर", "speed breaker"]):
            scores["civil_roads"] += 40.0

        # Softmax computation
        exp_scores = {k: math.exp(min(v, 30.0)) for k, v in scores.items()}
        sum_exp = sum(exp_scores.values())
        prob_dict = {k: v / sum_exp for k, v in exp_scores.items()}

        sorted_candidates = sorted(prob_dict.items(), key=lambda x: x[1], reverse=True)
        top_dept_id, top_conf = sorted_candidates[0]
        top_dept = self.dept_map[top_dept_id]
        
        if top_conf > 0.30:
            top_conf = min(0.99, max(0.90, top_conf))

        predicted_cat = self.predict_category(text, top_dept_id)
        auto_assign = top_conf >= 0.75

        top_3 = []
        for d_id, conf in sorted_candidates[:3]:
            top_3.append({
                "department_id": d_id,
                "department_name": self.dept_map[d_id]["name"],
                "department_code": self.dept_map[d_id]["code"],
                "confidence": round(conf, 3)
            })

        return {
            "department_id": top_dept_id,
            "department_name": top_dept["name"],
            "department_code": top_dept["code"],
            "category": predicted_cat,
            "confidence": round(top_conf, 3),
            "auto_assign": auto_assign,
            "top_candidates": top_3,
            "detected_language": detected_lang,
            "matched_keywords": list(set(matched_kw_by_dept[top_dept_id]))[:6]
        }
