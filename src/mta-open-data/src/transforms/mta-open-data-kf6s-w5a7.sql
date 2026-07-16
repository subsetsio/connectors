-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Published as a full Socrata snapshot table; no stable row key was asserted during schema-only profiling.
SELECT
    "month",
    "company",
    "fleet_age",
    "total_of_buses",
    "_of_buses_over_12_years" AS of_buses_over_12_years
FROM "mta-open-data-kf6s-w5a7"
