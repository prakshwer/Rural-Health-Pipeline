select
    diagnosis,
    village,
    visit_month,
    count(*) as monthly_cases,
    round(avg(temperature_c), 2) as avg_temperature,
    sum(case when referred_to_hospital = 1 then 1 else 0 end)
        as referrals,
    sum(case when is_child_under_5 = 1 then 1 else 0 end)
        as child_cases,
    sum(case when is_elderly = 1 then 1 else 0 end)
        as elderly_cases,
    case
        when count(*) >= 20 then 'OUTBREAK ALERT'
        when count(*) >= 10 then 'WATCH'
        else 'NORMAL'
    end as alert_level
from {{ ref('stg_patients') }}
group by diagnosis, village, visit_month
order by monthly_cases desc