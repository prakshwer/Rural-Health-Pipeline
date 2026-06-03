from pydantic import BaseModel, field_validator
from sqlalchemy import create_engine, text
import pandas as pd
import os
from ingestion.generate_data import generate_patient_records

os.makedirs("data", exist_ok=True)
engine = create_engine("sqlite:///data/health.db")

class PatientRecord(BaseModel):
    patient_id: str
    name: str
    age: int
    gender: str
    village: str
    visit_date: str
    diagnosis: str
    temperature_c: float
    systolic_bp: int
    diastolic_bp: int
    blood_glucose: int
    referred_to_hospital: bool
    health_worker_id: str
    health_worker_name: str
    is_child_under_5: bool
    is_elderly: bool
    is_high_risk_disease: bool
    visit_month: str
    visit_week: str
    created_at: str

    @field_validator('age')
    @classmethod
    def valid_age(cls, v):
        assert 0 <= v <= 120, "Age out of range"
        return v

    @field_validator('temperature_c')
    @classmethod
    def valid_temp(cls, v):
        assert 35.0 <= v <= 42.0, "Temperature out of range"
        return v

    @field_validator('gender')
    @classmethod
    def valid_gender(cls, v):
        assert v in ["Male", "Female", "Other"]
        return v

def ensure_table():
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS raw_patients (
                patient_id TEXT,
                name TEXT,
                age INTEGER,
                gender TEXT,
                village TEXT,
                visit_date TEXT,
                diagnosis TEXT,
                temperature_c REAL,
                systolic_bp INTEGER,
                diastolic_bp INTEGER,
                blood_glucose INTEGER,
                referred_to_hospital INTEGER,
                health_worker_id TEXT,
                health_worker_name TEXT,
                is_child_under_5 INTEGER,
                is_elderly INTEGER,
                is_high_risk_disease INTEGER,
                visit_month TEXT,
                visit_week TEXT,
                created_at TEXT
            )
        """))
        conn.commit()

def validate_and_load(df: pd.DataFrame):
    ensure_table()

    # Auto-fill missing columns so CSV uploads work
    # even if they don't have every column
    from datetime import datetime

    if 'is_child_under_5' not in df.columns:
        df['is_child_under_5'] = df['age'] < 5

    if 'is_elderly' not in df.columns:
        df['is_elderly'] = df['age'] >= 60

    if 'is_high_risk_disease' not in df.columns:
        high_risk = ["Malaria", "Dengue", "Tuberculosis"]
        df['is_high_risk_disease'] = df['diagnosis'].isin(high_risk)

    if 'visit_month' not in df.columns:
        df['visit_month'] = pd.to_datetime(
            df['visit_date']).dt.strftime("%Y-%m")

    if 'visit_week' not in df.columns:
        df['visit_week'] = pd.to_datetime(
            df['visit_date']).dt.strftime("%Y-W%W")

    if 'created_at' not in df.columns:
        df['created_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if 'health_worker_name' not in df.columns:
        df['health_worker_name'] = "Unknown"

    # Convert referred_to_hospital to bool
    if 'referred_to_hospital' in df.columns:
        df['referred_to_hospital'] = df['referred_to_hospital'].astype(str).str.lower().isin(['true', '1', 'yes'])

    valid_records = []
    errors = 0

    for _, row in df.iterrows():
        try:
            record = PatientRecord(**row.to_dict())
            valid_records.append(record.model_dump())
        except Exception as e:
            errors += 1
            print(f"Validation error on row: {e}")

    if valid_records:
        valid_df = pd.DataFrame(valid_records)
        valid_df.to_sql("raw_patients", engine,
                        if_exists="append", index=False)
        print(f"Loaded {len(valid_records)} records. "
              f"Skipped {errors} invalid.")
    else:
        print("No valid records to load!")