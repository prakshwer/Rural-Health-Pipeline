import random
import pandas as pd
from faker import Faker
from datetime import datetime, timedelta

fake = Faker('en_IN')

VILLAGES = [
    "Jhargram", "Purulia", "Bankura", "Sundarbans",
    "Paschim Medinipur", "Birbhum", "Murshidabad",
    "Nadia", "Hooghly", "South 24 Parganas"
]

DISEASES = [
    "Malaria", "Dengue", "Tuberculosis", "Diarrhoea",
    "Anaemia", "Hypertension", "Diabetes",
    "Respiratory Infection", "Skin Infection", "Malnutrition"
]

HEALTH_WORKERS = [
    {"id": "HW101", "name": "Priya Sharma"},
    {"id": "HW102", "name": "Ramesh Das"},
    {"id": "HW103", "name": "Sunita Mondal"},
    {"id": "HW104", "name": "Amit Ghosh"},
    {"id": "HW105", "name": "Rekha Patel"},
    {"id": "HW106", "name": "Suresh Mahato"},
    {"id": "HW107", "name": "Anita Devi"},
    {"id": "HW108", "name": "Biplab Roy"},
]

def generate_patient_records(n=200):
    records = []
    for _ in range(n):
        age = random.randint(1, 85)
        gender = random.choice(["Male", "Female", "Other"])
        village = random.choice(VILLAGES)
        disease = random.choice(DISEASES)
        worker = random.choice(HEALTH_WORKERS)
        visit_date = datetime.now() - timedelta(days=random.randint(0, 90))

        # Realistic vitals based on disease
        if disease == "Hypertension":
            systolic = random.randint(140, 180)
            diastolic = random.randint(90, 110)
        else:
            systolic = random.randint(100, 130)
            diastolic = random.randint(70, 85)

        if disease == "Diabetes":
            blood_glucose = random.randint(140, 300)
        else:
            blood_glucose = random.randint(70, 110)

        if disease in ["Malaria", "Dengue", "Tuberculosis"]:
            temperature = round(random.uniform(38.5, 40.5), 1)
        else:
            temperature = round(random.uniform(36.5, 37.5), 1)

        is_child = age < 5
        is_elderly = age >= 60
        is_high_risk = disease in ["Tuberculosis", "Malaria", "Dengue"]

        records.append({
            "patient_id": fake.uuid4()[:8].upper(),
            "name": fake.name(),
            "age": age,
            "gender": gender,
            "village": village,
            "visit_date": visit_date.strftime("%Y-%m-%d"),
            "diagnosis": disease,
            "temperature_c": temperature,
            "systolic_bp": systolic,
            "diastolic_bp": diastolic,
            "blood_glucose": blood_glucose,
            "referred_to_hospital": random.choice(
                [True, False, False, False, False]),
            "health_worker_id": worker["id"],
            "health_worker_name": worker["name"],
            "is_child_under_5": is_child,
            "is_elderly": is_elderly,
            "is_high_risk_disease": is_high_risk,
            "visit_month": visit_date.strftime("%Y-%m"),
            "visit_week": visit_date.strftime("%Y-W%W"),
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    return pd.DataFrame(records)