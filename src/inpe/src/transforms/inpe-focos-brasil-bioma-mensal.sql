-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Biome labels are INPE's Brazilian biome names in Portuguese.
SELECT
    make_date("ano", "mes", 1) AS period_start,
    "ano" AS year,
    "mes" AS month,
    "bioma" AS biome,
    "n_focos" AS active_fire_detections
FROM "inpe-focos-brasil-bioma-mensal"
