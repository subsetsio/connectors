-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("time_period" AS BIGINT) AS time_period,
    "time_identifier",
    "geographic_level",
    "country_code",
    "country_name",
    "region_code",
    "region_name",
    "old_la_code",
    "new_la_code",
    "la_name",
    "category",
    "referral_count",
    "rereferral_count",
    "rereferral_percent",
    "no_further_action_count",
    "no_further_action_percent",
    "not_in_need_count",
    "not_in_need_percent",
    "referral_child_count",
    "rereferral_child_count",
    "rereferral_child_percent"
FROM "dfe-342f9a01-26f0-2a71-91a1-f8bc0bee8b11"
