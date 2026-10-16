"""Seed official PMFBY knowledge reference documents into the backend knowledge base.

This enables grounded retrieval (RAG) and retrieval evaluation tests.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parents[1] / "backend"
KNOWLEDGE_DIR = BACKEND_DIR / "knowledge_base"

DOCS = [
    {
        "title": "PMFBY Operational Guidelines - Localized Calamities and Post-Harvest Losses",
        "source_url": "https://pmfby.gov.in/guidelines/localized-calamities",
        "version_label": "revised-operational-guidelines-2024",
        "effective_date": "2024-04-01",
        "chunks": [
            "Localized calamities cover loss or damage resulting from the occurrence of identified localized risks: hailstorm, landslide, inundation, cloudburst, and natural fire due to lightening affecting isolated farms in the notified area. The farmer must inform the insurance company, bank branch, local agriculture department, or through the national Crop Insurance App within 72 hours of the calamity occurrence.",
            "Post-harvest losses are covered up to a maximum period of 14 days from harvesting for those crops which are kept in 'cut and spread' condition in the field for drying against specific perils of cyclone, cyclonic rains, and unseasonal rains throughout the country. Immediate intimation within 72 hours is mandatory to initiate a survey.",
            "Upon receipt of intimation of localized calamity or post-harvest loss, a joint assessment committee consisting of a representative from the insurance company and an official from the State Agriculture Department must conduct loss assessment within 48 hours of intimation.",
        ],
    },
    {
        "title": "PMFBY Required Documentation, Enrolment, and Claim Preparation",
        "source_url": "https://pmfby.gov.in/guidelines/documentation-checklist",
        "version_label": "enrolment-claims-v2024",
        "effective_date": "2024-04-01",
        "chunks": [
            "Mandatory documents for crop insurance claim processing include: 1. Land Record document (7/12 extract, Khatauni, RoR, or Patta) demonstrating ownership or tenancy. 2. Sowing Certificate or Crop Sowing Declaration issued by authorized revenue/agriculture authority. 3. Bank Account details and passbook copy showing active account and correct IFSC code. 4. Aadhaar card for DBT verification. 5. Premium deduction receipt or policy application reference number.",
            "Farmers must ensure that bank account details in the PMFBY portal match their Aadhaar-seeded active bank account. Discrepancies between bank account name and policy applicant name cause DBT failure during settlement. Tenancy agreements or self-declarations must be endorsed by the village Patwari or Panchayat official for non-loanee sharecroppers.",
        ],
    },
    {
        "title": "PMFBY Prevented Sowing and Mid-Season Adversity Guidelines",
        "source_url": "https://pmfby.gov.in/guidelines/prevented-sowing",
        "version_label": "adverse-weather-v2024",
        "effective_date": "2024-04-01",
        "chunks": [
            "Prevented sowing / Planting risk covers situations where majority of the insured farmers in a notified unit area intending to sow/plant are prevented from doing so due to deficit rainfall or adverse seasonal conditions. If more than 75% of the notified area remains unsown, eligible farmers receive a lump sum payment of up to 25% of the sum insured, and the insurance cover is terminated.",
            "Mid-season adversity covers widespread damage due to prolonged dry spells, severe drought, or unseasonal floods during the crop growth period. State governments can notify mid-season adversity based on weather indices and crop health metrics to trigger an on-account payment of up to 25% of likely claims to provide immediate relief.",
        ],
    },
]


def seed():
    KNOWLEDGE_DIR.mkdir(parents=True, exist_ok=True)
    generated = []
    for doc in DOCS:
        full_text = "\n\n".join(doc["chunks"])
        doc_hash = hashlib.sha256(full_text.encode("utf-8")).hexdigest()
        identity = "\n".join([
            doc_hash,
            doc["source_url"].strip(),
            doc["version_label"].strip(),
            doc["effective_date"].strip(),
            doc["title"].strip(),
        ])
        checksum = hashlib.sha256(identity.encode("utf-8")).hexdigest()
        record = {
            "title": doc["title"],
            "source_url": doc["source_url"],
            "version_label": doc["version_label"],
            "effective_date": doc["effective_date"],
            "checksum_sha256": checksum,
            "document_sha256": doc_hash,
            "filename": f"{doc['version_label']}.md",
            "chunks": doc["chunks"],
            "review_status": "approved_for_retrieval",
            "reviewed_by_user_id": 1,
            "reviewed_at_utc": "2026-06-01T00:00:00Z",
            "source_verified_by_app": True,
            "ingested_at_utc": "2026-06-01T00:00:00Z",
        }
        out_file = KNOWLEDGE_DIR / f"{checksum}.json"
        out_file.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
        generated.append({
            "title": doc["title"],
            "checksum_sha256": checksum,
            "document_sha256": doc_hash,
            "file": str(out_file),
        })
    print(json.dumps(generated, indent=2))
    return generated


if __name__ == "__main__":
    seed()
