-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "environment_activities",
    "number_of_participants_or_target_audience",
    "number_of_activities",
    "cost_qr",
    "l_nsht_lbyy_y"
FROM "qatar-planning-and-statistics-authority-environmental-commitments-in-district-cooling-service-providers"
