"""Reproducible Auto-Fill Coverage and Field Correctness Evaluation for FasalSahay Form Engine.

Measures:
  Metric A: Form auto-fill coverage percentage against the 90% target.
  Metric B: Field-level correctness and exact-match accuracy against ground-truth labels.
"""
from __future__ import annotations
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
BACKEND_DIR = REPO_ROOT / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.services.form_service import populate_form_data

SCENARIOS = [
    {
        "name": "Scenario 1: Localized Inundation (Maharashtra Soybean Kharif) - Full Evidence",
        "claim": type("Claim", (), {
            "id": 1, "reference": "CLM-EVAL-01", "crop": "Soybean", "season": "Kharif", "year": 2024,
            "state": "Maharashtra", "district": "Nagpur", "village": "Saoner", "loss_type": "localized",
            "incident_date": datetime(2024, 8, 14, 14, 0, tzinfo=timezone.utc),
            "reported_at": datetime(2024, 8, 15, 10, 0, tzinfo=timezone.utc),
            "area_hectares": 2.5, "policy_reference": "PMFBY/2024/MH/1001", "sum_insured": 125000.0,
            "premium_paid": 2500.0, "insurer_name": "AIC of India",
            "description": "Flash flooding following 140mm rainfall inundated standing crop.",
        })(),
        "farmer": type("Farmer", (), {
            "full_name": "Ramesh Tukaram Patil", "phone": "9822114455", "email": "ramesh@example.com",
            "aadhaar_last4": "5544", "bank_account_last4": "1234", "bank_ifsc": "MAHB0000123",
        })(),
        "damage_report": type("DamageReport", (), {
            "damage_category": "localized_inundation", "description": "Water submerged crop for 36 hours.",
            "incident_date": datetime(2024, 8, 14, 14, 0, tzinfo=timezone.utc),
            "affected_area_ha": 2.0, "latitude": 21.3852, "longitude": 78.9184,
            "gps_accuracy_meters": 3.8, "location_source": "device_gps",
            "photos": [1, 2, 3],
        })(),
        "weather": type("Weather", (), {
            "start_date": "2024-08-11", "end_date": "2024-08-17",
            "cumulative_rainfall_mm": 142.5, "extreme_rain_flag": True, "provider": "open-meteo",
        })(),
        "ground_truth": {
            "farmer_name": "Ramesh Tukaram Patil",
            "crop": "Soybean",
            "season": "Kharif",
            "year": "2024",
            "state": "Maharashtra",
            "district": "Nagpur",
            "policy_reference": "PMFBY/2024/MH/1001",
            "loss_type": "localized",
            "damage_category": "localized_inundation",
            "sown_area_ha": "2.50 ha",
            "affected_area_ha": "2.00 ha",
        }
    },
    {
        "name": "Scenario 2: Localized Hailstorm (Madhya Pradesh Wheat Rabi) - Full Evidence",
        "claim": type("Claim", (), {
            "id": 2, "reference": "CLM-EVAL-02", "crop": "Wheat", "season": "Rabi", "year": 2024,
            "state": "Madhya Pradesh", "district": "Sehore", "village": "Ashta", "loss_type": "localized",
            "incident_date": datetime(2024, 2, 28, 16, 30, tzinfo=timezone.utc),
            "reported_at": datetime(2024, 3, 1, 9, 0, tzinfo=timezone.utc),
            "area_hectares": 3.0, "policy_reference": "PMFBY/2024/MP/2002", "sum_insured": 180000.0,
            "premium_paid": 2700.0, "insurer_name": "SBI General Insurance",
            "description": "Severe hailstorm damaged flowering wheat crop.",
        })(),
        "farmer": type("Farmer", (), {
            "full_name": "Dinesh Kumar Verma", "phone": "9893112233", "email": "dinesh@example.com",
            "aadhaar_last4": "7788", "bank_account_last4": "4321", "bank_ifsc": "SBIN0001122",
        })(),
        "damage_report": type("DamageReport", (), {
            "damage_category": "hailstorm", "description": "Hail stones broke stems and stripped foliage.",
            "incident_date": datetime(2024, 2, 28, 16, 30, tzinfo=timezone.utc),
            "affected_area_ha": 2.8, "latitude": 23.0189, "longitude": 76.7183,
            "gps_accuracy_meters": 4.5, "location_source": "device_gps",
            "photos": [1, 2],
        })(),
        "weather": type("Weather", (), {
            "start_date": "2024-02-25", "end_date": "2024-03-02",
            "cumulative_rainfall_mm": 38.0, "extreme_rain_flag": False, "provider": "open-meteo",
        })(),
        "ground_truth": {
            "farmer_name": "Dinesh Kumar Verma",
            "crop": "Wheat",
            "season": "Rabi",
            "year": "2024",
            "state": "Madhya Pradesh",
            "district": "Sehore",
            "policy_reference": "PMFBY/2024/MP/2002",
            "loss_type": "localized",
            "damage_category": "hailstorm",
            "sown_area_ha": "3.00 ha",
            "affected_area_ha": "2.80 ha",
        }
    },
    {
        "name": "Scenario 3: Post-Harvest Unseasonal Rain (Odisha Paddy Kharif) - Cut & Spread",
        "claim": type("Claim", (), {
            "id": 3, "reference": "CLM-EVAL-03", "crop": "Paddy", "season": "Kharif", "year": 2024,
            "state": "Odisha", "district": "Puri", "village": "Nimapada", "loss_type": "post_harvest",
            "incident_date": datetime(2024, 11, 10, 11, 0, tzinfo=timezone.utc),
            "reported_at": datetime(2024, 11, 11, 15, 0, tzinfo=timezone.utc),
            "area_hectares": 1.8, "policy_reference": "PMFBY/2024/OD/3003", "sum_insured": 90000.0,
            "premium_paid": 1800.0, "insurer_name": "Bajaj Allianz",
            "description": "Cyclonic rains submerged paddy bundles kept in field for drying.",
        })(),
        "farmer": type("Farmer", (), {
            "full_name": "Pradeep Mohapatra", "phone": "9437112233", "email": "pradeep@example.com",
            "aadhaar_last4": "9900", "bank_account_last4": "5566", "bank_ifsc": "PUNB0004455",
        })(),
        "damage_report": type("DamageReport", (), {
            "damage_category": "unseasonal_cyclonic_rain", "description": "Harvested crop kept in cut and spread condition.",
            "incident_date": datetime(2024, 11, 10, 11, 0, tzinfo=timezone.utc),
            "affected_area_ha": 1.8, "latitude": 19.9984, "longitude": 85.8752,
            "gps_accuracy_meters": 5.1, "location_source": "device_gps",
            "photos": [1, 2, 3, 4],
        })(),
        "weather": type("Weather", (), {
            "start_date": "2024-11-08", "end_date": "2024-11-14",
            "cumulative_rainfall_mm": 95.4, "extreme_rain_flag": True, "provider": "open-meteo",
        })(),
        "ground_truth": {
            "farmer_name": "Pradeep Mohapatra",
            "crop": "Paddy",
            "season": "Kharif",
            "year": "2024",
            "state": "Odisha",
            "district": "Puri",
            "policy_reference": "PMFBY/2024/OD/3003",
            "loss_type": "post_harvest",
            "sown_area_ha": "1.80 ha",
            "affected_area_ha": "1.80 ha",
        }
    },
]


