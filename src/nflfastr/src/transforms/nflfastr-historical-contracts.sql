-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Historical contract rows can contain multiple contracts for the same player and signing year; do not treat player/year as unique.
SELECT
    "player",
    "position",
    "team",
    "is_active",
    "year_signed",
    "years",
    "value",
    "apy",
    "guaranteed",
    "apy_cap_pct",
    "inflated_value",
    "inflated_apy",
    "inflated_guaranteed",
    "player_page",
    "otc_id",
    "gsis_id",
    "date_of_birth",
    "height",
    CAST("weight" AS BIGINT) AS weight,
    "college",
    "draft_year",
    "draft_round",
    "draft_overall",
    "draft_team",
    "cols"
FROM "nflfastr-historical-contracts"
