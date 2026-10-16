"""
Generate Synthetic Sample Claim Assistance PDF for demonstration and verification.
Uses clearly labeled synthetic data.
"""
import sys
import os
from pathlib import Path
from datetime import datetime, timezone

# Add backend directory to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from app.services.form_service import populate_form_data, generate_claim_assistance_pdf

class FakeUser:
    id = 901
    full_name = "Ramesh Tukaram Patil (Demo Farmer)"
    phone = "9876543210"
    email = "farmer.demo@example.com"
    aadhaar_last4 = "4321"
    bank_account_last4 = "8899"
    bank_ifsc = "MAHB0001234"

class FakeClaim:
    id = 9999
    reference = "DEMO-CLM-2024-MH"
    crop = "Soybean"
    season = "Kharif"
    year = 2024
    state = "Maharashtra"
    district = "Nagpur"
    village = "Saoner"
    loss_type = "localized"
    incident_date = datetime(2024, 8, 14, 14, 30, tzinfo=timezone.utc)
    reported_at = datetime(2024, 8, 15, 10, 0, tzinfo=timezone.utc)
    area_hectares = 2.5
    policy_reference = "PMFBY/2024/MH/77889911"
    sum_insured = 125000.0
    premium_paid = 2500.0
    insurer_name = "Agriculture Insurance Company of India (AIC)"
    description = "Inundation of soybean field due to sudden heavy downpour and flash flooding."

class FakeDamageReport:
    damage_category = "localized_inundation"
    description = "Water stagnation in lower field section for over 36 hours causing crop rot."
    incident_date = datetime(2024, 8, 14, 14, 30, tzinfo=timezone.utc)
    affected_area_ha = 1.8
    latitude = 21.3852
    longitude = 78.9184
    gps_accuracy_meters = 4.2
    location_source = "device_gps"
    photos = [{"id": 1}, {"id": 2}]

class FakeWeather:
    start_date = "2024-08-11"
    end_date = "2024-08-17"
    cumulative_rainfall_mm = 142.6
    extreme_rain_flag = True
    provider = "open-meteo"

def main():
    claim = FakeClaim()
    farmer = FakeUser()
    damage_report = FakeDamageReport()
    weather = FakeWeather()

    form_data = populate_form_data(
        claim=claim,
        farmer=farmer,
        damage_report=damage_report,
        weather_evidence=weather,
    )

    pdf_bytes = generate_claim_assistance_pdf(
        claim=claim,
        farmer=farmer,
        form_data=form_data,
        damage_report=damage_report,
        weather_evidence=weather,
    )

    out_path = Path(__file__).resolve().parent.parent / "docs" / "sample_claim_assistance_form.pdf"
    with open(out_path, "wb") as f:
        f.write(pdf_bytes)

    print(f"Sample PDF generated successfully at: {out_path} ({len(pdf_bytes)} bytes)")
    print(f"Auto-fill Coverage: {form_data['coverage_pct']}% ({form_data.get('auto_filled_count', 0)}/{form_data.get('eligible_count', 0)} fields)")

if __name__ == "__main__":
    main()
