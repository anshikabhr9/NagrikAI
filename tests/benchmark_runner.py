"""
NDMC Smart Grievance Management System — AI Accuracy & Benchmark Runner
Author: AI / Automation Engineer (Member 2)
File: tests/benchmark_runner.py

Evaluates test_complaints.csv across:
- Overall Department Classification Accuracy (Target >= 85%)
- Per-Language Accuracy (English, Hindi, Hinglish)
- Priority Detection Accuracy & Safety Hazard Recall
- Latency & Throughput Metrics
"""

import os
import sys
import csv
import time
from collections import defaultdict

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

def run_benchmark():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(base_dir, "data", "test_complaints.csv")
    
    print("=" * 70)
    print("🏛️  NDMC SMART GRIEVANCE SYSTEM — AI BENCHMARK EVALUATION")
    print("=" * 70)
    
    classifier = GrievanceClassifier()
    priority_detector = PriorityDetector()
    
    total = 0
    correct_dept = 0
    correct_prio = 0
    hazard_tp = 0 # True Positives
    hazard_fn = 0 # False Negatives
    hazard_fp = 0 # False Positives
    hazard_tn = 0 # True Negatives
    
    dept_metrics = defaultdict(lambda: {"total": 0, "correct": 0})
    lang_metrics = defaultdict(lambda: {"total": 0, "correct": 0})
    prio_metrics = defaultdict(lambda: {"total": 0, "correct": 0})
    
    latencies = []
    misclassifications = []

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            total += 1
            tc_id = row["id"]
            text = row["text"]
            exp_dept = row["expected_department"]
            exp_prio = row["expected_priority"]
            exp_haz = row["is_hazard"].strip().lower() == "true"
            lang = row.get("language", "en")

            t0 = time.perf_counter()
            pred_class = classifier.classify(text)
            pred_prio = priority_detector.detect_priority(text, pred_class["department_id"])
            t1 = time.perf_counter()
            latencies.append((t1 - t0) * 1000) # in ms

            dept_ok = (pred_class["department_id"] == exp_dept)
            prio_ok = (pred_prio["priority"].upper() == exp_prio.upper())
            
            if dept_ok:
                correct_dept += 1
            else:
                misclassifications.append({
                    "id": tc_id,
                    "text": text,
                    "expected": exp_dept,
                    "predicted": pred_class["department_id"],
                    "confidence": pred_class["confidence"]
                })

            if prio_ok:
                correct_prio += 1

            # Hazard detection confusion matrix
            pred_haz = pred_prio["is_hazard"]
            if exp_haz and pred_haz:
                hazard_tp += 1
            elif exp_haz and not pred_haz:
                hazard_fn += 1
            elif not exp_haz and pred_haz:
                hazard_fp += 1
            else:
                hazard_tn += 1

            dept_metrics[exp_dept]["total"] += 1
            if dept_ok:
                dept_metrics[exp_dept]["correct"] += 1

            lang_metrics[lang]["total"] += 1
            if dept_ok:
                lang_metrics[lang]["correct"] += 1

            prio_metrics[exp_prio]["total"] += 1
            if prio_ok:
                prio_metrics[exp_prio]["correct"] += 1

    dept_acc = (correct_dept / total) * 100 if total else 0
    prio_acc = (correct_prio / total) * 100 if total else 0
    hazard_recall = (hazard_tp / (hazard_tp + hazard_fn)) * 100 if (hazard_tp + hazard_fn) else 0
    hazard_precision = (hazard_tp / (hazard_tp + hazard_fp)) * 100 if (hazard_tp + hazard_fp) else 0
    avg_latency = sum(latencies) / len(latencies) if latencies else 0

    print(f"\n📊 SUMMARY RESULTS (N = {total} Test Cases):")
    print(f"• Overall Department Classification Accuracy: {dept_acc:.2f}% (Target: >= 85.0%)")
    print(f"• Priority Detection Accuracy:               {prio_acc:.2f}%")
    print(f"• Critical Hazard Recall (Safety Rate):      {hazard_recall:.2f}% (Identified {hazard_tp}/{hazard_tp+hazard_fn} hazards)")
    print(f"• Critical Hazard Precision:                 {hazard_precision:.2f}%")
    print(f"• Average Classification Latency:            {avg_latency:.2f} ms")

    print("\n🌐 MULTILINGUAL ACCURACY BREAKDOWN:")
    for lang, m in sorted(lang_metrics.items()):
        acc = (m["correct"] / m["total"]) * 100 if m["total"] else 0
        print(f"  - {lang.upper():<10}: {m['correct']}/{m['total']} ({acc:.1f}%)")

    print("\n🏛️ ACCURACY BY NDMC DEPARTMENT:")
    for d_id, m in sorted(dept_metrics.items()):
        acc = (m["correct"] / m["total"]) * 100 if m["total"] else 0
        print(f"  - {d_id:<28}: {m['correct']}/{m['total']} ({acc:.1f}%)")

    if misclassifications:
        print("\n⚠️ MISCLASSIFIED EXAMPLES (Edge Cases):")
        for mc in misclassifications:
            print(f"  [{mc['id']}] Expected: {mc['expected']} -> Pred: {mc['predicted']} (Conf: {mc['confidence']})")
            print(f"       Text: \"{mc['text']}\"")
    else:
        print("\n✅ PERFECT CLASSIFICATION: 0 misclassifications across test dataset!")

    print("\n" + "=" * 70)
    return {
        "total": total,
        "dept_accuracy": dept_acc,
        "prio_accuracy": prio_acc,
        "hazard_recall": hazard_recall,
        "avg_latency_ms": avg_latency
    }

if __name__ == "__main__":
    run_benchmark()
