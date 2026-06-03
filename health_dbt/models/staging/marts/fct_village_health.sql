select
    village,
    count(*) as total_patients,
    count(distinct diagnosis) as unique_diseases,
    count(distinct health_worker_id) as active_workers,
    round(avg(age), 1) as avg_patient_age,
    round(avg(temperature_c), 2) as avg_temperature,
    sum(case when fever_status = 'High Fever' then 1 else 0 end)
        as high_fever_cases,
    sum(case when bp_status = 'Hypertensive' then 1 else 0 end)
        as hypertension_cases,
    sum(case when is_child_under_5 = 1 then 1 else 0 end)
        as children_under_5,
    sum(case when is_elderly = 1 then 1 else 0 end)
        as elderly_patients,
    sum(case when referred_to_hospital = 1 then 1 else 0 end)
        as hospital_referrals,
    round(
        100.0 * sum(case when referred_to_hospital = 1 then 1 else 0 end)
        / count(*), 1
    ) as referral_rate_pct,
    case
        when sum(case when fever_status='High Fever' then 1 else 0 end)
             >= 15 then 'OUTBREAK ALERT'
        when sum(case when fever_status='High Fever' then 1 else 0 end)
             >= 8  then 'WATCH'
        else 'NORMAL'
    end as outbreak_status
from {{ ref('stg_patients') }}
group by village
order by total_patients desc