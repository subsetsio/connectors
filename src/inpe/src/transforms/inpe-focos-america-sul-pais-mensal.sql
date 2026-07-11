-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Country labels are INPE's Portuguese names for South American countries and territories.
SELECT
    make_date("ano", "mes", 1) AS period_start,
    "ano" AS year,
    "mes" AS month,
    "pais" AS country,
    "n_focos" AS active_fire_detections
FROM "inpe-focos-america-sul-pais-mensal"
