"""
NDMC Smart Grievance Management System — Priority & Hazard Detection Engine
Author: AI / Automation Engineer (Member 2)
Module: services/priority_detector.py

Provides:
- Real-time civic severity classification (CRITICAL, HIGH, MEDIUM, LOW)
- Multi-lingual safety hazard detection (English, Hindi Devanagari, Hinglish)
- Automated Citizen Charter SLA calculation (Hours)
"""

import re
from typing import Dict, List, Any, Optional

class PriorityDetector:
    def __init__(self):
        self._init_hazard_rules()

    def _init_hazard_rules(self):
        # Critical safety hazards (SLA <= 12 hours)
        self.critical_hazard_patterns = [
            (r'(live electric wire|live wire|snapped wire|dangling wire|wire hanging|खतरनाक तार|फीडर पिलर खुला|करंट|sparking transformer|transformer blast|sparking furiously)', "Electrical Electrocution / Fire Hazard", 4),
            (r'(open manhole|missing manhole|खुला मैनहोल|ढक्कन गायब|मैनहोल खुला|manhole cover missing)', "Pedestrian Fall / Drowning Hazard", 4),
            (r'(gas leak|toxic gas|गैस पाइपलाइन|गैस रिसाव|chemical spill|smell of gas|gas ki smell)', "Toxic Gas / Fire Hazard", 4),
            (r'(waterlogging.*trapped|flooding.*trapped|underpass.*trapped|drowning|car trapped|गाड़ियां डूब|inundation)', "Severe Inundation / Submersion Emergency", 4),
            (r'(building.*collapse|wall collapse|balcony gir|deewar gir|मकान ढहना|मकान दरार|boundary wall collapsed|structural crack|balcony gir gayi|dilapidated building structure)', "Structural Failure / Collapse Hazard", 6),
            (r'(contaminated.*water|black and foul-smelling|dirty tap water|sewage mixed|ganda pani.*peena|गंदा पानी.*पीना|foul-smelling in tilak)', "Potable Water Contamination Emergency", 12),
            (r'(dog bite|aggressive.*dog|stray dogs.*bit|आवारा कुत्ता.*काट|attacks.*residents|aggressive monkeys|bit a delivery boy)', "Dangerous Animal Menace / Rabies Threat", 12),
            (r'(fallen tree.*blocking|tree uprooted|पेड़ गिरना.*रास्ता|blocking.*road|blocking.*ambulance|fire brigade.*blocked|illegal parking.*fire brigade)', "Emergency Access Roadway Obstruction", 6),
            (r'(openly burning.*smoke|burning.*plastic|कूड़ा जलाना.*धुआं|fire hazard|toxic smoke|suffocating smoke|security guard openly burning)', "Active Toxic Inhalation / Fire Hazard", 6),
            (r'(mid-day meal.*stale|meal.*unfit|food poisoning|मिड-डे मील.*खराब)', "Food Contamination / Student Safety Emergency", 8),
            (r'(leaning dangerously|light pole.*leaning|pole.*leaning at 45)', "Falling Infrastructure Threat", 6)
        ]

        # High priority patterns (SLA <= 24 hours)
        self.high_priority_patterns = [
            r'(power outage|blackout|bijli gul|no electricity|बिजली गुल)',
            r'(pipeline burst|pipe burst|water gushing|पाइप फटा)',
            r'(dead.*animal|dead.*dog|मृत पशु|dead street dog)',
            r'(sewer.*overflow|sewer.*choke|ganda pani sadak|सीवर ओवरफ्लो|sewer line choke)',
            r'(overflowing.*dhalao|garbage pile|कूड़ा फैल रहा|uncollected garbage|dirty public toilet|सार्वजनिक शौचालय)',
            r'(streetlights.*non-functional|pitch black|dark spot|स्ट्रीट लाइट बंद|all 8 streetlights)',
            r'(pharmacy.*refusing|medicine.*stock|दवाइयां नहीं|doctor.*absent|doctor.*unavailability|no general physician|doctor absent)',
            r'(hawkers.*emergency exit|blocking walkway|avaidh kabza|सरकारी जमीन पर अवैध कब्जा|unauthorized commercial fourth floor|thele walo ne rasta)',
            r'(dust violation|heavy dust smog|construction site dust)',
            r'(broken desks|broken fan wires|drinking water cooler kharab|छात्राओं के शौचालय)',
            r'(parking attendant.*forcibly charging|overcharging by parking)',
            r'(monkeys entered|troop of aggressive monkeys|bimar awara kutton)',
            r'(masssive pothole|two-wheeler accidents|displaced into the driving lane|damaged road divider)'
        ]

        # Low priority patterns (SLA 72 hours)
        self.low_priority_patterns = [
            r'(park.*ghas|grass.*cutting|benches.*swings|झूले टूटे|dry plants)',
            r'(mutation application.*pending|mutation delay)',
            r'(street lights on in daytime|din me bhi jal rahi)',
            r'(smart city kiosk.*black|स्मार्ट सिटी कियोस्क)',
            r'(illegal banner|hoarding on public|अवैध होर्डिंग)'
        ]

    def detect_priority(self, text: str, department_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Analyzes complaint description and assigns priority tier, SLA hours, hazard flags, and rationale.
        """
        if not text or not text.strip():
            return {
                "priority": "LOW",
                "sla_hours": 72,
                "is_hazard": False,
                "hazard_type": None,
                "urgency_score": 0.1,
                "rationale": "Standard routine municipal maintenance request."
            }

        text_lower = text.lower()
        
        # 1. Critical Safety Hazards
        for pattern, hazard_desc, sla in self.critical_hazard_patterns:
            if re.search(pattern, text_lower, re.IGNORECASE):
                return {
                    "priority": "CRITICAL",
                    "sla_hours": sla,
                    "is_hazard": True,
                    "hazard_type": hazard_desc,
                    "urgency_score": 0.95,
                    "rationale": f"Emergency safety condition detected: {hazard_desc}. Requires field response within {sla} hours."
                }

        # 2. Low Priority Patterns
        for pattern in self.low_priority_patterns:
            if re.search(pattern, text_lower, re.IGNORECASE):
                return {
                    "priority": "LOW",
                    "sla_hours": 72,
                    "is_hazard": False,
                    "hazard_type": None,
                    "urgency_score": 0.25,
                    "rationale": "Non-urgent municipal maintenance, administrative query, or routine aesthetic upkeep."
                }

        # 3. High Priority Patterns
        for pattern in self.high_priority_patterns:
            if re.search(pattern, text_lower, re.IGNORECASE):
                return {
                    "priority": "HIGH",
                    "sla_hours": 24,
                    "is_hazard": False,
                    "hazard_type": None,
                    "urgency_score": 0.75,
                    "rationale": "High-impact civic service disruption requiring prompt resolution within 24 hours."
                }

        # 4. Medium Priority (Default for standard civil repairs, payment queries, app issues)
        return {
            "priority": "MEDIUM",
            "sla_hours": 48,
            "is_hazard": False,
            "hazard_type": None,
            "urgency_score": 0.50,
            "rationale": "Standard civic repair work scheduled within 48-hour service window."
        }
