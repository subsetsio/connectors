-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The count uses the reference satellite series; FRP, fire-risk, precipitation, and dry-days columns are monthly means over detections with usable source values.
SELECT
    make_date("ano", "mes", 1) AS period_start,
    "ano" AS year,
    "mes" AS month,
    "n_focos" AS active_fire_detections,
    "frp_medio" AS mean_fire_radiative_power,
    "risco_fogo_medio" AS mean_fire_risk,
    "precipitacao_media" AS mean_precipitation,
    "dias_sem_chuva_medio" AS mean_days_without_rain
FROM "inpe-focos-brasil-mensal"