def evaluate_autofill():
    print("=" * 70)
    print("FASALSAHAY — CLAIM FORM AUTO-FILL & FIELD CORRECTNESS EVALUATION")
    print("=" * 70)

    total_scenarios = len(SCENARIOS)
    coverages = []
    correctness_scores = []
    summary_scenarios = []

    for sc in SCENARIOS:
        res = populate_form_data(
            claim=sc["claim"],
            farmer=sc["farmer"],
            damage_report=sc["damage_report"],
            weather_evidence=sc["weather"],
        )
        cov = res["coverage_pct"]
        coverages.append(cov)

        # Field Correctness Evaluation against Ground Truth
        gt = sc["ground_truth"]
        fields = res["fields"]
        matches = 0
        total_eval = len(gt)

        for k, expected in gt.items():
            actual = fields.get(k, {}).get("value")
            if str(actual).strip() == str(expected).strip():
                matches += 1

        acc = round((matches / total_eval) * 100.0, 1)
        correctness_scores.append(acc)

        summary_scenarios.append({
            "scenario": sc["name"],
            "eligible_fields": res["total_eligible_fields"],
            "populated_fields": res["populated_fields_count"],
            "missing_fields": res["missing_fields_count"],
            "coverage_pct": cov,
            "target_90_met": cov >= 90.0,
            "ground_truth_accuracy_pct": acc,
        })

    avg_cov = round(sum(coverages) / total_scenarios, 1)
    avg_acc = round(sum(correctness_scores) / total_scenarios, 1)

    report = {
        "evaluation_title": "PMFBY Claim Form Auto-Fill Coverage & Correctness Benchmark",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "total_scenarios_evaluated": total_scenarios,
        "metric_a_autofill_coverage": {
            "target_pct": 90.0,
            "average_coverage_pct": avg_cov,
            "target_met": avg_cov >= 90.0,
            "formula": "(eligible_populated_fields / total_eligible_fields) * 100",
        },
        "metric_b_field_correctness": {
            "average_accuracy_pct": avg_acc,
            "formula": "(exact_matches_against_ground_truth / evaluated_ground_truth_fields) * 100",
        },
        "scenario_breakdown": summary_scenarios,
    }

    out_file = REPO_ROOT / "ml" / "autofill_evaluation_report.json"
    out_file.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(json.dumps(report, indent=2))
    print(f"\nReport written to: {out_file}")
    return report


if __name__ == "__main__":
    evaluate_autofill()
