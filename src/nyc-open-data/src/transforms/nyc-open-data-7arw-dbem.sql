-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "report_id",
    "filing_year",
    "filing_period",
    "period_start_date",
    strptime("period_end_date", '%m/%d/%Y')::DATE AS period_end_date,
    "report_type",
    "entity_name",
    "street_address",
    "city",
    "state",
    "zip_code",
    "phone_number",
    "principal_last_name",
    "principal_first_name",
    "lobbyist_employees",
    "target_office",
    "candidate_last_name",
    "candidate_first_name",
    "candidate_type",
    "political_committee",
    "third_party",
    "compensation_owed",
    "total_expenses",
    "total_raised"
FROM "nyc-open-data-7arw-dbem"
