-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "key_performance_indicator",
    "goal",
    "objective",
    "kpi_definition",
    "metric",
    "baseline_measure_3q_2015",
    "_4q_2015_measure" AS 4q_2015_measure
FROM "nyc-open-data-nja7-3m37"
