-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "nationality",
    "ljnsy",
    "early_neonatal_mortality_rate_0_7_days",
    "late_neonatal_mortality_rate_7_28_days",
    "neonatal_mortality_rate_0_28_days",
    "post_neonatal_mortality_rate_28_264_days",
    "total"
FROM "qatar-planning-and-statistics-authority-neonatal-mortality-rate"
