-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "full_complaint_id",
    "complaint_year_number",
    "month_number",
    "record_create_date",
    "complaint_precinct_code",
    "patrol_borough_name",
    "county",
    "law_code_category_description",
    "offense_description",
    "pd_code_description",
    "bias_motive_description",
    "offense_category",
    "arrest_date",
    "arrest_id"
FROM "nyc-open-data-bqiq-cu78"
