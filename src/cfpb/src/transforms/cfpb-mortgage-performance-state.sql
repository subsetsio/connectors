-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: State rows are separate from county and metro tables; do not combine geographic levels without selecting one level.
SELECT
    "region_type",
    "region_name",
    "fips_code",
    "bucket",
    strptime("period", '%Y-%m')::DATE AS period,
    "delinquency_rate"
FROM "cfpb-mortgage-performance-state"
