-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_month" AS month,
    "borough",
    "community_board",
    "district",
    "cleaning_section",
    "acceptable_streets",
    "acceptable_sidewalks",
    "acceptable_streets_previous_month",
    "acceptable_sidewalks_previous_month",
    "acceptable_streets_previous_year",
    "acceptable_sidewalks_previous_year",
    "acceptable_streets_previous_fiscal_quarter",
    "acceptable_sidewalks_previous_fiscal_quarter"
FROM "nyc-open-data-rqhp-hivt"
