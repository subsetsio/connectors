-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Municipality names are not unique across Brazil, so state is part of the row identity.
SELECT
    make_date("ano", 1, 1) AS period_start,
    "ano" AS year,
    "estado" AS state,
    "municipio" AS municipality,
    "n_focos" AS active_fire_detections
FROM "inpe-focos-brasil-municipio-anual"
