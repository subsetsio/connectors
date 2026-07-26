-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "as_of_date",
    "complaint_id",
    "complaint_officer_number",
    "tax_id",
    "officer_rank_abbreviation_at_incident",
    "officer_rank_at_incident",
    "officer_command_at_incident",
    "officer_days_on_force_at_incident",
    "allegation_record_identity",
    "fado_type",
    "allegation",
    "victimalleged_victim_age_range_at_incident",
    "victimalleged_victim_gender",
    "victim_alleged_victim_race_legacy",
    "victim_alleged_victim_race_ethnicity",
    "ccrb_investigations_division_recommendation",
    "ccrb_allegation_disposition",
    "nypd_allegation_disposition"
FROM "nyc-open-data-6xgr-kwjq"
