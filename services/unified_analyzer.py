"""
NDMC Smart Grievance Management System — Unified AI Analyzer
Author: AI / Automation Engineer (Member 2)
Module: services/unified_analyzer.py

Provides:
- One-stop pipeline combining Classification, Priority, SLA, Hazard, Sentiment, and Duplicate detection
- Output contract for frontend / SDE Member 1 integration (`POST /api/ai/analyze`)
"""

import re
from typing import Dict, List, Any, Optional
from services.classifier import GrievanceClassifier
from services.priority_detector import PriorityDetector
from services.duplicate_detector import DuplicateDetector

class UnifiedAnalyzer:
    def __init__(self):
        self.classifier = GrievanceClassifier()
        self.priority_detector = PriorityDetector()
        self.duplicate_detector = DuplicateDetector()

    def _extract_entities(self, text: str) -> Dict[str, Any]:
        """Extract landmarks, ward hints, and contact numbers from raw complaint text."""
        # Phone number pattern
        phone_match = re.search(r'\b(?:\+91[\-\s]?)?[6789]\d{9}\b', text)
        
        # Landmarks & prominent NDMC localities
        known_landmarks = [
            "Connaught Place", "Janpath", "Tolstoy Marg", "Barakhamba", "Mandi House",
            "Khan Market", "Lodhi Colony", "Lodhi Road", "Sarojini Nagar", "Chanakyapuri",
            "Shanti Path", "Moti Bagh", "Gole Market", "Peshwa Road", "Babar Road",
            "Bengali Market", "Minto Bridge", "Palika Bazaar", "Palika Kendra"
        ]
        detected_landmarks = []
        for lm in known_landmarks:
            if re.search(r'\b' + re.escape(lm) + r'\b', text, re.IGNORECASE):
                detected_landmarks.append(lm)

        return {
            "contact_number": phone_match.group(0) if phone_match else None,
            "detected_landmarks": detected_landmarks,
            "has_location_details": len(detected_landmarks) > 0
        }

    def _generate_summary_title(self, text: str, category: str, dept_name: str) -> str:
        """Generates a clean, concise title/summary for the complaint ticket."""
        clean = text.strip()
        # Take first sentence or up to 70 chars
        first_sentence = re.split(r'[.!?\n]', clean)[0]
        if len(first_sentence) > 65:
            return first_sentence[:62].strip() + "..."
        return first_sentence if first_sentence else f"{category} - {dept_name}"

    def analyze(self, text: str, ward: Optional[str] = None, check_duplicates: bool = True) -> Dict[str, Any]:
        """
        Executes unified analysis over input grievance text.
        """
        # 1. Classification
        classification_res = self.classifier.classify(text)
        dept_id = classification_res["department_id"]

        # 2. Priority & Hazard Detection
        priority_res = self.priority_detector.detect_priority(text, department_id=dept_id)

        # 3. Duplicate Detection
        duplicates_res = None
        if check_duplicates:
            duplicates_res = self.duplicate_detector.find_duplicates(
                new_text=text,
                ward=ward,
                department_id=dept_id
            )

        # 4. Entity Extraction & Title
        entities = self._extract_entities(text)
        title = self._generate_summary_title(text, classification_res["category"], classification_res["department_name"])

        # 5. Citizen Sentiment Tone
        text_lower = text.lower()
        sentiment = "NEUTRAL"
        if any(w in text_lower for w in ["danger", "urgent", "emergency", "terrible", "khatra", "turant", "gussa", "unacceptable"]):
            sentiment = "URGENT_DISTRESSED"
        elif any(w in text_lower for w in ["please", "request", "kripya", "kindly"]):
            sentiment = "POLITE_REQUEST"

        return {
            "success": True,
            "title": title,
            "language": classification_res["detected_language"],
            "classification": {
                "department_id": classification_res["department_id"],
                "department_name": classification_res["department_name"],
                "department_code": classification_res["department_code"],
                "category": classification_res["category"],
                "confidence": classification_res["confidence"],
                "auto_assign": classification_res["auto_assign"],
                "top_candidates": classification_res["top_candidates"],
                "matched_keywords": classification_res["matched_keywords"]
            },
            "priority": {
                "tier": priority_res["priority"],
                "sla_hours": priority_res["sla_hours"],
                "is_safety_hazard": priority_res["is_hazard"],
                "hazard_type": priority_res["hazard_type"],
                "urgency_score": priority_res["urgency_score"],
                "rationale": priority_res["rationale"]
            },
            "duplicates": duplicates_res,
            "entities": entities,
            "sentiment": sentiment
        }
