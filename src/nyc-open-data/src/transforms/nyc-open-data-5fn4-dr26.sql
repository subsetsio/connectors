-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "record_id",
    "related_record_type",
    "business_unique_id",
    "business_name",
    "dbatrade_name",
    "business_category",
    "certificate_of_inspection",
    "inspection_number",
    "noh_number",
    "violation_date",
    "charge",
    "charge_count",
    "cure_eligible",
    "cured",
    "outcome",
    "guilty",
    "not_guilty",
    "dismissed"
FROM "nyc-open-data-5fn4-dr26"
