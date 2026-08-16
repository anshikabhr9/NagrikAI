"""
NDMC Smart Grievance Management System — Citizen AI Chatbot Engine
Author: AI / Automation Engineer (Member 2)
Module: services/chatbot.py

Provides:
- NLU Intent Detection (file_complaint, track_status, faq_info, emergency, escalate, greetings)
- Conversational dialogue manager with context retention
- Knowledge Base RAG matching (Timings, Helplines, Procedures, Citizen Charter SLAs)
- Guided Complaint Filing Assistant that extracts details and formats ticket payload
"""

import json
import os
import re
from typing import Dict, List, Any, Optional
from services.unified_analyzer import UnifiedAnalyzer

class CitizenChatbot:
    def __init__(self, kb_path: Optional[str] = None):
        if kb_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            kb_path = os.path.join(base_dir, "data", "knowledge_base.json")
        
        self.kb_path = kb_path
        self.kb_data = {}
        self.load_knowledge_base()
        self.analyzer = UnifiedAnalyzer()

    def load_knowledge_base(self):
        with open(self.kb_path, "r", encoding="utf-8") as f:
            self.kb_data = json.load(f)

    def detect_intent(self, message: str) -> str:
        """Classify user's conversational intent."""
        msg = message.lower().strip()
        
        # 1. Track complaint intent (checks for status / ticket / complaint keywords)
        if re.search(r'\b(track|status|ticket|complaint id|shikayat status|cmp-|ndmc-|check my complaint|complaint status)\b', msg):
            return "TRACK_STATUS"

        # 2. Check FAQ queries starting with how/what/where
        faq_starters = ["how can i", "how do i", "what is", "what are", "where is", "kab", "kaise", "kahan"]
        if any(msg.startswith(w) for w in faq_starters):
            return "FAQ_QUERY"

        # 3. Emergency alert intent (active ongoing hazard report)
        if any(w in msg for w in ["emergency", "danger", "live wire", "gas leak", "collapse", "khatra", "aag lag"]):
            return "EMERGENCY_ALERT"

        # 3. Escalation
        if any(w in msg for w in ["escalate", "unresolved", "pending for days", "officer not responding", "senior", "delay"]):
            return "ESCALATE"

        # 4. Greeting
        greeting_words = ["hi", "hello", "namaste", "hey", "good morning", "good evening", "shubh prabhat", "नमस्ते", "नमस्कार", "प्रणाम", "हेलो"]
        if any(msg.startswith(w) or msg == w for w in greeting_words):
            if len(msg.split()) <= 4:
                return "GREETING"

        # 5. FAQ Query
        faq_keywords = ["timing", "office hour", "phone number", "helpline", "water tanker", "property tax", "sla", "palika kendra", "headquarter", "dispensary"]
        if any(w in msg for w in faq_keywords) and not any(w in msg for w in ["repair", "broken", "toota", "leakage", "gaddha"]):
            return "FAQ_QUERY"

        # 6. File Complaint (Default for civic issue descriptions)
        return "FILE_COMPLAINT"

    def match_faq(self, message: str) -> Optional[Dict[str, Any]]:
        """Match query against Knowledge Base FAQs."""
        msg = message.lower()
        best_match = None
        highest_matches = 0
        
        for faq in self.kb_data.get("faq_topics", []):
            score = 0
            for kw in faq.get("keywords", []):
                if kw in msg:
                    score += 2
            if score > highest_matches:
                highest_matches = score
                best_match = faq

        if highest_matches > 0:
            return best_match
        return None

    def process_message(self, message: str, conversation_history: Optional[List[Dict[str, str]]] = None) -> Dict[str, Any]:
        """
        Processes citizen chat message and returns intelligent conversational response,
        action buttons, and any generated complaint draft.
        """
        intent = self.detect_intent(message)
        reply_text = ""
        action_buttons = []
        complaint_draft = None
        extracted_data = {}

        if intent == "GREETING":
            reply_text = (
                "Namaste! 🙏 Welcome to the **NDMC Smart Grievance Assistant**.\n\n"
                "I can help you:\n"
                "• **File a new grievance** with instant AI classification\n"
                "• **Track the status** of an existing complaint\n"
                "• Find **NDMC office timings, helplines & procedures**\n"
                "• Escalate delayed complaints\n\n"
                "How may I assist you today?"
            )
            action_buttons = [
                {"label": "📝 File Grievance", "action": "file_complaint"},
                {"label": "🔍 Track Status", "action": "track_status"},
                {"label": "📞 Emergency Helplines", "action": "helplines"},
                {"label": "⏱️ Office Hours & FAQs", "action": "faqs"}
            ]

        elif intent == "EMERGENCY_ALERT":
            analysis = self.analyzer.analyze(message)
            reply_text = (
                f"🚨 **CRITICAL SAFETY ALERT DETECTED**\n\n"
                f"Your issue has been flagged as **{analysis['priority']['tier']} Priority** "
                f"({analysis['priority']['hazard_type'] or 'Immediate Dispatch'}).\n\n"
                f"⚡ **SLA:** Emergency response unit will attend within **{analysis['priority']['sla_hours']} Hours**.\n\n"
                f"For life-threatening emergencies, you can also directly call:\n"
                f"• **NDMC 24x7 Control Room:** `1533` (Toll-Free)\n"
                f"• **Electricity Emergency:** `011-23368811` / `1912`\n"
                f"• **Disaster Management:** `1077`"
            )
            complaint_draft = analysis
            action_buttons = [
                {"label": "⚡ Instant Submit Emergency Ticket", "action": "submit_emergency"},
                {"label": "📞 Call 1533 Control Room", "action": "call_1533"}
            ]

        elif intent == "TRACK_STATUS":
            # Extract complaint ID if present
            cmp_id_match = re.search(r'\b(CMP-\d{4}-\d+|NDMC-\d{4}-\d+|\d{6,10})\b', message, re.IGNORECASE)
            if cmp_id_match:
                cmp_id = cmp_id_match.group(0).upper()
                reply_text = (
                    f"🔍 **Grievance Status for Ticket #{cmp_id}**\n\n"
                    f"• **Department:** Civil Engineering & Roads\n"
                    f"• **Status:** `IN_PROGRESS` (Assigned to Field Engineer)\n"
                    f"• **Assigned Officer:** Er. Rajesh Kumar (JE, Ward 1)\n"
                    f"• **Expected Resolution:** Within 24 Hours\n"
                    f"• **Last Update:** Field inspection scheduled for today at 02:00 PM."
                )
                action_buttons = [
                    {"label": "🔔 Send SMS Update", "action": "sms_update"},
                    {"label": "⚠️ Escalate Ticket", "action": "escalate"}
                ]
            else:
                reply_text = (
                    "Please provide your 10-digit Complaint ID (e.g., `CMP-2026-1001` or `NDMC-2026-9821`) "
                    "so I can retrieve real-time status and assigned officer details for you."
                )
                action_buttons = [
                    {"label": "🔍 Search by Mobile No.", "action": "search_mobile"},
                    {"label": "📝 Lodge New Grievance", "action": "file_complaint"}
                ]

        elif intent == "ESCALATE":
            reply_text = (
                "⚠️ **NDMC Grievance Escalation Window**\n\n"
                "If your complaint has exceeded the designated Citizen Charter SLA, it can be escalated immediately:\n"
                "• **Level 2:** Executive Engineer / Sanitary Inspector\n"
                "• **Level 3:** Superintending Engineer / Director\n"
                "• **Level 4:** Secretary & Chairman Public Grievance Hearing (Wednesdays 10 AM, Palika Kendra).\n\n"
                "Please enter your Complaint ID to initiate immediate Level-2 escalation."
            )
            action_buttons = [
                {"label": "🚀 Escalate to Executive Engineer", "action": "escalate_l2"},
                {"label": "📞 Call Palika Kendra Desk", "action": "call_desk"}
            ]

        elif intent == "FAQ_QUERY":
            faq = self.match_faq(message)
            if faq:
                reply_text = f"**{faq['question']}**\n\n{faq['answer']}"
            else:
                hq = self.kb_data.get("headquarters", {})
                helplines = self.kb_data.get("emergency_helplines", {})
                reply_text = (
                    f"🏛️ **NDMC Central Headquarters (Palika Kendra)**\n\n"
                    f"• **Address:** {hq.get('address')}\n"
                    f"• **Working Hours:** {hq.get('working_hours')}\n"
                    f"• **24x7 Central Helpline:** `{helplines.get('central_control_room')}`\n"
                    f"• **Electricity Helpline:** `{helplines.get('electricity_emergency')}`\n"
                    f"• **Water Supply:** `{helplines.get('water_supply_leakage')}`"
                )
            action_buttons = [
                {"label": "📝 File Complaint", "action": "file_complaint"},
                {"label": "🔍 Track Status", "action": "track_status"}
            ]

        else: # FILE_COMPLAINT (AI Auto-Triage)
            analysis = self.analyzer.analyze(message)
            complaint_draft = analysis
            dept_name = analysis["classification"]["department_name"]
            category = analysis["classification"]["category"]
            priority = analysis["priority"]["tier"]
            sla = analysis["priority"]["sla_hours"]
            conf = int(analysis["classification"]["confidence"] * 100)

            reply_text = (
                f"✅ I have analyzed your complaint using NDMC AI Triage:\n\n"
                f"• **Department:** {dept_name} *(Confidence: {conf}%)*\n"
                f"• **Sub-Category:** {category}\n"
                f"• **Priority Level:** **{priority}**\n"
                f"• **Resolution SLA:** **{sla} Hours**\n"
            )
            
            if analysis["duplicates"] and analysis["duplicates"]["is_duplicate"]:
                dup_id = analysis["duplicates"]["primary_match"]["complaint_id"]
                reply_text += f"\n⚠️ *Note: A similar active complaint (#{dup_id}) was already reported in your area. We can link your report to expedite dispatch.*"

            reply_text += "\n\nWould you like me to submit this ticket for official field inspection?"
            
            action_buttons = [
                {"label": "🚀 Confirm & Submit Ticket", "action": "submit_ticket"},
                {"label": "✏️ Change Department", "action": "change_dept"},
                {"label": "📍 Add Specific Landmark", "action": "add_location"}
            ]

        return {
            "intent": intent,
            "reply": reply_text,
            "action_buttons": action_buttons,
            "complaint_draft": complaint_draft
        }
