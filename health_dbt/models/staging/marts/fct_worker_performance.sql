select
    health_worker_id,
    health_worker_name,
    count(*) as total_visits,
    count(distinct village) as villages_covered,
    count(distinct patient_id) as unique_patients,
    count(distinct diagnosis) as diseases_handled,
    sum(case when referred_to_hospital = 1 then 1 else 0 end)
        as total_referrals,
    round(
        100.0 * sum(case when referred_to_hospital = 1 then 1 else 0 end)
        / count(*), 1
    ) as referral_rate_pct,
    sum(case when is_child_under_5 = 1 then 1 else 0 end)
        as child_visits,
    sum(case when is_elderly = 1 then 1 else 0 end)
        as elderly_visits,
    sum(case when is_high_risk_disease = 1 then 1 else 0 end)
        as high_risk_cases,
    visit_month
from {{ ref('stg_patients') }}
group by health_worker_id, health_worker_name, visit_month
order by total_visits desc