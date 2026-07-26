-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "violation_number",
    "bic_number",
    "account_name",
    "type_of_violation",
    "violation_phase",
    "violation_disposition",
    "account_type",
    "violation_account_address",
    "violation_account_city",
    "violation_account_state",
    "violation_account_postcode",
    "borough_of_violation",
    "date_of_violation",
    "date_violation_issued",
    "maximum_fine",
    "fine_amount",
    "date_fine_paid",
    "early_settlement_violation",
    "settlement_date",
    "rule_code",
    "number_of_counts",
    "description_of_rule",
    "export_date",
    "latitude",
    "longitude",
    "community_board",
    "council_district",
    "census_tract",
    "bin",
    "bbl",
    "nta"
FROM "nyc-open-data-upii-frjc"
