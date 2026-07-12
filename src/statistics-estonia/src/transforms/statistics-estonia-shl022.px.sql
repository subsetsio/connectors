-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "change_in_health_self_assessment",
    "indicator",
    "birth_cohort",
    "value"
FROM "statistics-estonia-shl022.px"
