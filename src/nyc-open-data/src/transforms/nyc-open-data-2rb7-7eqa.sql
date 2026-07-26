-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "offense_type",
    "report_date",
    "incident_precinct_code",
    "borough_name",
    "intimate_relationship_flag",
    "victim_race",
    "victim_sex",
    "victim_reported_age",
    "suspect_race",
    "suspect_sex",
    "suspect_reported_age",
    "commdist",
    "poverty",
    "median_income",
    "unemployment"
FROM "nyc-open-data-2rb7-7eqa"
