-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is a current per-chamber demographic snapshot, not a historical age time series.
SELECT
    "chamber_code",
    "chamber_name",
    "country_name",
    "country_code",
    "structure_of_parliament",
    "struct_parl_status",
    "age_average",
    "total_younger_30_percentage",
    "total_younger_40_percentage",
    "total_younger_45_percentage",
    "is_suspended_chamber"
FROM "inter-parliamentary-union-report-age-brackets"
