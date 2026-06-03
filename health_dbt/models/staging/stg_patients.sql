select
    patient_id,
    name,
    age,
    gender,
    village,
    visit_date,
    diagnosis,
    temperature_c,
    systolic_bp,
    diastolic_bp,
    blood_glucose,
    referred_to_hospital,
    health_worker_id,
    health_worker_name,
    is_child_under_5,
    is_elderly,
    is_high_risk_disease,
    visit_month,
    visit_week,
    created_at,
    case
        when age < 5  then 'Under 5'
        when age < 18 then 'Child'
        when age < 60 then 'Adult'
        else 'Senior'
    end as age_group,
    case
        when temperature_c >= 38.5 then 'High Fever'
        when temperature_c >= 37.5 then 'Mild Fever'
        else 'Normal'
    end as fever_status,
    case
        when systolic_bp >= 140 then 'Hypertensive'
        when systolic_bp >= 120 then 'Elevated'
        else 'Normal'
    end as bp_status,
    case
        when blood_glucose >= 140 then 'High'
        when blood_glucose >= 100 then 'Borderline'
        else 'Normal'
    end as glucose_status
from {{ source('raw', 'raw_patients') }}
where patient_id is not null
  and age between 0 and 120
  and temperature_c between 35.0 and 42.0